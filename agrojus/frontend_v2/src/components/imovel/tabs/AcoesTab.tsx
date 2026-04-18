"use client";

import { useState } from "react";
import {
  CheckSquare,
  FileText,
  Download,
  Scale,
  Loader2,
  AlertCircle,
  Copy,
  ExternalLink,
} from "lucide-react";
import { fetchWithAuth, API_URL } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type MinutaTipo =
  | "notificacao_extrajudicial"
  | "peticao_inicial_anulacao_auto"
  | "defesa_administrativa"
  | "contrarrazoes"
  | "livre";

const TIPO_LABEL: Record<MinutaTipo, string> = {
  notificacao_extrajudicial: "Notificação extrajudicial",
  peticao_inicial_anulacao_auto: "Ação anulatória de auto de infração",
  defesa_administrativa: "Defesa administrativa (IBAMA)",
  contrarrazoes: "Contrarrazões a recurso",
  livre: "Peça livre (descreva nas observações)",
};

type MinutaResponse = {
  tipo: string;
  title: string;
  body_markdown: string;
  model: string;
  tokens_input: number | null;
  tokens_output: number | null;
};

export function AcoesTab({ property }: { property: PropertyData }) {
  return (
    <div className="p-6 space-y-6 max-w-5xl">
      <header>
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <CheckSquare className="w-5 h-5 text-emerald-400" />
          Ações do imóvel
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Exporte o dossiê em formatos oficiais ou gere uma minuta jurídica
          inicial com base em todos os dados coletados sobre o imóvel.
        </p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <ExportCard
          title="Laudo PDF"
          description="Relatório consolidado: identificação, sobreposições, crédito rural e avisos legais. Pronto para anexar a processo."
          filename={`laudo_${property.car_code}.pdf`}
          endpoint={`/property/${encodeURIComponent(property.car_code)}/laudo.pdf`}
          icon={FileText}
        />
        <ExportCard
          title="GeoJSON"
          description="Geometria do imóvel + overlaps. Compatível com QGIS, ArcGIS, Leaflet, Mapbox e ogr2ogr."
          filename={`${property.car_code}.geojson`}
          endpoint={`/property/${encodeURIComponent(property.car_code)}/export.geojson?overlaps=true`}
          icon={Download}
        />
        <ExportCard
          title="GeoPackage (.gpkg)"
          description="OGC GeoPackage SQLite — abre direto em QGIS com camadas separadas por tipo."
          filename={`${property.car_code}.gpkg`}
          endpoint={`/property/${encodeURIComponent(property.car_code)}/export.gpkg?overlaps=true`}
          icon={Download}
        />
        <ExportCard
          title="Shapefile (.shp.zip)"
          description="Shapefile ESRI zipado para uso em ArcGIS e software legado."
          filename={`${property.car_code}_shp.zip`}
          endpoint={`/property/${encodeURIComponent(property.car_code)}/export.shp.zip?overlaps=true`}
          icon={Download}
        />
      </section>

      <MinutaPanel property={property} />
    </div>
  );
}

// --------------------------------------------------------------------------
// Card de export (download)
// --------------------------------------------------------------------------

function ExportCard({
  title,
  description,
  filename,
  endpoint,
  icon: Icon,
}: {
  title: string;
  description: string;
  filename: string;
  endpoint: string;
  icon: typeof FileText;
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function download() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchWithAuth(endpoint);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border border-slate-800 bg-slate-900/20 rounded-xl p-4 flex flex-col">
      <div className="flex items-center gap-2 text-slate-100 font-medium mb-1.5">
        <Icon className="w-4 h-4 text-emerald-400" />
        {title}
      </div>
      <p className="text-xs text-slate-400 leading-relaxed flex-1 mb-3">
        {description}
      </p>
      {error && (
        <div className="text-[10px] text-red-300 mb-2 flex items-start gap-1">
          <AlertCircle className="w-3 h-3 flex-shrink-0 mt-0.5" />
          {error}
        </div>
      )}
      <button
        onClick={download}
        disabled={loading}
        className="w-full py-1.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm rounded-lg transition flex items-center justify-center gap-1.5"
      >
        {loading ? (
          <>
            <Loader2 className="w-3.5 h-3.5 animate-spin" /> Gerando…
          </>
        ) : (
          <>
            <Download className="w-3.5 h-3.5" /> Baixar
          </>
        )}
      </button>
    </div>
  );
}

// --------------------------------------------------------------------------
// Painel minuta Claude API
// --------------------------------------------------------------------------

