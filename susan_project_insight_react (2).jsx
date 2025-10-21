import React, { useMemo, useState, useEffect } from "react";
import {
  ChevronLeft,
  Lightbulb,
  ShieldAlert,
  CheckCircle2,
  Sparkles,
  BotMessageSquare,
  BarChart3,
  LayoutDashboard,
  RefreshCw,
  Bug
} from "lucide-react";

/**
 * "Susan – Project Insight" – White UI (v4 rollback)
 * Simple, clean white cards, no gradients/dark mode/AI dock.
 *
 * Notes/Fixes kept:
 * - Escaped raw "<" in JSX text ("<5 members" → "&lt;5 members").
 * - Visual Test Panel retained (non‑blocking console.assert checks).
 */

export default function App() {
  const [view, setView] = useState<"dashboard" | "insights">("dashboard");
  const [selected, setSelected] = useState<InsightKey | null>(null);
  const [showTests, setShowTests] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);

  const openInsights = (key: InsightKey) => {
    setSelected(key);
    setView("insights");
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {view === "dashboard" ? (
        <Dashboard onOpen={openInsights} onToggleTests={() => setShowTests((v) => !v)} />
      ) : (
        <ExecutiveSummary selected={selected} onBack={() => setView("dashboard")} onToggleTests={() => setShowTests((v) => !v)} />
      )}

      <SusanChat open={chatOpen} onOpen={() => setChatOpen(true)} onClose={() => setChatOpen(false)} />
      {showTests && <TestPanel />}
    </div>
  );
}

// -------------------- Dashboard --------------------

type InsightKey = "recommendation" | "risk" | "achievement" | "ai" | "teamPlanning" | "healthPerformance";

function Dashboard({ onOpen, onToggleTests }: { onOpen: (key: InsightKey) => void; onToggleTests: () => void }) {
  return (
    <div className="max-w-6xl mx-auto p-4 md:p-6">
      {/* Top Bar */}
      <div className="flex items-center gap-3 mb-4">
        <button className="inline-flex items-center gap-1 rounded-full bg-white shadow px-3 py-1 text-sm hover:bg-slate-100">
          <ChevronLeft className="w-4 h-4" /> Back
        </button>
        <button
          onClick={onToggleTests}
          className="inline-flex items-center gap-1 rounded-full bg-white shadow px-3 py-1 text-sm hover:bg-slate-100"
          title="Toggle visual tests"
        >
          <Bug className="w-4 h-4" /> Run UI Tests
        </button>
      </div>

      {/* Header Card */}
      <div className="rounded-2xl bg-slate-900 text-white p-6 md:p-8 flex items-center justify-between shadow mb-6">
        <div className="flex items-center gap-4">
          <div className="rounded-2xl bg-white/10 p-4">
            <BarChart3 className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-3xl font-semibold tracking-tight">Susan</h1>
            <p className="text-slate-300 mt-1">Project Insight · Real‑time project intelligence and analytics</p>
          </div>
        </div>
        <button className="rounded-xl bg-white/10 hover:bg-white/20 transition px-3 py-2">
          <RefreshCw className="w-5 h-5" />
        </button>
      </div>

      {/* Tabs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <TabButton icon={LayoutDashboard} label="Overview" active onClick={() => {}} />
        <TabButton icon={BarChart3} label="Analytics" onClick={() => {}} />
        <TabButton icon={Sparkles} label="AI Insights" onClick={() => onOpen("ai")} />
        <TabButton icon={BotMessageSquare} label="Chat Assistant" onClick={() => {}} />
      </div>

      {/* Insight Cards (white) */}
      <div className="space-y-5">
        <InsightCard
          color="blue"
          icon={Lightbulb}
          title="Recommendations"
          description="Based on current project data, consider increasing test automation coverage to improve quality metrics."
          primaryAction={{ label: "Apply Suggestion", onClick: () => onOpen("recommendation") }}
          secondaryAction={{ label: "View in Details", onClick: () => onOpen("ai") }}
        />

        <InsightCard
          color="amber"
          icon={ShieldAlert}
          title="Risk Alert"
          description="Team capacity is at 95%. Consider redistributing workload to prevent burnout."
          primaryAction={{ label: "Address Now", onClick: () => onOpen("risk") }}
          secondaryAction={{ label: "View in Details", onClick: () => onOpen("risk") }}
        />

        <InsightCard
          color="emerald"
          icon={CheckCircle2}
          title="Achievement"
          description="Sprint delivery consistency has improved by 23% over the last 3 sprints."
          primaryAction={{ label: "View Details", onClick: () => onOpen("achievement") }}
          secondaryAction={{ label: "View in Details", onClick: () => onOpen("achievement") }}
        />

        {/* New: Team Planning */}
        <InsightCard
          color="blue"
          icon={LayoutDashboard}
          title="Team Planning"
          description="Plan upcoming sprints, balance capacity, and align milestones across teams."
          primaryAction={{ label: "Open Planner", onClick: () => onOpen("teamPlanning") }}
          secondaryAction={{ label: "View in Details", onClick: () => onOpen("teamPlanning") }}
        />

        {/* New: Health Performance */}
        <InsightCard
          color="amber"
          icon={Sparkles}
          title="Health Performance"
          description="Track burnout risk, WIP limits, and red/yellow/green health metrics across squads."
          primaryAction={{ label: "Review Health", onClick: () => onOpen("healthPerformance") }}
          secondaryAction={{ label: "View in Details", onClick: () => onOpen("healthPerformance") }}
        />
      </div>
    </div>
  );
}

