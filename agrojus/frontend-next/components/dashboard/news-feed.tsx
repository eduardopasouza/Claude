"use client";

import { useNews } from "@/lib/hooks/use-news";

export function NewsFeed() {
  const { articles, isLoading, error } = useNews(20);

  if (isLoading) {
    return (
      <div className="flex flex-col gap-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="h-16 bg-agrojus-elevated rounded-lg animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <p className="text-xs text-[var(--muted-foreground)] py-4 text-center">
        Não foi possível carregar as notícias.
      </p>
    );
  }

  if (articles.length === 0) {
    return (
      <p className="text-xs text-[var(--muted-foreground)] py-4 text-center">
        Nenhuma notícia disponível.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {articles.map((article, i) => (
        <a
          key={article.url ?? i}
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block bg-agrojus-surface border border-[var(--border)] rounded-lg px-4 py-3
                     hover:border-agrojus-emerald/30 transition-colors duration-150"
        >
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate leading-snug">
                {article.title}
              </p>
              <p className="text-xs text-[var(--muted-foreground)] mt-0.5 truncate">
                {article.source}
              </p>
            </div>

            {article.category && (
              <span
                className="flex-shrink-0 text-xs border border-[var(--border)] text-[var(--muted-foreground)]
                           rounded-full px-2 py-0.5 whitespace-nowrap"
              >
                {article.category}
              </span>
            )}
          </div>
        </a>
      ))}
    </div>
  );
}
