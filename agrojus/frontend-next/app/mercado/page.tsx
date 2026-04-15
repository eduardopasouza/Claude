"use client";

import { TrendingUp, BarChart3, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import { cn } from "@/lib/utils";

interface Commodity {
  nome: string;
  preco: string;
  variacao: number;
  unidade: string;
}

// Dados de referência — substitui por API CEPEA/IBGE quando integrada
const COMMODITIES: Commodity[] = [
  { nome: "Soja (Paranaguá)", preco: "R$ 139,50", variacao: 1.2, unidade: "sc 60kg" },
  { nome: "Milho (Campinas)", preco: "R$ 73,80", variacao: -0.5, unidade: "sc 60kg" },
  { nome: "Café Arábica (Cerrado)", preco: "R$ 1.420,00", variacao: 3.1, unidade: "sc 60kg" },
  { nome: "Boi Gordo (SP)", preco: "R$ 305,00", variacao: 0.8, unidade: "@" },
  { nome: "Algodão (MT)", preco: "R$ 142,30", variacao: -1.1, unidade: "ct lbs" },
  { nome: "Dólar PTAX", preco: "R$ 5,72", variacao: -0.3, unidade: "USD" },
  { nome: "Selic", preco: "14,25%", variacao: 0, unidade: "a.a." },
  { nome: "Terra Nua (MT)", preco: "R$ 28.500/ha", variacao: 2.4, unidade: "lavoura" },
];

export default function MercadoPage() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-display font-bold flex items-center gap-2">
          <TrendingUp className="text-agrojus-emerald" size={24} />
          Mercado e Indicadores
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Cotações CEPEA, IBGE SIDRA e indicadores macroeconômicos em tempo real
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {COMMODITIES.map((c) => (
          <div
            key={c.nome}
            className="glass rounded-xl p-5 glow-hover transition-all duration-200"
          >
            <p className="text-xs uppercase tracking-wider text-[var(--muted-foreground)] font-medium mb-1 truncate">
              {c.nome}
            </p>
            <p className="text-2xl font-display font-bold text-foreground">
              {c.preco}
            </p>
            <div className="flex items-center gap-1 mt-1">
              {c.variacao > 0 ? (
                <ArrowUpRight size={14} className="text-risk-low" />
              ) : c.variacao < 0 ? (
                <ArrowDownRight size={14} className="text-risk-critical" />
              ) : null}
              <span
                className={cn(
                  "text-xs font-medium",
                  c.variacao > 0
                    ? "text-risk-low"
                    : c.variacao < 0
                    ? "text-risk-critical"
                    : "text-[var(--muted-foreground)]"
                )}
              >
                {c.variacao > 0 ? "+" : ""}
                {c.variacao}%
              </span>
              <span className="text-[10px] text-[var(--muted-foreground)] ml-1">
                {c.unidade}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Placeholder para gráficos futuros */}
      <div className="glass rounded-xl p-8 text-center space-y-3">
        <BarChart3 size={32} className="mx-auto text-[var(--muted-foreground)]" />
        <p className="text-sm text-[var(--muted-foreground)]">
          Gráficos históricos e séries temporais em breve — integração IBGE SIDRA + BCB em andamento
        </p>
      </div>
    </div>
  );
}
