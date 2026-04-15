"use client";

import useSWR from "swr";
import { swrFetcher } from "@/lib/api";
import { Activity, ShieldAlert, Zap, Globe, TrendingUp, ChevronRight, Loader2 } from "lucide-react";

export default function Dashboard() {
  const { data, error, isLoading } = useSWR("/dashboard/metrics", swrFetcher, {
    refreshInterval: 60000,
    revalidateOnFocus: true,
  });

  const kpis = [
    { 
      label: "Imóveis Rurais (CAR)", 
      value: data?.kpis?.cars_imoveis?.total?.toLocaleString('pt-BR') || "0", 
      icon: Globe, 
      color: "text-emerald-500", 
      glow: "group-hover:bg-emerald-500/10" 
    },
    { 
      label: "Alertas Desmatamento", 
      value: data?.kpis?.desmatamento?.total?.toLocaleString('pt-BR') || "0", 
      icon: ShieldAlert, 
      color: "text-rose-500", 
      glow: "group-hover:bg-rose-500/10" 
    },
    { 
      label: "Fiscalizações (IBAMA/ICMBio)", 
      value: ((data?.kpis?.ibama_embargos?.total || 0) + (data?.kpis?.icmbio?.total || 0)).toLocaleString('pt-BR'), 
      icon: Activity, 
      color: "text-primary", 
      glow: "group-hover:bg-primary/10" 
    },
    { 
      label: "Latência DB (P99)", 
      value: data ? `${data.db_latency_ms}ms` : "0ms", 
      icon: Zap, 
      color: "text-emerald-500", 
      glow: "group-hover:bg-emerald-500/10" 
    },
  ];

  return (
    <div className="p-8 max-w-[1400px] mx-auto space-y-10 animate-in fade-in zoom-in-95 duration-500">
      
      {/* Hero Section */}
      <section className="flex flex-col gap-4">
        <h1 className="text-4xl font-heading font-extrabold text-white tracking-tight">Plataforma de Inteligência</h1>
        <p className="text-muted-foreground text-base max-w-2xl">
          Dados processados em D-1 usando PostGIS e BigQuery. Acompanhe os indicadores nacionais.
        </p>
      </section>

      {/* KPI Grid */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {kpis.map((kpi, i) => (
          <div key={i} className="p-6 rounded-2xl border border-border bg-card shadow-sm hover:shadow-[0_0_20px_-5px_rgba(255,255,255,0.05)] hover:border-border/80 transition-all relative overflow-hidden group">
            <div className="flex items-center justify-between mb-4 relative z-10">
               <span className="text-sm font-semibold tracking-wide text-muted-foreground">{kpi.label}</span>
               <kpi.icon className={`h-5 w-5 ${kpi.color}`} />
            </div>
            {isLoading ? (
               <div className="h-10 w-24 bg-border/40 animate-pulse rounded-md relative z-10" />
            ) : (
               <h3 className="text-4xl font-bold font-heading relative z-10">{kpi.value}</h3>
            )}
            
            <div className={`absolute -right-8 -bottom-8 w-32 h-32 bg-transparent rounded-full blur-3xl transition-colors duration-500 ${kpi.glow}`} />
          </div>
        ))}
      </section>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        {/* Main Panel: News / Feed */}
        <section className="xl:col-span-2 space-y-5">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold font-heading flex items-center gap-2">
               <Activity className="h-5 w-5 text-primary" />
               Últimas Atualizações Oficiais
            </h2>
          </div>
          
          <div className="rounded-2xl border border-border bg-card overflow-hidden">
             {[
               { src: "IBAMA", msg: "Base de embargos atualizada e vetores reconstruídos.", time: "Há 2 horas", type: "success" },
               { src: "INPE", msg: "Processamento de DETER atrasado na infraestrutura federal.", time: "Há 4 horas", type: "error" },
               { src: "MTE", msg: "Ingestão da Lista Suja Trabalho Análogo à Escravidão concluída.", time: "Há 12 horas", type: "success" },
               { src: "SICOR", msg: "Lote de créditos rurais cruzados com MapBiomas Alertas.", time: "Há 14 horas", type: "success" },
             ].map((feed, i) => (
                <div key={i} className="p-5 border-b border-border/50 last:border-0 flex items-start gap-4 hover:bg-muted/30 transition-colors cursor-pointer group">
                   <div className={`mt-1.5 h-2 w-2 rounded-full ring-4 flex-shrink-0 ${feed.type === 'success' ? 'bg-emerald-500 ring-emerald-500/10 group-hover:ring-emerald-500/20' : 'bg-rose-500 ring-rose-500/10 group-hover:ring-rose-500/20'} transition-all`} />
                   <div className="flex-1">
                      <p className="text-sm font-medium text-foreground/90">{feed.msg}</p>
                      <div className="flex items-center gap-2 mt-2">
                         <span className="text-[10px] uppercase font-bold tracking-widest text-muted-foreground bg-muted px-1.5 py-0.5 rounded">{feed.src}</span>
                         <span className="text-xs text-muted-foreground font-mono">&bull; {feed.time}</span>
                      </div>
                   </div>
                </div>
             ))}
          </div>
        </section>

        {/* Side Panel: Markets */}
        <section className="space-y-5">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold font-heading flex items-center gap-2">
               <TrendingUp className="h-5 w-5 text-primary" />
               Mercado Ativo
            </h2>
          </div>
          
          <div className="grid grid-cols-1 gap-4">
             {[
                { label: "Soja (Saca 60kg)", price: "R$ 138,50", diff: "+1.2%", up: true },
                { label: "Milho (Saca 60kg)", price: "R$ 58,20", diff: "-0.5%", up: false },
                { label: "Boi Gordo (@)", price: "R$ 295,00", diff: "+2.1%", up: true },
                { label: "Dólar Comercial", price: "R$ 5,020", diff: "-0.1%", up: true },
             ].map((quote, i) => (
                <div key={i} className="p-5 rounded-2xl border border-border bg-card flex items-center justify-between hover:border-primary/40 transition-all cursor-pointer">
                   <div>
                     <p className="text-xs tracking-wide text-muted-foreground font-semibold uppercase">{quote.label}</p>
                     <p className="text-2xl font-bold font-mono mt-1 text-white">{quote.price}</p>
                   </div>
                   <div className={`text-xs font-bold px-2.5 py-1.5 rounded-lg border ${quote.up ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border-rose-500/20'}`}>
                      {quote.diff}
                   </div>
                </div>
             ))}
          </div>
        </section>
        
      </div>
    </div>
  );
}
