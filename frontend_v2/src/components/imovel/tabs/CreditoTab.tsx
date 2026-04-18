"use client";

import useSWR from "swr";
import { Coins, Loader2, TrendingUp, Landmark } from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type CreditRecord = {
  order_number?: string;
  year?: number;
  car_code?: string;
  vl_parc_credito?: number;
  vl_area_financ?: number;
  dt_emissao?: string;
  cnpj_if?: string;
};

type CreditResponse = {
  car_code: string;
  summary: {
    total_contratos: number;
    valor_total_rs: number;
    area_financiada_ha: number;
    por_ano: Array<{
      year: string;
      valor_total: number;
      area_total: number;
      contratos: number;
    }>;
  };
  records: CreditRecord[];
  error?: string;
};

export function CreditoTab({ property }: { property: PropertyData }) {
  const { data, isLoading, error } = useSWR<CreditResponse>(
    `/property/${property.car_code}/credit?limit=100`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  if (isLoading) {
    return (
      <div className="p-12 flex items-center justify-center text-slate-400">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        Buscando contratos SICOR intersectando CAR…
      </div>
    );
  }

  if (error || data?.error) {
    return (
      <div className="p-6 text-red-300">
        Erro: {data?.error || "falha ao consultar crédito"}
      </div>
    );
  }

  const s = data?.summary;
  const records = data?.records || [];
  const maxYear = Math.max(1, ...(s?.por_ano || []).map((x) => x.valor_total || 0));

  return (
    <div className="p-6 space-y-5">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Coins className="w-5 h-5 text-emerald-400" />
          Crédito Rural
        </h2>
        <span className="text-xs text-slate-500">
          MapBiomas × SICOR (BCB) · 5.6M contratos
        </span>
      </header>

      {records.length === 0 ? (
        <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-8 text-center">
          <Landmark className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-slate-300 font-medium mb-1">
            Nenhum contrato cruzado com este CAR
          </h3>
          <p className="text-sm text-slate-500">
            A base MapBiomas × SICOR não encontrou contratos de crédito rural
            cujas coordenadas intersectem a geometria deste imóvel.
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <StatBig
              label="Contratos"
              value={s?.total_contratos.toString() || "0"}
              icon={Landmark}
            />
            <StatBig
              label="Valor total"
              value={formatBRL(s?.valor_total_rs || 0)}
              icon={Coins}
            />
            <StatBig
              label="Área financiada"
              value={`${(s?.area_financiada_ha || 0).toFixed(1)} ha`}
              icon={TrendingUp}
            />
          </div>

          {/* Chart por ano */}
          {(s?.por_ano || []).length > 0 && (
            <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
              <h3 className="text-sm font-semibold text-slate-200 mb-4">
                Histórico por ano
              </h3>
              <div className="space-y-2">
                {(s?.por_ano || []).map((y) => {
                  const pct = ((y.valor_total || 0) / maxYear) * 100;
                  return (
                    <div key={y.year}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">{y.year}</span>
                        <span className="text-slate-500">
                          {y.contratos} contrato(s) · {formatBRL(y.valor_total)}
                        </span>
                      </div>
                      <div className="h-2 bg-slate-800 rounded overflow-hidden">
                        <div
                          className="h-full bg-emerald-500/60"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>
          )}

          {/* Tabela de contratos */}
          <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-slate-200 mb-3">
              Contratos (top {Math.min(records.length, 20)})
            </h3>
            <div className="divide-y divide-slate-800">
              {records.slice(0, 20).map((r, i) => (
                <div
                  key={i}
                  className="py-2 text-sm grid grid-cols-12 gap-2 items-baseline"
                >
                  <span className="col-span-2 text-xs text-slate-500 font-mono">
                    {r.year}
                  </span>
                  <span className="col-span-3 text-slate-400 font-mono text-xs">
                    {(r.order_number || "").slice(0, 16)}
                  </span>
                  <span className="col-span-3 text-slate-300 text-xs">
                    IF: {(r.cnpj_if || "").slice(0, 18)}
                  </span>
                  <span className="col-span-2 text-slate-400 text-xs tabular-nums">
                    {r.vl_area_financ ? `${r.vl_area_financ.toFixed(1)}ha` : "—"}
                  </span>
                  <span className="col-span-2 text-slate-100 tabular-nums font-semibold text-right">
                    {formatBRL(r.vl_parc_credito || 0)}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function StatBig({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: string;
  icon: typeof Coins;
}) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs uppercase tracking-wider text-slate-500">
          {label}
        </span>
        <Icon className="w-4 h-4 text-emerald-400/80" />
      </div>
      <div className="text-xl font-semibold text-slate-100 tabular-nums">
        {value}
      </div>
    </div>
  );
}

function formatBRL(v: number): string {
  if (!v) return "R$ 0";
  if (v >= 1_000_000)
    return `R$ ${(v / 1_000_000).toFixed(2).replace(".", ",")}M`;
  if (v >= 1_000) return `R$ ${(v / 1_000).toFixed(0)}k`;
  return `R$ ${v.toFixed(0)}`;
}
