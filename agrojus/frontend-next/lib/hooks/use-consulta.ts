"use client";

import { useMutation } from "@tanstack/react-query";
import { apiPost } from "@/lib/api";

export interface ConsultaResult {
  cpf_cnpj: string;
  risk_score: {
    overall: string;
    environmental: string;
    legal: string;
    labor: string;
    financial: string;
  };
  sources: Record<string, unknown>;
}

export function useConsulta() {
  return useMutation({
    mutationFn: async (cpf_cnpj: string): Promise<ConsultaResult> => {
      const res = await apiPost<ConsultaResult>("/api/v1/consulta/completa", {
        cpf_cnpj,
      });
      if (res.error) {
        throw new Error(res.error);
      }
      return res.data!;
    },
  });
}
