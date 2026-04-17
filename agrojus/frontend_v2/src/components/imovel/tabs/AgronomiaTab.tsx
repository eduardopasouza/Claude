"use client";

import useSWR from "swr";
import { Loader2, Leaf, TrendingUp, Calendar } from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type MunicipioData = {
  meta?: { totalCount: number };
  data?: Array<{
    codigoIBGE: number;
    nome: string;
    uf: string;
    latitude: number;
    longitude: number;
    regiaoSoja: string;
    regiaoTrigo: string;
  }>;
};

type CulturasMunicipio = {
  meta?: { totalCount: number };
  data?: Array<{
    id: number;
    nome: string;
    cultivo: string;
    clima: string;
    hasZoneamento: boolean;
    hasCultivares?: boolean;
  }>;
};

type ProducaoAgricola = {
  municipio_code: string;
  culturas: Array<{
    cultura: string;
    variavel: string;
    valor: string;
    unidade: string;
    ano: string;
  }>;
};

export function AgronomiaTab({ property }: { property: PropertyData }) {
  const codIbge = property.cod_municipio_ibge;

  const { data: agritecMun } = useSWR<MunicipioData>(
    codIbge ? `/embrapa/agritec/municipio/${codIbge}` : null,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const { data: culturas } = useSWR<CulturasMunicipio>(
    codIbge ? `/embrapa/agritec/municipio/${codIbge}/culturas` : null,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const { data: producao } = useSWR<ProducaoAgricola>(
    codIbge ? `/property/search?municipio=${codIbge}` : null,
    null, // Skip for now
    { revalidateOnFocus: false }
  );

  const mun = agritecMun?.data?.[0] || (agritecMun as unknown as Record<string, unknown>);
  const zoneamentoSoja = (mun as Record<string, unknown>)?.regiaoSoja as string | undefined;
  const zoneamentoTrigo = (mun as Record<string, unknown>)?.regiaoTrigo as string | undefined;

  const culturasComZarc =
    culturas?.data?.filter((c) => c.hasZoneamento) || [];
  const culturasComCultivares =
    culturas?.data?.filter((c) => c.hasCultivares) || [];

  if (!codIbge) {
    return (
      <div className="p-6 text-sm text-slate-400">
        Código IBGE do município não disponível para este imóvel. Não foi
        possível cruzar com Embrapa Agritec.
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Leaf className="w-5 h-5 text-emerald-400" />
          Agronomia & Zoneamento Agrícola
        </h2>
        <span className="text-xs text-slate-500">
          Embrapa Agritec v2 · IBGE SIDRA
        </span>
      </header>

      {/* Context municipal */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <InfoCard
          label="Zoneamento Soja"
          value={zoneamentoSoja || "—"}
          hint={zoneamentoSoja ? `Região ZARC ${zoneamentoSoja}` : undefined}
        />
        <InfoCard
          label="Zoneamento Trigo"
          value={zoneamentoTrigo || "—"}
          hint={zoneamentoTrigo ? `Região ZARC ${zoneamentoTrigo}` : undefined}
        />
        <InfoCard
          label="Coordenada"
          value={
            (mun as Record<string, unknown>)?.latitude
              ? `${(
                  (mun as Record<string, unknown>).latitude as number
                ).toFixed(3)}, ${(
                  (mun as Record<string, unknown>).longitude as number
                ).toFixed(3)}`
              : "—"
          }
        />
      </div>

      {/* Culturas disponíveis */}
      {culturas ? (
        <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <div className="flex items-baseline justify-between mb-4">
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-emerald-400" />
              Culturas com ZARC no município
            </h3>
            <span className="text-sm text-slate-400">
              {culturas?.data?.length || 0} culturas · {culturasComZarc.length}{" "}
              com zoneamento
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
            {culturas?.data?.slice(0, 16).map((c) => (
              <div
                key={c.id}
                className={`border rounded-lg p-3 text-sm ${
                  c.hasZoneamento
                    ? "border-emerald-700/40 bg-emerald-950/20"
                    : "border-slate-800 bg-slate-900/30"
                }`}
              >
                <div className="font-medium text-slate-100 truncate">
                  {c.nome}
                </div>
                <div className="text-xs text-slate-400 mt-0.5 flex items-center gap-1">
                  {c.cultivo}
                  {c.hasZoneamento && (
                    <span className="text-emerald-400 ml-auto" title="Com ZARC">
                      ZARC
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {(culturas?.data?.length || 0) > 16 && (
            <p className="text-xs text-slate-500 mt-3">
              + {(culturas?.data?.length || 0) - 16} outras culturas
            </p>
          )}
        </section>
      ) : (
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <Loader2 className="w-4 h-4 animate-spin" /> Consultando Embrapa
          Agritec…
        </div>
      )}

      <footer className="text-xs text-slate-500">
        Para consulta ZARC detalhada (janelas de plantio por cultura × risco),
        use o endpoint <code className="text-emerald-400">/embrapa/agritec/zoneamento?idCultura=&codigoIBGE={codIbge}&risco=20</code>.
      </footer>
    </div>
  );
}

function InfoCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-lg p-4">
      <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">
        {label}
      </div>
      <div className="text-base font-semibold text-slate-100">{value}</div>
      {hint && <div className="text-xs text-slate-500 mt-1">{hint}</div>}
    </div>
  );
}
