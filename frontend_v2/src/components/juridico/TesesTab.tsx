"use client";

/**
 * Aba Teses do Hub Jurídico-Agro.
 *
 * Usa GET /api/v1/juridico/teses[?area=...&q=...] e
 * GET /api/v1/juridico/teses/{slug}.
 *
 * Agrupa por área (ambiental, fundiário, trabalhista, tributário,
 * previdenciário…), mostra título + situação e expande accordion
 * para exibir argumentos, precedentes, legislação, próxima ação.
 */

import { useMemo, useState } from "react";
import useSWR from "swr";
import {
  Loader2,
  Lightbulb,
  Search as SearchIcon,
  ChevronDown,
  ChevronRight,
  Scale,
  Leaf,
  Users,
  Coins,
  HeartHandshake,
  FileText,
  ExternalLink,
  BookOpen,
  ShieldCheck,
  AlertTriangle,
  CheckSquare,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";

type TeseResumo = {
  id: number;
  slug: string;
  titulo: string;
  area: string;
  situacao?: string;
  sumula_propria?: string;
  publico_alvo?: string[];
  n_argumentos: number;
  n_precedentes: number;
};

type Precedente = {
  tribunal?: string;
  orgao?: string;
  numero?: string;
  ementa?: string;
  url?: string;
  data?: string;
};

type TeseDetalhe = TeseResumo & {
  argumentos_principais?: string[];
  precedentes_sugeridos?: Precedente[];
  legislacao_aplicavel?: string[];
  aplicabilidade?: string;
  contra_argumentos?: string[];
  proxima_acao?: string;
};

const AREAS = [
  { value: "", label: "Todas as áreas", icon: Lightbulb, color: "text-primary" },
  { value: "ambiental", label: "Ambiental", icon: Leaf, color: "text-emerald-400" },
  { value: "fundiario", label: "Fundiário", icon: Scale, color: "text-amber-400" },
  { value: "trabalhista", label: "Trabalhista rural", icon: Users, color: "text-sky-400" },
  { value: "tributario", label: "Tributário", icon: Coins, color: "text-yellow-400" },
  {
    value: "previdenciario",
    label: "Previdenciário rural",
    icon: HeartHandshake,
    color: "text-rose-400",
  },
  {
    value: "contratual",
    label: "Contratual/Agrário",
    icon: FileText,
    color: "text-indigo-400",
  },
];

function areaMeta(area: string): (typeof AREAS)[number] {
  return AREAS.find((a) => a.value === area) ?? AREAS[0];
}

export function TesesTab() {
  const [area, setArea] = useState("");
  const [q, setQ] = useState("");

  const endpoint = useMemo(() => {
    const params = new URLSearchParams();
    if (area) params.set("area", area);
    if (q.trim()) params.set("q", q.trim());
    params.set("limit", "100");
    return `/juridico/teses?${params.toString()}`;
  }, [area, q]);

  const { data, isLoading, error } = useSWR<{
    total: number;
    teses: TeseResumo[];
  }>(endpoint, swrFetcher, { revalidateOnFocus: false });

  const teses = useMemo(() => data?.teses ?? [], [data]);

  // Agrupa por área
  const grouped = useMemo(() => {
    const map = new Map<string, TeseResumo[]>();
    teses.forEach((t) => {
      if (!map.has(t.area)) map.set(t.area, []);
      map.get(t.area)!.push(t);
    });
    return Array.from(map.entries());
  }, [teses]);

  return (
    <div className="space-y-5">
      {/* Filtros */}
      <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm flex flex-wrap items-end gap-3">
        <div className="flex-1 min-w-[220px]">
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Buscar
          </label>
          <div className="mt-1 relative">
            <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="palavra-chave na tese…"
              className="w-full bg-input/40 border border-border rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>
        <div className="flex gap-1 flex-wrap">
          {AREAS.map((a) => {
            const Icon = a.icon;
            const selected = area === a.value;
            return (
              <button
                key={a.value || "all"}
                onClick={() => setArea(a.value)}
                className={`
                  inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition
                  ${
                    selected
                      ? "bg-primary/10 text-primary border-primary/30"
                      : "bg-muted/30 text-muted-foreground border-border hover:bg-muted/50"
                  }
                `}
              >
                <Icon className={`h-3.5 w-3.5 ${selected ? "text-primary" : a.color}`} />
                {a.label}
              </button>
            );
          })}
        </div>
        <div className="ml-auto text-xs text-muted-foreground font-mono">
          {data?.total ?? 0} tese(s)
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm">
          Erro ao carregar teses.
        </div>
      )}

      {isLoading ? (
        <div className="p-10 text-center text-muted-foreground flex items-center justify-center gap-3">
          <Loader2 className="h-4 w-4 animate-spin" /> Carregando teses…
        </div>
      ) : teses.length === 0 ? (
        <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
          <Lightbulb className="h-10 w-10 mx-auto mb-4 text-muted-foreground/50" />
          <div className="text-sm font-medium">
            Nenhuma tese encontrada com esses filtros.
          </div>
        </div>
      ) : (
        <div className="space-y-5">
          {grouped.map(([areaName, items]) => (
            <AreaGroup key={areaName} area={areaName} teses={items} />
          ))}
        </div>
      )}
    </div>
  );
}

function AreaGroup({ area, teses }: { area: string; teses: TeseResumo[] }) {
  const meta = areaMeta(area);
  const Icon = meta.icon;
  return (
    <section>
      <header className="flex items-center gap-2 mb-2">
        <Icon className={`h-5 w-5 ${meta.color}`} />
        <h3 className="font-semibold text-sm uppercase tracking-wider">
          {meta.label}
        </h3>
        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
          {teses.length}
        </span>
      </header>
      <div className="space-y-2">
        {teses.map((t) => (
          <TeseAccordion key={t.slug} tese={t} />
        ))}
      </div>
    </section>
  );
}

