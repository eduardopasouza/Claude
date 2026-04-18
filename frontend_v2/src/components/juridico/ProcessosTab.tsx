"use client";

/**
 * Aba Processos do Hub Jurídico-Agro.
 *
 * Consulta consolidada por CPF/CNPJ usando o endpoint
 *   GET /api/v1/juridico/processos/{cpf_cnpj}/dossie
 * que retorna:
 *   - datajud_processos
 *   - djen_publicacoes
 *   - autos_ibama
 *   - ceis / cnep
 *   - lista_suja
 *   - sumario (totais)
 *   - risco_consolidado (BAIXO | MEDIO | ALTO | CRITICO)
 */

import { useState } from "react";
import useSWR from "swr";
import {
  Search as SearchIcon,
  Loader2,
  Gavel,
  FileText,
  AlertOctagon,
  ShieldAlert,
  ShieldX,
  ShieldCheck,
  Building2,
  AlertTriangle,
  Users,
  ExternalLink,
  Calendar,
  MapPin,
  Copy,
  Check,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";

type DatajudProcesso = {
  tipo: string;
  tribunal?: string;
  numero: string;
  objeto?: string;
  valor?: number;
  status?: string;
  data_distribuicao?: string;
  municipio?: string;
  uf?: string;
};

type DjenPublicacao = {
  numero_processo?: string;
  tribunal?: string;
  orgao?: string;
  tipo_comunicacao?: string;
  data?: string;
  texto?: string;
  link?: string;
};

type AutoIbama = {
  numero_auto: string;
  data?: string;
  uf?: string;
  municipio?: string;
  valor_auto?: number;
  status_debito?: string;
  desc_infracao?: string;
  enq_legal?: string;
};

type Sancao = {
  nome?: string;
  tipo_sancao?: string;
  valor_multa?: number;
  data_inicio?: string;
  data_fim?: string;
  orgao_sancionador?: string;
  processo?: string;
};

type ListaSuja = {
  alert_type?: string;
  description?: string;
  data?: string;
  raw_data?: Record<string, unknown>;
};

type DossieJuridico = {
  cpf_cnpj_mask: string;
  datajud_processos: DatajudProcesso[];
  djen_publicacoes: DjenPublicacao[];
  autos_ibama: AutoIbama[];
  ceis: Sancao[];
  cnep: Sancao[];
  lista_suja: ListaSuja[];
  sumario: {
    processos_datajud: number;
    djen_publicacoes: number;
    autos_ibama: number;
    valor_autos_ibama: number;
    ceis: number;
    cnep: number;
    lista_suja_mte: number;
    valor_processos: number;
  };
  risco_consolidado: "BAIXO" | "MEDIO" | "ALTO" | "CRITICO";
};

const RISCO_META: Record<
  DossieJuridico["risco_consolidado"],
  { color: string; label: string; icon: typeof ShieldCheck }
> = {
  BAIXO: {
    color: "bg-emerald-500/10 border-emerald-500/30 text-emerald-400",
    label: "Risco baixo",
    icon: ShieldCheck,
  },
  MEDIO: {
    color: "bg-amber-500/10 border-amber-500/30 text-amber-400",
    label: "Risco médio",
    icon: ShieldAlert,
  },
  ALTO: {
    color: "bg-orange-500/10 border-orange-500/30 text-orange-400",
    label: "Risco alto",
    icon: AlertOctagon,
  },
  CRITICO: {
    color: "bg-rose-500/10 border-rose-500/30 text-rose-400",
    label: "Risco crítico",
    icon: ShieldX,
  },
};

export function ProcessosTab() {
  const [input, setInput] = useState("");
  const [submitted, setSubmitted] = useState<string | null>(null);

  const endpoint = submitted
    ? `/juridico/processos/${encodeURIComponent(submitted)}/dossie`
    : null;

  const { data, error, isLoading } = useSWR<DossieJuridico>(
    endpoint,
    swrFetcher,
    { revalidateOnFocus: false, dedupingInterval: 60_000 },
  );

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const clean = input.replace(/\D/g, "");
    if (clean.length === 11 || clean.length === 14) {
      setSubmitted(clean);
    }
  }

  return (
    <div className="space-y-6">
      <form
        onSubmit={handleSearch}
        className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm flex flex-wrap items-end gap-3"
      >
        <div className="flex-1 min-w-[260px]">
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            CPF ou CNPJ da parte investigada
          </label>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Digite só números ou com máscara"
            className="mt-1 w-full bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <p className="mt-1 text-[11px] text-muted-foreground">
            Busca em 6 bases: DataJud, DJEN, autos IBAMA, CEIS, CNEP, Lista Suja.
          </p>
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="px-5 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition font-semibold text-sm disabled:opacity-40 disabled:cursor-not-allowed inline-flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Consultando…
            </>
          ) : (
            <>
              <SearchIcon className="h-4 w-4" /> Consultar dossiê
            </>
          )}
        </button>
      </form>

      {error && !isLoading && (
        <div className="p-6 rounded-2xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm">
          Erro ao consultar o dossiê. Verifique o documento informado.
        </div>
      )}

      {data && <DossieView data={data} />}

      {!submitted && !isLoading && <EmptyState />}
    </div>
  );
}

