"use client";

import { useMemo, useState } from "react";
import useSWR from "swr";
import {
  TrendingUp,
  TrendingDown,
  Activity,
  DollarSign,
  Loader2,
  Newspaper,
  ExternalLink,
} from "lucide-react";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Area,
  AreaChart,
} from "recharts";
import { swrFetcher } from "@/lib/api";

type Quote = {
  commodity: string;
  price: number;
  unit: string;
  date: string;
  source: string;
  variation_pct: number;
  location: string;
  ticker?: string;
};

type HistoryPoint = {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
};

type HistoryResponse = { ticker: string; history: HistoryPoint[]; error?: string };

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
  category?: string;
};

// Map commodities principais → ticker Yahoo Finance
const COMMODITY_TICKERS: Record<string, { ticker: string; label: string; color: string }> = {
  soja: { ticker: "ZS=F", label: "Soja", color: "#22c55e" },
  milho: { ticker: "ZC=F", label: "Milho", color: "#eab308" },
  cafe: { ticker: "KC=F", label: "Café Arábica", color: "#a16207" },
  acucar: { ticker: "SB=F", label: "Açúcar Bruto", color: "#8b5cf6" },
  algodao: { ticker: "CT=F", label: "Algodão", color: "#e5e7eb" },
  trigo: { ticker: "ZW=F", label: "Trigo", color: "#d97706" },
  boi_gordo: { ticker: "LE=F", label: "Boi Gordo (CME)", color: "#dc2626" },
  oleo_soja: { ticker: "ZL=F", label: "Óleo de Soja", color: "#16a34a" },
};