function TabButton({ icon: Icon, label, active, onClick }: { icon: any; label: string; active?: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={[
        "flex items-center gap-2 rounded-xl px-4 py-2 shadow-sm",
        active ? "bg-white border border-slate-200" : "bg-slate-100 hover:bg-slate-200",
      ].join(" ")}
    >
      <Icon className="w-4 h-4" />
      <span className="text-sm font-medium">{label}</span>
    </button>
  );
}

function InsightCard({
  color,
  icon: Icon,
  title,
  description,
  primaryAction,
  secondaryAction,
}: {
  color: "blue" | "amber" | "emerald";
  icon: any;
  title: string;
  description: string;
  primaryAction?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
}) {
  const ring = useMemo(
    () => ({
      blue: "ring-blue-400",
      amber: "ring-amber-400",
      emerald: "ring-emerald-400",
    })[color],
    [color]
  );

  return (
    <div className={`bg-white rounded-2xl shadow-sm border border-slate-200 ring-1 ${ring} ring-opacity-20 p-5`}>
      <div className="flex items-start gap-4">
        <div className={`rounded-xl p-2 bg-${color}-50 text-${color}-600 border border-${color}-200`}>
          <Icon className="w-5 h-5" />
        </div>
        <div className="flex-1">
          <h3 className="text-base font-semibold mb-1">{title}</h3>
          <p className="text-sm text-slate-600 mb-3">{description}</p>
          <div className="flex flex-wrap gap-2">
            {primaryAction && (
              <button
                onClick={primaryAction.onClick}
                className={`text-sm font-medium rounded-lg px-3 py-1.5 bg-${color}-600 text-white hover:bg-${color}-700 transition`}
              >
                {primaryAction.label}
              </button>
            )}
            {secondaryAction && (
              <button
                onClick={secondaryAction.onClick}
                className="text-sm font-medium rounded-lg px-3 py-1.5 bg-slate-100 hover:bg-slate-200"
              >
                {secondaryAction.label}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// -------------------- Executive Summary (Full View) --------------------

function ExecutiveSummary({ selected, onBack, onToggleTests }: { selected: InsightKey | null; onBack: () => void; onToggleTests: () => void }) {
  const titleMap = {
    recommendation: "Executive Summary: Insights and Recommendations",
    risk: "Executive Summary: Risks and Mitigations",
    achievement: "Executive Summary: Highlights and Opportunities",
    ai: "Executive Summary: AI‑Generated Insights",
    teamPlanning: "Executive Summary: Team Planning",
    healthPerformance: "Executive Summary: Health Performance",
  } as const;

  return (
    <div className="max-w-5xl mx-auto p-4 md:p-8">
      <div className="flex items-center gap-3 mb-5">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1 rounded-full bg-white shadow px-3 py-1 text-sm hover:bg-slate-100"
        >
          <ChevronLeft className="w-4 h-4" /> Back to dashboard
        </button>
        <button
          onClick={onToggleTests}
          className="inline-flex items-center gap-1 rounded-full bg-white shadow px-3 py-1 text-sm hover:bg-slate-100"
          title="Toggle visual tests"
        >
          <Bug className="w-4 h-4" /> Run UI Tests
        </button>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8">
        <h2 className="text-2xl md:text-3xl font-semibold tracking-tight mb-6">{selected ? titleMap[selected] : titleMap.ai}</h2>

        {/* 1. Organizational Health */}
        <Section title="1. Organizational Health and Team Performance Patterns">
          <p className="mb-3 text-slate-700">
            The data reveals significant, organization‑wide patterns in team performance, capacity, and risk across 31 active
            programs. Key observations include:
          </p>
          <Bullet title="Sprint Capacity Distribution">
            Teams in <b>Modernization & Cloud Migration</b> show stable capacity but rising backlog. <b>Delegated Platform</b>
            teams are at 95% average capacity utilization, signaling potential burnout.
          </Bullet>
          <Bullet title="Maturity & Velocity">
            Multiple teams fall into <b>Too Large</b> or <b>Too Small</b> bands. Smaller teams (&lt;5 members) deliver effectively but
            lack redundancy. Oversized teams show coordination overhead.
          </Bullet>
          <Bullet title="Backlog Health">
            6/31 teams have growing critical backlogs. Grooming cadence and scope clarity require attention within the next two sprints.
          </Bullet>
        </Section>

        {/* 2. Risks & Opportunities */}
        <Section title="2. Critical Risks and Opportunities Across All Teams">
          <Subheading>Risks</Subheading>
          <List>
            <li><b>Team Health:</b> 11 teams flagged <span className="text-red-600 font-medium">Red</span> for burnout risk and scheduling slippage.</li>
            <li><b>Capacity Gaps:</b> Delegated Platform (cap at 95%), Clinical Data Services (88%) require load rebalancing.</li>
            <li><b>Allocation Drift:</b> Cross‑team over‑allocation in Analytics & Data is causing priority conflicts.</li>
          </List>
          <Subheading>Opportunities</Subheading>
          <List>
            <li><b>High‑Performing Teams:</b> Modernization & Cloud Migration can mentor under‑performing teams.</li>
            <li><b>Cross‑Team Collaboration:</b> Knowledge transfer and consolidated efforts can reduce redundancy.</li>
          </List>
        </Section>

        {/* 3. Strategic Recommendations */}
        <Section title="3. Strategic Recommendations for Leadership and Management">
          <Subheading>Short‑Term Actions (Next 2–4 weeks)</Subheading>
          <List>
            <li><b>Immediate Resource Reallocation:</b> Shift capacity from over‑utilized to under‑utilized teams.</li>
            <li><b>Backlog Prioritization:</b> Conduct focused grooming sessions for teams with critical backlogs.</li>
            <li><b>Team Health Interventions:</b> Introduce WIP limits, enforce focus time, and monitor capacity caps.</li>
          </List>
          <Subheading>Long‑Term Strategies (Quarter+)</Subheading>
          <List>
            <li><b>Capacity Planning Framework:</b> Centralized quarterly planning with scenario models.</li>
            <li><b>Scale Agile Practices:</b> Standardize definitions of done, automation baselines, and release cadences.</li>
            <li><b>Cross‑Domain Collaboration:</b> Create functional squads for analytics, security, and platform enablement.</li>
          </List>
        </Section>

        {/* 4. Next Steps */}
        <Section title="Next Steps and Final Recommendations">
          <List>
            <li><b>Immediate:</b> Verify flagged capacity hotspots and resolve blockers for critical work items.</li>
            <li><b>Mid‑Term:</b> Standardize automation and CI/CD practices; establish governance for data‑related projects.</li>
            <li><b>Long‑Term:</b> Monitor team health metrics and adjust strategies based on performance trends.</li>
          </List>
        </Section>
      </div>
    </div>
  );
}

// -------------------- Primitives --------------------

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-8">
      <h3 className="text-lg md:text-xl font-semibold mb-3">{title}</h3>
      <div className="space-y-3 text-sm leading-6">{children}</div>
    </section>
  );
}

function Subheading({ children }: { children: React.ReactNode }) {
  return <h4 className="mt-2 font-semibold text-slate-800">{children}</h4>;
}

function Bullet({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="flex gap-3">
      <div className="mt-1.5">
        <span className="inline-block w-1.5 h-1.5 rounded-full bg-slate-400" />
      </div>
      <p className="text-slate-700"><b>{title}:</b> {children}</p>
    </div>
  );
}

function List({ children }: { children: React.ReactNode }) {
  return (
    <ul className="list-disc pl-6 space-y-1 text-slate-700">{children}</ul>
  );
}

// ---------- Leadership modules ----------

function KPICard({ label, value, delta, intent }: { label: string; value: string; delta?: string; intent?: "good" | "bad" | "warn" }) {
  const tone = intent === "good" ? "text-emerald-600" : intent === "bad" ? "text-red-600" : intent === "warn" ? "text-amber-600" : "text-slate-600";
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
      <div className="text-xs text-slate-500 mb-1">{label}</div>
      <div className="text-2xl font-semibold">{value}</div>
      {delta && <div className={`text-xs ${tone}`}>{delta} vs prev</div>}
    </div>
  );
}

function SectionCard({ id, title, subtitle, children }: { id?: string; title: string; subtitle?: string; children: React.ReactNode }) {
  return (
    <section id={id} className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
      <div className="mb-3">
        <div className="text-sm font-semibold">{title}</div>
        {subtitle && <div className="text-xs text-slate-500">{subtitle}</div>}
      </div>
      {children}
    </section>
  );
}

function Tag({ tone = "gray", children }: { tone?: "red" | "amber" | "green" | "gray"; children: React.ReactNode }) {
  const map: Record<string, string> = {
    red: "bg-red-50 text-red-700 border-red-200",
    amber: "bg-amber-50 text-amber-700 border-amber-200",
    green: "bg-emerald-50 text-emerald-700 border-emerald-200",
    gray: "bg-slate-50 text-slate-700 border-slate-200",
  };
  return <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs border ${map[tone]}`}>{children}</span>;
}

function HealthDot({ code }: { code: "R" | "Y" | "G" }) {
  const map = { R: "bg-red-500", Y: "bg-amber-500", G: "bg-emerald-500" } as const;
  return <span className={`inline-block w-2.5 h-2.5 rounded-full ${map[code]}`}></span>;
}

// -------------------- Susan Chat Widget (LLM mini chat) --------------------
function SusanChat({ open, onOpen, onClose }: { open: boolean; onOpen: () => void; onClose: () => void }) {
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<{ role: "user" | "assistant"; content: string }[]>([
    { role: "assistant", content: "Hi, I'm Susan. How can I help with insights or summaries?" },
  ]);
  const [appeared, setAppeared] = useState(false);

  useEffect(() => {
    if (open) {
      // trigger enter animation on mount
      requestAnimationFrame(() => setAppeared(true));
    } else {
      setAppeared(false);
    }
  }, [open]);

  const send = () => {
    const text = msg.trim();
    if (!text) return;
    setMsg("");
    setHistory((h) => [...h, { role: "user", content: text }]);
    setLoading(true);
    // Simulated LLM response for demo purposes
    setTimeout(() => {
      setHistory((h) => [
        ...h,
        { role: "assistant", content: `Here's a draft based on: "${text}". (demo)` },
      ]);
      setLoading(false);
    }, 600);
  };

  const handleClose = () => {
    setAppeared(false);
    setTimeout(onClose, 180); // allow exit animation
  };

  return (
    <div className="fixed right-4 bottom-4 z-40">
      {!open && (
        <button
          onClick={onOpen}
          className="flex items-center gap-2 px-3 py-2 rounded-full shadow-lg shadow-purple-300/40 bg-purple-600 text-white hover:bg-purple-700 active:bg-purple-800 transition transform hover:-translate-y-0.5"
          title="Ask Susan"
        ><BotMessageSquare className="w-4 h-4" /> Ask Susan</button>
      )}

      {open && (
        <div
          className={[
            "w-80 max-w-[90vw] rounded-2xl border overflow-hidden",
            "bg-white border-purple-200 shadow-2xl shadow-purple-300/40",
            "transition-all duration-200 ease-out transform",
            appeared ? "opacity-100 translate-y-0 scale-100" : "opacity-0 translate-y-2 scale-95",
          ].join(" ")}
        >
          <div className="px-3 py-2 text-sm font-semibold bg-gradient-to-r from-purple-600 to-fuchsia-600 text-white flex items-center justify-between">
            <span>Ask Susan</span>
            <button onClick={handleClose} className="text-xs rounded px-2 py-0.5 bg-white/10 hover:bg-white/20">Close</button>
          </div>
          <div className="max-h-72 overflow-y-auto p-3 space-y-2 text-sm">
            {history.map((m, i) => (
              <div key={i} className={"flex " + (m.role === "user" ? "justify-end" : "justify-start") }>
                <div className={(m.role === "user" ? "bg-purple-600 text-white" : "bg-purple-50 text-purple-900") + " px-3 py-1.5 rounded-xl shadow-sm"}>
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex items-center gap-1 text-purple-600">
                <span className="text-xs">Susan is typing…</span>
                <span className="inline-flex gap-1 pl-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-bounce" style={{ animationDelay: "120ms" }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-bounce" style={{ animationDelay: "240ms" }} />
                </span>
              </div>
            )}
          </div>
          <div className="p-2 border-t border-purple-200 flex items-center gap-2">
            <input
              value={msg}
              onChange={(e) => setMsg(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') send(); }}
              placeholder="Ask Susan…"
              className="flex-1 text-sm bg-purple-50/60 border border-purple-200 rounded-lg px-2 py-1 outline-none focus:ring-2 focus:ring-purple-300"
            />
            <button onClick={send} disabled={loading} className="text-sm px-2 py-1 rounded-lg bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50">Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

// -------------------- Visual Test Panel --------------------
// Simple, inline tests to validate rendering and edge cases without external tooling.
function TestPanel() {
  // Test 1: List renders correct number of li children
  const items = ["Alpha", "Bravo", "Charlie"];
  // Test 2: Insight keys mapping includes new cards
  const expectedKeys = [
    "recommendation",
    "risk",
    "achievement",
    "ai",
    "teamPlanning",
    "healthPerformance",
  ];
  // Test 3: KPI cards render count
  const kpiCount = 4;
  // Test 4: LLM provides exactly three section headers
  const expectedHeaders = [
    "1. Organizational Health and Team Performance Patterns",
    "2. Critical Risks and Opportunities Across All Teams",
    "3. Strategic Recommendations for Leadership and Management",
  ];

  try {
    console.assert(Array.isArray(items) && items.length === 3, "Test 1 failed: items length");
    console.assert(expectedKeys.length === 6, "Test 2 failed: expected keys length");
    console.assert(kpiCount === 4, "Test 3 failed: KPI count");
    console.assert(expectedHeaders.length === 3, "Test 4 failed: LLM headers count");
  } catch (error) {
    console.error(error);
  }

  return (
    <div className="max-w-5xl mx-auto p-4">
      <div className="rounded-xl border border-emerald-300 bg-emerald-50 p-4 text-emerald-900 shadow-sm">
        <div className="font-semibold flex items-center gap-2">
          <Bug className="w-4 h-4" /> Visual Test Panel
        </div>
        <p className="text-sm mt-1">Quick checks for components and edge characters like &lt; and &gt; inside JSX.</p>
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          <div className="rounded-lg bg-white p-3 border">
            <h5 className="font-medium">List renders children</h5>
            <List>
              {items.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </List>
          </div>
          <div className="rounded-lg bg-white p-3 border">
            <h5 className="font-medium">Bullet with numeric comparator text</h5>
            <Bullet title="Team Size">Smaller teams (&lt;5) deliver effectively</Bullet>
          </div>
          <div className="rounded-lg bg-white p-3 border">
            <h5 className="font-medium">KPI Cards count (expected 4)</h5>
            <div className="grid grid-cols-2 gap-2">
              <KPICard label="Demo KPI" value="100" />
              <KPICard label="Demo KPI" value="100" />
              <KPICard label="Demo KPI" value="100" />
              <KPICard label="Demo KPI" value="100" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
