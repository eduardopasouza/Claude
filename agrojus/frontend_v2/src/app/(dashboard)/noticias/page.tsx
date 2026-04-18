"use client";

import { useState } from "react";
import useSWR from "swr";
import {
  Newspaper,
  Loader2,
  ExternalLink,
  Scale,
  TrendingUp,
  Globe,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";

type NewsArticle = {
  title: string;
  url: string;
  source: string;
  published_at: string;
  summary?: string;
  category?: string;
  image_url?: string | null;
};

type Response = {
  articles: NewsArticle[];
  total: number;
  skip: number;
  limit: number;
  is_reference?: boolean;
};

type Category = "all" | "legal" | "market";

const CATEGORIES: Array<{ id: Category; label: string; icon: typeof Globe; endpoint: string }> = [
  { id: "all", label: "Todas", icon: Globe, endpoint: "/news/?limit=50" },
  { id: "market", label: "Mercado", icon: TrendingUp, endpoint: "/news/market?limit=50" },
  { id: "legal", label: "Jurídico", icon: Scale, endpoint: "/news/legal?limit=50" },
];

export default function NoticiasPage() {
  const [cat, setCat] = useState<Category>("all");
  const current = CATEGORIES.find((c) => c.id === cat) || CATEGORIES[0];

  const { data, isLoading } = useSWR<Response>(current.endpoint, swrFetcher, {
    refreshInterval: 600_000,
  });

  const articles = data?.articles || [];
  const isReference = data?.is_reference;

  return (
    <div className="p-6 lg:p-8 max-w-[1200px] mx-auto space-y-6 animate-in fade-in duration-500">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-heading font-extrabold text-slate-100 tracking-tight flex items-center gap-3">
          <Newspaper className="h-8 w-8 text-emerald-400" />
          Notícias do Agronegócio
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Curadoria em tempo real de Canal Rural, Agrolink, Notícias Agrícolas,
          Portal do Agronegócio, Embrapa e mais. Atualização a cada 10 min.
        </p>
      </header>

      {/* Filtros */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
        {CATEGORIES.map((c) => {
          const Icon = c.icon;
          const active = cat === c.id;
          return (
            <button
              key={c.id}
              onClick={() => setCat(c.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
                active
                  ? "bg-emerald-500/20 border border-emerald-500/40 text-emerald-300"
                  : "text-slate-400 hover:text-slate-200 border border-transparent"
              }`}
            >
              <Icon className="w-4 h-4" />
              {c.label}
            </button>
          );
        })}
        {data && (
          <span className="ml-auto text-xs text-slate-500">
            {articles.length} de {data.total}
            {isReference && " · dados de referência (RSS offline)"}
          </span>
        )}
      </div>

      {isLoading && (
        <div className="p-16 flex items-center justify-center text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          Coletando feeds RSS…
        </div>
      )}

      {!isLoading && articles.length === 0 && (
        <div className="p-16 text-center text-slate-500 text-sm">
          Nenhuma notícia encontrada na categoria.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {articles.map((n, i) => (
          <NewsCardFull key={i} article={n} />
        ))}
      </div>
    </div>
  );
}

function NewsCardFull({ article }: { article: NewsArticle }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noreferrer"
      className="flex flex-col bg-slate-900/40 border border-slate-800 rounded-xl overflow-hidden hover:border-emerald-500/40 transition group"
    >
      {article.image_url && (
        /* eslint-disable-next-line @next/next/no-img-element */
        <img
          src={article.image_url}
          alt=""
          className="h-36 w-full object-cover"
          onError={(e) => {
            (e.target as HTMLImageElement).style.display = "none";
          }}
        />
      )}
      <div className="p-4 flex-1 flex flex-col gap-2">
        <div className="flex items-center justify-between text-[10px] text-slate-500 uppercase tracking-wider">
          <span className="font-medium text-emerald-400/80">{article.source}</span>
          <span>{formatDate(article.published_at)}</span>
        </div>
        <h3 className="text-sm font-semibold text-slate-100 line-clamp-3 group-hover:text-emerald-300">
          {article.title}
        </h3>
        {article.summary && (
          <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
            {article.summary}
          </p>
        )}
        <div className="mt-auto flex items-center justify-between pt-2 border-t border-slate-800/60">
          {article.category && (
            <span
              className={`text-[10px] uppercase font-semibold px-2 py-0.5 rounded ${
                article.category === "juridico"
                  ? "bg-purple-500/10 text-purple-300"
                  : "bg-emerald-500/10 text-emerald-300"
              }`}
            >
              {article.category}
            </span>
          )}
          <ExternalLink className="w-3 h-3 text-slate-600 group-hover:text-emerald-400 ml-auto" />
        </div>
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