function TeseAccordion({ tese }: { tese: TeseResumo }) {
  const [open, setOpen] = useState(false);
  const { data: detalhe, isLoading } = useSWR<TeseDetalhe>(
    open ? `/juridico/teses/${tese.slug}` : null,
    swrFetcher,
    { revalidateOnFocus: false },
  );

  return (
    <div className="border border-border rounded-xl bg-card/30 overflow-hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full px-4 py-3 flex items-start gap-3 text-left hover:bg-card/60 transition"
      >
        {open ? (
          <ChevronDown className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
        ) : (
          <ChevronRight className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
        )}
        <div className="min-w-0 flex-1">
          <div className="font-medium text-sm">{tese.titulo}</div>
          {tese.sumula_propria && (
            <div className="text-xs text-muted-foreground italic line-clamp-2 mt-1">
              “{tese.sumula_propria}”
            </div>
          )}
          <div className="mt-1.5 flex flex-wrap gap-2 text-[10px]">
            {tese.situacao && (
              <span className="uppercase tracking-wider text-muted-foreground">
                Situação: {tese.situacao}
              </span>
            )}
            <span className="ml-auto font-mono text-muted-foreground">
              {tese.n_argumentos} arg. · {tese.n_precedentes} preced.
            </span>
          </div>
        </div>
      </button>

      {open && (
        <div className="border-t border-border p-4 bg-background/40">
          {isLoading || !detalhe ? (
            <div className="text-xs text-muted-foreground flex items-center gap-2">
              <Loader2 className="h-3 w-3 animate-spin" /> Carregando detalhes…
            </div>
          ) : (
            <TeseDetalheView detalhe={detalhe} />
          )}
        </div>
      )}
    </div>
  );
}

function TeseDetalheView({ detalhe }: { detalhe: TeseDetalhe }) {
  return (
    <div className="space-y-4 text-sm">
      {detalhe.aplicabilidade && (
        <div>
          <h4 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1 flex items-center gap-1">
            <ShieldCheck className="h-3 w-3" /> Quando aplicar
          </h4>
          <p className="text-muted-foreground">{detalhe.aplicabilidade}</p>
        </div>
      )}

      {detalhe.argumentos_principais &&
        detalhe.argumentos_principais.length > 0 && (
          <div>
            <h4 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1 flex items-center gap-1">
              <Lightbulb className="h-3 w-3" /> Argumentos principais
            </h4>
            <ol className="space-y-1.5 list-decimal list-inside text-foreground/90">
              {detalhe.argumentos_principais.map((a, i) => (
                <li key={i}>{a}</li>
              ))}
            </ol>
          </div>
        )}

      {detalhe.precedentes_sugeridos &&
        detalhe.precedentes_sugeridos.length > 0 && (
          <div>
            <h4 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1 flex items-center gap-1">
              <Scale className="h-3 w-3" /> Precedentes sugeridos
            </h4>
            <div className="space-y-1.5">
              {detalhe.precedentes_sugeridos.map((p, i) => (
                <div
                  key={i}
                  className="p-2 rounded border border-border bg-card/30 text-xs"
                >
                  <div className="flex items-center gap-2 mb-0.5">
                    {p.tribunal && (
                      <span className="font-mono font-semibold text-primary">
                        {p.tribunal}
                      </span>
                    )}
                    {p.numero && <span className="font-mono">{p.numero}</span>}
                    {p.data && (
                      <span className="text-muted-foreground ml-auto">
                        {p.data}
                      </span>
                    )}
                  </div>
                  {p.orgao && (
                    <div className="text-muted-foreground text-[11px]">
                      {p.orgao}
                    </div>
                  )}
                  {p.ementa && (
                    <div className="text-muted-foreground italic mt-1 line-clamp-3">
                      {p.ementa}
                    </div>
                  )}
                  {p.url && (
                    <a
                      href={p.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 inline-flex items-center gap-1 text-primary text-[11px] hover:underline"
                    >
                      ver decisão <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

      {detalhe.legislacao_aplicavel &&
        detalhe.legislacao_aplicavel.length > 0 && (
          <div>
            <h4 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1 flex items-center gap-1">
              <BookOpen className="h-3 w-3" /> Legislação aplicável
            </h4>
            <ul className="space-y-0.5 text-xs text-muted-foreground">
              {detalhe.legislacao_aplicavel.map((l, i) => (
                <li key={i}>• {l}</li>
              ))}
            </ul>
          </div>
        )}

      {detalhe.contra_argumentos &&
        detalhe.contra_argumentos.length > 0 && (
          <div>
            <h4 className="text-[10px] uppercase tracking-wider text-amber-400 font-semibold mb-1 flex items-center gap-1">
              <AlertTriangle className="h-3 w-3" /> Contra-argumentos prováveis
            </h4>
            <ul className="space-y-0.5 text-xs text-amber-200/80">
              {detalhe.contra_argumentos.map((c, i) => (
                <li key={i}>• {c}</li>
              ))}
            </ul>
          </div>
        )}

      {detalhe.proxima_acao && (
        <div className="p-3 rounded-lg border border-primary/30 bg-primary/10">
          <h4 className="text-[10px] uppercase tracking-wider text-primary font-semibold mb-1 flex items-center gap-1">
            <CheckSquare className="h-3 w-3" /> Próxima ação
          </h4>
          <p className="text-xs text-foreground/90">{detalhe.proxima_acao}</p>
        </div>
      )}
    </div>
  );
}
