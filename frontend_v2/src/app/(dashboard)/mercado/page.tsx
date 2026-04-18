"use client";

import { useEffect, useMemo, useState } from "react";
import useSWR from "swr";
import {
  TrendingUp,
  TrendingDown,
  Activity,
  Loader2,
  Newspaper,
  ExternalLink,
  MapPin,
  Minus,
} from "lucide-react";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  LineChart,
  Line,
} from "recharts";
import { swrFetcher } from "@/lib/api";

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------
type Indicators = Record<
  string,
  { name: string; value: string; date: string; unit: string }
>;

type NewsArticle = {
  title: string;
  url: string;
  source: string;
  published_at: string;
  summary?: string;
};

type AgrolinkUfStat = {
  uf: string;
  preco_atual: number;
  preco_nacional: number | null;
  mes_ref: string;
  total_meses_historico: number;
};

type AgrolinkUfDetail = {
  uf: string;
  historico: Array<{
    mes: string;
    estadual: number | null;
    nacional: number | null;
  }>;
};

type AgrolinkResponse = {
  commodity: string;
  label: string;
  unit: string;
  total_ufs: number;
  ufs: AgrolinkUfDetail[];
  uf_stats: AgrolinkUfStat[];
  error?: string;
};

type CommodityDef = {
  id: string;
  label: string;
  group: "graos" | "industriais" | "proteinas";
  color: string;
  unit_short?: string;
};

const COMMODITIES: CommodityDef[] = [
  { id: "soja", label: "Soja", group: "graos", color: "#22c55e" },
  { id: "milho", label: "Milho", group: "graos", color: "#eab308" },
  { id: "sorgo", label: "Sorgo", group: "graos", color: "#a16207" },
  { id: "trigo", label: "Trigo", group: "graos", color: "#d97706" },
  { id: "arroz", label: "Arroz", group: "graos", color: "#fbbf24" },
  { id: "feijao", label: "Feijão", group: "graos", color: "#78350f" },
  { id: "cafe", label: "Café", group: "industriais", color: "#a16207" },
  { id: "algodao", label: "Algodão", group: "industriais", color: "#e5e7eb" },
  { id: "cana", label: "Cana", group: "industriais", color: "#84cc16" },
  { id: "acucar", label: "Açúcar", group: "industriais", color: "#fef3c7" },
  { id: "boi", label: "Boi gordo", group: "proteinas", color: "#dc2626" },
  { id: "frango", label: "Frango", group: "proteinas", color: "#fbbf24" },
  { id: "leite", label: "Leite", group: "proteinas", color: "#fb7185" },
];

const UF_NAMES: Record<string, string> = {
  AC: "Acre", AL: "Alagoas", AM: "Amazonas", AP: "Amapá", BA: "Bahia",
  CE: "Ceará", DF: "Distrito Federal", ES: "Espírito Santo", GO: "Goiás",
  MA: "Maranhão", MG: "Minas Gerais", MS: "Mato Grosso do Sul", MT: "Mato Grosso",
  PA: "Pará", PB: "Paraíba", PE: "Pernambuco", PI: "Piauí", PR: "Paraná",
  RJ: "Rio de Janeiro", RN: "Rio Grande do Norte", RO: "Rondônia", RR: "Roraima",
  RS: "Rio Grande do Sul", SC: "Santa Catarina", SE: "Sergipe", SP: "São Paulo",
  TO: "Tocantins",
};
const UFS_ORDER = Object.keys(UF_NAMES).sort();

// ---------------------------------------------------------------------------
// Hook para UF do usuário (persistida em localStorage)
// ---------------------------------------------------------------------------
function useUserUF(): [string, (uf: string) => void] {
  const [uf, setUfState] = useState<string>("MA");
  useEffect(() => {
    if (typeof window === "undefined") return;
    const saved = localStorage.getItem("agrojus_uf");
    if (saved) setUfState(saved);
  }, []);
  const setUf = (newUf: string) => {
    setUfState(newUf);
    if (typeof window !== "undefined") {
      localStorage.setItem("agrojus_uf", newUf);
    }
  };
  return [uf, setUf];
}

