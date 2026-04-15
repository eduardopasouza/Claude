"use client";

import { Newspaper, ExternalLink, Clock } from "lucide-react";

// Notícias curadas — futuro: scraper automático do agro
const NEWS = [
  {
    title: "Novo Marco Legal do Carbono é sancionado e abre mercado bilionário",
    source: "Valor Econômico",
    date: "11 abr 2026",
    url: "#",
    tag: "Legislação",
  },
  {
    title: "EUDR entra em vigor e impacta exportações de soja e café brasileiro",
    source: "Reuters Brasil",
    date: "10 abr 2026",
    url: "#",
    tag: "Compliance",
  },
  {
    title: "MapBiomas lança Coleção 10 com resolução de 10m para todo o Brasil",
    source: "MapBiomas",
    date: "09 abr 2026",
    url: "#",
    tag: "Dados",
  },
  {
    title: "BCB publica novas regras para MCR 2.9 sobre crédito rural e compliance ambiental",
    source: "Banco Central",
    date: "08 abr 2026",
    url: "#",
    tag: "MCR 2.9",
  },
  {
    title: "Lista Suja do trabalho escravo é atualizada com 187 novos nomes pelo MTE",
    source: "Portal Transparência",
    date: "07 abr 2026",
    url: "#",
    tag: "Trabalho",
  },
  {
    title: "IBAMA embarga 12 mil hectares em Mato Grosso por desmatamento ilegal",
    source: "G1 Agro",
    date: "06 abr 2026",
    url: "#",
    tag: "Ambiental",
  },
];

const TAG_COLORS: Record<string, string> = {
  Legislação: "bg-blue-500/20 text-blue-400",
  Compliance: "bg-risk-medium/20 text-risk-medium",
  Dados: "bg-agrojus-emerald/20 text-agrojus-emerald",
  "MCR 2.9": "bg-purple-500/20 text-purple-400",
  Trabalho: "bg-risk-critical/20 text-risk-critical",
  Ambiental: "bg-risk-high/20 text-risk-high",
};

export default function NoticiasPage() {
  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h2 className="text-2xl font-display font-bold flex items-center gap-2">
          <Newspaper className="text-agrojus-emerald" size={24} />
          Notícias e Inteligência
        </h2>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          Feed curado de notícias relevantes para compliance, legislação e mercado agrícola
        </p>
      </div>

      <div className="space-y-3">
        {NEWS.map((n, i) => (
          <article
            key={i}
            className="glass rounded-xl p-5 hover:bg-agrojus-elevated/50 transition-colors group cursor-pointer"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1.5">
                  <span
                    className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                      TAG_COLORS[n.tag] || "bg-agrojus-elevated text-[var(--muted-foreground)]"
                    }`}
                  >
                    {n.tag}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-foreground group-hover:text-agrojus-emerald transition-colors">
                  {n.title}
                </h3>
                <div className="flex items-center gap-3 mt-2 text-xs text-[var(--muted-foreground)]">
                  <span>{n.source}</span>
                  <span className="flex items-center gap-1">
                    <Clock size={10} />
                    {n.date}
                  </span>
                </div>
              </div>
              <ExternalLink
                size={14}
                className="text-[var(--muted-foreground)] group-hover:text-agrojus-emerald transition-colors shrink-0 mt-1"
              />
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