export default function Mercado() {
  const [selectedTicker, setSelectedTicker] = useState<string>("ZS=F");
  const [range, setRange] = useState<string>("6mo");

  const { data: quotesData, isLoading: loadingQuotes } = useSWR<{ quotes: Quote[] }>(
    "/market/quotes",
    swrFetcher,
    { refreshInterval: 300_000 }
  );

  const { data: indicatorsData } = useSWR<{ indicators: Indicators }>(
    "/market/indicators",
    swrFetcher,
    { refreshInterval: 300_000 }
  );

  const { data: historyData, isLoading: loadingHistory } = useSWR<HistoryResponse>(
    `/market/quotes/history/${selectedTicker}?range=${range}&interval=1d`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const { data: newsData } = useSWR<{ articles: NewsArticle[] }>(
    "/news/market?limit=8",
    swrFetcher,
    { refreshInterval: 600_000 }
  );

  const quotes = quotesData?.quotes || [];
  const indicators = indicatorsData?.indicators || {};

  const chartData = useMemo(() => {
    return (historyData?.history || []).map((p) => ({
      date: new Date(p.time * 1000).toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
      }),
      price: p.close,
    }));
  }, [historyData]);

  const currentCommodity = Object.values(COMMODITY_TICKERS).find(
    (c) => c.ticker === selectedTicker
  );

  return (
    <div className="p-6 lg:p-8 max-w-[1400px] mx-auto space-y-8 animate-in fade-in duration-500">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-heading font-extrabold text-slate-100 tracking-tight flex items-center gap-3">
          <TrendingUp className="h-8 w-8 text-emerald-400" />
          Mercado &amp; Commodities
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Cotações CEPEA/ESALQ (físico BR) + futuros CBOT/CME (Yahoo Finance) +
          indicadores macro BCB. Atualização a cada 5 min.
        </p>
      </header>

      {/* Gráfico principal */}
      <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-6">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">
              {currentCommodity?.label || "Cotação"} —{" "}
              <span className="text-xs text-slate-500 font-mono">{selectedTicker}</span>
            </h2>
            <p className="text-xs text-slate-500">
              Contrato futuro · fonte Yahoo Finance (CBOT/CME/ICE)
            </p>
          </div>
          <div className="flex items-center gap-1 bg-slate-950 border border-slate-800 rounded-lg p-1">
            {["1mo", "3mo", "6mo", "1y", "2y"].map((r) => (
              <button
                key={r}
                onClick={() => setRange(r)}
                className={`px-2.5 py-1 text-xs rounded ${
                  range === r
                    ? "bg-emerald-500/20 text-emerald-300"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {r}
              </button>
            ))}
          </div>
        </div>

        {/* Seletor de commodity */}
        <div className="flex flex-wrap gap-2 mb-5">
          {Object.values(COMMODITY_TICKERS).map((c) => (
            <button
              key={c.ticker}
              onClick={() => setSelectedTicker(c.ticker)}
              className={`px-3 py-1.5 text-xs rounded-lg border transition ${
                selectedTicker === c.ticker
                  ? "bg-emerald-500/20 border-emerald-500/40 text-emerald-300"
                  : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-600"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>

        <div className="h-80">
          {loadingHistory ? (
            <div className="h-full flex items-center justify-center text-slate-400">
              <Loader2 className="w-5 h-5 animate-spin mr-2" /> Carregando série…
            </div>
          ) : chartData.length === 0 ? (
            <div className="h-full flex items-center justify-center text-slate-500">
              Sem dados disponíveis para {selectedTicker}
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                    <stop
                      offset="0%"
                      stopColor={currentCommodity?.color || "#10b981"}
                      stopOpacity={0.35}
                    />
                    <stop
                      offset="100%"
                      stopColor={currentCommodity?.color || "#10b981"}
                      stopOpacity={0}
                    />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f293750" />
                <XAxis
                  dataKey="date"
                  stroke="#64748b"
                  tick={{ fontSize: 11 }}
                  interval="preserveStartEnd"
                />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} width={55} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    border: "1px solid #1e293b",
                    borderRadius: "8px",
                    color: "#e2e8f0",
                  }}
                  labelStyle={{ color: "#94a3b8", fontSize: 11 }}
                  formatter={(v) => [
                    typeof v === "number" ? v.toFixed(2) : String(v),
                    "Fechamento",
                  ]}
                />
                <Area
                  type="monotone"
                  dataKey="price"
                  stroke={currentCommodity?.color || "#10b981"}
                  strokeWidth={2}
                  fill="url(#grad)"
                />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cards de cotações CEPEA */}
        <section className="lg:col-span-2 bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm uppercase tracking-wider font-bold text-slate-400 mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <DollarSign className="h-4 w-4" /> Cotações CEPEA/ESALQ
            </div>
            {loadingQuotes && <Loader2 className="h-4 w-4 animate-spin" />}
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {quotes.map((q, i) => (
              <QuoteCard key={i} quote={q} />
            ))}
            {quotes.length === 0 && !loadingQuotes && (
              <p className="text-slate-500 text-sm col-span-full text-center py-6">
                Nenhuma cotação disponível.
              </p>
            )}
          </div>
        </section>

        {/* Indicadores macro */}
        <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm uppercase tracking-wider font-bold text-slate-400 mb-4 flex items-center gap-2">
            <Activity className="h-4 w-4" /> Macro BCB
          </h2>
          <div className="space-y-3">
            {Object.entries(indicators).map(([key, ind]) => (
              <div
                key={key}
                className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg"
              >
                <div className="text-[10px] uppercase tracking-wider text-slate-500">
                  {ind.name}
                </div>
                <div className="text-xl font-mono font-bold text-slate-100 mt-0.5 flex items-baseline gap-1">
                  {parseFloat(ind.value).toLocaleString("pt-BR", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 4,
                  })}
                  <span className="text-xs font-normal text-slate-500">
                    {ind.unit}
                  </span>
                </div>
                <div className="text-[10px] text-slate-600 mt-0.5">{ind.date}</div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Notícias de mercado */}
      <section className="bg-slate-900/40 border border-slate-800 rounded-xl p-5">
        <h2 className="text-sm uppercase tracking-wider font-bold text-slate-400 mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Newspaper className="h-4 w-4" /> Notícias de mercado
          </div>
          <a
            href="/noticias"
            className="text-xs text-emerald-400 hover:text-emerald-300"
          >
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
  );
}

function QuoteCard({ quote }: { quote: Quote }) {
  const up = (quote.variation_pct || 0) >= 0;
  return (
    <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-lg hover:border-slate-700 transition">
      <div className="flex justify-between items-start mb-1">
        <div className="text-sm font-semibold text-slate-100 truncate">
          {quote.commodity}
        </div>
        {quote.variation_pct !== 0 && (
          <span
            className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded flex items-center gap-0.5 ${
              up
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-rose-500/10 text-rose-400"
            }`}
          >
            {up ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            {quote.variation_pct > 0 ? "+" : ""}
            {quote.variation_pct.toFixed(2)}%
          </span>
        )}
      </div>
      <div className="text-lg font-mono font-bold text-emerald-400 tabular-nums">
        {quote.unit === "R$" ? "R$ " : ""}
        {quote.price.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
        <span className="text-xs text-slate-500 font-normal ml-1">
          {quote.unit !== "R$" && quote.unit}
        </span>
      </div>
      <div className="text-[10px] text-slate-500 mt-0.5 flex justify-between">
        <span>{quote.location}</span>
        <span>{quote.date}</span>
      </div>
    </div>
  );
}

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
      <div className="text-[10px] text-slate-500 flex items-center gap-2">
        <span className="font-medium">{article.source}</span>
        <span>·</span>
        <span>{formatDate(article.published_at)}</span>
      </div>
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
