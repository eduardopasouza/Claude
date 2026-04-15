"use client";

import { Scale, Search, ExternalLink, Loader2 } from "lucide-react";
import { useState } from "react";
import { apiGet } from "@/lib/api";
import { cn } from "@/lib/utils";

interface Processo {
  numero: string;
  classe: string;
  assunto: string;
  tribunal: string;
  data: string;
  status: string;
}

export default function JurisdicaoPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Processo[]>([]);
  const [searched, setSearched] = useState(false);

  const search = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    const { data } = await apiGet<{ results: Processo[] }>(
      `/api/v1/consulta/datajud?q=${encodeURIComponent(query)}`
    );
    setResults(data?.results || []);
    setLoading(false);
  };

  return (
    <div className="space-y-8 max-w-5xl">
      <div>
        <h2 className="text-2xl font-display font-bold flex items-center gap-2">
          <Scale className="text-agrojus-emerald" size={24} />
          Jurisdição e Processos
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Busca unificada no DataJud/CNJ — processos judiciais por CPF, CNPJ ou nome
        </p>
      </div>

      <div className="glass rounded-xl p-4 flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && search()}
          placeholder="CPF, CNPJ, nome do réu ou número do processo…"
          className="flex-1 bg-agrojus-body border border-[var(--border)] rounded-lg px-4 py-2.5 text-sm text-foreground placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-1 focus:ring-agrojus-emerald"
        />
        <button
          onClick={search}
          disabled={loading}
          className="bg-agrojus-emerald text-agrojus-body rounded-lg px-5 py-2.5 text-sm font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
          Buscar
        </button>
      </div>

      {loading && (
        <div className="flex justify-center py-12">
          <Loader2 size={24} className="animate-spin text-agrojus-emerald" />
        </div>
      )}

      {!loading && searched && results.length === 0 && (
        <div className="text-center py-12 text-[var(--muted-foreground)] text-sm">
          Nenhum processo encontrado para esta consulta.
        </div>
      )}

      {results.length > 0 && (
        <div className="space-y-2">
          {results.map((p, i) => (
            <div key={i} className="glass rounded-xl p-4 hover:bg-agrojus-elevated/50 transition-colors">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-semibold font-mono">{p.numero}</p>
                  <p className="text-xs text-[var(--muted-foreground)] mt-0.5">
                    {p.classe} • {p.assunto}
                  </p>
                </div>
                <span
                  className={cn(
                    "text-xs px-2 py-0.5 rounded-full font-medium",
                    p.status === "Ativo"
                      ? "bg-risk-medium/20 text-risk-medium"
                      : "bg-risk-low/20 text-risk-low"
                  )}
                >
                  {p.status}
                </span>
              </div>
              <div className="flex items-center gap-4 mt-2 text-xs text-[var(--muted-foreground)]">
                <span>{p.tribunal}</span>
                <span>{p.data}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
