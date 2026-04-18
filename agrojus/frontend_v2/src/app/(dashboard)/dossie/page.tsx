"use client";

/**
 * Dossiê Agrofundiário — renderização em tela cheia.
 *
 * Aceita input de 4 formas:
 *  1. Query string ?car=MA-... ou ?cpf=000...
 *  2. sessionStorage chave "agrojus:dossie_request" (usado quando vem de
 *     click em feature do mapa / AOI desenhada — passa a geometry completa)
 *  3. Formulário manual (se nada acima)
 *
 * Render: sumário lateral + seções rolando, com botão "Exportar PDF".
 */

import { useEffect, useMemo, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  FileText,
  MapPin,
  Scale,
  Sprout,
  ShieldCheck,
  Users,
  Coins,
  Truck,
  Zap,
  Calculator,
  Gavel,
  Leaf,
  AlertTriangle,
  Download,
  Loader2,
  Check,
  Building2,
  ChevronRight,
} from "lucide-react";
import { fetchWithAuth, API_URL } from "@/lib/api";

type DossieResult = {
  dossie_id: string;
  generated_at: string;
  title: string;
  persona: string;
  contexto: {
    input_type: string;
    car_code: string | null;
    cpf_cnpj_mask: string | null;
    area_ha: number | null;
    centroid: { lat: number; lon: number } | null;
    bbox: number[] | null;
    municipio: string | null;
    uf: string | null;
    bioma: string | null;
  };
  secoes: Record<string, Record<string, unknown>>;
  recomendacao: {
    persona: string;
    risk_level: string;
    overall_status: string;
    score: number;
    red_flags: string[];
    tips: string[];
  };
  errors: Record<string, string>;
  metadata: {
    generator: string;
    fontes: string[];
    caveats: string[];
  };
};

const SECTION_META: Record<string, { icon: typeof MapPin; label: string; color: string }> = {
  identificacao: { icon: MapPin, label: "Identificação Territorial", color: "text-emerald-400" },
  fundiario: { icon: Scale, label: "Situação Fundiária", color: "text-amber-400" },
  compliance: { icon: ShieldCheck, label: "Compliance MCR 2.9", color: "text-emerald-400" },
  ambiental: { icon: Sprout, label: "Situação Ambiental", color: "text-lime-400" },
  proprietario: { icon: Users, label: "Dossiê do Proprietário", color: "text-blue-400" },
  credito_rural: { icon: Coins, label: "Crédito Rural", color: "text-yellow-400" },
  mercado: { icon: Building2, label: "Mercado (UF)", color: "text-indigo-400" },
  logistica: { icon: Truck, label: "Logística", color: "text-slate-400" },
  energia: { icon: Zap, label: "Energia (ANEEL)", color: "text-orange-400" },
  valuation: { icon: Calculator, label: "Valuation", color: "text-emerald-400" },
  juridico: { icon: Gavel, label: "Situação Jurídica", color: "text-red-400" },
  agronomia: { icon: Leaf, label: "Agronomia", color: "text-green-400" },
};

export default function DossiePage() {
  return (
    <Suspense fallback={<div className="p-8 text-slate-400">Carregando…</div>}>
      <DossieInner />
    </Suspense>
  );
}

