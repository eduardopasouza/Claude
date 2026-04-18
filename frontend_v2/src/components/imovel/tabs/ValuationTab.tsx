"use client";

import useSWR from "swr";
import { Calculator, Loader2, TrendingDown, AlertTriangle } from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type ValuationResponse = {
  car_code: string;
  area_ha: number;
  uf: string;
  metodologia: string;
  preco_medio_ha_uf: number;
  valor_base_rs: number;
  descontos: Array<{ layer: string; count: number; pct: number }>;
  fator_desconto_total: number;
  valor_estimado_rs: number;
  fonte_precos: string;
  disclaimer: string;
  error?: string;
};

export function ValuationTab({ property }: { property: PropertyData }) {
  const { data, isLoading, error } = useSWR<ValuationResponse>(
    `/property/${property.car_code}/valuation`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (isLoading) {
    return (
      <div className="p-12 flex items-center justify-center text-slate-400">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        Calculando valuation…
      </div>
    );
  }

  if (error || data?.error) {
    return (
      <div className="p-6 text-red-300">
        Erro: {data?.error || "falha ao calcular valuation"}
      </div>
    );
  }

  if (!data) return null;

  const hasDiscount = data.fator_desconto_total > 0;

  return (
    <div className="p-6 space-y-5">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Calculator className="w-5 h-5 text-emerald-400" />
          Valuation Rural
        </h2>
        <span className="text-xs text-slate-500">{data.metodologia}</span>
      </header>

      {/* Valor final em destaque */}
      <div
        className={`border rounded-xl p-6 ${
          hasDiscount
            ? "bg-amber-950/20 border-amber-500/30"
            : "bg-emerald-950/20 border-emerald-500/30"
        }`}
      >
        <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">
          Valor estimado
        </div>
        <div className="text-4xl font-bold text-slate-100 tabular-nums">
          {formatBRL(data.valor_estimado_rs)}
        </div>
        <div className="mt-2 text-sm text-slate-400">
          {data.area_ha.toFixed(2)} ha em {data.uf} ·{" "}
          {formatBRL(data.preco_medio_ha_uf)}/ha regional
        </div>
      </div>

      {/* Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Stat
          label="Área"
          value={`${data.area_ha.toFixed(2)} ha`}
        />
        <Stat
          label="Preço médio UF"
          value={`${formatBRL(data.preco_medio_ha_uf)}/ha`}
        />
        <Stat
          label="Valor base"
          value={formatBRL(data.valor_base_rs)}
        />
      </div>

      {/* Descontos aplicados */}
      {hasDiscount && (
        <section className="bg-red-950/20 border border-red-900/40 rounded-xl p-5">
          <h3 className="font-semibold text-red-300 mb-3 flex items-center gap-2">
            <TrendingDown className="w-4 h-4" />
            Descontos por risco socioambiental
          </h3>
          <div className="space-y-2">
            {data.descontos.map((d, i) => (
              <div
                key={i}
                className="flex justify-between text-sm py-2 border-b border-red-900/30 last:border-0"
              >
                <span className="text-slate-300">
                  Sobreposição com{" "}
                  <span className="font-semibold">
                    {d.layer.replace(/_/g, " ")}
                  </span>{" "}
                  ({d.count})
                </span>
                <span className="text-red-300 font-semibold">
                  {d.pct}%
                </span>
              </div>
            ))}
            <div className="flex justify-between text-sm pt-2 font-semibold">
              <span className="text-slate-200">
                Fator desconto total aplicado
              </span>
              <span className="text-red-300">
                −{(data.fator_desconto_total * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </section>
      )}

      {/* Disclaimer */}
      <div className="bg-slate-900/40 border border-slate-800 rounded-lg p-4 flex items-start gap-3">
        <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
        <div className="text-xs text-slate-400 leading-relaxed">
          <p className="mb-1">
            <span className="font-semibold text-slate-300">Disclaimer:</span>{" "}
            {data.disclaimer}
          </p>
          <p>
            Fonte de preços: {data.fonte_precos}. Valuation definitivo requer
            comparativos locais, vistoria técnica, avaliação de benfeitorias e
            método de capitalização (NBR 14.653-3 nível II ou III).
          </p>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-lg p-4">
      <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">
        {label}
      </div>
      <div className="text-lg font-semibold text-slate-100 tabular-nums">
        {value}
      </div>
    </div>
  );
}

function formatBRL(v: number): string {
  if (v >= 1_000_000) {
    return `R$ ${(v / 1_000_000).toFixed(2).replace(".", ",")} mi`;
  }
  if (v >= 1_000) {
    return `R$ ${(v / 1_000).toLocaleString("pt-BR", {
      maximumFractionDigits: 1,
    })} mil`;
  }
  return `R$ ${v.toFixed(0)}`;
}
