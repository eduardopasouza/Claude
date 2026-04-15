"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchWithAuth } from "@/lib/api";
import { Loader2, ShieldCheck } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("dev@agrojus.br"); // Usuário de teste
  const [password, setPassword] = useState("test123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetchWithAuth("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Credenciais inválidas ou serviço indisponível");
      }

      const data = await res.json();
      localStorage.setItem("agrojus_token", data.access_token);
      router.push("/");
      
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-black relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-emerald-700/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-sm p-8 bg-card/60 border border-border rounded-3xl shadow-[0_0_80px_-15px_rgba(16,185,129,0.1)] relative z-10 backdrop-blur-2xl">
        <div className="flex justify-center mb-6">
           <div className="w-16 h-16 bg-primary/10 border border-primary/30 flex items-center justify-center rounded-2xl shadow-[0_0_15px_-5px_rgba(16,185,129,0.5)]">
             <span className="text-4xl text-primary font-bold tracking-tighter">⚖</span>
           </div>
        </div>
        
        <div className="text-center mb-8">
           <h1 className="text-3xl font-heading font-black tracking-tight text-white uppercase">AgroJus<span className="text-primary">.</span></h1>
           <p className="text-muted-foreground text-[10px] uppercase tracking-widest font-mono mt-1 font-bold">Autenticação Segura</p>
        </div>

        {error && (
           <div className="p-3 mb-6 bg-rose-500/10 border border-rose-500/30 rounded-xl text-center text-xs font-semibold text-rose-500">
             {error}
           </div>
        )}

        <form onSubmit={handleLogin} className="space-y-5">
           <div className="space-y-1.5">
             <label className="text-[10px] uppercase tracking-wider font-bold text-muted-foreground pl-1">Credencial Operacional</label>
             <input 
               type="email"
               value={email}
               onChange={(e) => setEmail(e.target.value)}
               className="w-full bg-black/40 border border-border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all text-white font-mono text-sm"
               required
             />
           </div>
           
           <div className="space-y-1.5">
             <label className="text-[10px] uppercase tracking-wider font-bold text-muted-foreground pl-1">Chave de Criptologia</label>
             <input 
               type="password"
               value={password}
               onChange={(e) => setPassword(e.target.value)}
               className="w-full bg-black/40 border border-border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all text-white font-mono text-sm tracking-widest"
               required
             />
           </div>

           <button 
             type="submit" 
             disabled={loading}
             className="w-full mt-6 bg-primary hover:bg-emerald-400 text-primary-foreground font-bold py-4 rounded-xl shadow-[0_0_20px_-5px_rgba(16,185,129,0.3)] hover:shadow-[0_0_30px_-5px_rgba(16,185,129,0.5)] transition-all flex items-center justify-center gap-2"
           >
              {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <><ShieldCheck className="h-5 w-5" /> Iniciar Sessão</>}
           </button>
        </form>
      </div>

    </div>
  );
}
