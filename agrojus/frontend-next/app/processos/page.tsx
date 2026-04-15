"use client";

import { Gavel, Search, Loader2, FileText, AlertTriangle } from "lucide-react";
import { useState } from "react";
import { apiGet } from "@/lib/api";
import { cn } from "@/lib/utils";

export default function ProcessosPage() {
  const [cpf, setCpf] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Record<string, unknown> | null>(null);
  const [searched, setSearched] = useState(false);

  const search = async () => {
    if (!cpf.trim()) return;
    setLoading(true);
    setSearched(true);
    const clean = cpf.replace(/\D/g, "");
    const { data } = await apiGet<Record<string, unknown>>(
      `/api/v1/consulta/completa/${clean}`
    );
    setResults(data);
    setLoading(false);
  };

  return (
    <div className="space-y-8 max-w-5xl">
      <div>
        <h2 className="text-2xl font-display font-bold flex items-center gap-2">
          <Gavel className="text-agrojus-emerald" size={24} />
          Dossiê Completo
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Consulta unificada em todas as fontes — Receita, DataJud, IBAMA, MTE, SICOR, SICAR
        </p>
      </div>

      <div className="glass rounded-xl p-4 flex gap-3">
        <input
          type="text"
          value={cpf}
          onChange={(e) => setCpf(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && search()}
          placeholder="CPF ou CNPJ completo…"
          className="flex-1 bg-agrojus-body border border-[var(--border)] rounded-lg px-4 py-2.5 text-sm text-foreground placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-1 focus:ring-agrojus-emerald"
        />
        <button
          onClick={search}
          disabled={loading}
          className="bg-agrojus-emerald text-agrojus-body rounded-lg px-5 py-2.5 text-sm font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
          Gerar Dossiê
        </button>
      </div>

      {loading && (
        <div className="flex flex-col items-center justify-center py-16 gap-3">
          <Loader2 size={28} className="animate-spin text-agrojus-emerald" />
          <p className="text-sm text-[var(--muted-foreground)]">
            Consultando 6 fontes simultâneas…
          </p>
        </div>
      )}

      {!loading && searched && !results && (
        <div className="text-center py-12 text-[var(--muted-foreground)] text-sm flex flex-col items-center gap-2">
          <AlertTriangle size={20} />
          Nenhum resultado encontrado ou erro de conexão.
        </div>
      )}

      {results && (
        <div className="space-y-4">
          {Object.entries(results).map(([source, data]) => (
            <details key={source} className="glass rounded-xl group" open>
              <summary className="cursor-pointer p-4 flex items-center gap-3 hover:bg-agrojus-elevated/50 transition-colors rounded-xl">
                <FileText size={16} className="text-agrojus-emerald shrink-0" />
                <span className="font-semibold text-sm">
                  {source.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                </span>
                <span className="text-[10px] text-[var(--muted-foreground)] ml-auto uppercase tracking-wider">
                  {data ? "Dados encontrados" : "Sem dados"}
                </span>
              </summary>
              <div className="px-4 pb-4">
                <pre className="text-xs font-mono text-[var(--muted-foreground)] bg-agrojus-body rounded-lg p-3 overflow-x-auto max-h-64">
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
            </details>
          ))}
        </div>
      )}
    </div>
  );
}
