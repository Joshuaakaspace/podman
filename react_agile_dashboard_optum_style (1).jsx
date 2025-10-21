import React, { useMemo, useState } from "react";
import { ChevronDown, Filter, Bell, Settings, ArrowLeft, RotateCcw, LayoutGrid, BarChart3, MessageSquare } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  CartesianGrid,
  Area,
  ReferenceDot,
} from "recharts";

// -----------------------------
// Helpers & Data
// -----------------------------
export const calcDefinedPct = (ratio: number) =>
  Math.round(Math.max(0, Math.min(1, ratio)) * 100);

// --- lightweight smoke tests (run only under test env) ---
try {
  if (typeof process !== "undefined" && process.env?.NODE_ENV === "test") {
    console.assert(calcDefinedPct(0.67) === 67, "calcDefinedPct(0.67) should be 67");
    console.assert(calcDefinedPct(1.2) === 100, ">1 should clamp to 100");
    console.assert(calcDefinedPct(-0.2) === 0, "<0 should clamp to 0");
    console.assert(calcDefinedPct(0) === 0, "0 -> 0%");
    console.assert(calcDefinedPct(1) === 100, "1 -> 100%");
    // Additional tests
    console.assert(calcDefinedPct(0.345) === 35, "0.345 -> 35% (rounded)");
    console.assert(calcDefinedPct(0.995) === 100, "0.995 -> 100% (rounded)");
  }
} catch {}

const kpis = {
  undefinedCount: 35,
  definedRatio: 0.67, // 67%
  plannedPoints: 78,
  nextSprintPoints: 24,
  avgVelocity: 41.6,
};

const monthlyStatus = [
  { month: "May", green: 3, yellow: 2, red: 7 },
  { month: "June", green: 2, yellow: 2, red: 8 },
  { month: "July", green: 2, yellow: 1, red: 9 },
  { month: "August", green: 1, yellow: 2, red: 9 },
  { month: "September", green: 1, yellow: 1, red: 10 },
  { month: "October", green: 2, yellow: 2, red: 9 },
];

const velocity = [
  { month: "May", points: 40 },
  { month: "June", points: 78 },
  { month: "July", points: 45 },
  { month: "August", points: 56 },
  { month: "September", points: 72 },
  { month: "October", points: 120 },
];

const teams = [
  { name: "AAA2(Design&Platform)", status: "Red", prev: "Red", backlog: 18 },
  { name: "DelEng&Support(DesignPlatform)", status: "Red", prev: "Red", backlog: 22 },
  { name: "OrangeSquad(DesignPlatform)", status: "Yellow", prev: "Green", backlog: 9 },
  { name: "Solution(Design&Dev)", status: "Green", prev: "Green", backlog: 54 },
  { name: "SupportTeam(DesignPlatform)", status: "Red", prev: "Orange", backlog: 8 },
  { name: "SystemTeam(DesignPlatform)", status: "Red", prev: "Red", backlog: 12 },
];

const statusColor = (s: string) =>
  s === "Green" ? "bg-emerald-500" : s === "Yellow" ? "bg-yellow-400" : "bg-rose-500";

// Simple animated card wrapper for subtle 3D/hover
const AnimatedCard: React.FC<React.PropsWithChildren<{ className?: string }>> = ({ className = "", children }) => (
  <motion.div
    className={`rounded-2xl border bg-white shadow-sm ${className}`}
    initial={{ y: 12, opacity: 0 }}
    animate={{ y: 0, opacity: 1 }}
    transition={{ type: "spring", stiffness: 140, damping: 18 }}
    whileHover={{ y: -3, boxShadow: "0 12px 30px rgba(0,0,0,0.10)" }}
    style={{ perspective: 1000 }}
  >
    {children}
  </motion.div>
);

