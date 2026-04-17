"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import useSWR from "swr";
import {
  Building2,
  Calendar,
  Clock,
  FileText,
  Filter,
  Gavel,
  Loader2,
  Scale,
  Search as SearchIcon,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------
type LawsuitRecord = {
  case_number?: string;
  tribunal?: string;
  court?: string;
  municipality?: string;
  state?: string;
  subjects?: string[];
  class_name?: string;
  filing_date?: string;
  last_update?: string;
  status?: string;
  degree?: string;
  system?: string;
};

type SearchResponse = {
  source: string;
  cpf_cnpj?: string;
  subject?: string;
  subject_code?: string;
  tribunal?: string;
  total: number;
  records: LawsuitRecord[];
};

// ---------------------------------------------------------------------------
// Assuntos CNJ agro/ambientais com nomes amigáveis
// ---------------------------------------------------------------------------
const ASSUNTOS = [
  { code: "10432", name: "Usucapião" },
  { code: "10445", name: "Desapropriação" },
  { code: "10452", name: "Servidão" },
  { code: "10455", name: "Posse" },
  { code: "10456", name: "Propriedade" },
  { code: "10673", name: "Dano Ambiental" },
  { code: "11793", name: "Trabalho Rural" },
  { code: "14045", name: "Contratos Agrários" },
  { code: "14046", name: "Arrendamento Rural" },
  { code: "14047", name: "Parceria Rural" },
];

const TRIBUNAIS_POPULARES = [
  { code: "TRF1", name: "TRF1 (DF,GO,MA,MG,BA,MT,PA,PI,RR,AM,AP,AC,RO,TO)" },
  { code: "TRF2", name: "TRF2 (RJ,ES)" },
  { code: "TRF3", name: "TRF3 (SP,MS)" },
  { code: "TRF4", name: "TRF4 (RS,SC,PR)" },
  { code: "TRF5", name: "TRF5 (CE,AL,PB,PE,RN,SE)" },
  { code: "TRF6", name: "TRF6 (MG)" },
  { code: "TJMA", name: "TJ Maranhão" },
  { code: "TJSP", name: "TJ São Paulo" },
  { code: "TJMT", name: "TJ Mato Grosso" },
  { code: "TJPA", name: "TJ Pará" },
  { code: "TJGO", name: "TJ Goiás" },
  { code: "TJBA", name: "TJ Bahia" },
  { code: "TJTO", name: "TJ Tocantins" },
];

// ---------------------------------------------------------------------------
// Página
// ---------------------------------------------------------------------------
export default function ProcessosPage() {
  return (
    <Suspense
      fallback={
        <div className="p-8 text-center text-muted-foreground">Carregando…</div>
      }
    >
      <ProcessosContent />
    </Suspense>
  );
}

function ProcessosContent() {
  const sp = useSearchParams();
  const qParam = sp.get("q") ?? "";

  const [mode, setMode] = useState<"documento" | "assunto">("documento");
  const [documento, setDocumento] = useState(isDocument(qParam) ? qParam : "");
  const [assunto, setAssunto] = useState("10673");
  const [tribunal, setTribunal] = useState("TRF1");
  const [tribunaisAdicionais, setTribunaisAdicionais] = useState<string[]>([
    "TRF1",
    "TRF2",
    "TRF3",
    "TRF4",
    "TRF5",
  ]);
  const [maxResults, setMaxResults] = useState(20);
  const [triggered, setTriggered] = useState(Boolean(documento));

  const endpoint = useMemo(() => {
    if (!triggered) return null;
    if (mode === "documento" && documento) {
      const clean = documento.replace(/\D/g, "");
      const trib = tribunaisAdicionais.join(",");
      return `/lawsuits/search/${clean}?tribunais=${trib}&max_results=${maxResults}`;
    }
    if (mode === "assunto") {
      return `/lawsuits/subject/${assunto}?tribunal=${tribunal}&max_results=${maxResults}`;
    }
    return null;
  }, [triggered, mode, documento, assunto, tribunal, tribunaisAdicionais, maxResults]);

  const { data, error, isLoading, mutate } = useSWR<SearchResponse>(
    endpoint,
    swrFetcher,
    { revalidateOnFocus: false, dedupingInterval: 30_000 }
  );

  useEffect(() => {
    if (qParam && isDocument(qParam)) {
      setDocumento(qParam);
      setMode("documento");
      setTriggered(true);
    }
  }, [qParam]);

  const records = data?.records ?? [];

  const kpis = useMemo(() => {
    const porTribunal: Record<string, number> = {};
    records.forEach((r) => {
      if (r.tribunal) porTribunal[r.tribunal] = (porTribunal[r.tribunal] ?? 0) + 1;
    });
    return {
      total: records.length,
      porTribunal,
      ultimoAno: records.filter((r) => {
        if (!r.filing_date) return false;
        try {
          return new Date(r.filing_date).getFullYear() >= new Date().getFullYear() - 1;
        } catch {
          return false;
        }
      }).length,
    };
  }, [records]);

  return (
    <div className="p-6 md:p-8 max-w-[1400px] mx-auto">
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Scale className="h-6 w-6 text-primary" />
          <h1 className="font-heading font-bold text-2xl md:text-3xl">
            Processos Judiciais
          </h1>
          <span className="text-[10px] font-mono px-2 py-1 rounded bg-primary/10 text-primary border border-primary/20 uppercase tracking-wider">
            DataJud CNJ
          </span>
        </div>
        <p className="text-sm text-muted-foreground">
          Consulta direta à API Pública do CNJ — 88 tribunais (TRFs, TJs, TRTs,
          STJ, TST). Filtros por CPF/CNPJ ou por assunto agrário/ambiental.
        </p>
      </div>

      <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm mb-6 space-y-4">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setMode("documento")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              mode === "documento"
                ? "bg-primary/10 text-primary border border-primary/30"
                : "bg-muted/30 text-muted-foreground border border-border hover:bg-muted/50"
            }`}
          >
            <SearchIcon className="h-3.5 w-3.5 inline mr-2" />
            Por CPF/CNPJ
          </button>
          <button
            onClick={() => setMode("assunto")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              mode === "assunto"
                ? "bg-primary/10 text-primary border border-primary/30"
                : "bg-muted/30 text-muted-foreground border border-border hover:bg-muted/50"
            }`}
          >
            <Filter className="h-3.5 w-3.5 inline mr-2" />
            Por Assunto CNJ
          </button>
        </div>

        {mode === "documento" ? (
          <div className="flex flex-wrap items-end gap-3">
            <div className="flex-1 min-w-[240px]">
              <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                CPF ou CNPJ
              </label>
              <input
                value={documento}
                onChange={(e) => setDocumento(e.target.value)}
                placeholder="Digite só números ou com máscara"
                className="mt-1 w-full bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                Tribunais
              </label>
              <select
                multiple
                value={tribunaisAdicionais}
                onChange={(e) =>
                  setTribunaisAdicionais(
                    Array.from(e.target.selectedOptions).map((o) => o.value)
                  )
                }
                className="mt-1 bg-input/40 border border-border rounded-lg px-2 py-2 text-xs font-mono w-56 h-24 focus:outline-none focus:ring-1 focus:ring-primary"
              >
                {TRIBUNAIS_POPULARES.map((t) => (
                  <option key={t.code} value={t.code}>
                    {t.code}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                Limite
              </label>
              <select
                value={maxResults}
                onChange={(e) => setMaxResults(Number(e.target.value))}
                className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm"
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
            <button
              onClick={() => {
                setTriggered(true);
                mutate();
              }}
              disabled={!documento}
              className="px-5 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition font-semibold text-sm disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Buscar no DataJud
            </button>
          </div>
        ) : (
          <div className="flex flex-wrap items-end gap-3">
            <div>
              <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                Assunto CNJ
              </label>
              <select
                value={assunto}
                onChange={(e) => setAssunto(e.target.value)}
                className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm min-w-[220px]"
              >
                {ASSUNTOS.map((a) => (
                  <option key={a.code} value={a.code}>
                    {a.name} ({a.code})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                Tribunal
              </label>
              <select
                value={tribunal}
                onChange={(e) => setTribunal(e.target.value)}
                className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm min-w-[200px]"
              >
                {TRIBUNAIS_POPULARES.map((t) => (
                  <option key={t.code} value={t.code}>
                    {t.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                Limite
              </label>
              <select
                value={maxResults}
                onChange={(e) => setMaxResults(Number(e.target.value))}
                className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm"
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
            <button
              onClick={() => {
                setTriggered(true);
                mutate();
              }}
              className="px-5 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition font-semibold text-sm"
            >
              Buscar no DataJud
            </button>
          </div>
        )}
      </div>

      {triggered && data && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <KpiCard label="Total encontrado" value={kpis.total} color="text-foreground" />
          <KpiCard label="Último ano" value={kpis.ultimoAno} color="text-amber-400" />
          <KpiCard
            label="Tribunais"
            value={Object.keys(kpis.porTribunal).length}
            color="text-sky-400"
          />
          <KpiCard label="Fonte" value="CNJ" color="text-primary" isText />
        </div>
      )}

      {isLoading && triggered && (
        <div className="p-10 text-center text-muted-foreground flex items-center justify-center gap-3">
          <Loader2 className="h-5 w-5 animate-spin" /> Consultando DataJud…
        </div>
      )}

      {error && !isLoading && (
        <div className="p-6 rounded-2xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm">
          Erro ao consultar DataJud. Verifique o documento ou tente outros
          tribunais.
        </div>
      )}

      {triggered && data && records.length === 0 && !isLoading && (
        <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
          Nenhum processo encontrado nos tribunais selecionados.
          <div className="text-xs mt-2">
            Sugestão: expanda para mais TRFs ou inclua TJs estaduais.
          </div>
        </div>
      )}

      {triggered && records.length > 0 && (
        <div className="space-y-3">
          {records.map((r, i) => (
            <ProcessoCard key={r.case_number ?? i} record={r} />
          ))}
        </div>
      )}

      {!triggered && (
        <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
          <FileText className="h-10 w-10 mx-auto mb-4 text-muted-foreground/50" />
          <div className="text-sm font-medium mb-2">
            Digite um CPF/CNPJ ou escolha um assunto CNJ e clique em Buscar.
          </div>
          <div className="text-xs">
            A API Pública do CNJ devolve metadados e movimentações, sem teor de
            peças.
          </div>
        </div>
      )}
    </div>
  );
}

function KpiCard({
  label,
  value,
  color,
  isText,
}: {
  label: string;
  value: number | string;
  color: string;
  isText?: boolean;
}) {
  return (
    <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm">
      <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1">
        {label}
      </div>
      <div
        className={`font-heading font-bold ${color} ${
          isText ? "text-base" : "text-2xl"
        }`}
      >
        {typeof value === "number" ? value.toLocaleString("pt-BR") : value}
      </div>
    </div>
  );
}

function ProcessoCard({ record }: { record: LawsuitRecord }) {
  return (
    <div className="p-4 rounded-2xl border border-border bg-card/30 hover:bg-card/60 hover:border-primary/30 transition-all">
      <div className="flex items-start gap-3">
        <div className="shrink-0 p-2 rounded-lg border bg-primary/10 border-primary/30">
          <Gavel className="h-4 w-4 text-primary" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            {record.tribunal && (
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                {record.tribunal}
              </span>
            )}
            {record.degree && (
              <span className="text-xs text-muted-foreground">
                Grau: {record.degree}
              </span>
            )}
            {record.filing_date && (
              <span className="ml-auto text-xs text-muted-foreground flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                {formatDate(record.filing_date)}
              </span>
            )}
          </div>
          <div className="text-sm font-medium mb-1 font-mono">
            {record.case_number ?? "(número não disponível)"}
          </div>
          {record.class_name && (
            <div className="text-xs text-muted-foreground mb-1">
              {record.class_name}
            </div>
          )}
          {record.court && (
            <div className="text-xs text-muted-foreground flex items-center gap-1">
              <Building2 className="h-3 w-3" />
              {record.court}
              {record.municipality && ` · ${record.municipality}`}
              {record.state && `/${record.state}`}
            </div>
          )}
          {record.subjects && record.subjects.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {record.subjects.slice(0, 4).map((s, i) => (
                <span
                  key={i}
                  className="text-[10px] px-1.5 py-0.5 rounded bg-muted/50 border border-border"
                >
                  {s}
                </span>
              ))}
              {record.subjects.length > 4 && (
                <span className="text-[10px] text-muted-foreground">
                  +{record.subjects.length - 4}
                </span>
              )}
            </div>
          )}
          {record.last_update && (
            <div className="mt-2 text-[10px] text-muted-foreground font-mono flex items-center gap-1">
              <Clock className="h-3 w-3" />
              Últ. mov.: {formatDate(record.last_update)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function isDocument(s: string): boolean {
  const clean = s.replace(/\D/g, "");
  return clean.length === 11 || clean.length === 14;
}

function formatDate(iso: string): string {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("pt-BR");
  } catch {
    return iso;
  }
}
