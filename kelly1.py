"""
Susan (Persona) – LangGraph Multi‑Agent with Text‑to‑SQL over DB/CSV/Excel,
Text‑to‑Chart, and Web Checker

This single file gives you a runnable LangGraph app with three specialists:
  1) SQL Analyst  – natural‑language → SQL → answer from:
       • a SQL database (SQLite/any SQLAlchemy URL), or
       • CSV/Excel files (loaded to an in‑memory SQLite table), or
       • Pandas DataFrame (optional Pandas agent mode)
  2) Chart Builder – natural‑language → chart spec → matplotlib image saved to ./artifacts
  3) Web Checker   – fetches + summarizes web pages you point it to

You can choose the data backend via CLI flags or env vars.

Quickstart
==========
1) Python 3.10+
2) Install deps:
   pip install -U langchain langgraph langchain-openai sqlalchemy aiosqlite pandas matplotlib \
                  httpx beautifulsoup4 trafilatura tenacity rich openpyxl tiktoken
   # Optional (Pandas agent):
   pip install -U langchain-experimental

3) Set your LLM key (example for OpenAI):
   export OPENAI_API_KEY=sk-...

4) Option A – Demo DB:
   python susan_langgraph.py --init-demo-db
   python susan_langgraph.py --repl

5) Option B – CSV/Excel as your data source:
   python susan_langgraph.py --csv ./data/sales.csv --repl
   # or
   python susan_langgraph.py --excel ./data/sales.xlsx --sheet Sheet1 --repl

6) Try prompts:
   • "Susan, list the top 5 customers by revenue."
   • "Plot monthly sales for 2024 as a line chart."
   • "Check this page: https://example.com/news and give me 5 bullets + a one‑line takeaway."

Notes
-----
• All SQL execution is READ‑ONLY (SELECT/CTE only).\n• Charts are saved under ./artifacts and paths are printed.\n• Web checker fetches up to 3 URLs from a prompt and summarizes.
• Optional Pandas agent mode: set SUSAN_PANDAS_AGENT=true to use Pandas ops instead of SQL for CSV/Excel.

"""
from __future__ import annotations
import os
import re
import json
import asyncio
import textwrap
import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Literal

import pandas as pd
import matplotlib.pyplot as plt
from tenacity import retry, wait_exponential_jitter, stop_after_attempt

# LangChain / LangGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# SQL
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text as sql_text

# Optional Pandas agent
try:
    from langchain_experimental.agents import create_pandas_dataframe_agent
except Exception:
    create_pandas_dataframe_agent = None

# Web fetch & parse
import httpx
from bs4 import BeautifulSoup
try:
    import trafilatura
except Exception:
    trafilatura = None

