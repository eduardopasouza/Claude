"use client";

import { DocInput } from "@/components/consulta/doc-input";
import { RiskMatrix } from "@/components/consulta/risk-matrix";
import { SourceBlock } from "@/components/consulta/source-block";
import { useConsulta } from "@/lib/hooks/use-consulta";

export default function ConsultaPage() {
  const { mutate, data, isPending, error } = useConsulta();

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-[family-name:var(--font-display)] font-bold">
          Consulta Unificada
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Auditoria completa em 6 fontes simultaneas para qualquer CPF ou CNPJ
        </p>
      </div>

      <DocInput onSubmit={(doc) => mutate(doc)} isLoading={isPending} />

      {error && (
        <div className="p-4 rounded-lg bg-risk-critical/10 border border-risk-critical/30 text-risk-critical text-sm">
          {error.message}
        </div>
      )}

      {data && (
        <div className="space-y-6">
          <RiskMatrix
            overall={data.risk_score?.overall || "—"}
            environmental={data.risk_score?.environmental || "—"}
            legal={data.risk_score?.legal || "—"}
            labor={data.risk_score?.labor || "—"}
            financial={data.risk_score?.financial || "—"}
          />

          <div className="space-y-3">
            <h3 className="text-lg font-[family-name:var(--font-display)] font-semibold">
              Fontes Consultadas
            </h3>
            {data.sources &&
              Object.entries(data.sources).map(([key, value]) => (
                <SourceBlock
                  key={key}
                  title={key
                    .replace(/_/g, " ")
                    .replace(/\b\w/g, (l) => l.toUpperCase())}
                  source={key}
                  data={value}
                  isReference={
                    (value as Record<string, unknown>)?.is_reference === true
                  }
                />
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
