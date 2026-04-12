import { cn } from "@/lib/utils";

// Compatible with LucideIcon signature; works without lucide-react installed
type IconComponent = React.FC<React.SVGProps<SVGSVGElement>>;

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: IconComponent;
  trend?: "positive" | "negative" | "neutral";
}

const subtitleColor: Record<NonNullable<KpiCardProps["trend"]>, string> = {
  positive: "text-risk-low",
  negative: "text-risk-critical",
  neutral: "text-[var(--muted-foreground)]",
};

export function KpiCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend = "neutral",
}: KpiCardProps) {
  return (
    <div
      className={cn(
        "bg-agrojus-surface border border-[var(--border)] rounded-xl p-5",
        "flex items-start gap-4",
        "glow-hover transition-all duration-200"
      )}
    >
      {/* Icon */}
      <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-agrojus-emerald/10 flex items-center justify-center">
        <Icon className="w-5 h-5 text-agrojus-emerald" aria-hidden="true" />
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p className="text-xs uppercase tracking-wider text-[var(--muted-foreground)] font-medium mb-1">
          {title}
        </p>
        <p className="text-2xl font-display font-bold text-foreground leading-none">
          {value}
        </p>
        {subtitle && (
          <p className={cn("text-xs mt-1 truncate", subtitleColor[trend])}>
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}