# ----------------------
# Configuration & Models
# ----------------------
LLM_MODEL = os.getenv("SUSAN_LLM_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("SUSAN_TEMPERATURE", "0.2"))
DB_URL = os.getenv("SUSAN_DB_URL", "sqlite:///./demo_sales.db")
ARTIFACTS_DIR = os.getenv("SUSAN_ARTIFACTS", "./artifacts")
PANDAS_AGENT = os.getenv("SUSAN_PANDAS_AGENT", "false").lower() in {"1","true","yes"}

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Initialize LLM
llm = ChatOpenAI(model=LLM_MODEL, temperature=TEMPERATURE)

# -----------------
# Persona: "Susan"
# -----------------
SUSAN_SYSTEM = (
    "You are Susan, a precise, friendly technology analyst who can reason step-by-step, "
    "choose tools, and explain results succinctly. Favor tables and bullet points. "
    "When the user asks about data, you may call the SQL or Chart tools. "
    "When they ask about web pages or 'check this link', use the Web Checker tool. "
    "Never fabricate facts; if uncertain, say so and propose how to verify."
)

# ---------------
# Graph State
# ---------------
@dataclass
class SusanState:
    user_input: str
    intent: Optional[Literal["sql", "chart", "web", "chat"]] = None
    sql_result: Optional[pd.DataFrame] = None
    chart_path: Optional[str] = None
    web_summary: Optional[str] = None
    messages: List[Dict[str, str]] = dataclasses.field(default_factory=list)


# -----------------
# Utility Functions
# -----------------

def make_engine(url: str = DB_URL) -> Engine:
    return create_engine(url, future=True)


def is_select_only(query: str) -> bool:
    q = query.strip().lower()
    if not q.startswith("select") and not q.startswith("with"):
        return False
    # very conservative guards
    forbidden = [" update ", " delete ", " insert ", " drop ", " alter ", " create ", " truncate ", " attach ", " detach ", " pragma "]
    if ";" in q and not q.endswith(";"):
        return False
    for token in forbidden:
        if token in q:
            return False
    return True


async def llm_json(prompt: str, schema_hint: str) -> Dict[str, Any]:
    template = ChatPromptTemplate.from_messages([
        ("system", SUSAN_SYSTEM + " Always return a minified JSON only, no prose."),
        ("human", "Schema hint: {schema}\n\nTask: {task}")
    ])
    msg = await llm.ainvoke(template.format_messages(schema=schema_hint, task=prompt))
    # try strict JSON parse; fallback to regex extract
    try:
        return json.loads(msg.content)
    except Exception:
        import re
        m = re.search(r"\{.*\}", msg.content, re.DOTALL)
        return json.loads(m.group(0)) if m else {"error": "no json"}


# -----------------
# Data Backends (DB, CSV, Excel)
# -----------------
class DataBackend:
    def __init__(self):
        self.kind = "db"
        self.table_name: Optional[str] = None

    def ready(self) -> bool:
        raise NotImplementedError

    def run_select(self, query: str) -> pd.DataFrame:
        raise NotImplementedError


class SQLAlchemyBackend(DataBackend):
    def __init__(self, url: str):
        super().__init__()
        self.kind = "db"
        self.url = url
        self.engine = make_engine(url)

    def ready(self) -> bool:
        return True

    def run_select(self, query: str) -> pd.DataFrame:
        with self.engine.connect() as conn:
            return pd.read_sql_query(sql_text(query), conn)


class SQLiteFromFrameBackend(DataBackend):
    """Load a DataFrame into an in-memory SQLite DB and query it with SQL."""
    def __init__(self, df: pd.DataFrame, table_name: str = "data"):
        super().__init__()
        self.kind = "frame"
        self.table_name = table_name
        self.engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
        with self.engine.begin() as conn:
            df.to_sql(self.table_name, conn, if_exists="replace", index=False)

    def ready(self) -> bool:
        return True

    def run_select(self, query: str) -> pd.DataFrame:
        # help: if query forgets table name, try SELECT * FROM {table}
        if " from " not in query.lower():
            query = f"SELECT * FROM {self.table_name}"
        with self.engine.connect() as conn:
            return pd.read_sql_query(sql_text(query), conn)


def load_csv_backend(path: str, table_name: str = "data") -> DataBackend:
    df = pd.read_csv(path)
    return SQLiteFromFrameBackend(df, table_name)


def load_excel_backend(path: str, sheet: Optional[str] = None, table_name: str = "data") -> DataBackend:
    df = pd.read_excel(path, sheet_name=sheet)
    return SQLiteFromFrameBackend(df, table_name)


# -----------------
# Router (intent)
# -----------------
async def router(state: SusanState) -> SusanState:
    """Infer intent: sql / chart / web / chat."""
    schema = textwrap.dedent(
        """
        {"intent": "one of: sql|chart|web|chat",
         "note": "short reason"}
        """
    )
    plan = await llm_json(f"Classify the user request: {state.user_input}", schema)
    intent = plan.get("intent", "chat")
    state.intent = intent if intent in {"sql", "chart", "web", "chat"} else "chat"
    state.messages.append({"role": "system", "content": f"Router chose: {state.intent} ({plan.get('note','')})"})
    return state


# -----------------
# SQL Specialist (supports DB/CSV/Excel/Pandas Agent)
# -----------------
async def sql_specialist(state: SusanState, backend: DataBackend = None, pandas_agent=None) -> SusanState:
    # Pandas agent mode
    if pandas_agent is not None:
        try:
            ans = await pandas_agent.ainvoke(state.user_input)
            content = ans["output"] if isinstance(ans, dict) and "output" in ans else str(ans)
            # Pandas agent can also produce plots; here we just capture the text output
            state.messages.append({"role": "assistant", "content": content})
            # Try to capture a DataFrame if one was printed (not guaranteed)
            state.sql_result = None
            return state
        except Exception as e:
            state.messages.append({"role": "assistant", "content": f"Pandas agent error: {e}"})
            return state

    # LLM plans a SQL SELECT
    schema = textwrap.dedent(
        """
        {"sql": "a single safe SELECT query (SQLite dialect)",
         "columns": ["list of expected columns in output"],
         "explanation": "1-2 lines"}
        """
    )
    plan = await llm_json(
        f"Write a single SELECT SQL (SQLite dialect) to answer: {state.user_input}. Strictly READ-ONLY.",
        schema,
    )
    query = (plan.get("sql") or "").strip()
    if not is_select_only(query):
        state.messages.append({"role": "assistant", "content": "I couldn't produce a safe SELECT. Please rephrase your data request."})
        return state

    # Execute
    try:
        df = backend.run_select(query) if backend else pd.DataFrame()
    except Exception as e:
        state.messages.append({"role": "assistant", "content": f"SQL error: {e}"})
        return state

    state.sql_result = df

    # Summarize
    preview = df.head(10).to_markdown(index=False) if not df.empty else "(no rows)"
    expl = plan.get("explanation", "")
    state.messages.append({
        "role": "assistant",
        "content": f"SQL executed. Columns: {list(df.columns)}\nReason: {expl}\nTop rows:\n{preview}"
    })
    return state


# -----------------
# Chart Specialist
# -----------------
async def chart_builder(state: SusanState, backend: DataBackend = None, pandas_agent=None) -> SusanState:
    # If we don't have data yet, try to fetch via SQL specialist
    if state.sql_result is None or state.sql_result.empty:
        state = await sql_specialist(state, backend=backend, pandas_agent=pandas_agent)
        if state.sql_result is None or state.sql_result.empty:
            state.messages.append({"role": "assistant", "content": "No data available to chart."})
            return state

    df = state.sql_result

    # Decide a simple chart spec
    schema = textwrap.dedent(
        """
        {"x": "x column name",
         "y": "y column name or list of columns",
         "kind": "one of: line|bar|scatter",
         "title": "short title"}
        """
    )
    plan = await llm_json(
        f"Given columns {list(df.columns)}, pick a chart spec for: {state.user_input}", schema
    )
    kind = plan.get("kind", "bar")
    x = plan.get("x")
    y = plan.get("y")
    title = plan.get("title", "Chart")

    if not x or y is None or x not in df.columns:
        state.messages.append({"role": "assistant", "content": "Couldn't infer chart mapping. Please specify x/y."})
        return state

    plt.figure()
    if isinstance(y, list):
        for col in y:
            if col in df.columns:
                df.plot(x=x, y=col, kind=kind)
    else:
        if y not in df.columns:
            state.messages.append({"role": "assistant", "content": f"Column '{y}' not found."})
            return state
        df.plot(x=x, y=y, kind=kind)
    plt.title(title)
    plt.tight_layout()
    out_path = os.path.join(ARTIFACTS_DIR, f"chart_{abs(hash(title)) % (10**8)}.png")
    plt.savefig(out_path, dpi=160)
    plt.close()

    state.chart_path = out_path
    state.messages.append({"role": "assistant", "content": f"Chart saved: {out_path}"})
    return state


# -----------------
# Web Checker
# -----------------
@retry(wait=wait_exponential_jitter(initial=1, max=8), stop=stop_after_attempt(3))
async def fetch_url(url: str, timeout: int = 15) -> str:
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers={"User-Agent": "SusanBot/1.0"}) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text


