"use client";

import { useState } from "react";
import { ChevronDown, Moon, Sun, Satellite, Mountain } from "lucide-react";
import { BASEMAPS, BasemapId } from "@/lib/basemaps";

const ICONS: Record<BasemapId, typeof Moon> = {
  dark: Moon,
  light: Sun,
  satellite: Satellite,
  topo: Mountain,
};

export function BasemapSwitcher({
  value,
  onChange,
}: {
  value: BasemapId;
  onChange: (id: BasemapId) => void;
}) {
  const [open, setOpen] = useState(false);
  const current = BASEMAPS.find((b) => b.id === value) ?? BASEMAPS[0];
  const Icon = ICONS[current.id];

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-2 px-3 py-2 rounded-xl bg-background/85 backdrop-blur-xl border border-border shadow-[0_4px_24px_-4px_rgba(0,0,0,0.6)] text-xs hover:border-primary/40 transition"
        title="Mudar mapa base"
      >
        <Icon className="h-4 w-4 text-primary" />
        <span className="font-medium">{current.label}</span>
        <ChevronDown className={`h-3 w-3 transition ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="absolute top-full right-0 mt-2 w-56 rounded-xl bg-background/95 backdrop-blur-xl border border-border shadow-[0_8px_40px_-8px_rgba(0,0,0,0.8)] overflow-hidden z-[1000]">
          {BASEMAPS.map((b) => {
            const I = ICONS[b.id];
            const active = b.id === value;
            return (
              <button
                key={b.id}
                onClick={() => {
                  onChange(b.id);
                  setOpen(false);
                }}
                className={`w-full flex items-start gap-3 px-3 py-2.5 text-left transition ${
                  active ? "bg-primary/10" : "hover:bg-muted/40"
                }`}
              >
                <I className={`h-4 w-4 mt-0.5 ${active ? "text-primary" : "text-muted-foreground"}`} />
                <div className="flex-1 min-w-0">
                  <div className={`text-xs font-semibold ${active ? "text-primary" : ""}`}>
                    {b.label}
                  </div>
                  <div className="text-[10px] text-muted-foreground line-clamp-2">
                    {b.description}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
