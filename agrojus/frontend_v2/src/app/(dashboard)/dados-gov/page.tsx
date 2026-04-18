"use client";

import { useState } from "react";
import useSWR, { mutate } from "swr";
import {
  Database,
  Play,
  Loader2,
  CheckCircle2,
  XCircle,
  Clock,
  AlertCircle,
  RefreshCw,
} from "lucide-react";
import { fetchWithAuth, swrFetcher } from "@/lib/api";

type LayerStat = {
  table: string;
  label: string;
  rows: number;
  active: boolean;
};

type IngestExec = {
  id: number;
  loader: string;
  dataset_id: string | null;
  status: string;
  started_at: string | null;
  finished_at: string | null;
  rows_fetched: number | null;
  rows_persisted: number | null;
  duration_sec: number | null;
  error: string | null;
};

type LoaderResult = {
  loader: string;
  fetched: number;
  persisted: number;
  status: string;
  error?: string;
};

export default function DadosGovAdminPage() {
  const { data: stats } = useSWR<{ total_tables: number; active: number; stats: LayerStat[] }>(
    "/dados-gov/stats",
    swrFetcher,
    { refreshInterval: 15_000 }
  );
  const { data: loadersList } = useSWR<{ loaders: string[]; total: number }>(
    "/dados-gov/loaders",
    swrFetcher
  );
  const { data: status } = useSWR<{ total: number; executions: IngestExec[] }>(
    "/dados-gov/status?limit=30",
    swrFetcher,
    { refreshInterval: 10_000 }
  );

  const [running, setRunning] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<LoaderResult | null>(null);

  async function runLoader(name: string) {
    setRunning(name);
    setLastResult(null);
    try {
      const res = await fetchWithAuth(`/dados-gov/run?loader=${name}`, { method: "POST" });
      const data = (await res.json()) as LoaderResult;
      setLastResult(data);
      mutate("/dados-gov/stats");
      mutate("/dados-gov/status?limit=30");
    } catch (e) {
      setLastResult({ loader: name, fetched: 0, persisted: 0, status: "failed", error: String(e) });
    } finally {
      setRunning(null);
    }
  }

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
          <Database className="h-8 w-8 text-emerald-400" />
          Dados Gov — ETL Admin
        </h1>
        <p className="text-slate-400 mt-2">
          Operação dos 10 coletores dados.gov.br + 2 do Portal da Transparência.
          Execução síncrona (pode levar minutos). Em produção: agendado via cron diário às 03h.
        </p>
      </header>

      {/* Resumo */}
      {stats && (
        <section className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <StatCard label="Tabelas" value={stats.total_tables} color="slate" />
          <StatCard label="Ativas" value={stats.active} color="emerald" />
          <StatCard
            label="Registros totais"
            value={stats.stats.reduce((a, s) => a + s.rows, 0).toLocaleString("pt-BR")}
            color="emerald"
          />
          <StatCard
            label="Vazias"
            value={stats.total_tables - stats.active}
            color="amber"
          />
        </section>
      )}

      {/* Tabela de stats por camada */}
      <section className="border border-slate-800 rounded-xl overflow-hidden">
        <div className="bg-slate-900/60 px-4 py-2.5 border-b border-slate-800 flex items-center gap-2">
          <h2 className="text-sm font-semibold text-slate-200">Camadas integradas</h2>
          <button
            onClick={() => mutate("/dados-gov/stats")}
            className="ml-auto p-1 hover:bg-slate-800 rounded text-slate-500 hover:text-slate-200"
            title="Atualizar"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
        <table className="w-full text-sm">
          <thead className="bg-slate-900/30 text-xs uppercase tracking-wider text-slate-500">
            <tr>
              <th className="text-left px-4 py-2.5 font-medium">Tabela</th>
              <th className="text-left px-4 py-2.5 font-medium">Fonte</th>
              <th className="text-right px-4 py-2.5 font-medium">Registros</th>
              <th className="text-center px-4 py-2.5 font-medium">Status</th>
              <th className="text-center px-4 py-2.5 font-medium">Ação</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {(stats?.stats || []).map((s) => {
              const loaderName = tableToLoader(s.table);
              return (
                <tr key={s.table} className="hover:bg-slate-900/30">
                  <td className="px-4 py-2 font-mono text-xs text-slate-400">{s.table}</td>
                  <td className="px-4 py-2 text-slate-300">{s.label}</td>
                  <td className="px-4 py-2 text-right font-mono">
                    {s.rows > 0 ? (
                      <span className="text-emerald-400">
                        {s.rows.toLocaleString("pt-BR")}
                      </span>
                    ) : (
                      <span className="text-slate-600">—</span>
                    )}
                  </td>
                  <td className="px-4 py-2 text-center">
                    {s.active ? (
                      <span className="inline-flex items-center gap-1 text-[10px] bg-emerald-950/40 text-emerald-300 px-2 py-0.5 rounded uppercase tracking-wider">
                        <CheckCircle2 className="w-3 h-3" /> ativa
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-[10px] bg-slate-800 text-slate-500 px-2 py-0.5 rounded uppercase tracking-wider">
                        vazia
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-2 text-center">
                    {loaderName && (
                      <button
                        onClick={() => runLoader(loaderName)}
                        disabled={running !== null}
                        className="inline-flex items-center gap-1 text-xs px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded transition"
                      >
                        {running === loaderName ? (
                          <>
                            <Loader2 className="w-3 h-3 animate-spin" /> rodando
                          </>
                        ) : (
                          <>
                            <Play className="w-3 h-3" /> executar
                          </>
                        )}
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>

      {lastResult && (
        <section
          className={`border rounded-xl p-4 ${
            lastResult.status === "success"
              ? "border-emerald-900/40 bg-emerald-950/20 text-emerald-300"
              : "border-red-900/40 bg-red-950/20 text-red-300"
          }`}
        >
          <div className="flex items-center gap-2">
            {lastResult.status === "success" ? (
              <CheckCircle2 className="w-5 h-5" />
            ) : (
              <XCircle className="w-5 h-5" />
            )}
            <strong>
              {lastResult.loader} — {lastResult.status}
            </strong>
            <span className="text-xs opacity-80 ml-auto">
              fetched {lastResult.fetched} · persisted {lastResult.persisted}
            </span>
          </div>
          {lastResult.error && (
            <pre className="mt-2 text-xs opacity-80 whitespace-pre-wrap">{lastResult.error}</pre>
          )}
        </section>
      )}

      {/* Log de execuções */}
      <section className="border border-slate-800 rounded-xl overflow-hidden">
        <div className="bg-slate-900/60 px-4 py-2.5 border-b border-slate-800">
          <h2 className="text-sm font-semibold text-slate-200">
            Últimas execuções
            {status && (
              <span className="text-xs text-slate-500 ml-2 font-normal">
                ({status.total} registradas)
              </span>
            )}
          </h2>
        </div>
        <div className="divide-y divide-slate-800">
          {(status?.executions || []).slice(0, 20).map((e) => (
            <ExecutionRow key={e.id} exec={e} />
          ))}
          {(!status || status.executions.length === 0) && (
            <div className="px-4 py-8 text-center text-slate-500 text-sm">
              Nenhuma execução registrada.
            </div>
          )}
        </div>
      </section>

      <footer className="text-xs text-slate-500 pt-4 border-t border-slate-800">
        <p>
          <strong>Produção:</strong> agendar ETL diário via{" "}
          <code className="bg-slate-800 px-1 py-0.5 rounded text-xs">
            docker exec agrojus-backend-1 python -m scripts.run_dados_gov_etl --all
          </code>
        </p>
        <p className="mt-1">
          Loaders disponíveis: {loadersList?.loaders.join(" · ") || "—"}
        </p>
      </footer>
    </div>
  );
}

function StatCard({
  label,
  value,
  color,
}: {
  label: string;
  value: number | string;
  color: "slate" | "emerald" | "amber";
}) {
  const colors = {
    slate: "text-slate-200",
    emerald: "text-emerald-400",
    amber: "text-amber-400",
  };
  return (
    <div className="border border-slate-800 bg-slate-900/20 rounded-lg p-4">
      <div className="text-xs text-slate-500 uppercase tracking-wider font-medium">
        {label}
      </div>
      <div className={`text-3xl font-bold mt-1 ${colors[color]}`}>{value}</div>
    </div>
  );
}

function ExecutionRow({ exec }: { exec: IngestExec }) {
  const Icon =
    exec.status === "success"
      ? CheckCircle2
      : exec.status === "failed"
      ? XCircle
      : Clock;
  const color =
    exec.status === "success"
      ? "text-emerald-400"
      : exec.status === "failed"
      ? "text-red-400"
      : "text-amber-400";

  return (
    <div className="px-4 py-2.5 flex items-center gap-3 text-sm hover:bg-slate-900/30">
      <Icon className={`w-4 h-4 flex-shrink-0 ${color}`} />
      <span className="font-mono text-xs text-slate-400 w-32 truncate">
        {exec.loader}
      </span>
      <span className={`text-xs font-medium ${color} uppercase w-16`}>
        {exec.status}
      </span>
      <span className="text-xs text-slate-400">
        {exec.rows_persisted?.toLocaleString("pt-BR") || 0} rows
      </span>
      {exec.duration_sec && (
        <span className="text-xs text-slate-500 ml-auto">
          {exec.duration_sec.toFixed(0)}s
        </span>
      )}
      <span className="text-xs text-slate-500 ml-2">
        {exec.started_at && new Date(exec.started_at).toLocaleString("pt-BR")}
      </span>
      {exec.error && (
        <span className="text-xs text-red-400 truncate max-w-xs" title={exec.error}>
          <AlertCircle className="w-3 h-3 inline mr-1" />
          {exec.error}
        </span>
      )}
    </div>
  );
}

function tableToLoader(table: string): string | null {
  const map: Record<string, string> = {
    sigmine_processos: "sigmine",
    ana_outorgas_full: "ana_outorgas",
    ana_bho: "ana_bho",
    incra_assentamentos: "assentamentos",
    incra_quilombolas: "quilombolas",
    aneel_usinas: "aneel_usinas",
    aneel_linhas_transmissao: "aneel_linhas",
    garantia_safra: "garantia_safra",
    ceis_registros: "ceis",
    cnep_registros: "cnep",
  };
  return map[table] || null;
}