def extract_main_text(html: str, url: str) -> str:
    if trafilatura is not None:
        downloaded = trafilatura.extract(html, url=url, include_comments=False, include_tables=False)
        if downloaded:
            return downloaded
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = "\n".join(t.strip() for t in soup.get_text("\n").splitlines() if t.strip())
    return text[:100000]


async def web_checker(state: SusanState) -> SusanState:
    urls = re.findall(r"https?://\S+", state.user_input)
    if not urls:
        state.messages.append({"role": "assistant", "content": "Provide a URL to check, or ask me to search specific sites."})
        return state

    summaries = []
    for url in urls[:3]:
        try:
            html = await fetch_url(url)
            text = extract_main_text(html, url)
            template = ChatPromptTemplate.from_messages([
                ("system", SUSAN_SYSTEM),
                ("human", "Summarize this page in 5 bullets and one‑line takeaway.\nURL: {u}\n\nTEXT:\n{t}")
            ])
            msg = await llm.ainvoke(template.format_messages(u=url, t=text[:12000]))
            summaries.append(f"Summary for {url}:\n{msg.content}")
        except Exception as e:
            summaries.append(f"Error for {url}: {e}")

    state.web_summary = "\n\n".join(summaries)
    state.messages.append({"role": "assistant", "content": state.web_summary})
    return state


