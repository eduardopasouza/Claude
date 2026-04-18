"use client";

import { useState } from "react";
import { Palette, X, Check } from "lucide-react";

export type PriceOption = {
  id: string;
  label: string;
  unit: string;
  group: "graos" | "industriais" | "proteinas";
};

// Mesmas opções da layers-catalog.ts, mapeadas
const PRICE_OPTIONS: PriceOption[] = [
  { id: "preco_soja_uf", label: "Soja", unit: "R$/sc 60kg", group: "graos" },
  { id: "preco_milho_uf", label: "Milho", unit: "R$/sc 60kg", group: "graos" },
  { id: "preco_sorgo_uf", label: "Sorgo", unit: "R$/sc 60kg", group: "graos" },
  { id: "preco_cafe_uf", label: "Café", unit: "R$/sc 60kg", group: "industriais" },
  { id: "preco_cana_uf", label: "Cana", unit: "R$/ton", group: "industriais" },
  { id: "preco_algodao_uf", label: "Algodão", unit: "R$/@", group: "industriais" },
  { id: "preco_acucar_uf", label: "Açúcar", unit: "R$/sc 50kg", group: "industriais" },
  { id: "preco_boi_uf", label: "Boi gordo", unit: "R$/@", group: "proteinas" },
  { id: "preco_frango_uf", label: "Frango", unit: "R$/kg", group: "proteinas" },
  { id: "preco_leite_uf", label: "Leite", unit: "R$/L", group: "proteinas" },
];

const GROUP_LABELS: Record<string, string> = {
  graos: "Grãos",
  industriais: "Permanentes & Industriais",
  proteinas: "Proteínas",
};

type Props = {
  activeLayerId: string | null;
  onSelect: (id: string | null) => void;
};

export function PriceChoroplethWidget({ activeLayerId, onSelect }: Props) {
  const [open, setOpen] = useState(false);
  const active = PRICE_OPTIONS.find((o) => o.id === activeLayerId);

  const grouped = PRICE_OPTIONS.reduce((acc, opt) => {
    (acc[opt.group] ||= []).push(opt);
    return acc;
  }, {} as Record<string, PriceOption[]>);

  return (
    <div className="absolute top-4 left-[17rem] z-[800]">
      <button
        onClick={() => setOpen((v) => !v)}
        className={`
          flex items-center gap-2 px-3 py-2 rounded-lg backdrop-blur-md border text-sm
          ${
            active
              ? "bg-emerald-500/20 border-emerald-400/50 text-emerald-100"
              : "bg-slate-950/70 border-slate-700 text-slate-200 hover:border-slate-500"
          }
        `}
        title="Colorir o mapa por preço de uma commodity"
      >
        <Palette className="w-4 h-4" />
        <span className="font-medium">
          {active ? `Preço: ${active.label}` : "Colorir por preço"}
        </span>
        {active && (
          <span
            role="button"
            onClick={(e) => {
              e.stopPropagation();
              onSelect(null);
              setOpen(false);
            }}
            className="ml-1 hover:bg-red-500/20 rounded p-0.5"
          >
            <X className="w-3 h-3" />
          </span>
        )}
      </button>

      {open && (
        <div className="absolute top-full mt-1.5 w-64 bg-slate-950/95 backdrop-blur-xl border border-slate-700 rounded-xl shadow-2xl p-2">
          {Object.entries(grouped).map(([group, opts]) => (
            <div key={group} className="mb-2 last:mb-0">
              <div className="text-[10px] uppercase tracking-wider text-slate-500 font-bold px-2 py-1">
                {GROUP_LABELS[group]}
              </div>
              {opts.map((o) => {
                const isActive = o.id === activeLayerId;
                return (
                  <button
                    key={o.id}
                    onClick={() => {
                      onSelect(isActive ? null : o.id);
                      setOpen(false);
                    }}
                    className={`
                      w-full text-left px-2 py-1.5 rounded-lg flex items-center justify-between gap-2
                      ${
                        isActive
                          ? "bg-emerald-500/20 text-emerald-200"
                          : "text-slate-300 hover:bg-slate-800"
                      }
                    `}
                  >
                    <span className="text-sm">{o.label}</span>
                    <span className="flex items-center gap-2">
                      <span className="text-[10px] text-slate-500">{o.unit}</span>
                      {isActive && <Check className="w-3 h-3 text-emerald-400" />}
                    </span>
                  </button>
                );
              })}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
