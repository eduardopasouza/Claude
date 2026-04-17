"use client";

import { useMemo, useState } from "react";
import useSWR from "swr";
import {
  AlertTriangle,
  Calendar,
  CheckCircle2,
  Clock,
  ExternalLink,
  Filter,
  Gavel,
  Loader2,
  RefreshCw,
  Search as SearchIcon,
  X,
} from "lucide-react";
import { swrFetcher, fetchWithAuth } from "@/lib/api";

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------
type UrgenciaLevel = "critico" | "alto" | "medio" | "baixo" | "desconhecida";

type Advogado = {
  id: number;
  nome: string;
  numero_oab: string;
  uf_oab: string;
};

type DestinatarioAdvogado = {
  id: number;
  advogado_id: number;
  advogado: Advogado;
};

type Destinatario = {
  polo: string;
  nome: string;
};

type PublicacaoItem = {
  id: number;
  hash?: string;
  data_disponibilizacao: string;
  datadisponibilizacao?: string;
  siglaTribunal: string;
  tipoComunicacao: string;
  tipoDocumento?: string;
  nomeOrgao: string;
  nomeClasse?: string;
  numeroprocessocommascara?: string;
  numero_processo?: string;
  texto: string;
  resumo: string;
  urgencia: UrgenciaLevel;
  meiocompleto?: string;
  link?: string;
  destinatarios?: Destinatario[];
  destinatarioadvogados?: DestinatarioAdvogado[];
};

type PublicacoesResponse = {
  status: string;
  count: number;
  pagina: number;
  itens_por_pagina: number;
  oab: { numero: string; uf: string };
  periodo: { inicio: string; fim: string };
  items: PublicacaoItem[];
};

// ---------------------------------------------------------------------------
// Utils
// ---------------------------------------------------------------------------
const URGENCIA_META: Record<
  UrgenciaLevel,
  { label: string; color: string; bg: string; icon: typeof AlertTriangle }
> = {
  critico: {
    label: "Crítico",
    color: "text-rose-400",
    bg: "bg-rose-500/10 border-rose-500/30",
    icon: AlertTriangle,
  },
  alto: {
    label: "Alto",
    color: "text-amber-400",
    bg: "bg-amber-500/10 border-amber-500/30",
    icon: Clock,
  },
  medio: {
    label: "Médio",
    color: "text-sky-400",
    bg: "bg-sky-500/10 border-sky-500/30",
    icon: Clock,
  },
  baixo: {
    label: "Baixo",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10 border-emerald-500/30",
    icon: CheckCircle2,
  },
  desconhecida: {
    label: "—",
    color: "text-muted-foreground",
    bg: "bg-muted/30 border-border",
    icon: Clock,
  },
};

function formatarDataBR(iso?: string): string {
  if (!iso) return "—";
  try {
    const d = iso.includes("/") ? iso : new Date(iso).toLocaleDateString("pt-BR");
    return d;
  } catch {
    return iso;
  }
}

