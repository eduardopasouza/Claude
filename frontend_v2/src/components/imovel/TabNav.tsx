"use client";

import { LucideIcon } from "lucide-react";

export type TabId =
  | "visao"
  | "compliance"
  | "dossie"
  | "historico"
  | "agronomia"
  | "clima"
  | "valuation"
  | "logistica"
  | "juridico"
  | "credito"
  | "monitoramento"
  | "acoes";

export type TabDef = {
  id: TabId;
  label: string;
  icon: LucideIcon;
  implemented: boolean;
};

type Props = {
  tabs: TabDef[];
  current: TabId;
  onChange: (id: TabId) => void;
};

export function TabNav({ tabs, current, onChange }: Props) {
  return (
    <nav className="border-b border-slate-800 bg-slate-950/40 overflow-x-auto">
      <div className="flex min-w-max px-4">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const active = current === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onChange(tab.id)}
              disabled={!tab.implemented}
              className={`
                relative flex items-center gap-2 px-4 py-3 text-sm font-medium transition
                whitespace-nowrap
                ${
                  active
                    ? "text-emerald-400"
                    : tab.implemented
                    ? "text-slate-400 hover:text-slate-200"
                    : "text-slate-600 cursor-not-allowed"
                }
              `}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
              {!tab.implemented && (
                <span className="ml-1 text-[9px] uppercase bg-slate-800 text-slate-500 px-1.5 py-0.5 rounded">
                  em breve
                </span>
              )}
              {active && (
                <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-emerald-400" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
