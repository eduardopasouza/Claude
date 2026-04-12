"use client";

import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ApiStatusProps {
  collapsed: boolean;
}

export function ApiStatus({ collapsed }: ApiStatusProps) {
  const { data } = useQuery({
    queryKey: ["api-health"],
    queryFn: checkHealth,
    refetchInterval: 10_000,
    refetchIntervalInBackground: true,
    retry: false,
  });

  const online = data?.online ?? false;
  const latencyMs = data?.latencyMs ?? 0;

  return (
    <div
      className={cn(
        "flex items-center gap-2 px-3 py-2 rounded-lg",
        collapsed ? "justify-center" : "justify-start"
      )}
      title={online ? `Online — ${latencyMs}ms` : "Offline"}
    >
      {/* Pulsing status dot */}
      <span className="relative flex h-2 w-2 shrink-0">
        {online && (
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-agrojus-emerald opacity-60" />
        )}
        <span
          className={cn(
            "relative inline-flex h-2 w-2 rounded-full",
            online ? "bg-agrojus-emerald" : "bg-risk-critical"
          )}
        />
      </span>

      {!collapsed && (
        <span className="flex items-center gap-1.5 text-xs font-medium">
          <span
            className={cn(
              online ? "text-agrojus-emerald" : "text-risk-critical"
            )}
          >
            {online ? "Online" : "Offline"}
          </span>
          {online && latencyMs > 0 && (
            <span className="text-[var(--muted-foreground)]">
              {latencyMs}ms
            </span>
          )}
        </span>
      )}
    </div>
  );
}
