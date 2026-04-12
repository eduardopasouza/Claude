"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import {
  LayoutDashboard,
  Search,
  Map,
  Shield,
  Scale,
  TrendingUp,
  Newspaper,
  Gavel,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { ApiStatus } from "@/components/layout/api-status";

const NAV_ITEMS = [
  { label: "Dashboard",  href: "/",           icon: LayoutDashboard },
  { label: "Consulta",   href: "/consulta",   icon: Search          },
  { label: "Mapa GIS",   href: "/mapa",       icon: Map             },
  { label: "Compliance", href: "/compliance", icon: Shield          },
  { label: "Jurisdição", href: "/jurisdicao", icon: Scale           },
  { label: "Mercado",    href: "/mercado",    icon: TrendingUp      },
  { label: "Notícias",   href: "/noticias",   icon: Newspaper       },
  { label: "Processos",  href: "/processos",  icon: Gavel           },
] as const;

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 flex flex-col glass border-r border-[var(--border)]",
        "transition-all duration-300 ease-in-out",
        collapsed ? "w-16" : "w-60"
      )}
    >
      {/* Brand */}
      <div
        className={cn(
          "flex items-center gap-3 px-3 py-4 shrink-0",
          collapsed && "justify-center"
        )}
      >
        {/* AJ icon */}
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-agrojus-emerald font-display font-bold text-sm text-agrojus-body select-none">
          AJ
        </span>

        {!collapsed && (
          <div className="flex flex-col min-w-0 leading-tight">
            <span className="font-display font-bold text-sm text-foreground tracking-tight truncate">
              AgroJus
            </span>
            <span className="text-[10px] font-medium text-agrojus-emerald uppercase tracking-widest">
              Enterprise
            </span>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto px-2 py-2 space-y-0.5">
        {NAV_ITEMS.map(({ label, href, icon: Icon }) => {
          const isActive =
            href === "/" ? pathname === "/" : pathname.startsWith(href);

          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-2 py-2 text-sm font-medium transition-colors duration-150 glow-hover",
                isActive
                  ? "bg-agrojus-emerald/20 text-agrojus-emerald"
                  : "text-[var(--muted-foreground)] hover:text-foreground hover:bg-agrojus-elevated",
                collapsed && "justify-center px-2"
              )}
              title={collapsed ? label : undefined}
            >
              <Icon
                size={18}
                className={cn(
                  "shrink-0",
                  isActive ? "text-agrojus-emerald" : "text-current"
                )}
              />
              {!collapsed && <span className="truncate">{label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* API Status */}
      <div className="shrink-0 border-t border-[var(--border)] py-2">
        <ApiStatus collapsed={collapsed} />
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className={cn(
          "flex items-center justify-center h-10 w-full shrink-0",
          "border-t border-[var(--border)] text-[var(--muted-foreground)]",
          "hover:text-foreground hover:bg-agrojus-elevated transition-colors duration-150"
        )}
        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>
    </aside>
  );
}
