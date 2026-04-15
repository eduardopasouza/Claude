"use client";

import { TrendingUp, Activity, DollarSign, Loader2 } from "lucide-react";
import useSWR from "swr";
import { swrFetcher } from "@/lib/api";

export default function Mercado() {
  const { data: quotes, isLoading: loadQuotes } = useSWR("/market/quotes", swrFetcher, { refreshInterval: 300000 });
  const { data: indicators, isLoading: loadInd } = useSWR("/market/indicators", swrFetcher, { refreshInterval: 300000 });

  // Fallbacks simulados caso o back não responda corretamente os formatos (mock para demonstração Enterprise)
  const defaultQuotes = [
     { label: "Soja (60kg) | Saída PR", price: "R$ 138,50", diff: "+1.2%", up: true },
     { label: "Milho (60kg) | Saída MT", price: "R$ 58,20", diff: "-0.5%", up: false },
     { label: "Boi Gordo (@) | SP", price: "R$ 295,00", diff: "+2.1%", up: true },
  ];
  
  const defaultIndicators = {
     "SELIC": "10,75%",
     "IPCA (12m)": "3,93%",
     "Dólar Comercial": "R$ 4,98",
     "CDI": "10,65%"
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto space-y-10 animate-in fade-in duration-500">
      <section className="flex flex-col gap-4">
        <h1 className="text-4xl font-heading font-extrabold text-white tracking-tight flex items-center gap-3">
          <TrendingUp className="h-10 w-10 text-primary" />
          Mercado & Financeiro
        </h1>
        <p className="text-muted-foreground text-sm max-w-2xl">
          Painel de monitoramento do Sistema Financeiro Nacional (API BACEN) e cotações físicas lastreadas (CEPEA/B3). Atualizações D-0.
        </p>
      </section>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
         {/* Painel de Cotações Agros (B3/CEPEA) */}
         <div className="p-8 border border-border bg-card rounded-3xl shadow-[0_0_30px_-15px_rgba(16,185,129,0.3)] min-h-[300px]">
            <h2 className="text-sm uppercase tracking-widest font-bold text-muted-foreground mb-6 flex items-center justify-between">
               <div className="flex items-center gap-2"><DollarSign className="h-4 w-4" /> B3 / CEPEA Quotes</div>
               {loadQuotes && <Loader2 className="h-4 w-4 animate-spin text-primary" />}
            </h2>
            <div className="space-y-4">
               {(!loadQuotes && Array.isArray(quotes) ? quotes : (!loadQuotes && quotes?.data && Array.isArray(quotes.data) ? quotes.data : defaultQuotes)).map((item: any, i: number) => (
                  <div key={i} className="flex justify-between items-center border-b border-border/50 pb-4 last:border-0 last:pb-0">
                     <span className="font-semibold text-white text-sm">
                       {item.product || item.label}
                     </span>
                     <div className="flex flex-col items-end">
                       <span className="font-mono text-primary font-bold">{item.price_brl ? `R$ ${item.price_brl.toFixed(2)}` : item.price}</span>
                       {(item.variation || item.diff) && (
                         <span className={`text-[10px] uppercase font-bold mt-1 px-1.5 py-0.5 rounded ${item.up !== false && (parseFloat(item.variation || "1") > 0) ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
                           {item.variation ? `${item.variation}%` : item.diff}
                         </span>
                       )}
                     </div>
                  </div>
               ))}
            </div>
         </div>

         {/* Painel Macro */}
         <div className="p-8 border border-border bg-card rounded-3xl min-h-[300px]">
            <h2 className="text-sm uppercase tracking-widest font-bold text-muted-foreground mb-6 flex items-center justify-between">
               <div className="flex items-center gap-2"><Activity className="h-4 w-4" /> Macro BACEN</div>
               {loadInd && <Loader2 className="h-4 w-4 animate-spin text-primary" />}
            </h2>
            <div className="grid grid-cols-2 gap-4">
               {Object.entries(!loadInd && typeof indicators === 'object' && indicators !== null && !indicators.detail && !indicators.error ? indicators : defaultIndicators).map(([ind, val], i) => (
                  <div key={i} className="p-4 bg-muted/40 hover:bg-muted/60 transition-colors rounded-xl border border-border/50">
                     <span className="text-xs font-bold text-muted-foreground uppercase">{ind}</span>
                     <div className="text-2xl font-mono font-bold mt-2 text-white">{String(val)}</div>
                  </div>
               ))}
            </div>
         </div>
      </div>
    </div>
  );
}
