"use client";

import { useState, useEffect, useRef } from "react";
import { apiGet } from "@/lib/api";

export interface NewsArticle {
  title: string;
  summary: string;
  source: string;
  url: string;
  published: string;
  category: string;
}

interface NewsResponse {
  results: NewsArticle[];
}

interface UseNewsResult {
  articles: NewsArticle[];
  isLoading: boolean;
  error: string | null;
}

const STALE_TIME_MS = 5 * 60 * 1000; // 5 minutes

// Module-level cache so re-mounts don't re-fetch within stale window
const cache: {
  data: NewsArticle[] | null;
  fetchedAt: number | null;
} = { data: null, fetchedAt: null };

export function useNews(limit = 20): UseNewsResult {
  const [articles, setArticles] = useState<NewsArticle[]>(cache.data ?? []);
  const [isLoading, setIsLoading] = useState<boolean>(
    cache.data === null || cache.fetchedAt === null
  );
  const [error, setError] = useState<string | null>(null);

  // Prevent duplicate in-flight requests
  const fetchingRef = useRef(false);

  useEffect(() => {
    const now = Date.now();
    const isFresh =
      cache.data !== null &&
      cache.fetchedAt !== null &&
      now - cache.fetchedAt < STALE_TIME_MS;

    if (isFresh) {
      setArticles(cache.data!);
      setIsLoading(false);
      return;
    }

    if (fetchingRef.current) return;
    fetchingRef.current = true;

    setIsLoading(true);
    setError(null);

    apiGet<NewsResponse | NewsArticle[]>(`/api/v1/news/?limit=${limit}`)
      .then(({ data, error: apiError }) => {
        if (apiError || data === null) {
          setError(apiError ?? "Unknown error");
          return;
        }

        // Handle both {results: [...]} and bare array shapes
        const list = Array.isArray(data) ? data : (data as NewsResponse).results ?? [];

        cache.data = list;
        cache.fetchedAt = Date.now();
        setArticles(list);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Network error");
      })
      .finally(() => {
        setIsLoading(false);
        fetchingRef.current = false;
      });
  }, [limit]);

  return { articles, isLoading, error };
}