function DossieInner() {
  const searchParams = useSearchParams();
  const [result, setResult] = useState<DossieResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [activeSection, setActiveSection] = useState<string>("identificacao");

  // === Resolve entrada (query, session ou form) ===
  useEffect(() => {
    const car = searchParams.get("car");
    const cpf = searchParams.get("cpf");
    const persona = searchParams.get("persona") || "geral";
    const sessionKey = searchParams.get("sk");

    let body: Record<string, unknown> | null = null;

    if (sessionKey) {
      // veio do mapa via sessionStorage
      try {
        const raw = sessionStorage.getItem(`agrojus:dossie:${sessionKey}`);
        if (raw) body = JSON.parse(raw);
      } catch {
        /* ignore */
      }
    } else if (car) {
      body = { car_code: car, persona };
    } else if (cpf) {
      body = { cpf_cnpj: cpf, persona };
    }

    if (body) {
      run(body);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function run(body: Record<string, unknown>) {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchWithAuth("/dossie", {
        method: "POST",
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult((await res.json()) as DossieResult);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function downloadPdf() {
    if (!result) return;
    setPdfLoading(true);
    try {
      // Reusa o mesmo body
      const car = searchParams.get("car");
      const cpf = searchParams.get("cpf");
      const sessionKey = searchParams.get("sk");
      const persona = result.persona;

      let body: Record<string, unknown> = { persona };
      if (sessionKey) {
        const raw = sessionStorage.getItem(`agrojus:dossie:${sessionKey}`);
        if (raw) body = { ...JSON.parse(raw), persona };
      } else if (car) {
        body = { car_code: car, persona };
      } else if (cpf) {
        body = { cpf_cnpj: cpf, persona };
      }

      const res = await fetchWithAuth("/dossie/pdf", {
        method: "POST",
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await res.text());
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `dossie_${result.dossie_id}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert(String(e));
    } finally {
      setPdfLoading(false);
    }
  }

  // === Navegação ===
  const sections = useMemo(() => {
    if (!result) return [];
    return Object.keys(SECTION_META).filter((k) => result.secoes[k]);
  }, [result]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-slate-300">
        <div className="flex items-center gap-3">
          <Loader2 className="w-5 h-5 animate-spin text-emerald-400" />
          Gerando dossiê (consulta ~15 fontes paralelas)…
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 max-w-3xl mx-auto">
        <div className="p-4 bg-red-950/30 border border-red-900/40 rounded text-red-300">
          Erro: {error}
        </div>
      </div>
    );
  }

  if (!result) {
    return <DossieManualForm onSubmit={run} />;
  }

  const rec = result.recomendacao;
  const isBlocked = rec.overall_status === "blocked";
  const isRestricted = rec.overall_status === "restricted";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-slate-950/95 backdrop-blur border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
          <FileText className="w-6 h-6 text-emerald-400 flex-shrink-0" />
          <div className="min-w-0 flex-1">
            <h1 className="text-lg font-bold truncate">{result.title}</h1>
            <div className="text-xs text-slate-400 mt-0.5 flex items-center gap-3 flex-wrap">
              <span>
                {result.contexto.area_ha ? `${result.contexto.area_ha.toFixed(2)} ha` : "—"}
                {result.contexto.municipio && ` · ${result.contexto.municipio}/${result.contexto.uf}`}
              </span>
              {result.contexto.bioma && <span>· Bioma {result.contexto.bioma}</span>}
              <span>· Persona: <strong className="text-emerald-400">{rec.persona}</strong></span>
            </div>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <StatusBadge status={rec.overall_status} risk={rec.risk_level} score={rec.score} />
            <button
              onClick={downloadPdf}
              disabled={pdfLoading}
              className="inline-flex items-center gap-2 px-3 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-sm rounded-lg transition"
            >
              {pdfLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              PDF
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-6 grid grid-cols-12 gap-6">
        {/* Sidebar navegação */}
        <aside className="col-span-3 sticky top-24 self-start h-fit">
          <nav className="border border-slate-800 rounded-xl p-2 bg-slate-900/40">
            {sections.map((key) => {
              const meta = SECTION_META[key];
              const Icon = meta.icon;
              return (
                <a
                  key={key}
                  href={`#${key}`}
                  onClick={() => setActiveSection(key)}
                  className={`flex items-center gap-2 px-3 py-2 rounded text-sm transition ${
                    activeSection === key
                      ? "bg-emerald-950/40 text-emerald-300"
                      : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/50"
                  }`}
                >
                  <Icon className={`w-4 h-4 ${meta.color}`} />
                  <span className="truncate">{meta.label}</span>
                </a>
              );
            })}
          </nav>
        </aside>

        {/* Conteúdo */}
        <main className="col-span-9 space-y-6">
          {/* Sumário executivo */}
          <section
            className={`border rounded-xl p-5 ${
              isBlocked
                ? "border-red-500/40 bg-red-950/30"
                : isRestricted
                ? "border-amber-500/40 bg-amber-950/30"
                : "border-emerald-500/40 bg-emerald-950/20"
            }`}
          >
            <h2 className="font-bold text-lg mb-3 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Sumário executivo
            </h2>
            {rec.red_flags.length > 0 && (
              <div className="mb-4">
                <h3 className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2">
                  Pontos de atenção
                </h3>
                <ul className="space-y-1.5">
                  {rec.red_flags.map((f, i) => (
                    <li key={i} className="text-sm flex items-start gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 text-red-400 flex-shrink-0 mt-0.5" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {rec.tips.length > 0 && (
              <div>
                <h3 className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2">
                  Recomendação para {rec.persona}
                </h3>
                <ul className="space-y-1.5">
                  {rec.tips.map((t, i) => (
                    <li key={i} className="text-sm flex items-start gap-2">
                      <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {rec.red_flags.length === 0 && rec.tips.length === 0 && (
              <p className="text-sm text-slate-400">Sem apontamentos críticos identificados.</p>
            )}
          </section>

          {/* Seções */}
          {sections.map((key) => (
            <SectionCard key={key} id={key} data={result.secoes[key]} />
          ))}

          {/* Metadata */}
          <section className="border border-slate-800 rounded-xl p-5 bg-slate-900/20 text-xs text-slate-400 space-y-2">
            <h3 className="font-semibold text-slate-300 text-sm">Metadata do dossiê</h3>
            <div>
              <strong>ID:</strong> {result.dossie_id}
            </div>
            <div>
              <strong>Gerado em:</strong>{" "}
              {new Date(result.generated_at).toLocaleString("pt-BR")}
            </div>
            <div>
              <strong>Fontes consultadas:</strong> {result.metadata.fontes.join(" · ")}
            </div>
            <div className="mt-3 pt-3 border-t border-slate-800">
              {result.metadata.caveats.map((c, i) => (
                <p key={i} className="italic text-slate-500">• {c}</p>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

function StatusBadge({
  status,
  risk,
  score,
}: {
  status: string;
  risk: string;
  score: number;
}) {
  const color =
    status === "blocked"
      ? "bg-red-950/40 border-red-500/40 text-red-300"
      : status === "restricted"
      ? "bg-amber-950/30 border-amber-500/40 text-amber-300"
      : status === "indeterminate"
      ? "bg-slate-900 border-slate-700 text-slate-300"
      : "bg-emerald-950/30 border-emerald-500/40 text-emerald-300";

  return (
    <div className={`border rounded-lg px-3 py-1.5 text-xs ${color}`}>
      <div className="font-bold uppercase tracking-wider">{status}</div>
      <div className="opacity-80 font-mono text-[10px]">
        Score {score}/1000 · {risk}
      </div>
    </div>
  );
}

function SectionCard({ id, data }: { id: string; data: Record<string, unknown> }) {
  const meta = SECTION_META[id];
  if (!meta) return null;
  const Icon = meta.icon;

  const isEmpty =
    !data ||
    Object.keys(data).length === 0 ||
    (Object.keys(data).length === 1 && (data.note || data.error));

  return (
    <section id={id} className="border border-slate-800 rounded-xl bg-slate-900/20 scroll-mt-24">
      <header className="px-5 py-3 border-b border-slate-800 flex items-center gap-3">
        <Icon className={`w-5 h-5 ${meta.color}`} />
        <h2 className="font-semibold text-slate-100">{meta.label}</h2>
      </header>
      <div className="p-5">
        {data.error ? (
          <p className="text-sm text-red-400">{String(data.error)}</p>
        ) : data.note ? (
          <p className="text-sm text-slate-400 italic">{String(data.note)}</p>
        ) : isEmpty ? (
          <p className="text-sm text-slate-500">Nenhum dado coletado.</p>
        ) : id === "compliance" ? (
          <ComplianceSection data={data as any} />
        ) : (
          <KeyValueGrid data={data} />
        )}
      </div>
    </section>
  );
}

function ComplianceSection({ data }: { data: any }) {
  if (!data || !data.axis_scores) {
    return <KeyValueGrid data={data} />;
  }
  return (
    <div className="space-y-3">
      {data.summary && (
        <p className="text-sm text-slate-300 leading-relaxed">{data.summary}</p>
      )}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
        {data.axis_scores.map((a: any) => (
          <div key={a.axis} className="border border-slate-800 rounded p-2.5 bg-slate-950/40">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 font-semibold">
              {a.label}
            </div>
            <div className="text-xl font-bold mt-0.5 text-emerald-300">
              {a.weighted_score.toFixed(0)}%
            </div>
            <div className="text-[10px] text-slate-500">
              {a.passed}✓ · {a.failed}✗ · {a.pending}?
            </div>
          </div>
        ))}
      </div>
      {data.recommendation && (
        <p className="text-sm text-slate-400 pt-3 border-t border-slate-800">
          <strong className="text-slate-300">Recomendação:</strong> {data.recommendation}
        </p>
      )}
    </div>
  );
}

function KeyValueGrid({ data }: { data: Record<string, unknown> }) {
  const entries = Object.entries(data).filter(
    ([k, v]) => k !== "error" && k !== "note" && v !== null && v !== undefined && v !== "",
  );
  if (entries.length === 0) {
    return <p className="text-sm text-slate-500">Nenhum dado relevante.</p>;
  }
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {entries.map(([k, v]) => (
        <div key={k} className="border border-slate-800 rounded p-3 bg-slate-950/40">
          <div className="text-[10px] uppercase tracking-wider text-slate-500 font-semibold mb-1">
            {k.replace(/_/g, " ")}
          </div>
          <ValueRender value={v} />
        </div>
      ))}
    </div>
  );
}

function ValueRender({ value }: { value: unknown }) {
  if (value === null || value === undefined) return <span className="text-slate-500">—</span>;
  if (typeof value === "boolean") {
    return (
      <span className={value ? "text-emerald-400" : "text-red-400"}>
        {value ? "Sim" : "Não"}
      </span>
    );
  }
  if (typeof value === "number") {
    return <span className="text-sm font-mono tabular-nums">{value.toLocaleString("pt-BR")}</span>;
  }
  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="text-slate-500">vazio</span>;
    const isObjectList = typeof value[0] === "object";
    if (isObjectList) {
      return (
        <div className="space-y-1.5">
          <div className="text-xs text-slate-400 mb-1">{value.length} item(ns)</div>
          {value.slice(0, 5).map((item: any, i) => (
            <div key={i} className="text-xs bg-slate-900/80 rounded p-2 border border-slate-800">
              {Object.entries(item || {})
                .filter(([, vv]) => vv !== null)
                .slice(0, 4)
                .map(([kk, vv]) => (
                  <div key={kk}>
                    <span className="text-slate-500">{kk}:</span>{" "}
                    <span className="text-slate-200">{String(vv)}</span>
                  </div>
                ))}
            </div>
          ))}
          {value.length > 5 && (
            <div className="text-[10px] text-slate-500 italic">
              …e mais {value.length - 5} item(ns)
            </div>
          )}
        </div>
      );
    }
    return <span className="text-sm">{value.join(", ")}</span>;
  }
  if (typeof value === "object") {
    return (
      <div className="space-y-0.5 text-xs">
        {Object.entries(value as object)
          .slice(0, 8)
          .map(([k, v]) => (
            <div key={k}>
              <span className="text-slate-500">{k}:</span>{" "}
              <span className="text-slate-200">{String(v)}</span>
            </div>
          ))}
      </div>
    );
  }
  return <span className="text-sm">{String(value)}</span>;
}

// --------------------------------------------------------------------------
// Formulário manual
// --------------------------------------------------------------------------

function DossieManualForm({ onSubmit }: { onSubmit: (body: Record<string, unknown>) => void }) {
  const [car, setCar] = useState("");
  const [cpf, setCpf] = useState("");
  const [municipio, setMunicipio] = useState("");
  const [persona, setPersona] = useState("geral");

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-3 mb-2">
        <FileText className="w-7 h-7 text-emerald-400" />
        Dossiê Agrofundiário
      </h1>
      <p className="text-slate-400 text-sm mb-6">
        Relatório completo sobre uma área rural agregando ~15 fontes públicas
        (SICAR, SIGEF, FUNAI, ICMBio, IBAMA, INPE, MapBiomas, BCB, CGU, DataJud,
        Agrolink, ANEEL…). Informe um CAR, CPF/CNPJ ou clique numa camada do mapa.
      </p>

      <div className="space-y-3">
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">Código CAR</span>
          <input
            value={car}
            onChange={(e) => setCar(e.target.value)}
            placeholder="MA-2100055-0013026E975B48D9B4F045D7352A1CB9"
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 font-mono"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">CPF/CNPJ do proprietário</span>
          <input
            value={cpf}
            onChange={(e) => setCpf(e.target.value)}
            placeholder="000.000.000-00"
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 font-mono"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">Código IBGE do município</span>
          <input
            value={municipio}
            onChange={(e) => setMunicipio(e.target.value)}
            placeholder="2111300"
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 font-mono"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">Persona (foco do relatório)</span>
          <select
            value={persona}
            onChange={(e) => setPersona(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100"
          >
            <option value="geral">Geral</option>
            <option value="comprador">Comprador de imóvel rural</option>
            <option value="advogado">Advogado / Diligência jurídica</option>
            <option value="investidor">Investidor / Banco / Cooperativa</option>
            <option value="trading">Trading / Exportador (EUDR)</option>
            <option value="consultor">Consultor ambiental</option>
            <option value="produtor">Produtor rural</option>
          </select>
        </label>

        <button
          onClick={() => {
            const body: Record<string, unknown> = { persona };
            if (car) body.car_code = car;
            if (cpf) body.cpf_cnpj = cpf;
            if (municipio) body.municipio_ibge = municipio;
            onSubmit(body);
          }}
          disabled={!car && !cpf && !municipio}
          className="w-full mt-3 inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-sm font-semibold rounded-lg transition"
        >
          <ChevronRight className="w-4 h-4" />
          Gerar dossiê
        </button>
      </div>
    </div>
  );
}
