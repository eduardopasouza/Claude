"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  Scale,
  FileSearch,
  FileSignature,
  Lightbulb,
  BookOpen,
  BellRing,
} from "lucide-react";
import { ProcessosTab } from "@/components/juridico/ProcessosTab";
import { ContratosTab } from "@/components/juridico/ContratosTab";
import { TesesTab } from "@/components/juridico/TesesTab";
import { LegislacaoTab } from "@/components/juridico/LegislacaoTab";
import { MonitoramentoTab } from "@/components/juridico/MonitoramentoTab";

type TabId = "processos" | "contratos" | "teses" | "legislacao" | "monitoramento";

const TABS: Array<{
  id: TabId;
  label: string;
  icon: typeof Scale;
  description: string;
}> = [
  {
    id: "processos",
    label: "Processos",
    icon: FileSearch,
    description:
      "Dossiê consolidado por CPF/CNPJ — DataJud + DJEN + autos IBAMA + CEIS + CNEP + Lista Suja",
  },
  {
    id: "contratos",
    label: "Contratos",
    icon: FileSignature,
    description: "Templates agro prontos para uso com campos preenchíveis",
  },
  {
    id: "teses",
    label: "Teses",
    icon: Lightbulb,
    description: "Teses de defesa com precedentes, legislação e próxima ação",
  },
  {
    id: "legislacao",
    label: "Legislação",
    icon: BookOpen,
    description: "Normas federais, estaduais e municipais aplicáveis ao agro",
  },
  {
    id: "monitoramento",
    label: "Monitoramento",
    icon: BellRing,
    description: "Acompanhamento contínuo de CPF/CNPJ — terceiros, vendedores, fornecedores",
  },
];

export default function JuridicoPage() {
  return (
    <Suspense
      fallback={
        <div className="p-8 text-center text-muted-foreground">Carregando…</div>
      }
    >
      <JuridicoContent />
    </Suspense>
  );
}

function JuridicoContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const initialTab = (searchParams.get("tab") as TabId) || "processos";
  const [currentTab, setCurrentTab] = useState<TabId>(
    TABS.some((t) => t.id === initialTab) ? initialTab : "processos",
  );

  function changeTab(id: TabId) {
    setCurrentTab(id);
    const params = new URLSearchParams(searchParams.toString());
    params.set("tab", id);
    router.replace(`/juridico?${params.toString()}`, { scroll: false });
  }

  const active = TABS.find((t) => t.id === currentTab)!;

  return (
    <div className="p-6 md:p-8 max-w-[1400px] mx-auto">
      <header className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Scale className="h-6 w-6 text-primary" />
          <h1 className="font-heading font-bold text-2xl md:text-3xl">
            Hub Jurídico-Agro
          </h1>
          <span className="text-[10px] font-mono px-2 py-1 rounded bg-primary/10 text-primary border border-primary/20 uppercase tracking-wider">
            Beta
          </span>
        </div>
        <p className="text-sm text-muted-foreground max-w-3xl">
          Plataforma unificada para consulta jurídica, gestão de contratos
          agrários, teses de defesa, legislação aplicável e monitoramento de
          terceiros. Para advogados, produtores, tradings, investidores e
          consultores.
        </p>
      </header>

      <nav className="border-b border-border mb-6 overflow-x-auto">
        <div className="flex gap-1 min-w-max">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = currentTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => changeTab(tab.id)}
                className={`
                  relative flex items-center gap-2 px-4 py-3 text-sm font-medium transition
                  whitespace-nowrap
                  ${
                    isActive
                      ? "text-primary"
                      : "text-muted-foreground hover:text-foreground"
                  }
                `}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
                {isActive && (
                  <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />
                )}
              </button>
            );
          })}
        </div>
      </nav>

      <div className="text-xs text-muted-foreground mb-5 italic">
        {active.description}
      </div>

      <div>
        {currentTab === "processos" && <ProcessosTab />}
        {currentTab === "contratos" && <ContratosTab />}
        {currentTab === "teses" && <TesesTab />}
        {currentTab === "legislacao" && <LegislacaoTab />}
        {currentTab === "monitoramento" && <MonitoramentoTab />}
      </div>
    </div>
  );
}
