"use client";

import { Database, Search, FileText, Activity } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/lib/api";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { NewsFeed } from "@/components/dashboard/news-feed";

export default function DashboardPage() {
  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 10000,
  });

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Visao geral da plataforma AgroJus
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="Fontes de Dados"
          value="13"
          subtitle="11/13 online"
          icon={Database}
          trend="positive"
        />
        <KpiCard
          title="Buscas Hoje"
          value="—"
          subtitle="Plano Free: 10/dia"
          icon={Search}
        />
        <KpiCard
          title="Relatorios/Mes"
          value="—"
          subtitle="Plano Free: 3/mes"
          icon={FileText}
        />
        <KpiCard
          title="Latencia API"
          value={health?.online ? `${health.latencyMs}ms` : "—"}
          subtitle={health?.online ? "Sistema online" : "Offline"}
          icon={Activity}
          trend={health?.online ? "positive" : "negative"}
        />
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Noticias Agro</h3>
        <NewsFeed />
      </div>
    </div>
  );
}