# -----------------
# Fallback Chat
# -----------------
async def chit_chat(state: SusanState) -> SusanState:
    template = ChatPromptTemplate.from_messages([
        ("system", SUSAN_SYSTEM),
        ("human", "{q}")
    ])
    msg = await llm.ainvoke(template.format_messages(q=state.user_input))
    state.messages.append({"role": "assistant", "content": msg.content})
    return state


# -----------------
# Graph Wiring
# -----------------

def build_graph(backend: DataBackend = None, pandas_agent=None) -> StateGraph:
    graph = StateGraph(SusanState)

    # Wrap nodes to capture backend/agent
    async def _sql(state: SusanState) -> SusanState:
        return await sql_specialist(state, backend=backend, pandas_agent=pandas_agent)

    async def _chart(state: SusanState) -> SusanState:
        return await chart_builder(state, backend=backend, pandas_agent=pandas_agent)

    graph.add_node("router", router)
    graph.add_node("sql", _sql)
    graph.add_node("chart", _chart)
    graph.add_node("web", web_checker)
    graph.add_node("chat", chit_chat)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda s: s.intent,
        {
            "sql": "sql",
            "chart": "chart",
            "web": "web",
            "chat": "chat",
        },
    )

    graph.add_edge("sql", END)
    graph.add_edge("chart", END)
    graph.add_edge("web", END)
    graph.add_edge("chat", END)

    return graph


# -----------------
# Demo DB (SQLite)
# -----------------
DEMO_SQL = """
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
  id INTEGER PRIMARY KEY,
  order_date TEXT,
  customer TEXT,
  product TEXT,
  qty INTEGER,
  unit_price REAL
);
"""

DEMO_ROWS = [
    ("2024-01-15", "Acme Corp", "Widget A", 10, 12.5),
    ("2024-02-01", "Beta LLC", "Widget B", 5, 20.0),
    ("2024-02-12", "Acme Corp", "Widget A", 7, 12.5),
    ("2024-03-05", "Delta Inc", "Widget C", 3, 50.0),
    ("2024-03-18", "Acme Corp", "Widget C", 1, 50.0),
    ("2024-04-02", "Beta LLC", "Widget A", 15, 12.5),
    ("2024-04-11", "Echo Co",  "Widget B", 8, 20.0),
]


