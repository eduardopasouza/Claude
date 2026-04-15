"use client";

import { Search, Bell, User } from "lucide-react";

export function TopBar() {
  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-border bg-background/60 backdrop-blur-lg sticky top-0 z-50">
      
      {/* OmniSearch Center */}
      <div className="flex-1 max-w-2xl mx-auto hidden md:flex items-center relative group">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
          <Search className="h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
        </div>
        <input
          type="text"
          placeholder="Busca Profunda (CAR, CPF, CNPJ, Coordenada)..."
          className="w-full bg-input/40 border border-border text-sm rounded-xl pl-10 pr-12 py-2.5 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-all placeholder:text-muted-foreground shadow-sm focus:shadow-[0_0_20px_-5px_rgba(16,185,129,0.15)] focus:bg-background"
        />
        <div className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none">
           <kbd className="hidden sm:inline-flex items-center gap-1 bg-muted border border-border rounded px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground font-mono">
             <span className="text-xs">⌘</span>K
           </kbd>
        </div>
      </div>
      
      {/* Right User Actions */}
      <div className="flex items-center gap-5 ml-auto">
         <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors hidden sm:block">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-primary border-2 border-background" />
         </button>
         
         <div className="flex items-center gap-3 pl-5 border-l border-border cursor-pointer group">
            <div className="flex flex-col items-end">
               <span className="text-sm font-medium leading-none">Usuário VIP</span>
               <span className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Enterprise</span>
            </div>
            <div className="h-9 w-9 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
               <User className="h-4 w-4 text-primary" />
            </div>
         </div>
      </div>
      
    </header>
  );
}
