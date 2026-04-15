"use client";

import {
  Database,
  Search,
  FileText,
  Activity,
  Shield,
  AlertTriangle,
  MapPin,
  TrendingUp,
  ArrowRight,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { checkHealth, apiGet } from "@/lib/api";
import { KpiCard } from "@/components/dashboard/kpi-card";
import Link from "next/link";
import { cn } from "@/lib/utils";

interface DbStats {
  tables: Record<string, number>;
}

// Quick links para as seções principais
const QUICK_ACTIONS = [
  {
    label: "Consulta por CPF/CNPJ",
    desc: "Auditoria em 6 fontes simultâneas",
    href: "/consulta",
    icon: Search,
    color: "text-agrojus-emerald",
  },
  {
    label: "Mapa Geoespacial",
    desc: "Camadas IBAMA, FUNAI, CAR, INPE",
    href: "/mapa",
    icon: MapPin,
    color: "text-blue-400",
  },
  {
    label: "Compliance MCR / EUDR",
    desc: "Verificação contra bases oficiais",
    href: "/compliance",
    icon: Shield,
    color: "text-risk-medium",
  },
  {
    label: "Cotações e Mercado",
    desc: "Soja, milho, boi gordo, dólar",
    href: "/mercado",
    icon: TrendingUp,
    color: "text-purple-400",
  },
];

// Alertas recentes estáticos por ora — serão backend-driven
const RECENT_ALERTS = [
  {
    type: "embargo",
    title: "3 embargos IBAMA indexados no banco local",
    time: "Hoje",
    severity: "high" as const,
  },
  {
    type: "slave_labour",
    title: "4 registros MTE (Lista Suja) carregados via ETL",
    time: "Hoje",
    severity: "critical" as const,
  },
  {
    type: "data",
    title: "Parcelas de financiamento (4.7 GB GPKG) em ingestão",
    time: "Em andamento",
    severity: "info" as const,
  },
];

const severityStyle = {
  info: "border-l-blue-400 bg-blue-400/5",
  high: "border-l-risk-high bg-risk-high/5",
  critical: "border-l-risk-critical bg-risk-critical/5",
};

export default function DashboardPage() {
  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 10000,
  });

  return (
    <div className="space-y-8">
      {/* Título */}
      <div>
        <h2 className="text-2xl font-display font-bold">
          Painel de Inteligência
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          AgroJus — Inteligência Fundiária, Ambiental e de Mercado
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="Fontes Conectadas"
          value="13"
          subtitle="11 online • 2 parciais"
          icon={Database}
          trend="positive"
        />
        <KpiCard
          title="Embargos IBAMA"
          value="3"
          subtitle="Banco local atualizado"
          icon={AlertTriangle}
          trend="negative"
        />
        <KpiCard
          title="Lista Suja MTE"
          value="4"
          subtitle="91 trabalhadores resgatados"
          icon={Shield}
          trend="negative"
        />
        <KpiCard
          title="Latência API"
          value={health?.online ? `${health.latencyMs}ms` : "—"}
          subtitle={health?.online ? "Backend operacional" : "Offline"}
          icon={Activity}
          trend={health?.online ? "positive" : "negative"}
        />
      </div>

      {/* Ações rápidas + Alertas */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-2 space-y-3">
          <h3 className="text-lg font-display font-semibold">Acesso Rápido</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {QUICK_ACTIONS.map((action) => (
              <Link
                key={action.href}
                href={action.href}
                className="glass rounded-xl p-4 flex items-center gap-4 glow-hover transition-all duration-200 group"
              >
                <div className="w-10 h-10 rounded-lg bg-agrojus-elevated flex items-center justify-center shrink-0">
                  <action.icon size={20} className={action.color} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold group-hover:text-agrojus-emerald transition-colors">
                    {action.label}
                  </p>
                  <p className="text-xs text-[var(--muted-foreground)] truncate">
                    {action.desc}
                  </p>
                </div>
                <ArrowRight
                  size={14}
                  className="text-[var(--muted-foreground)] group-hover:text-agrojus-emerald transition-colors shrink-0"
                />
              </Link>
            ))}
          </div>
        </div>

        {/* Alertas */}
        <div className="space-y-3">
          <h3 className="text-lg font-display font-semibold">Alertas Recentes</h3>
          <div className="space-y-2">
            {RECENT_ALERTS.map((alert, i) => (
              <div
                key={i}
                className={cn(
                  "rounded-lg p-3 border-l-2 text-sm",
                  severityStyle[alert.severity]
                )}
              >
                <p className="font-medium text-foreground text-xs">
                  {alert.title}
                </p>
                <p className="text-[10px] text-[var(--muted-foreground)] mt-0.5">
                  {alert.time}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
