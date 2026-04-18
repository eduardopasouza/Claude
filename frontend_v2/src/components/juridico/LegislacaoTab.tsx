"use client";

/**
 * Aba Legislação do Hub Jurídico-Agro.
 *
 * GET /api/v1/juridico/legislacao[?esfera=...&uf=...&municipio_ibge=...&tema=...&q=...]
 * Filtros: UF (texto livre), município (IBGE code), esfera, tema, busca textual.
 * Lista com link para norma oficial / LexML.
 */

import { useMemo, useState } from "react";
import useSWR from "swr";
import {
  Loader2,
  BookOpen,
  Search as SearchIcon,
  ExternalLink,
  Landmark,
  Building2,
  MapPin,
  Leaf,
  Scale,
  Coins,
  Users,
  ShieldCheck,
  Globe,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";

type Norma = {
  id: number;
  slug: string;
  titulo: string;
  esfera: "federal" | "estadual" | "municipal" | string;
  uf?: string | null;
  municipio?: string | null;
  tipo?: string;
  numero?: string;
  ano?: number;
  orgao?: string;
  temas?: string[];
  resumo?: string;
  situacao?: string;
  url_oficial?: string;
};

const ESFERAS = [
  { value: "", label: "Todas as esferas" },
  { value: "federal", label: "Federal" },
  { value: "estadual", label: "Estadual" },
  { value: "municipal", label: "Municipal" },
];

const TEMAS = [
  { value: "", label: "Todos os temas", icon: BookOpen, color: "text-muted-foreground" },
  { value: "ambiental", label: "Ambiental", icon: Leaf, color: "text-emerald-400" },
  { value: "fundiario", label: "Fundiário", icon: Scale, color: "text-amber-400" },
  { value: "credito_rural", label: "Crédito rural", icon: Coins, color: "text-yellow-400" },
  { value: "trabalhista", label: "Trabalhista", icon: Users, color: "text-sky-400" },
  { value: "sanitario", label: "Sanitário/SIF", icon: ShieldCheck, color: "text-rose-400" },
  { value: "tributario", label: "Tributário", icon: Coins, color: "text-indigo-400" },
];

const UFS = [
  "", "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
  "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO",
  "RR", "RS", "SC", "SE", "SP", "TO",
];

export function LegislacaoTab() {
  const [esfera, setEsfera] = useState("");
  const [uf, setUf] = useState("");
  const [municipio, setMunicipio] = useState("");
  const [tema, setTema] = useState("");
  const [q, setQ] = useState("");

  const endpoint = useMemo(() => {
    const params = new URLSearchParams();
    if (esfera) params.set("esfera", esfera);
    if (uf) params.set("uf", uf);
    if (municipio.trim()) params.set("municipio_ibge", municipio.trim());
    if (tema) params.set("tema", tema);
    if (q.trim()) params.set("q", q.trim());
    params.set("limit", "200");
    return `/juridico/legislacao?${params.toString()}`;
  }, [esfera, uf, municipio, tema, q]);

  const { data, isLoading, error } = useSWR<{
    total: number;
    legislacao: Norma[];
  }>(endpoint, swrFetcher, { revalidateOnFocus: false });

  const normas = useMemo(() => data?.legislacao ?? [], [data]);

  // Agrupa por esfera
  const grouped = useMemo(() => {
    const map = new Map<string, Norma[]>();
    for (const n of normas) {
      const key = n.esfera || "outras";
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(n);
    }
    const order = ["federal", "estadual", "municipal"];
    return Array.from(map.entries()).sort(
      (a, b) => order.indexOf(a[0]) - order.indexOf(b[0]),
    );
  }, [normas]);

  return (
    <div className="space-y-5">
      {/* Filtros */}
      <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm space-y-3">
        <div className="flex flex-wrap items-end gap-3">
          <div className="flex-1 min-w-[200px]">
            <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              Buscar
            </label>
            <div className="mt-1 relative">
              <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="título ou ementa…"
                className="w-full bg-input/40 border border-border rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>
          <div>
            <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              Esfera
            </label>
            <select
              value={esfera}
              onChange={(e) => setEsfera(e.target.value)}
              className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm"
            >
              {ESFERAS.map((es) => (
                <option key={es.value} value={es.value}>
                  {es.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              UF
            </label>
            <select
              value={uf}
              onChange={(e) => setUf(e.target.value)}
              className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm w-24"
            >
              {UFS.map((u) => (
                <option key={u || "all"} value={u}>
                  {u || "Todas"}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              Município (IBGE)
            </label>
            <input
              value={municipio}
              onChange={(e) => setMunicipio(e.target.value)}
              placeholder="ex. 2111300"
              className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono w-32"
            />
          </div>
          <div className="ml-auto text-xs text-muted-foreground font-mono">
            {data?.total ?? 0} norma(s)
          </div>
        </div>

        <div className="flex gap-1 flex-wrap">
          {TEMAS.map((t) => {
            const Icon = t.icon;
            const selected = tema === t.value;
            return (
              <button
                key={t.value || "all"}
                onClick={() => setTema(t.value)}
                className={`
                  inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-xs font-medium transition
                  ${
                    selected
                      ? "bg-primary/10 text-primary border-primary/30"
                      : "bg-muted/30 text-muted-foreground border-border hover:bg-muted/50"
                  }
                `}
              >
                <Icon className={`h-3 w-3 ${selected ? "text-primary" : t.color}`} />
                {t.label}
              </button>
            );
          })}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm">
          Erro ao carregar legislação.
        </div>
      )}

      {isLoading ? (
        <div className="p-10 text-center text-muted-foreground flex items-center justify-center gap-3">
          <Loader2 className="h-4 w-4 animate-spin" /> Carregando normas…
        </div>
      ) : normas.length === 0 ? (
        <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
          <BookOpen className="h-10 w-10 mx-auto mb-4 text-muted-foreground/50" />
          <div className="text-sm font-medium">
            Nenhuma norma encontrada com esses filtros.
          </div>
        </div>
      ) : (
        <div className="space-y-5">
          {grouped.map(([esferaName, items]) => (
            <EsferaGroup key={esferaName} esfera={esferaName} normas={items} />
          ))}
        </div>
      )}
    </div>
  );
}

function EsferaGroup({ esfera, normas }: { esfera: string; normas: Norma[] }) {
  const Icon =
    esfera === "federal"
      ? Globe
      : esfera === "estadual"
      ? Landmark
      : esfera === "municipal"
      ? Building2
      : BookOpen;

  return (
    <section>
      <header className="flex items-center gap-2 mb-2">
        <Icon className="h-4 w-4 text-primary" />
        <h3 className="font-semibold text-sm uppercase tracking-wider">
          {esfera}
        </h3>
        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
          {normas.length}
        </span>
      </header>
      <div className="space-y-2">
        {normas.map((n) => (
          <NormaCard key={n.slug} norma={n} />
        ))}
      </div>
    </section>
  );
}

function NormaCard({ norma }: { norma: Norma }) {
  const situacaoColor =
    norma.situacao === "revogada"
      ? "text-rose-300 bg-rose-500/10 border-rose-500/30"
      : norma.situacao === "vigente"
      ? "text-emerald-300 bg-emerald-500/10 border-emerald-500/30"
      : "text-muted-foreground bg-muted border-border";

  return (
    <div className="p-3 rounded-xl border border-border bg-card/30 hover:bg-card/60 transition">
      <div className="flex flex-wrap items-baseline gap-2 mb-1">
        {norma.tipo && (
          <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
            {norma.tipo}
          </span>
        )}
        {norma.numero && (
          <span className="text-sm font-mono font-semibold">{norma.numero}</span>
        )}
        {norma.ano && (
          <span className="text-xs text-muted-foreground">/{norma.ano}</span>
        )}
        {norma.situacao && (
          <span
            className={`text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border ${situacaoColor}`}
          >
            {norma.situacao}
          </span>
        )}
      </div>

      <div className="text-sm font-medium mb-1">{norma.titulo}</div>

      {norma.resumo && (
        <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
          {norma.resumo}
        </p>
      )}

      <div className="flex flex-wrap items-center gap-2 text-[11px] text-muted-foreground">
        {norma.orgao && (
          <span className="flex items-center gap-1">
            <Landmark className="h-3 w-3" /> {norma.orgao}
          </span>
        )}
        {(norma.uf || norma.municipio) && (
          <span className="flex items-center gap-1">
            <MapPin className="h-3 w-3" />
            {[norma.municipio, norma.uf].filter(Boolean).join("/")}
          </span>
        )}
        {norma.temas && norma.temas.length > 0 && (
          <span className="flex flex-wrap gap-1">
            {norma.temas.slice(0, 4).map((t) => (
              <span
                key={t}
                className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-muted/60 border border-border uppercase tracking-wider"
              >
                {t}
              </span>
            ))}
          </span>
        )}
        {norma.url_oficial && (
          <a
            href={norma.url_oficial}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-auto inline-flex items-center gap-1 text-primary hover:underline"
          >
            texto oficial <ExternalLink className="h-3 w-3" />
          </a>
        )}
      </div>
    </div>
  );
}
