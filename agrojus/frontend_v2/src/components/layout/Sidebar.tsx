"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Search,
  Map,
  ShieldCheck,
  TrendingUp,
  Newspaper,
  FileText,
  Gavel,
} from "lucide-react";

type NavItem = {
  name: string;
  href: string;
  icon: typeof LayoutDashboard;
  badge?: string;
};

type NavGroup = {
  label: string;
  items: NavItem[];
};

const NAV: NavGroup[] = [
  {
    label: "Plataforma",
    items: [
      { name: "Dashboard", href: "/", icon: LayoutDashboard },
      { name: "DeepSearch", href: "/consulta", icon: Search },
      { name: "Mapa GIS", href: "/mapa", icon: Map },
    ],
  },
  {
    label: "Jurídico",
    items: [
      { name: "Publicações", href: "/publicacoes", icon: Gavel, badge: "DJEN" },
      { name: "Processos", href: "/processos", icon: FileText },
    ],
  },
  {
    label: "Compliance & Mercado",
    items: [
      { name: "Compliance", href: "/compliance", icon: ShieldCheck },
      { name: "Mercado & Agro", href: "/mercado", icon: TrendingUp },
      { name: "Notícias", href: "/noticias", icon: Newspaper, badge: "RSS" },
      { name: "Monitoramento", href: "/alertas", icon: ShieldCheck },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 flex flex-col border-r border-border bg-sidebar h-full pb-4 shrink-0 shadow-[4px_0_24px_-10px_rgba(0,0,0,0.5)]">
      <div className="p-6 flex items-center gap-3">
        <span className="text-primary text-2xl font-bold bg-primary/10 w-10 h-10 flex items-center justify-center rounded-lg border border-primary/20">
          ⚖
        </span>
        <div>
          <h1 className="font-heading font-bold text-xl leading-tight uppercase tracking-tight">
            AgroJus<span className="text-primary">.</span>
          </h1>
          <span className="text-[10px] uppercase text-muted-foreground tracking-[0.2em] font-mono font-semibold">
            Enterprise
          </span>
        </div>
      </div>

      <nav className="flex-1 px-3 space-y-5 overflow-y-auto mt-2">
        {NAV.map((group) => (
          <div key={group.label}>
            <div className="mb-2 px-3 text-[10px] font-bold text-muted-foreground tracking-[0.15em] uppercase">
              {group.label}
            </div>
            <div className="space-y-1.5">
              {group.items.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 text-sm font-medium border ${
                      isActive
                        ? "bg-primary/10 text-primary border-primary/20 shadow-[0_0_15px_-3px_rgba(16,185,129,0.15)]"
                        : "text-muted-foreground border-transparent hover:bg-muted hover:text-foreground"
                    }`}
                  >
                    <item.icon
                      className={`h-4 w-4 ${
                        isActive ? "text-primary stroke-[2.5]" : "stroke-2"
                      }`}
                    />
                    <span className="flex-1">{item.name}</span>
                    {item.badge && (
                      <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20 uppercase tracking-wider">
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* API Status Ping */}
      <div className="px-6 mt-auto pt-6 border-t border-border/50">
        <div className="flex items-center gap-3 bg-muted/30 p-3 rounded-lg border border-border/50">
          <div className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
          </div>
          <div className="flex flex-col mt-0.5">
            <span className="text-[10px] font-bold text-primary tracking-widest">
              SYSTEM ONLINE
            </span>
            <span className="text-[10px] text-muted-foreground font-mono">
              API v0.5.0
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
