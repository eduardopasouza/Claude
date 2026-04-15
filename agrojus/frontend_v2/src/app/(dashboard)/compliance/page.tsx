"use client";

import { ShieldCheck, Calendar, Filter, Download } from "lucide-react";

export default function Compliance() {
  return (
    <div className="p-8 max-w-[1200px] mx-auto space-y-10 animate-in fade-in duration-500">
      <section className="flex flex-col gap-4">
        <h1 className="text-4xl font-heading font-extrabold text-white tracking-tight flex items-center gap-3">
          <ShieldCheck className="h-10 w-10 text-primary" />
          MCR 2.9 & EUDR Compliance
        </h1>
        <p className="text-muted-foreground text-sm max-w-2xl">
          Visão consolidada da carteira. Monitoramento em massa contínuo contra desmatamentos e embargos ambientais de acordo com as requisições normativas do Bacen.
        </p>
      </section>
      
      <div className="flex gap-4 mb-4">
         <select className="bg-card border border-border px-4 py-2.5 rounded-xl font-bold text-sm text-white">
            <option>Safra 2025/2026</option>
            <option>Safra 2024/2025</option>
         </select>
         <button className="bg-muted hover:bg-muted/80 text-white font-bold border border-border px-4 py-2.5 rounded-xl transition-colors flex items-center gap-2">
            <Filter className="h-4 w-4" /> Somente Regulares
         </button>
         <button className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 font-bold border border-emerald-500/20 px-4 py-2.5 rounded-xl transition-colors flex items-center gap-2 ml-auto">
            <Download className="h-4 w-4" /> Exportar Auditoria Mensal (PDF)
         </button>
      </div>

      <div className="rounded-3xl border border-border bg-card overflow-hidden">
         <table className="w-full text-left text-sm">
            <thead className="bg-black/40 text-muted-foreground text-xs uppercase font-bold border-b border-border/50">
               <tr>
                  <th className="px-6 py-4">ID Operação</th>
                  <th className="px-6 py-4">Beneficiário (CPF/CNPJ)</th>
                  <th className="px-6 py-4">Área (ha)</th>
                  <th className="px-6 py-4 text-center">EUDR</th>
                  <th className="px-6 py-4 text-center">MCR 2.9</th>
               </tr>
            </thead>
            <tbody className="divide-y divide-border/50 text-white font-medium">
               {[
                  { op: "BNDES-101", doc: "044.212.***-99", ha: "420,5", eudr: "OK", mcr: "OK" },
                  { op: "BNDES-102", doc: "10.452.***-00", ha: "1.200,8", eudr: "OFF", mcr: "OK" },
                  { op: "BNDES-103", doc: "722.111.***-20", ha: "85,0", eudr: "OFF", mcr: "OFF" },
               ].map((o, i) => (
                  <tr key={i} className="hover:bg-muted/30 transition-colors">
                     <td className="px-6 py-4 font-mono text-muted-foreground">{o.op}</td>
                     <td className="px-6 py-4">{o.doc}</td>
                     <td className="px-6 py-4 font-mono">{o.ha}</td>
                     <td className="px-6 py-4 text-center">
                        <span className={`text-[10px] uppercase font-bold px-2 py-1 rounded border tracking-widest ${o.eudr === 'OK' ? 'bg-primary/10 text-primary border-primary/20' : 'bg-rose-500/10 text-rose-500 border-rose-500/20'}`}>
                           {o.eudr === 'OK' ? 'Regular' : 'Inibido'}
                        </span>
                     </td>
                     <td className="px-6 py-4 text-center">
                        <span className={`text-[10px] uppercase font-bold px-2 py-1 rounded border tracking-widest ${o.mcr === 'OK' ? 'bg-primary/10 text-primary border-primary/20' : 'bg-rose-500/10 text-rose-500 border-rose-500/20'}`}>
                           {o.mcr === 'OK' ? 'Apto' : 'Bloqueado'}
                        </span>
                     </td>
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
    </div>
  );
}