def init_demo_db(url: str = DB_URL):
    eng = make_engine(url)
    with eng.begin() as conn:
        for stmt in DEMO_SQL.strip().split(";\n"):
            if stmt.strip():
                conn.execute(sql_text(stmt))
        conn.execute(sql_text(
            "INSERT INTO sales (order_date, customer, product, qty, unit_price) "
            "VALUES (:d,:c,:p,:q,:u)"
        ), [
            {"d": d, "c": c, "p": p, "q": q, "u": u} for (d, c, p, q, u) in DEMO_ROWS
        ])


# -----------------
# Runner / CLI
# -----------------
async def run_once(app, question: str) -> SusanState:
    config = {"configurable": {"thread_id": "demo-thread"}}
    return await app.ainvoke(SusanState(user_input=question), config)


def pretty_print(state: SusanState):
    from rich.console import Console
    from rich.markdown import Markdown
    cons = Console()
    cons.rule("Susan")
    for m in state.messages:
        role = m.get("role")
        content = m.get("content", "")
        cons.print(f"[bold]{role}[/bold]:")
        cons.print(Markdown(content))
        cons.print()
    if state.chart_path:
        cons.print(f"[green]Chart saved:[/green] {state.chart_path}")


def build_app(backend: DataBackend = None, pandas_agent=None):
    graph = build_graph(backend=backend, pandas_agent=pandas_agent)
    checkpointer = SqliteSaver.from_conn_string("susan_memory.sqlite")
    app = graph.compile(checkpointer=checkpointer)
    return app


def repl(app):
    print("Susan is ready. Type 'exit' to quit.\n")
    loop = asyncio.get_event_loop()
    while True:
        try:
            q = input("You: ").strip()
            if q.lower() in {"exit", "quit"}:
                break
            state = loop.run_until_complete(run_once(app, q))
            pretty_print(state)
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Susan – LangGraph multi-agent")
    parser.add_argument("--init-demo-db", action="store_true", help="Initialize demo SQLite DB")
    parser.add_argument("--repl", action="store_true", help="Start a simple REPL")
    parser.add_argument("--db-url", type=str, default=DB_URL, help="SQLAlchemy DB URL (default from env)")
    parser.add_argument("--csv", type=str, default=None, help="Path to a CSV file to use as data source")
    parser.add_argument("--excel", type=str, default=None, help="Path to an Excel .xlsx file")
    parser.add_argument("--sheet", type=str, default=None, help="Excel sheet name (optional)")
    parser.add_argument("--table", type=str, default="data", help="Table name for CSV/Excel loading")
    args = parser.parse_args()

    # Demo DB init only
    if args.init_demo_db:
        init_demo_db(url=args.db_url)
        print("Demo DB initialized at:", args.db_url)

    # Choose backend
    backend: Optional[DataBackend] = None
    pandas_agent = None

    if args.csv:
        backend = load_csv_backend(args.csv, table_name=args.table)
        print(f"Loaded CSV into in-memory SQLite table '{args.table}'.")
        if PANDAS_AGENT and create_pandas_dataframe_agent is not None:
            df = pd.read_csv(args.csv)
            pandas_agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=False, verbose=False)
    elif args.excel:
        backend = load_excel_backend(args.excel, sheet=args.sheet, table_name=args.table)
        print(f"Loaded Excel into in-memory SQLite table '{args.table}'.")
        if PANDAS_AGENT and create_pandas_dataframe_agent is not None:
            df = pd.read_excel(args.excel, sheet_name=args.sheet)
            pandas_agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=False, verbose=False)
    else:
        # default: DB URL
        backend = SQLAlchemyBackend(args.db_url)
        print("Using SQLAlchemy backend:", args.db_url)

    app = build_app(backend=backend, pandas_agent=pandas_agent)

    if args.repl:
        repl(app)
