"use client";

import { useState } from "react";
import { Search, Loader2, ShieldCheck, FileWarning, Briefcase, Building, Landmark, ChevronDown, CheckCircle2, Scale, ShieldAlert } from "lucide-react";
import { PieChart, Pie, Cell } from "recharts";

export default function DeepSearch() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(false);
  const [doc, setDoc] = useState("");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!doc.trim()) return;
    setLoading(true);
    setResults(false);
    
    // Simula o tempo do backend (3-5 segundos para consolidar dados)
    setTimeout(() => {
      setLoading(false);
      setResults(true);
    }, 3500);
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto space-y-10 animate-in fade-in zoom-in-95 duration-500">
      
      {/* Search Header */}
      <section className="flex flex-col gap-4 text-center items-center justify-center py-10">
        <div className="h-16 w-16 bg-primary/10 border border-primary/20 rounded-2xl flex items-center justify-center mb-2 shadow-[0_0_30px_-5px_rgba(16,185,129,0.2)]">
          <Search className="h-8 w-8 text-primary" />
        </div>
        <h1 className="text-4xl font-heading font-extrabold text-white tracking-tight">Dossiê DeepSearch</h1>
        <p className="text-muted-foreground text-sm max-w-lg">
          Varredura profunda em +15 bases governamentais e privadas simultaneamente. Informe um CPF ou CNPJ para gerar o relatório de conformidade.
        </p>
      </section>

      {/* Search Input Form */}
      <form onSubmit={handleSearch} className="max-w-2xl mx-auto flex items-center gap-3 relative z-20">
         <div className="relative flex-1">
            <input 
              type="text" 
              value={doc}
              onChange={(e) => setDoc(e.target.value)}
              placeholder="Digite o CPF (11 dígitos) ou CNPJ (14 dígitos)..."
              autoFocus
              className="w-full bg-card border-2 border-border text-lg rounded-2xl pl-6 pr-6 py-4 focus:outline-none focus:ring-4 focus:ring-primary/20 focus:border-primary transition-all text-white placeholder:text-muted-foreground/60 shadow-xl"
            />
         </div>
         <button 
           type="submit"
           disabled={loading || !doc.trim()}
           className="bg-primary hover:bg-emerald-400 text-primary-foreground text-lg font-bold py-4 px-8 rounded-2xl transition-all shadow-[0_0_20px_-5px_rgba(16,185,129,0.4)] hover:shadow-[0_0_30px_-5px_rgba(16,185,129,0.6)] disabled:opacity-50 disabled:pointer-events-none flex items-center gap-2 border border-emerald-400/50"
         >
           {loading ? <Loader2 className="h-6 w-6 animate-spin" /> : "Auditar"}
         </button>
      </form>

      {/* Loading Skeleton */}
      {loading && (
        <div className="mt-16 space-y-8 animate-pulse max-w-4xl mx-auto">
          <div className="flex items-center justify-center gap-3 text-primary font-mono mb-8">
             <Loader2 className="h-5 w-5 animate-spin" />
             Consolidando bases: DataJud, IBAMA, MTE, SICOR...
          </div>
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-card border border-border rounded-2xl" />
            ))}
          </div>
          <div className="grid grid-cols-2 gap-6">
             <div className="h-64 bg-card border border-border rounded-2xl" />
             <div className="h-64 bg-card border border-border rounded-2xl" />
          </div>
        </div>
      )}

      {/* Results Matrix & Cards */}
      {results && !loading && (
        <div className="mt-16 space-y-8 animate-in slide-in-from-bottom-10 fade-in duration-700">
           
           {/* Risk Matrix Gauges */}
           <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="rounded-3xl bg-card border-2 border-rose-500/30 flex flex-col items-center justify-center p-6 relative overflow-hidden shadow-[0_0_40px_-10px_rgba(244,63,94,0.15)] col-span-1 md:col-span-2">
                 <div className="absolute inset-0 bg-gradient-to-b from-rose-500/5 to-transparent pointer-events-none" />
                 <h2 className="text-xl font-heading font-black text-rose-500 mb-2 relative z-10">MCR 2.9 / Risco Global</h2>
                 
                 {/* Recharts Semi-Donut (Gauge 0-1000) */}
                 <div className="relative w-full h-[140px] flex items-center justify-center mt-2">
                    <PieChart width={300} height={150}>
                       <Pie
                         data={[
                           { name: "Score", value: 245, color: "#ef4444" }, // Red
                           { name: "Rest", value: 755, color: "#232d28" }
                         ]}
                         cx="50%"
                         cy="100%"
                         startAngle={180}
                         endAngle={0}
                         innerRadius={80}
                         outerRadius={110}
                         dataKey="value"
                         stroke="none"
                         cornerRadius={4}
                       >
                         {
                           [
                             { name: "Score", value: 245, color: "#ef4444" }, 
                             { name: "Rest", value: 755, color: "#232d28" }
                           ].map((entry, index) => (
                             <Cell key={`cell-${index}`} fill={entry.color} />
                           ))
                         }
                       </Pie>
                    </PieChart>
                    <div className="absolute bottom-0 flex flex-col items-center justify-end pb-2">
                       <span className="text-[10px] text-muted-foreground font-mono font-bold tracking-widest uppercase">Score Agro</span>
                       <span className="text-5xl font-black font-heading text-white tracking-tighter">245</span>
                       <span className="text-xs text-rose-500 font-bold bg-rose-500/10 px-2 py-0.5 rounded mt-1">Risco Crítico</span>
                    </div>
                 </div>
              </div>

              <div className="p-6 rounded-3xl bg-card border border-border flex flex-col items-center text-center justify-center">
                 <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Socioambiental</span>
                 <h2 className="text-2xl font-heading font-bold text-rose-500 mt-2">ALTO</h2>
                 <span className="text-xs text-muted-foreground mt-2 bg-muted px-2 py-1 rounded">2 Embargos IBAMA</span>
              </div>
              <div className="p-6 rounded-3xl bg-card border border-border flex flex-col items-center text-center justify-center">
                 <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Jurídico</span>
                 <h2 className="text-2xl font-heading font-bold text-amber-500 mt-2">MÉDIO</h2>
                 <span className="text-xs text-muted-foreground mt-2 bg-muted px-2 py-1 rounded">12 Processos (DataJud)</span>
              </div>
           </div>

           {/* Detailed Sections */}
           <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Receita Federal */}
              <div className="p-6 rounded-2xl bg-card border border-border hover:border-border/80 transition-colors">
                 <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-500"><Building className="h-5 w-5" /></div>
                    <div>
                       <h3 className="font-heading font-bold text-lg leading-tight">Receita Federal (Base Oficial)</h3>
                       <p className="text-xs text-muted-foreground">Atualizado há 14 minutos via BrasilAPI</p>
                    </div>
                    <div className="ml-auto bg-emerald-500/10 text-emerald-500 text-xs font-bold px-2 py-1 rounded border border-emerald-500/20 flex items-center gap-1">
                      <CheckCircle2 className="h-3 w-3" /> ATIVA
                    </div>
                 </div>
                 <div className="space-y-3">
                   <div>
                     <span className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Razão Social</span>
                     <p className="text-sm font-medium text-white break-words">AGROPECUARIA EXEMPLO LTDA</p>
                   </div>
                   <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">CNAE Principal</span>
                        <p className="text-sm font-medium text-white mt-1">01.15-6-00 (Cultivo de Soja)</p>
                      </div>
                      <div>
                        <span className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Capital Social</span>
                        <p className="text-sm font-mono text-white mt-1">R$ 5.400.000,00</p>
                      </div>
                   </div>
                 </div>
              </div>

              {/* IBAMA */}
              <div className="p-6 rounded-2xl bg-card border-2 border-rose-500/30 shadow-[0_0_20px_-10px_rgba(244,63,94,0.1)]">
                 <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-rose-500/10 rounded-lg text-rose-500"><FileWarning className="h-5 w-5" /></div>
                    <div>
                       <h3 className="font-heading font-bold text-lg leading-tight">Ambiental (IBAMA / SIFISC)</h3>
                       <p className="text-xs text-muted-foreground">Processado no Data Lake AgroJus</p>
                    </div>
                 </div>
                 
                 <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-4 flex items-start gap-4 mb-4">
                    <ShieldAlert className="h-6 w-6 text-rose-500 flex-shrink-0 mt-1" />
                    <div>
                       <h4 className="text-sm font-bold text-rose-500">2 Embargos Ativos Identificados</h4>
                       <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                         A autuação nº 844392-D indica 140ha embargados em área de Reserva Legal. Impede a emissão de conformidade MCR 2.9 (Cód. Verde).
                       </p>
                    </div>
                 </div>
              </div>

              {/* MTE */}
              <div className="p-6 rounded-2xl bg-card border border-border">
                 <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-500"><Briefcase className="h-5 w-5" /></div>
                    <div>
                       <h3 className="font-heading font-bold text-lg leading-tight">Lista Suja MTE</h3>
                       <p className="text-xs text-muted-foreground">Trabalho Análogo à Escravidão</p>
                    </div>
                 </div>
                 <div className="flex items-center gap-3 p-4 bg-muted/30 rounded-xl border border-border/50">
                    <CheckCircle2 className="h-6 w-6 text-emerald-500" />
                    <div>
                       <h4 className="text-sm font-bold text-white">Nenhuma Ocorrência</h4>
                       <p className="text-xs text-muted-foreground mt-0.5">O CNPJ auditado não consta nos registros oficiais do Ministério do Trabalho.</p>
                    </div>
                 </div>
              </div>

              {/* SICOR */}
              <div className="p-6 rounded-2xl bg-card border border-border">
                 <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-primary/10 rounded-lg text-primary"><Landmark className="h-5 w-5" /></div>
                    <div>
                       <h3 className="font-heading font-bold text-lg leading-tight">Crédito Rural (BCB / SICOR)</h3>
                       <p className="text-xs text-muted-foreground">Últimos 24 meses</p>
                    </div>
                 </div>
                 <div className="space-y-4">
                    <div className="flex justify-between items-end border-b border-border/50 pb-3">
                       <div>
                          <p className="text-xs text-muted-foreground font-semibold">Banco do Brasil S.A.</p>
                          <p className="text-sm font-medium mt-0.5">Custeio Agrícola - Soja</p>
                       </div>
                       <p className="text-sm font-mono text-emerald-400">R$ 1.250.000</p>
                    </div>
                    <div className="flex justify-between items-end">
                       <div>
                          <p className="text-xs text-muted-foreground font-semibold">Banco Cooperativo Sicredi</p>
                          <p className="text-sm font-medium mt-0.5">Investimento - Máquinas</p>
                       </div>
                       <p className="text-sm font-mono text-emerald-400">R$ 840.500</p>
                    </div>
                 </div>
              </div>

           </div>

               {/* DataJud - Processos */}
               <div className="lg:col-span-2 p-6 rounded-2xl bg-card border border-border mt-4 shadow-[0_0_20px_-10px_rgba(255,255,255,0.05)]">
                 <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-500"><Scale className="h-5 w-5" /></div>
                    <div>
                       <h3 className="font-heading font-bold text-lg leading-tight">Tribunais de Justiça (DataJud / CNJ)</h3>
                       <p className="text-xs text-muted-foreground">Consulta Unificada em 88 Tribunais do Brasil</p>
                    </div>
                 </div>
                 
                 <div className="rounded-xl border border-border/50 overflow-hidden bg-black/20">
                    <table className="w-full text-left text-sm">
                       <thead className="bg-muted text-muted-foreground text-xs uppercase font-bold">
                          <tr>
                             <th className="px-4 py-3">Tribunal</th>
                             <th className="px-4 py-3">Classe</th>
                             <th className="px-4 py-3">Assunto</th>
                             <th className="px-4 py-3">Data</th>
                             <th className="px-4 py-3 text-right">Status</th>
                          </tr>
                       </thead>
                       <tbody className="divide-y divide-border/50 text-white">
                          {[
                             { court: "TJ-SP", class: "Execução de Título Extrajudicial", subject: "Cédula de Produto Rural (CPR)", date: "12/03/2026", status: "ATIVO" },
                             { court: "TRF-1", class: "Ação Civil Pública", subject: "Dano Ambiental Acumulado", date: "05/11/2025", status: "ATIVO" },
                             { court: "TJ-MT", class: "Recuperação Judicial", subject: "Agropecuária", date: "22/01/2024", status: "JULGADO" }
                          ].map((lawsuit, i) => (
                             <tr key={i} className="hover:bg-muted/30 transition-colors">
                                <td className="px-4 py-3 font-mono font-bold text-muted-foreground text-xs">{lawsuit.court}</td>
                                <td className="px-4 py-3 font-medium">{lawsuit.class}</td>
                                <td className="px-4 py-3 text-muted-foreground">{lawsuit.subject}</td>
                                <td className="px-4 py-3 font-mono text-xs">{lawsuit.date}</td>
                                <td className="px-4 py-3 text-right">
                                   <span className={`text-[10px] font-bold px-2 py-1 rounded border tracking-widest ${lawsuit.status === 'ATIVO' ? 'bg-rose-500/10 text-rose-500 border-rose-500/20' : 'bg-muted text-muted-foreground border-border'}`}>
                                      {lawsuit.status}
                                   </span>
                                </td>
                             </tr>
                          ))}
                       </tbody>
                    </table>
                 </div>
               </div>

           <div className="flex justify-center mt-8">
              <button className="text-sm font-bold bg-muted hover:bg-white/10 text-white border border-border px-6 py-3 rounded-xl transition-all flex items-center gap-2">
                 Ver Laudo Integral em Scroll <ChevronDown className="h-4 w-4" />
              </button>
           </div>
        </div>
      )}
    </div>
  );
}