function DossieView({ data }: { data: DossieJuridico }) {
  const meta = RISCO_META[data.risco_consolidado];
  const RiscoIcon = meta.icon;

  return (
    <div className="space-y-5">
      {/* Banner de risco consolidado */}
      <section
        className={`p-5 rounded-2xl border flex items-start gap-4 ${meta.color}`}
      >
        <RiscoIcon className="h-9 w-9 flex-shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <div className="flex items-baseline gap-3 flex-wrap">
            <h2 className="font-bold text-lg">{meta.label}</h2>
            <span className="text-xs font-mono opacity-80">
              CPF/CNPJ {data.cpf_cnpj_mask}
            </span>
          </div>
          <p className="text-sm mt-2 opacity-90">
            {descreveRisco(data)}
          </p>
        </div>
      </section>

      {/* KPIs */}
      <section className="grid grid-cols-2 md:grid-cols-6 gap-3">
        <Kpi
          label="Processos DataJud"
          value={data.sumario.processos_datajud}
          icon={Gavel}
          color="text-sky-400"
        />
        <Kpi
          label="Publicações DJEN"
          value={data.sumario.djen_publicacoes}
          icon={FileText}
          color="text-indigo-400"
        />
        <Kpi
          label="Autos IBAMA"
          value={data.sumario.autos_ibama}
          icon={AlertOctagon}
          color="text-orange-400"
          subtitle={
            data.sumario.valor_autos_ibama > 0
              ? formatBRL(data.sumario.valor_autos_ibama)
              : undefined
          }
        />
        <Kpi
          label="CEIS (inidôneas)"
          value={data.sumario.ceis}
          icon={ShieldX}
          color="text-rose-400"
        />
        <Kpi
          label="CNEP"
          value={data.sumario.cnep}
          icon={ShieldAlert}
          color="text-amber-400"
        />
        <Kpi
          label="Lista Suja MTE"
          value={data.sumario.lista_suja_mte}
          icon={Users}
          color="text-red-400"
        />
      </section>

      {/* Seções */}
      <SectionDataJud processos={data.datajud_processos} />
      <SectionDjen publicacoes={data.djen_publicacoes} />
      <SectionIbama autos={data.autos_ibama} />
      <SectionCeisCnep
        title="CEIS · Cadastro de Empresas Inidôneas e Suspensas"
        icon={ShieldX}
        color="text-rose-400"
        items={data.ceis}
      />
      <SectionCeisCnep
        title="CNEP · Cadastro Nacional de Empresas Punidas"
        icon={ShieldAlert}
        color="text-amber-400"
        items={data.cnep}
      />
      <SectionListaSuja items={data.lista_suja} />
    </div>
  );
}

function descreveRisco(d: DossieJuridico): string {
  const bits: string[] = [];
  if (d.sumario.lista_suja_mte > 0)
    bits.push("Lista Suja do Trabalho Escravo (MTE)");
  if (d.sumario.ceis > 0) bits.push(`${d.sumario.ceis} sanção(ões) no CEIS`);
  if (d.sumario.cnep > 0) bits.push(`${d.sumario.cnep} sanção(ões) no CNEP`);
  if (d.sumario.autos_ibama >= 5)
    bits.push(`${d.sumario.autos_ibama} autos IBAMA`);
  else if (d.sumario.autos_ibama > 0)
    bits.push(`${d.sumario.autos_ibama} auto(s) IBAMA`);
  if (d.sumario.valor_autos_ibama > 500_000)
    bits.push(
      `multa ambiental total ${formatBRL(d.sumario.valor_autos_ibama)}`,
    );
  if (d.sumario.processos_datajud >= 10)
    bits.push(`${d.sumario.processos_datajud} processos judiciais`);

  if (bits.length === 0)
    return "Nenhum apontamento relevante nas bases consultadas.";
  return `Fatores detectados: ${bits.join("; ")}.`;
}

