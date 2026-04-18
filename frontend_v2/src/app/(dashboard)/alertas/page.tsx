"use client";

import { ShieldAlert, BellRing } from "lucide-react";

export default function Alertas() {
  return (
    <div className="p-8 max-w-[1200px] mx-auto space-y-10 animate-in fade-in duration-500">
      <section className="flex flex-col gap-4">
        <h1 className="text-4xl font-heading font-extrabold text-white tracking-tight flex items-center gap-3">
          <ShieldAlert className="h-10 w-10 text-rose-500" />
          Central de Monitoramento
        </h1>
        <p className="text-muted-foreground text-sm max-w-2xl">
          Feed contínuo (Near Real-Time) de embargos e alertas de desmatamento aplicados sobre os imóveis cadastrados.
        </p>
      </section>

      <div className="rounded-3xl border border-border bg-card overflow-hidden my-8">
        {[
          { origem: "IBAMA", msg: "Embargo SIFISC registrado no município de Balsas/MA.", data: "15 Abr 2026, 09:12", lvl: "CRITICAL" },
          { origem: "DETER", msg: "Supressão vegetal detectada em polígono CAR monitorado.", data: "14 Abr 2026, 18:45", lvl: "HIGH" },
          { origem: "MTE", msg: "Inclusão de CNPJ associado na Lista Suja recém divulgada.", data: "12 Abr 2026, 10:00", lvl: "CRITICAL" },
          { origem: "PRODES", msg: "Sincronização anual de dados do bioma Cerrado concluída.", data: "10 Abr 2026, 01:21", lvl: "INFO" },
        ].map((alert, i) => (
           <div key={i} className="p-6 border-b border-border/50 last:border-0 hover:bg-muted/30 transition-colors flex items-start gap-4 cursor-pointer">
              <div className={`mt-1 h-3 w-3 rounded-full flex-shrink-0 ${alert.lvl === 'CRITICAL' ? 'bg-rose-500 animate-pulse' : alert.lvl === 'HIGH' ? 'bg-amber-500' : 'bg-primary'}`} />
              <div className="flex-1">
                 <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-bold uppercase tracking-widest bg-muted px-2 py-0.5 rounded text-muted-foreground">{alert.origem}</span>
                    <span className="text-xs text-muted-foreground font-mono">{alert.data}</span>
                    {alert.lvl === 'CRITICAL' && <span className="text-[10px] bg-rose-500/10 text-rose-500 font-bold px-2 py-0.5 rounded border border-rose-500/20 ml-2">URGENTE</span>}
                 </div>
                 <p className="text-sm font-medium text-white">{alert.msg}</p>
                 <button className="text-xs mt-3 text-primary font-bold hover:underline">Ver Detalhes do Alvo</button>
              </div>
           </div>
        ))}
      </div>
    </div>
  );
}
