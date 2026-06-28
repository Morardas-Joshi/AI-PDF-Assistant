import { Outlet, NavLink } from "react-router-dom";
import { FileSearch, Files, MessageSquareText, Search, Settings, Sparkles } from "lucide-react";

import { cn } from "../utils/cn";
import { Button } from "../components/ui/Button";

const navItems = [
  { to: "/", label: "Overview", icon: FileSearch },
  { to: "/documents", label: "Documents", icon: Files },
  { to: "/chat", label: "Chat", icon: MessageSquareText },
  { to: "/search", label: "Search", icon: Search },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function AppShell() {
  return (
    <div className="min-h-screen bg-[#f6f7f4] text-stone-950 dark:bg-[#111412] dark:text-stone-50">
      <div className="flex min-h-screen">
        <aside className="hidden w-72 border-r border-stone-200 bg-white/78 px-4 py-5 backdrop-blur-xl dark:border-stone-800 dark:bg-stone-950/70 lg:block">
          <div className="mb-7 flex items-center gap-3 px-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-600 text-white">
              <Sparkles size={20} />
            </div>
            <div>
              <p className="text-sm font-semibold">AI PDF Assistant</p>
              <p className="text-xs text-stone-500 dark:text-stone-400">Local RAG workspace</p>
            </div>
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  cn(
                    "flex h-10 items-center gap-3 rounded-md px-3 text-sm font-medium text-stone-600 transition hover:bg-stone-100 hover:text-stone-950 dark:text-stone-300 dark:hover:bg-stone-900",
                    isActive && "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300",
                  )
                }
              >
                <item.icon size={18} />
                {item.label}
              </NavLink>
            ))}
          </nav>
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-20 border-b border-stone-200 bg-[#f6f7f4]/84 px-4 py-3 backdrop-blur-xl dark:border-stone-800 dark:bg-[#111412]/84 sm:px-6">
            <div className="flex items-center justify-between gap-4">
              <div className="min-w-0">
                <p className="text-xs font-medium uppercase tracking-[0.18em] text-emerald-700 dark:text-emerald-300">
                  Workspace
                </p>
                <h1 className="truncate text-xl font-semibold">Document Intelligence Console</h1>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="secondary" size="icon" aria-label="Settings">
                  <Settings size={18} />
                </Button>
                <Button>
                  <Files size={18} />
                  Upload
                </Button>
              </div>
            </div>
          </header>
          <main className="flex-1 px-4 py-5 sm:px-6 lg:px-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}