// ---------------------------------------------------------------------------
// PAGE
// ---------------------------------------------------------------------------
export default function Mercado() {
  const [userUF, setUserUF] = useUserUF();
  const [selectedCommodity, setSelectedCommodity] = useState<string>("soja");

  const { data: indicatorsData } = useSWR<{ indicators: Indicators }>(
    "/market/indicators",
    swrFetcher,
    { refreshInterval: 300_000 }
  );
  const indicators = indicatorsData?.indicators || {};

  const { data: newsData } = useSWR<{ articles: NewsArticle[] }>(
    "/news/market?limit=6",
    swrFetcher,
    { refreshInterval: 600_000 }
  );

  return (
    <div className="p-6 lg:p-8 max-w-[1400px] mx-auto space-y-6 animate-in fade-in duration-500">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-3xl font-heading font-extrabold text-slate-100 tracking-tight flex items-center gap-3">
          <TrendingUp className="h-8 w-8 text-emerald-400" />
          Mercado
        </h1>
        <UFPicker value={userUF} onChange={setUserUF} />
      </header>

      <p className="text-xs text-slate-500 italic max-w-3xl">
        Preços referenciais do mercado físico brasileiro, coletados de
        múltiplas fontes (cooperativas, corretores, sindicatos, bolsas).
        Variações monitoradas diariamente; podem ser diárias, semanais ou
        quinzenais. Indicadores econômicos via Banco Central (BCB).
      </p>

      {/* Hero: preços na região do usuário */}
      <MinhaRegiao
        uf={userUF}
        selected={selectedCommodity}
        onSelect={setSelectedCommodity}
      />

      {/* Gráfico histórico da commodity selecionada + UF */}
      <HistoricoCommodity commodity={selectedCommodity} uf={userUF} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Indicadores BCB */}
        <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm uppercase tracking-wider font-bold text-slate-400 mb-4 flex items-center gap-2">
            <Activity className="h-4 w-4" /> Indicadores econômicos
          </h2>
          <div className="space-y-2.5">
            {Object.entries(indicators).map(([key, ind]) => (
              <div
                key={key}
                className="p-2.5 bg-slate-950/40 border border-slate-800 rounded-lg flex items-baseline justify-between"
              >
                <span className="text-xs text-slate-400">{ind.name}</span>
                <span className="text-base font-mono font-bold text-slate-100 tabular-nums">
                  {parseFloat(ind.value).toLocaleString("pt-BR", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 4,
                  })}
                  <span className="text-[10px] font-normal text-slate-500 ml-1">
                    {ind.unit}
                  </span>
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* Notícias */}
        <section className="lg:col-span-2 bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm uppercase tracking-wider font-bold text-slate-400 mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Newspaper className="h-4 w-4" /> Notícias de mercado
            </div>
            <a href="/noticias" className="text-xs text-emerald-400 hover:text-emerald-300">
              Ver todas →
            </a>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {(newsData?.articles || []).slice(0, 6).map((n, i) => (
              <NewsCard key={i} article={n} />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Seletor de UF
// ---------------------------------------------------------------------------
function UFPicker({
  value,
  onChange,
}: {
  value: string;
  onChange: (uf: string) => void;
}) {
  return (
    <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 rounded-xl px-4 py-2">
      <MapPin className="h-4 w-4 text-emerald-400" />
      <span className="text-xs text-emerald-300/80">Sua região:</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-transparent font-bold text-emerald-200 text-sm outline-none cursor-pointer"
      >
        {UFS_ORDER.map((uf) => (
          <option key={uf} value={uf} className="bg-slate-900">
            {uf} — {UF_NAMES[uf]}
          </option>
        ))}
      </select>
    </div>
  );
}

// ---------------------------------------------------------------------------
// HERO: preços na região + cards por commodity
// ---------------------------------------------------------------------------
function MinhaRegiao({
  uf,
  selected,
  onSelect,
}: {
  uf: string;
  selected: string;
  onSelect: (id: string) => void;
}) {
  return (
    <section className="space-y-4">
      <h2 className="text-sm uppercase tracking-wider font-bold text-slate-400">
        Preço de hoje em {UF_NAMES[uf]} ({uf})
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 xl:grid-cols-7 gap-2">
        {COMMODITIES.map((c) => (
          <CommodityCard
            key={c.id}
            commodity={c}
            uf={uf}
            active={selected === c.id}
            onClick={() => onSelect(c.id)}
          />
        ))}
      </div>
    </section>
  );
}

function CommodityCard({
  commodity,
  uf,
  active,
  onClick,
}: {
  commodity: CommodityDef;
  uf: string;
  active: boolean;
  onClick: () => void;
}) {
  const { data } = useSWR<AgrolinkResponse>(
    `/market/quotes/history_db/${commodity.id}`,
    swrFetcher,
    { refreshInterval: 3600_000, revalidateOnFocus: false }
  );

  const stat = data?.uf_stats?.find((s) => s.uf === uf);
  const nacional = data?.uf_stats?.[0]?.preco_nacional;
  const diff =
    stat && nacional ? ((stat.preco_atual - nacional) / nacional) * 100 : null;

  return (
    <button
      onClick={onClick}
      className={`
        p-3 rounded-xl text-left transition border
        ${
          active
            ? "bg-emerald-500/15 border-emerald-500/50 shadow-lg shadow-emerald-500/10"
            : "bg-slate-900/40 border-slate-800 hover:border-slate-600"
        }
      `}
    >
      <div className="flex items-center gap-2 mb-1.5">
        <span
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: commodity.color }}
        />
        <span className="text-xs font-semibold text-slate-200">
          {commodity.label}
        </span>
      </div>
      {stat ? (
        <>
          <div className="text-lg font-bold font-mono tabular-nums text-slate-100">
            R$ {stat.preco_atual.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
          </div>
          <div className="flex items-center gap-1 mt-0.5">
            {diff != null && (
              <span
                className={`text-[10px] font-bold flex items-center gap-0.5 ${
                  diff > 0
                    ? "text-emerald-400"
                    : diff < 0
                    ? "text-rose-400"
                    : "text-slate-500"
                }`}
              >
                {diff > 0 ? (
                  <TrendingUp className="w-2.5 h-2.5" />
                ) : diff < 0 ? (
                  <TrendingDown className="w-2.5 h-2.5" />
                ) : (
                  <Minus className="w-2.5 h-2.5" />
                )}
                {diff > 0 ? "+" : ""}
                {diff.toFixed(1)}% vs BR
              </span>
            )}
          </div>
        </>
      ) : (
        <div className="text-xs text-slate-600 py-2">
          sem dado em {uf}
        </div>
      )}
    </button>
  );
}

// ---------------------------------------------------------------------------
// Histórico da commodity selecionada na UF
// ---------------------------------------------------------------------------
function HistoricoCommodity({
  commodity,
  uf,
}: {
  commodity: string;
  uf: string;
}) {
  const [range, setRange] = useState<number>(60); // meses

  const { data, isLoading } = useSWR<AgrolinkResponse>(
    `/market/quotes/history_db/${commodity}`,
    swrFetcher,
    { refreshInterval: 3600_000, revalidateOnFocus: false }
  );

  const commodityDef = COMMODITIES.find((c) => c.id === commodity);
  const ufDetail = data?.ufs.find((u) => u.uf === uf);
  const stat = data?.uf_stats?.find((s) => s.uf === uf);

  const serie = useMemo(() => {
    if (!ufDetail) return [];
    return [...ufDetail.historico].reverse().slice(-range).map((h) => ({
      mes: h.mes,
      estadual: h.estadual,
      nacional: h.nacional,
    }));
  }, [ufDetail, range]);

  if (!commodityDef) return null;

  return (
    <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">
            {commodityDef.label} — {uf}
          </h3>
          <p className="text-xs text-slate-500">
            {data?.unit ?? ""}
            {stat && ` · última referência ${stat.mes_ref}`}
          </p>
        </div>
        <div className="flex items-center gap-1 bg-slate-950 border border-slate-800 rounded-lg p-1">
          {[
            { m: 12, label: "1 ano" },
            { m: 24, label: "2 anos" },
            { m: 60, label: "5 anos" },
            { m: 120, label: "10 anos" },
            { m: 300, label: "tudo" },
          ].map((r) => (
            <button
              key={r.m}
              onClick={() => setRange(r.m)}
              className={`px-2.5 py-1 text-xs rounded ${
                range === r.m
                  ? "bg-emerald-500/20 text-emerald-300"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      <div className="h-64">
        {isLoading ? (
          <div className="h-full flex items-center justify-center text-slate-400">
            <Loader2 className="w-5 h-5 animate-spin mr-2" /> Carregando série…
          </div>
        ) : serie.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-500 text-sm">
            Sem série histórica para {commodityDef.label} em {uf}.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={serie}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f293750" />
              <XAxis
                dataKey="mes"
                stroke="#64748b"
                tick={{ fontSize: 10 }}
                interval={Math.max(0, Math.floor(serie.length / 10))}
              />
              <YAxis stroke="#64748b" tick={{ fontSize: 10 }} width={50} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid #1e293b",
                  borderRadius: "8px",
                  color: "#e2e8f0",
                  fontSize: 12,
                }}
                formatter={(v) =>
                  typeof v === "number"
                    ? v.toLocaleString("pt-BR", { minimumFractionDigits: 2 })
                    : String(v)
                }
              />
              <Line
                type="monotone"
                dataKey="estadual"
                name={uf}
                stroke={commodityDef.color}
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="nacional"
                name="Brasil"
                stroke="#64748b"
                strokeWidth={1.5}
                strokeDasharray="4 4"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// News Card
// ---------------------------------------------------------------------------
function NewsCard({ article }: { article: NewsArticle }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noreferrer"
      className="block p-3 bg-slate-950/40 border border-slate-800 rounded-lg hover:border-emerald-500/30 transition group"
    >
      <div className="flex justify-between items-start gap-2 mb-1">
        <h3 className="text-sm font-medium text-slate-100 line-clamp-2 group-hover:text-emerald-300">
          {article.title}
        </h3>
        <ExternalLink className="w-3 h-3 text-slate-600 flex-shrink-0 mt-1 group-hover:text-emerald-400" />
      </div>
      <div className="text-[10px] text-slate-500">{formatDate(article.published_at)}</div>
    </a>
  );
}

function formatDate(iso: string): string {
  try {
    const d = new Date(iso);
    const diffH = (Date.now() - d.getTime()) / 3_600_000;
    if (diffH < 1) return `${Math.round(diffH * 60)}min atrás`;
    if (diffH < 24) return `${Math.round(diffH)}h atrás`;
    const diffD = Math.round(diffH / 24);
    if (diffD < 7) return `${diffD}d atrás`;
    return d.toLocaleDateString("pt-BR");
  } catch {
    return iso.slice(0, 10);
  }
}
