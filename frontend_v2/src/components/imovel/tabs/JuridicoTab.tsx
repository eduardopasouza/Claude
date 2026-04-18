"use client";

import { useState } from "react";
import useSWR from "swr";
import {
  Scale,
  Loader2,
  Search as SearchIcon,
  Gavel,
  ExternalLink,
  User2,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type DataJudResult = {
  status: string;
  total_found?: number;
  results?: Array<{
    numero_processo: string;
    tribunal: string;
    classe?: string;
    assunto?: string;
    data_ajuizamento?: string;
    valor_causa?: number;
  }>;
  error?: string;
};

export function JuridicoTab({ property }: { property: PropertyData }) {
  const [cpfCnpj, setCpfCnpj] = useState("");
  const [submittedCpf, setSubmittedCpf] = useState<string | null>(null);

  const endpoint = submittedCpf
    ? `/lawsuits/search/${encodeURIComponent(submittedCpf)}`
    : null;

  const { data, error, isLoading } = useSWR<DataJudResult>(
    endpoint,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const clean = cpfCnpj.replace(/\D/g, "");
    if (clean.length >= 11) setSubmittedCpf(clean);
  }

  return (
    <div className="p-6 space-y-5">
      <header className="flex items-baseline justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Scale className="w-5 h-5 text-emerald-400" />
          Dossiê Jurídico
        </h2>
        <span className="text-xs text-slate-500">DataJud CNJ · DJEN</span>
      </header>

      {!property.cod_municipio_ibge && (
        <div className="text-xs text-slate-500 bg-slate-900/40 border border-slate-800 rounded p-3 flex items-start gap-2">
          <User2 className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <span>
            A ficha CAR não vincula proprietário (LGPD). Informe o CPF/CNPJ do
            proprietário abaixo para cruzar com DataJud e DJEN.
          </span>
        </div>
      )}

      <form
        onSubmit={handleSearch}
        className="flex gap-2 bg-slate-900/50 border border-slate-800 rounded-lg p-2"
      >
        <input
          type="text"
          placeholder="CPF ou CNPJ (só números ou com pontos)"
          value={cpfCnpj}
          onChange={(e) => setCpfCnpj(e.target.value)}
          className="flex-1 bg-transparent px-3 py-2 outline-none text-sm text-slate-100 placeholder:text-slate-500"
        />
        <button
          type="submit"
          disabled={cpfCnpj.replace(/\D/g, "").length < 11}
          className="px-4 py-2 bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 rounded text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:bg-emerald-500/30 transition flex items-center gap-2"
        >
          <SearchIcon className="w-4 h-4" />
          Buscar processos
        </button>
      </form>

      {isLoading && (
        <div className="p-8 flex items-center justify-center text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          Consultando 13 tribunais via DataJud CNJ…
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-950/30 border border-red-900/40 rounded text-red-300 text-sm">
          Erro: {String(error).slice(0, 200)}
        </div>
      )}

      {data && !isLoading && (
        <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <div className="flex items-baseline justify-between mb-4">
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              <Gavel className="w-4 h-4" />
              Resultados DataJud
            </h3>
            <span className="text-sm text-slate-400">
              {data.total_found || 0} processo(s) encontrado(s)
            </span>
          </div>

          {(data.results || []).length === 0 && (
            <div className="py-6 text-center text-slate-500 text-sm">
              Nenhum processo encontrado para {submittedCpf}.
            </div>
          )}

          <div className="divide-y divide-slate-800">
            {(data.results || []).slice(0, 15).map((p, i) => (
              <div key={i} className="py-3 flex flex-wrap gap-x-4 gap-y-1">
                <span className="font-mono text-xs text-slate-500">
                  {p.tribunal}
                </span>
                <span className="text-sm text-slate-200 font-mono">
                  {p.numero_processo}
                </span>
                {p.classe && (
                  <span className="text-xs text-slate-400">{p.classe}</span>
                )}
                {p.data_ajuizamento && (
                  <span className="text-xs text-slate-500 ml-auto">
                    {p.data_ajuizamento}
                  </span>
                )}
              </div>
            ))}
          </div>

          {(data.results || []).length > 15 && (
            <div className="text-xs text-slate-500 mt-3">
              + {(data.results || []).length - 15} mais…
            </div>
          )}
        </section>
      )}

      <footer className="text-xs text-slate-500 flex items-start gap-1">
        <ExternalLink className="w-3 h-3 mt-0.5 flex-shrink-0" />
        Futuro: publicações DJEN do proprietário + protestos SERASA + CNDT +
        quadro societário SERPRO.
      </footer>
    </div>
  );
}
