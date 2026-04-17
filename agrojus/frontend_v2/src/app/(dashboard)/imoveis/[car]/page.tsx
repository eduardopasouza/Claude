"use client";

import { useMemo, useState, use } from "react";
import useSWR from "swr";
import {
  Activity,
  Bell,
  BookOpen,
  Briefcase,
  Calculator,
  CheckSquare,
  CloudSun,
  Coins,
  FileText,
  Leaf,
  Scale,
  ShieldCheck,
  Truck,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";
import { PropertyHeader, type PropertyData } from "@/components/imovel/PropertyHeader";
import { TabNav, type TabId, type TabDef } from "@/components/imovel/TabNav";
import { VisaoGeralTab } from "@/components/imovel/tabs/VisaoGeralTab";
import { DossieTab } from "@/components/imovel/tabs/DossieTab";
import { HistoricoTab } from "@/components/imovel/tabs/HistoricoTab";
import { AgronomiaTab } from "@/components/imovel/tabs/AgronomiaTab";
import { ComplianceTab } from "@/components/imovel/tabs/ComplianceTab";
import { ClimaTab } from "@/components/imovel/tabs/ClimaTab";
import { JuridicoTab } from "@/components/imovel/tabs/JuridicoTab";

const TABS: TabDef[] = [
  { id: "visao", label: "Visão Geral", icon: Activity, implemented: true },
  { id: "compliance", label: "Compliance", icon: ShieldCheck, implemented: true },
  { id: "dossie", label: "Dossiê", icon: FileText, implemented: true },
  { id: "historico", label: "Histórico", icon: BookOpen, implemented: true },
  { id: "agronomia", label: "Agronomia", icon: Leaf, implemented: true },
  { id: "clima", label: "Clima", icon: CloudSun, implemented: true },
  { id: "juridico", label: "Jurídico", icon: Scale, implemented: true },
  { id: "valuation", label: "Valuation", icon: Calculator, implemented: false },
  { id: "logistica", label: "Logística", icon: Truck, implemented: false },
  { id: "credito", label: "Crédito", icon: Coins, implemented: false },
  { id: "monitoramento", label: "Monitoramento", icon: Bell, implemented: false },
  { id: "acoes", label: "Ações", icon: CheckSquare, implemented: false },
];

type SearchResult = {
  total: number;
  results: PropertyData[];
};

export default function ImovelDetalhePage(props: {
  params: Promise<{ car: string }>;
}) {
  const { car: carCodeRaw } = use(props.params);
  const carCode = decodeURIComponent(carCodeRaw);
  const [currentTab, setCurrentTab] = useState<TabId>("visao");

  // Busca dados básicos via /property/search?q=<car>
  const { data, error, isLoading } = useSWR<SearchResult>(
    `/property/search?q=${encodeURIComponent(carCode)}&page_size=1`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  const property = useMemo<PropertyData | null>(() => {
    if (!data?.results || data.results.length === 0) return null;
    return data.results[0];
  }, [data]);

  // Propriedade mínima para renderizar abas mesmo quando search falhar
  const effectiveProperty: PropertyData | null =
    property || (carCode ? { car_code: carCode } : null);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <PropertyHeader
        property={property}
        loading={isLoading}
        error={error ? "Erro ao carregar dados do imóvel" : undefined}
      />

      <TabNav tabs={TABS} current={currentTab} onChange={setCurrentTab} />

      <main>
        {effectiveProperty && currentTab === "visao" && (
          <VisaoGeralTab property={effectiveProperty} />
        )}
        {effectiveProperty && currentTab === "dossie" && (
          <DossieTab property={effectiveProperty} />
        )}
        {effectiveProperty && currentTab === "historico" && (
          <HistoricoTab property={effectiveProperty} />
        )}
        {effectiveProperty && currentTab === "agronomia" && (
          <AgronomiaTab property={effectiveProperty} />
        )}
        {effectiveProperty && currentTab === "compliance" && (
          <ComplianceTab property={effectiveProperty} />
        )}
        {effectiveProperty && currentTab === "clima" && (
          <ClimaTab property={effectiveProperty} />
        )}
        {effectiveProperty && currentTab === "juridico" && (
          <JuridicoTab property={effectiveProperty} />
        )}
        {effectiveProperty && !TABS.find((t) => t.id === currentTab)?.implemented && (
          <ComingSoon tabId={currentTab} />
        )}
      </main>
    </div>
  );
}

function ComingSoon({ tabId }: { tabId: TabId }) {
  const TAB_COPY: Partial<Record<TabId, string>> = {
    compliance:
      "Checklist MCR 2.9 + EUDR com 30 critérios auditáveis + score por eixo + geração de PDF.",
    clima:
      "Série histórica NASA POWER + estações INMET próximas + alertas CEMADEN.",
    valuation:
      "Valuation NBR 14.653-3 com método comparativo + dados CONAB/CEPEA + simulação.",
    logistica:
      "Distância a armazéns CONAB, frigoríficos SIF, portos ANTAQ e rodovias DNIT.",
    juridico:
      "Processos no DataJud + publicações DJEN + protestos + CNDT + quadro societário.",
    credito:
      "Crédito rural via SICOR (BCB) + histórico por linha de crédito + simulação PRONAMP/Pronaf.",
    monitoramento:
      "Webhooks para alertas em tempo real: MapBiomas, DETER, publicações e mudanças cadastrais.",
    acoes: "Gerar laudo PDF, minuta jurídica (Claude) e exportar GeoPackage.",
  };

  return (
    <div className="p-12 flex flex-col items-center justify-center text-center gap-3">
      <Briefcase className="w-10 h-10 text-slate-700" />
      <h3 className="text-slate-300 font-medium">Em construção</h3>
      <p className="text-sm text-slate-500 max-w-md">
        {TAB_COPY[tabId] || "Esta aba ainda não foi implementada."}
      </p>
    </div>
  );
}