// KPI card (with slight entrance + hover)
const KPI: React.FC<{ title: string; value: string | number; subtitle?: string; highlight?: boolean }> = ({ title, value, subtitle, highlight }) => (
  <motion.div
    className={`rounded-2xl border bg-white p-5 shadow-sm ${highlight ? "ring-2 ring-orange-500" : ""}`}
    initial={{ y: 16, opacity: 0, rotateX: 3 }}
    animate={{ y: 0, opacity: 1, rotateX: 0 }}
    transition={{ type: "spring", stiffness: 160, damping: 18 }}
    whileHover={{ y: -4, boxShadow: "0 16px 38px rgba(0,0,0,0.12)" }}
  >
    <div className="text-[11px] uppercase tracking-wide text-slate-500">{title}</div>
    <div className="mt-1 text-3xl font-semibold text-slate-800">{value}</div>
    {subtitle ? <div className="mt-1 text-xs text-slate-500">{subtitle}</div> : null}
  </motion.div>
);

// Simple dropdown filter button
const FilterButton: React.FC<{ label: string; value: string; options: string[]; onSelect: (v: string) => void }> = ({ label, value, options, onSelect }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="relative">
      <motion.button
        whileTap={{ scale: 0.98 }}
        onClick={() => setOpen((v) => !v)}
        className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm hover:bg-slate-50"
      >
        <Filter className="h-4 w-4" /> {label}: {value}
        <ChevronDown className="h-4 w-4" />
      </motion.button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 6 }}
            transition={{ type: "spring", stiffness: 260, damping: 22 }}
            className="absolute z-20 mt-2 w-56 rounded-xl border bg-white p-1 shadow-lg"
          >
            {options.map((opt) => (
              <button
                key={opt}
                onClick={() => {
                  onSelect(opt);
                  setOpen(false);
                }}
                className={`block w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-slate-50 ${
                  opt === value ? "bg-slate-100 font-medium" : ""
                }`}
              >
                {opt}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// -----------------------------
// Component
// -----------------------------
export default function AgileDashboard() {
  const [person] = useState("Ketan Desai");
  const [project, setProject] = useState("All Projects");

  const definedPct = calcDefinedPct(kpis.definedRatio);
  const donutData = useMemo(
    () => [
      { name: "Defined", value: calcDefinedPct(kpis.definedRatio) },
      { name: "Undefined", value: 100 - calcDefinedPct(kpis.definedRatio) },
    ],
    []
  );

  return (
    <div className="bg-white text-slate-800">
      {/* Top bar */}
      <div className="sticky top-0 z-30 flex items-center justify-between border-b bg-white/90 px-6 py-4 backdrop-blur">
        <div className="flex items-center gap-3">
          <button
            className="rounded-xl border p-2 hover:bg-slate-50"
            aria-label="Go back"
            onClick={() => (typeof window !== 'undefined' ? window.history.back() : null)}
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <div className="text-2xl font-extrabold tracking-tight">
            <span className="text-orange-600">Optum</span>
          </div>
          <div className="hidden text-sm text-slate-400 sm:block">Agile Leader Dashboard</div>
        </div>
        <div className="flex items-center gap-3">
          <span className="hidden sm:block text-xs text-slate-500">Logged in as <span className="font-medium">Leader</span></span>
          <button className="rounded-xl border bg-white p-2 hover:bg-slate-50">
            <Bell className="h-5 w-5" />
          </button>
          <button className="rounded-xl border bg-white p-2 hover:bg-slate-50">
            <Settings className="h-5 w-5" />
          </button>
        </div>
      </div>

      <div className="mx-auto max-w-[1240px] space-y-6 p-6">
        {/* Main */}
        <div className="space-y-6">
          <div className="-mb-2 text-sm">
            <button
              className="inline-flex items-center gap-1 rounded-lg px-2 py-1 text-slate-600 hover:bg-slate-100"
              onClick={() => (typeof window !== 'undefined' ? window.history.back() : null)}
            >
              Back
            </button>
          </div>
          <section aria-label="Susan Header">
            <AnimatedCard className="p-0 overflow-hidden">
              <div
                className="flex items-center justify-between rounded-t-2xl bg-slate-800 px-6 py-5 text-white"
                style={{
                  backgroundImage:
                    "radial-gradient(rgba(255,255,255,0.08) 1px, transparent 1px)",
                  backgroundSize: "22px 22px",
                }}
              >
                <div className="flex items-center gap-4">
                  <div className="grid h-14 w-14 place-items-center rounded-full bg-white/15 ring-4 ring-white/10">
                    <div className="h-9 w-9 rounded-md bg-white/50" />
                  </div>
                  <div>
                    <div className="text-3xl font-extrabold leading-tight drop-shadow">Susan</div>
                    <div className="text-[15px] font-semibold opacity-95">Project Insight</div>
                    <div className="-mt-0.5 text-xs opacity-80">Real-time project intelligence and analytics</div>
                  </div>
                </div>
                <button aria-label="Refresh" className="grid h-10 w-10 place-items-center rounded-full border border-white/25 bg-white/10 text-white/90 transition hover:bg-white/20">
                  <RotateCcw className="h-5 w-5" />
                </button>
              </div>
              <div className="flex gap-3 rounded-b-2xl bg-slate-100 p-3">
                <button className="inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2 text-sm text-slate-700 shadow-sm transition hover:bg-white/90">
                  <LayoutGrid className="h-4 w-4" /> Overview
                </button>
                <button className="inline-flex items-center gap-2 rounded-xl bg-slate-800 px-4 py-2 text-sm font-medium text-white shadow">
                  <BarChart3 className="h-4 w-4" /> Analytics
                </button>
                <button className="inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2 text-sm text-slate-700 shadow-sm transition hover:bg-white/90">
                  <Settings className="h-4 w-4" /> AI Insights
                </button>
                <button className="inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2 text-sm text-slate-700 shadow-sm transition hover:bg-white/90">
                  <MessageSquare className="h-4 w-4" /> Chat Assistant
                </button>
              </div>
            </AnimatedCard>
          </section>
          {/* Header row */}
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="text-sm text-slate-500">Hello {person}</div>
              <h1 className="text-2xl font-semibold">My Agile Dashboard</h1>
            </div>
            <div className="flex items-center gap-2">
              <FilterButton label="Person" value={person} options={["Ketan Desai", "Anita", "Rahul", "Priya"]} onSelect={() => {}} />
              <FilterButton label="Project" value={project} options={["All Projects", "Design Platform", "Delivery Support", "Orange Squad", "Solution", "Support Team", "System Team"]} onSelect={(v) => setProject(v)} />
            </div>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
            <KPI title="Unscheduled Defined" value={kpis.undefinedCount} />
            <KPI title="Defined vs Undefined Ratio" value={`${definedPct}%`} subtitle="October 2025" highlight />
            <KPI title="Planned Est. Pt." value={kpis.plannedPoints} />
            <KPI title="Planned Est. Next Sprint" value={kpis.nextSprintPoints} />
            <KPI title="Avg. Velocity" value={kpis.avgVelocity} />
          </div>

          {/* Team Status Trend + Table */}
          <AnimatedCard className="p-5">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-sm font-semibold">Team Status Trend by Month</h2>
            </div>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={monthlyStatus} stackOffset="expand" barCategoryGap={20}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="month" tickLine={false} axisLine={false} />
                  <YAxis hide />
                  <Tooltip cursor={{ fill: "rgba(0,0,0,0.04)" }} contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb" }} />
                  <Legend />
                  <Bar dataKey="green" stackId="a" name="Green" fill="#22c55e" isAnimationActive radius={[2, 2, 0, 0]} />
                  <Bar dataKey="yellow" stackId="a" name="Yellow" fill="#fde047" isAnimationActive radius={[2, 2, 0, 0]} />
                  <Bar dataKey="red" stackId="a" name="Red" fill="#ef4444" isAnimationActive radius={[2, 2, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-6 border-t pt-4">
              <div className="mb-2 flex items-center justify-between">
                <h3 className="text-sm font-semibold">Status by Team</h3>
              </div>
              <div className="max-h-64 overflow-auto rounded-xl border">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-slate-50 text-slate-600">
                    <tr>
                      <th className="px-4 py-3 text-left">Current Status</th>
                      <th className="px-4 py-3 text-left">Project Team</th>
                      <th className="px-4 py-3 text-left">Prior Month Status</th>
                      <th className="px-4 py-3 text-left">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {teams.map((t) => (
                      <tr key={t.name} className="border-t hover:bg-slate-50">
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`inline-flex h-2.5 w-2.5 rounded-full align-middle ${statusColor(t.status)}`} />
                          <span className="ml-2">{t.status}</span>
                        </td>
                        <td className="px-4 py-3">{t.name}</td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`inline-flex h-2.5 w-2.5 rounded-full align-middle ${statusColor(t.prev)}`} />
                          <span className="ml-2">{t.prev}</span>
                        </td>
                        <td className="px-4 py-3">
                          <motion.button whileTap={{ scale: 0.98 }} className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50">
                            Details
                          </motion.button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </AnimatedCard>

          {/* Velocity + Donut + Backlog */}
          <div className="grid grid-cols-12 gap-6">
            <AnimatedCard className="col-span-12 p-5 lg:col-span-7">
              <h2 className="mb-3 text-sm font-semibold">Team Velocity by Month</h2>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={velocity}>
                    <defs>
                      <linearGradient id="velArea" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.25} />
                        <stop offset="100%" stopColor="#f59e0b" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="month" tickLine={false} axisLine={false} />
                    <YAxis width={30} tickLine={false} axisLine={false} />
                    <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb" }} />
                    <Area type="monotone" dataKey="points" stroke="none" fill="url(#velArea)" />
                    <Line type="monotone" dataKey="points" stroke="#f59e0b" strokeWidth={3} dot={{ r: 3 }} activeDot={{ r: 5 }} />
                    <ReferenceDot x="June" y={78} r={5} stroke="#f59e0b" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </AnimatedCard>

            <div className="col-span-12 flex flex-col gap-6 lg:col-span-5">
              <AnimatedCard className="p-5">
                <h2 className="mb-2 text-sm font-semibold">Defined vs Undefined Ratio</h2>
                <div className="grid grid-cols-2 items-center gap-4">
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={donutData}
                          dataKey="value"
                          nameKey="name"
                          innerRadius={72}
                          outerRadius={96}
                          startAngle={90}
                          endAngle={-270}
                          cornerRadius={8}
                          paddingAngle={1}
                        >
                          <Cell key="defined" fill="#0ea5e9" />
                          <Cell key="undefined" fill="#e2e8f0" />
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div>
                    <div className="relative flex items-center justify-center">
                      <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ type: "spring", stiffness: 160, damping: 14 }}
                        className="text-5xl font-extrabold"
                      >
                        {definedPct}%
                      </motion.div>
                    </div>
                    <div className="mt-2 text-xs text-slate-500">Defined Stories<br />October 2025</div>
                    <div className="mt-3 space-y-1 text-xs">
                      <div className="flex items-center gap-2"><span className="inline-block h-2 w-2 rounded-full bg-sky-500" /> Defined (Scheduled)</div>
                      <div className="flex items-center gap-2"><span className="inline-block h-2 w-2 rounded-full bg-slate-300" /> Undefined (Unscheduled)</div>
                    </div>
                  </div>
                </div>
              </AnimatedCard>

              <AnimatedCard className="p-5">
                <h2 className="mb-3 text-sm font-semibold">Total Backlog Items by Team</h2>
                <div className="max-h-48 overflow-auto rounded-xl border">
                  <table className="w-full text-sm">
                    <thead className="sticky top-0 bg-slate-50 text-slate-600">
                      <tr>
                        <th className="px-4 py-3 text-left">Team Name</th>
                        <th className="px-4 py-3 text-left">Total Backlog</th>
                      </tr>
                    </thead>
                    <tbody>
                      {teams.map((t) => (
                        <tr key={t.name} className="border-t hover:bg-slate-50">
                          <td className="px-4 py-3">{t.name}</td>
                          <td className="px-4 py-3">{t.backlog}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </AnimatedCard>
            </div>
          </div>
        </div>
      </div>

      <footer className="mx-auto mt-2 max-w-[1240px] px-6 pb-10 text-center text-xs text-slate-400">
        © {new Date().getFullYear()} Optum-style Agile Dashboard (sample). Replace data with your APIs.
      </footer>
    </div>
  );
}