// ---------------------------------------------------------------------------
// Página
// ---------------------------------------------------------------------------
export default function PublicacoesPage() {
  // Controles do topo
  const [oab, setOab] = useState("12147");
  const [uf, setUf] = useState("MA");
  const [dias, setDias] = useState(30);
  const [filtroTribunal, setFiltroTribunal] = useState<string>("");
  const [filtroUrgencia, setFiltroUrgencia] = useState<string>("");
  const [busca, setBusca] = useState("");
  const [selecionada, setSelecionada] = useState<PublicacaoItem | null>(null);
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState<string | null>(null);

  // Data
  const endpoint = `/publicacoes/oab/${uf}/${oab}?itens_por_pagina=100&pagina=1${
    dias !== 30 ? `&data_inicio=${new Date(Date.now() - dias * 86400000).toISOString().slice(0, 10)}` : ""
  }`;
  const { data, error, isLoading, mutate } = useSWR<PublicacoesResponse>(
    oab && uf ? endpoint : null,
    swrFetcher,
    { revalidateOnFocus: false, dedupingInterval: 60_000 }
  );

  const items = data?.items ?? [];

  // Filtros client-side
  const filtrados = useMemo(() => {
    const q = busca.trim().toLowerCase();
    return items.filter((it) => {
      if (filtroTribunal && it.siglaTribunal !== filtroTribunal) return false;
      if (filtroUrgencia && it.urgencia !== filtroUrgencia) return false;
      if (q) {
        const hay =
          (it.texto || "").toLowerCase() +
          " " +
          (it.numeroprocessocommascara || "").toLowerCase() +
          " " +
          (it.nomeClasse || "").toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [items, filtroTribunal, filtroUrgencia, busca]);

  // Tribunais únicos para filtro
  const tribunais = useMemo(() => {
    const set = new Set<string>();
    items.forEach((i) => i.siglaTribunal && set.add(i.siglaTribunal));
    return Array.from(set).sort();
  }, [items]);

  // Agregados para KPIs
  const kpis = useMemo(() => {
    const total = items.length;
    const criticas = items.filter((i) => i.urgencia === "critico").length;
    const altas = items.filter((i) => i.urgencia === "alto").length;
    const medias = items.filter((i) => i.urgencia === "medio").length;
    return { total, criticas, altas, medias };
  }, [items]);

  // Sync: persiste no banco
  async function handleSync() {
    setSyncing(true);
    setSyncMsg(null);
    try {
      const res = await fetchWithAuth(
        `/publicacoes/sync-oab?uf=${uf}&numero=${oab}&dias=${dias}`,
        { method: "POST" }
      );
      const json = await res.json();
      if (res.ok) {
        setSyncMsg(
          `Sincronizado: ${json.novas} nova(s), ${json.atualizadas} atualizada(s).`
        );
        mutate();
      } else {
        setSyncMsg(`Erro: ${json.detail || "falha na sincronização"}`);
      }
    } catch (e: unknown) {
      setSyncMsg(`Erro: ${(e as Error).message}`);
    } finally {
      setSyncing(false);
      setTimeout(() => setSyncMsg(null), 5000);
    }
  }

  return (
    <div className="p-6 md:p-8 max-w-[1400px] mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Gavel className="h-6 w-6 text-primary" />
          <h1 className="font-heading font-bold text-2xl md:text-3xl">
            Publicações DJEN
          </h1>
          <span className="text-[10px] font-mono px-2 py-1 rounded bg-primary/10 text-primary border border-primary/20 uppercase tracking-wider">
            Comunica.PJe
          </span>
        </div>
        <p className="text-sm text-muted-foreground">
          Intimações e comunicações do Diário de Justiça Eletrônico Nacional por
          OAB. Fonte pública CNJ.
        </p>
      </div>

      {/* Controles OAB */}
      <div className="flex flex-wrap items-end gap-3 mb-6 p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm">
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            OAB Nº
          </label>
          <input
            value={oab}
            onChange={(e) => setOab(e.target.value.replace(/\D/g, ""))}
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono w-32 focus:outline-none focus:ring-1 focus:ring-primary"
            placeholder="12147"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            UF
          </label>
          <select
            value={uf}
            onChange={(e) => setUf(e.target.value)}
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono w-20 focus:outline-none focus:ring-1 focus:ring-primary"
          >
            {["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"].map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Período
          </label>
          <select
            value={dias}
            onChange={(e) => setDias(Number(e.target.value))}
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm w-40 focus:outline-none focus:ring-1 focus:ring-primary"
          >
            <option value={7}>Últimos 7 dias</option>
            <option value={15}>Últimos 15 dias</option>
            <option value={30}>Últimos 30 dias</option>
            <option value={60}>Últimos 60 dias</option>
            <option value={90}>Últimos 90 dias</option>
          </select>
        </div>

        <button
          onClick={() => mutate()}
          className="px-3 py-2 rounded-lg bg-muted/50 border border-border hover:bg-muted transition text-sm flex items-center gap-2"
          title="Recarregar do cache"
        >
          <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
          Recarregar
        </button>
        <button
          onClick={handleSync}
          disabled={syncing}
          className="px-4 py-2 rounded-lg bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20 transition text-sm flex items-center gap-2 font-semibold disabled:opacity-50"
          title="Buscar no DJEN e persistir no banco local"
        >
          {syncing ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <RefreshCw className="h-4 w-4" />
          )}
          Sincronizar
        </button>

        {syncMsg && (
          <div className="text-xs text-primary font-mono px-2">{syncMsg}</div>
        )}
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <KpiCard label="Total" value={kpis.total} color="text-foreground" />
        <KpiCard label="Críticas (≤5d)" value={kpis.criticas} color="text-rose-400" />
        <KpiCard label="Altas (≤10d)" value={kpis.altas} color="text-amber-400" />
        <KpiCard label="Médias (≤15d)" value={kpis.medias} color="text-sky-400" />
      </div>

      {/* Filtros secundários */}
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border bg-card/30 flex-1 min-w-[240px]">
          <SearchIcon className="h-4 w-4 text-muted-foreground shrink-0" />
          <input
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            placeholder="Filtrar nesta lista (texto, processo, classe)..."
            className="flex-1 bg-transparent text-sm focus:outline-none placeholder:text-muted-foreground"
          />
          {busca && (
            <button
              aria-label="Limpar busca"
              onClick={() => setBusca("")}
              className="text-muted-foreground hover:text-foreground"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
        <select
          value={filtroTribunal}
          onChange={(e) => setFiltroTribunal(e.target.value)}
          className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="">Todos os tribunais</option>
          {tribunais.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        <select
          value={filtroUrgencia}
          onChange={(e) => setFiltroUrgencia(e.target.value)}
          className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="">Todas as urgências</option>
          <option value="critico">Crítico (≤5d)</option>
          <option value="alto">Alto (≤10d)</option>
          <option value="medio">Médio (≤15d)</option>
          <option value="baixo">Baixo (&gt;15d)</option>
        </select>
      </div>

      {/* Feed */}
      <div className="space-y-3">
        {isLoading && (
          <div className="p-10 text-center text-muted-foreground flex items-center justify-center gap-3">
            <Loader2 className="h-5 w-5 animate-spin" /> Buscando no DJEN...
          </div>
        )}

        {error && !isLoading && (
          <div className="p-6 rounded-2xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm">
            Erro ao buscar publicações. Verifique a OAB/UF ou tente novamente.
          </div>
        )}

        {!isLoading && !error && filtrados.length === 0 && (
          <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
            Nenhuma publicação encontrada para {oab}/{uf} nos últimos {dias}{" "}
            dias.
          </div>
        )}

        {filtrados.map((p) => (
          <PublicacaoCard key={p.id} item={p} onClick={() => setSelecionada(p)} />
        ))}
      </div>

      {/* Drawer de detalhe */}
      {selecionada && (
        <DrawerPublicacao
          item={selecionada}
          onClose={() => setSelecionada(null)}
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Subcomponentes
// ---------------------------------------------------------------------------
function KpiCard({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm">
      <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1">
        {label}
      </div>
      <div className={`text-2xl font-heading font-bold ${color}`}>{value}</div>
    </div>
  );
}

function PublicacaoCard({
  item,
  onClick,
}: {
  item: PublicacaoItem;
  onClick: () => void;
}) {
  const meta = URGENCIA_META[item.urgencia] || URGENCIA_META.desconhecida;
  const Icon = meta.icon;
  return (
    <button
      onClick={onClick}
      className="w-full text-left p-4 rounded-2xl border border-border bg-card/30 hover:bg-card/60 hover:border-primary/30 transition-all group"
    >
      <div className="flex items-start gap-3">
        <div
          className={`shrink-0 p-2 rounded-lg border ${meta.bg}`}
          title={`Urgência: ${meta.label}`}
        >
          <Icon className={`h-4 w-4 ${meta.color}`} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
              {item.siglaTribunal}
            </span>
            <span className="text-xs text-muted-foreground">
              {item.tipoComunicacao}
            </span>
            {item.numeroprocessocommascara && (
              <span className="text-xs font-mono text-muted-foreground">
                · {item.numeroprocessocommascara}
              </span>
            )}
            <span className="ml-auto text-xs text-muted-foreground flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              {formatarDataBR(
                item.datadisponibilizacao || item.data_disponibilizacao
              )}
            </span>
          </div>
          <div className="text-sm font-medium mb-1 line-clamp-1">
            {item.nomeOrgao}
          </div>
          <div className="text-xs text-muted-foreground line-clamp-2">
            {item.resumo || item.texto?.slice(0, 280)}
          </div>
          {item.nomeClasse && (
            <div className="text-[10px] uppercase tracking-wide text-muted-foreground/70 mt-2 font-semibold">
              {item.nomeClasse}
            </div>
          )}
        </div>
      </div>
    </button>
  );
}

function DrawerPublicacao({
  item,
  onClose,
}: {
  item: PublicacaoItem;
  onClose: () => void;
}) {
  const meta = URGENCIA_META[item.urgencia] || URGENCIA_META.desconhecida;
  return (
    <div
      className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-end md:items-center justify-center p-0 md:p-6"
      onClick={onClose}
    >
      <div
        className="w-full md:max-w-3xl max-h-[92vh] overflow-y-auto bg-card border border-border rounded-t-3xl md:rounded-3xl shadow-[0_0_60px_-10px_rgba(0,0,0,0.9)]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-card/90 backdrop-blur-md border-b border-border p-4 flex items-start gap-3">
          <div className={`p-2 rounded-lg border ${meta.bg}`}>
            <Gavel className={`h-5 w-5 ${meta.color}`} />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-0.5">
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                {item.siglaTribunal}
              </span>
              <span className="text-xs text-muted-foreground">
                {item.tipoComunicacao}
              </span>
              <span
                className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${meta.bg} ${meta.color}`}
              >
                {meta.label}
              </span>
            </div>
            <h2 className="font-heading font-semibold text-base md:text-lg leading-tight">
              {item.nomeOrgao}
            </h2>
            <div className="text-xs text-muted-foreground mt-0.5 font-mono">
              {item.numeroprocessocommascara} · {formatarDataBR(item.datadisponibilizacao || item.data_disponibilizacao)}
            </div>
          </div>
          <button
            aria-label="Fechar"
            onClick={onClose}
            className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-5 space-y-5">
          {item.nomeClasse && (
            <div>
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1">
                Classe Processual
              </div>
              <div className="text-sm">{item.nomeClasse}</div>
            </div>
          )}

          {item.destinatarios && item.destinatarios.length > 0 && (
            <div>
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1">
                Destinatários (polos)
              </div>
              <div className="flex flex-wrap gap-2">
                {item.destinatarios.map((d, idx) => (
                  <span
                    key={idx}
                    className="text-xs px-2 py-1 rounded bg-muted/50 border border-border"
                  >
                    {d.polo}: {d.nome}
                  </span>
                ))}
              </div>
            </div>
          )}

          {item.destinatarioadvogados && item.destinatarioadvogados.length > 0 && (
            <div>
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1">
                Advogados envolvidos
              </div>
              <div className="flex flex-wrap gap-2">
                {item.destinatarioadvogados.map((a) => (
                  <span
                    key={a.id}
                    className="text-xs px-2 py-1 rounded bg-primary/5 border border-primary/20 font-mono"
                  >
                    {a.advogado.nome} · OAB/{a.advogado.uf_oab}{" "}
                    {a.advogado.numero_oab}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div>
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1">
              Texto da publicação
            </div>
            <div className="text-sm whitespace-pre-wrap leading-relaxed bg-muted/20 border border-border rounded-xl p-4 font-mono text-[13px]">
              {item.texto}
            </div>
          </div>

          {item.link && (
            <a
              href={item.link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20 transition text-sm font-semibold"
            >
              <ExternalLink className="h-4 w-4" /> Abrir peça no tribunal
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