function Kpi({
  label,
  value,
  icon: Icon,
  color,
  subtitle,
}: {
  label: string;
  value: number;
  icon: typeof Gavel;
  color: string;
  subtitle?: string;
}) {
  return (
    <div className="p-3 rounded-2xl border border-border bg-card/50 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-1">
        <Icon className={`h-3.5 w-3.5 ${color}`} />
        <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
          {label}
        </div>
      </div>
      <div className={`font-heading font-bold text-xl ${color}`}>
        {value.toLocaleString("pt-BR")}
      </div>
      {subtitle && (
        <div className="text-[10px] text-muted-foreground font-mono mt-0.5">
          {subtitle}
        </div>
      )}
    </div>
  );
}

function SectionDataJud({ processos }: { processos: DatajudProcesso[] }) {
  if (processos.length === 0) return null;
  return (
    <SectionWrapper
      title="Processos no DataJud"
      icon={Gavel}
      count={processos.length}
    >
      <div className="space-y-2">
        {processos.map((p, i) => (
          <div
            key={`${p.numero}-${i}`}
            className="p-3 rounded-xl border border-border bg-card/30 hover:bg-card/60 transition"
          >
            <div className="flex flex-wrap items-center gap-2 text-xs mb-1">
              {p.tribunal && (
                <span className="font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                  {p.tribunal}
                </span>
              )}
              {p.tipo && (
                <span className="text-muted-foreground">{p.tipo}</span>
              )}
              {p.data_distribuicao && (
                <span className="ml-auto text-muted-foreground flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formatDate(p.data_distribuicao)}
                </span>
              )}
            </div>
            <div className="text-sm font-mono font-medium mb-1 flex items-center gap-2">
              {p.numero}
              <CopyButton text={p.numero} />
            </div>
            {p.objeto && (
              <div className="text-xs text-muted-foreground line-clamp-2">
                {p.objeto}
              </div>
            )}
            {(p.municipio || p.uf || p.valor || p.status) && (
              <div className="mt-2 flex flex-wrap items-center gap-3 text-[11px] text-muted-foreground">
                {(p.municipio || p.uf) && (
                  <span className="flex items-center gap-1">
                    <MapPin className="h-3 w-3" />
                    {[p.municipio, p.uf].filter(Boolean).join("/")}
                  </span>
                )}
                {p.status && <span>· {p.status}</span>}
                {p.valor != null && p.valor > 0 && (
                  <span className="font-mono tabular-nums">
                    · {formatBRL(p.valor)}
                  </span>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}

function SectionDjen({ publicacoes }: { publicacoes: DjenPublicacao[] }) {
  if (publicacoes.length === 0) return null;
  return (
    <SectionWrapper
      title="Publicações no DJEN"
      icon={FileText}
      count={publicacoes.length}
    >
      <div className="space-y-2">
        {publicacoes.map((p, i) => (
          <div
            key={i}
            className="p-3 rounded-xl border border-border bg-card/30"
          >
            <div className="flex flex-wrap items-center gap-2 text-xs mb-1">
              {p.tribunal && (
                <span className="font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20">
                  {p.tribunal}
                </span>
              )}
              {p.tipo_comunicacao && (
                <span className="text-muted-foreground">
                  {p.tipo_comunicacao}
                </span>
              )}
              {p.data && (
                <span className="ml-auto text-muted-foreground flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formatDate(p.data)}
                </span>
              )}
            </div>
            {p.numero_processo && (
              <div className="text-sm font-mono font-medium mb-1">
                {p.numero_processo}
              </div>
            )}
            {p.orgao && (
              <div className="text-[11px] text-muted-foreground mb-1">
                {p.orgao}
              </div>
            )}
            {p.texto && (
              <div className="text-xs text-muted-foreground line-clamp-3">
                {p.texto}
              </div>
            )}
            {p.link && (
              <a
                href={p.link}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-1.5 inline-flex items-center gap-1 text-[11px] text-primary hover:underline"
              >
                ver publicação <ExternalLink className="h-3 w-3" />
              </a>
            )}
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}

function SectionIbama({ autos }: { autos: AutoIbama[] }) {
  if (autos.length === 0) return null;
  return (
    <SectionWrapper
      title="Autos de infração IBAMA"
      icon={AlertOctagon}
      count={autos.length}
    >
      <div className="space-y-2">
        {autos.map((a, i) => (
          <div
            key={i}
            className="p-3 rounded-xl border border-orange-500/20 bg-orange-500/5"
          >
            <div className="flex flex-wrap items-center gap-2 text-xs mb-1">
              <span className="font-mono font-semibold text-orange-300">
                Auto {a.numero_auto}
              </span>
              {a.status_debito && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-200 border border-orange-500/30">
                  {a.status_debito}
                </span>
              )}
              {a.data && (
                <span className="ml-auto text-muted-foreground flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formatDate(a.data)}
                </span>
              )}
            </div>
            {a.desc_infracao && (
              <div className="text-sm text-foreground/90 mb-1">
                {a.desc_infracao}
              </div>
            )}
            <div className="mt-1.5 flex flex-wrap items-center gap-3 text-[11px] text-muted-foreground">
              {(a.municipio || a.uf) && (
                <span className="flex items-center gap-1">
                  <MapPin className="h-3 w-3" />
                  {[a.municipio, a.uf].filter(Boolean).join("/")}
                </span>
              )}
              {a.valor_auto != null && a.valor_auto > 0 && (
                <span className="font-mono tabular-nums text-orange-300">
                  · {formatBRL(a.valor_auto)}
                </span>
              )}
              {a.enq_legal && (
                <span className="italic">· {a.enq_legal}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}

function SectionCeisCnep({
  title,
  icon: Icon,
  color,
  items,
}: {
  title: string;
  icon: typeof ShieldX;
  color: string;
  items: Sancao[];
}) {
  if (items.length === 0) return null;
  return (
    <SectionWrapper title={title} icon={Icon} count={items.length} iconColor={color}>
      <div className="space-y-2">
        {items.map((it, i) => (
          <div
            key={i}
            className="p-3 rounded-xl border border-rose-500/20 bg-rose-500/5"
          >
            {it.nome && (
              <div className="text-sm font-medium mb-1">{it.nome}</div>
            )}
            <div className="flex flex-wrap gap-3 text-[11px] text-muted-foreground">
              {it.tipo_sancao && <span>Sanção: {it.tipo_sancao}</span>}
              {it.orgao_sancionador && <span>· {it.orgao_sancionador}</span>}
              {it.data_inicio && (
                <span>· início {formatDate(it.data_inicio)}</span>
              )}
              {it.data_fim && <span>· fim {formatDate(it.data_fim)}</span>}
              {it.processo && <span>· proc. {it.processo}</span>}
              {it.valor_multa != null && it.valor_multa > 0 && (
                <span className="font-mono tabular-nums">
                  · {formatBRL(it.valor_multa)}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}

function SectionListaSuja({ items }: { items: ListaSuja[] }) {
  if (items.length === 0) return null;
  return (
    <SectionWrapper
      title="Lista Suja do Trabalho Escravo (MTE)"
      icon={AlertTriangle}
      count={items.length}
      iconColor="text-red-400"
    >
      <div className="space-y-2">
        {items.map((it, i) => (
          <div
            key={i}
            className="p-3 rounded-xl border border-red-500/30 bg-red-500/10"
          >
            {it.alert_type && (
              <div className="text-[10px] uppercase tracking-wider text-red-300 font-semibold mb-1">
                {it.alert_type}
              </div>
            )}
            {it.description && (
              <div className="text-sm text-foreground/90">{it.description}</div>
            )}
            {it.data && (
              <div className="text-[11px] text-muted-foreground mt-1">
                Detectado em {formatDate(it.data)}
              </div>
            )}
          </div>
        ))}
      </div>
    </SectionWrapper>
  );
}

function SectionWrapper({
  title,
  icon: Icon,
  count,
  iconColor = "text-muted-foreground",
  children,
}: {
  title: string;
  icon: typeof Gavel;
  count: number;
  iconColor?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="p-4 rounded-2xl border border-border bg-card/30">
      <header className="flex items-center gap-2 mb-3">
        <Icon className={`h-4 w-4 ${iconColor}`} />
        <h3 className="text-sm font-semibold">{title}</h3>
        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
          {count}
        </span>
      </header>
      {children}
    </section>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text);
          setCopied(true);
          setTimeout(() => setCopied(false), 1500);
        } catch {
          /* ignore */
        }
      }}
      className="text-muted-foreground hover:text-foreground transition"
      title="Copiar"
    >
      {copied ? (
        <Check className="h-3 w-3 text-emerald-400" />
      ) : (
        <Copy className="h-3 w-3" />
      )}
    </button>
  );
}

function EmptyState() {
  return (
    <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
      <Building2 className="h-10 w-10 mx-auto mb-4 text-muted-foreground/50" />
      <div className="text-sm font-medium mb-2">
        Informe um CPF/CNPJ para gerar o dossiê jurídico consolidado.
      </div>
      <div className="text-xs max-w-md mx-auto">
        Consulta cruzada em 6 bases oficiais com classificação de risco
        automática. Útil para due diligence de vendedores, fornecedores,
        sócios ou para monitoramento de terceiros.
      </div>
    </div>
  );
}

function formatBRL(n: number): string {
  return n.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 0,
  });
}

function formatDate(s: string): string {
  try {
    return new Date(s).toLocaleDateString("pt-BR");
  } catch {
    return s;
  }
}
