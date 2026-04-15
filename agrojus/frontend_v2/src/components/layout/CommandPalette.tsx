"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";
import { Calculator, Calendar, CreditCard, Settings, Smile, User, Search, Map, FileText, Database } from "lucide-react";

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const runCommand = (command: () => void) => {
    setOpen(false);
    command();
  };

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="OmniSearch: Busque CPF, CAR, Município ou Função..." />
      <CommandList>
        <CommandEmpty>Nenhum resultado encontrado. Tente um formato válido de CPF/CNPJ.</CommandEmpty>
        <CommandGroup heading="Ações Rápidas">
          <CommandItem onSelect={() => runCommand(() => router.push("/consulta"))}>
            <FileText className="mr-2 h-4 w-4 text-emerald-500" />
            <span>Nova Due Diligence (DeepSearch)</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/mapa"))}>
            <Map className="mr-2 h-4 w-4 text-emerald-500" />
            <span>Abrir Mapa Operacional (GIS Engine)</span>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Consultas Frequentes (Mock)">
          <CommandItem onSelect={() => runCommand(() => router.push("/consulta?q=MA-2107357-12345"))}>
            <Search className="mr-2 h-4 w-4" />
            <span>CAR: MA-2107357-XXXX</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/consulta?q=88.452.111/0001-99"))}>
            <Search className="mr-2 h-4 w-4" />
            <span>CNPJ: 88.452.111/0001-99 (Agropecuária)</span>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Ações">
          <CommandItem onSelect={() => runCommand(() => router.push("/consulta"))}>
            <Search className="mr-2 h-4 w-4" />
            <span>Executar Nova Due Diligence Completa</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/login"))}>
            <User className="mr-2 h-4 w-4" />
            <span>Trocar Usuário Ativo</span>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