function MinutaPanel({ property }: { property: PropertyData }) {
  const [tipo, setTipo] = useState<MinutaTipo>("notificacao_extrajudicial");
  const [destinatario, setDestinatario] = useState("");
  const [observacoes, setObservacoes] = useState("");
  const [processosText, setProcessosText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<MinutaResponse | null>(null);

  async function gerar() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const processos = processosText
        .split("\n")
        .map((s) => s.trim())
        .filter(Boolean);
      const res = await fetchWithAuth(
        `/property/${encodeURIComponent(property.car_code)}/minuta`,
        {
          method: "POST",
          body: JSON.stringify({
            tipo,
            destinatario: destinatario || null,
            observacoes: observacoes || null,
            processos: processos.length ? processos : null,
          }),
        }
      );
      if (!res.ok) {
        const body = await res.text();
        throw new Error(body);
      }
      setResult((await res.json()) as MinutaResponse);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="border border-slate-800 bg-slate-900/20 rounded-xl p-5 space-y-4">
      <header className="flex items-center gap-2">
        <Scale className="w-5 h-5 text-emerald-400" />
        <h3 className="font-semibold text-slate-100">Minuta jurídica (Claude)</h3>
      </header>
      <p className="text-xs text-slate-400">
        Monta uma minuta inicial em markdown combinando os dados reais do imóvel
        (CAR, overlaps, compliance) com o prompt específico do tipo escolhido.
        Nunca inventa números de precedentes — lacunas explícitas serão
        sinalizadas para verificação humana.
      </p>

      <div className="grid gap-3 sm:grid-cols-2">
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">Tipo da peça</span>
          <select
            value={tipo}
            onChange={(e) => setTipo(e.target.value as MinutaTipo)}
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100"
          >
            {(Object.keys(TIPO_LABEL) as MinutaTipo[]).map((k) => (
              <option key={k} value={k}>
                {TIPO_LABEL[k]}
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">Destinatário (opcional)</span>
          <input
            value={destinatario}
            onChange={(e) => setDestinatario(e.target.value)}
            placeholder="Sr. João Silva, CPF 123.456.789-00, residente em..."
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100"
          />
        </label>
      </div>

      <label className="flex flex-col gap-1">
        <span className="text-xs text-slate-400">Processos/autos relacionados (um por linha, opcional)</span>
        <textarea
          value={processosText}
          onChange={(e) => setProcessosText(e.target.value)}
          placeholder="0000123-45.2024.8.10.0001
Auto IBAMA nº 789456"
          rows={3}
          className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100 font-mono"
        />
      </label>

      <label className="flex flex-col gap-1">
        <span className="text-xs text-slate-400">
          Observações / contexto adicional (opcional)
        </span>
        <textarea
          value={observacoes}
          onChange={(e) => setObservacoes(e.target.value)}
          placeholder="Descreva fatos, pedidos específicos ou pontos que a minuta deve cobrir..."
          rows={4}
          className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100"
        />
      </label>

      {error && (
        <div className="p-3 bg-red-950/30 border border-red-900/40 rounded text-red-300 text-xs flex items-start gap-2">
          <AlertCircle className="w-3.5 h-3.5 flex-shrink-0 mt-0.5" />
          <div className="min-w-0 flex-1 break-words">{error}</div>
        </div>
      )}

      <div className="flex gap-2">
        <button
          onClick={gerar}
          disabled={loading}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm rounded-lg transition flex items-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" /> Redigindo (pode
              levar até 30s)…
            </>
          ) : (
            <>
              <Scale className="w-4 h-4" /> Gerar minuta
            </>
          )}
        </button>
      </div>

      {result && <MinutaResult result={result} />}
    </section>
  );
}

function MinutaResult({ result }: { result: MinutaResponse }) {
  const [copied, setCopied] = useState(false);

  function copy() {
    navigator.clipboard.writeText(result.body_markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function downloadMd() {
    const blob = new Blob([result.body_markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${result.title.replace(/[^\w]/g, "_").slice(0, 60)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="mt-4 border border-emerald-900/40 bg-emerald-950/10 rounded-xl overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-2.5 bg-emerald-950/20 border-b border-emerald-900/30">
        <Scale className="w-4 h-4 text-emerald-400" />
        <h4 className="text-sm font-medium text-emerald-300 flex-1 truncate">
          {result.title}
        </h4>
        <span className="text-[10px] text-slate-500">
          {result.tokens_output} tokens · {result.model}
        </span>
        <button
          onClick={copy}
          className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-slate-200 transition"
          title="Copiar markdown"
        >
          <Copy className="w-3.5 h-3.5" />
          {copied && (
            <span className="absolute text-[10px] mt-4 -ml-4 text-emerald-400">
              copiado!
            </span>
          )}
        </button>
        <button
          onClick={downloadMd}
          className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-slate-200 transition"
          title="Baixar .md"
        >
          <Download className="w-3.5 h-3.5" />
        </button>
      </div>
      <pre className="p-4 text-sm text-slate-200 whitespace-pre-wrap font-sans leading-relaxed max-h-[600px] overflow-auto">
        {result.body_markdown}
      </pre>
      <div className="px-4 py-2 border-t border-slate-800 text-[11px] text-slate-500 flex items-center gap-1.5">
        <ExternalLink className="w-3 h-3" />
        Revisão humana obrigatória antes de protocolo. Lacunas{" "}
        <code className="text-[10px] bg-slate-800 px-1 py-0.5 rounded">
          [buscar precedente]
        </code>{" "}
        devem ser preenchidas pelo advogado responsável.
      </div>
    </div>
  );
}
