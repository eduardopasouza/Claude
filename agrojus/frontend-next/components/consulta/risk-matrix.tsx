import { cn } from "@/lib/utils";

interface RiskMatrixProps {
  overall: string;
  environmental: string;
  legal: string;
  labor: string;
  financial: string;
}

const RISK_COLORS: Record<string, string> = {
  low: "bg-risk-low/20 text-risk-low border-risk-low/30",
  medium: "bg-risk-medium/20 text-risk-medium border-risk-medium/30",
  high: "bg-risk-high/20 text-risk-high border-risk-high/30",
  critical: "bg-risk-critical/20 text-risk-critical border-risk-critical/30",
};

const CELLS: { label: string; key: keyof RiskMatrixProps }[] = [
  { label: "Geral", key: "overall" },
  { label: "Ambiental", key: "environmental" },
  { label: "Legal", key: "legal" },
  { label: "Trabalhista", key: "labor" },
  { label: "Financeiro", key: "financial" },
];

function getRiskClass(level: string): string {
  const normalized = level.toLowerCase();
  return RISK_COLORS[normalized] ?? RISK_COLORS["medium"];
}

export function RiskMatrix(props: RiskMatrixProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
      {CELLS.map(({ label, key }) => {
        const value = props[key];
        return (
          <div
            key={key}
            className={cn(
              "rounded-lg border p-4 text-center",
              getRiskClass(value)
            )}
          >
            <div className="text-xs uppercase tracking-wider opacity-80">
              {label}
            </div>
            <div className="text-lg font-display font-bold mt-1 uppercase">
              {value}
            </div>
          </div>
        );
      })}
    </div>
  );
}
