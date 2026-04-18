"use client";

/**
 * Aba Contratos do Hub Jurídico-Agro.
 *
 * Lista templates de contratos via GET /api/v1/juridico/contratos
 * e detalhe via GET /api/v1/juridico/contratos/{slug}.
 *
 * Renderiza o markdown em um modal e permite preencher os campos
 * declarados no template para gerar uma versão customizada.
 * O download em .docx acontece no cliente, a partir do markdown
 * preenchido (sem depender de endpoint no backend).
 */

import { useMemo, useState } from "react";
import useSWR from "swr";
import {
  Loader2,
  FileSignature,
  Search as SearchIcon,
  X,
  Download,
  AlertCircle,
  ClipboardCopy,
  Check,
  FileText,
  BookOpen,
} from "lucide-react";
import { swrFetcher } from "@/lib/api";
import { fillTemplate, markdownToHtml, escapeHtml } from "@/lib/markdown";

type ContratoResumo = {
  id: number;
  slug: string;
  titulo: string;
  categoria: string;
  subcategoria?: string;
  sinopse?: string;
  aplicacao?: string;
  publico_alvo?: string[];
  n_campos: number;
  n_legislacao: number;
  versao?: string;
};

type Campo = {
  nome: string;
  tipo?: string;
  descricao?: string;
  obrigatorio?: boolean;
  exemplo?: string;
};

type ContratoDetalhe = ContratoResumo & {
  texto_markdown: string;
  campos: Campo[];
  legislacao_referencia?: string[];
  cautelas?: string[];
};

const CATEGORIAS = [
  { value: "", label: "Todas as categorias" },
  { value: "exploracao_rural", label: "Exploração rural" },
  { value: "compra_venda", label: "Compra e venda" },
  { value: "servicos_rurais", label: "Serviços rurais" },
  { value: "integracao", label: "Integração" },
  { value: "fornecimento", label: "Fornecimento" },
  { value: "credito", label: "Crédito" },
  { value: "ambiental", label: "Ambiental" },
];

const PUBLICOS = [
  { value: "", label: "Todos os públicos" },
  { value: "advogado", label: "Advogado" },
  { value: "produtor", label: "Produtor rural" },
  { value: "comprador", label: "Comprador" },
  { value: "trading", label: "Trading" },
  { value: "investidor", label: "Investidor" },
  { value: "consultor", label: "Consultor" },
];

export function ContratosTab() {
  const [categoria, setCategoria] = useState("");
  const [publico, setPublico] = useState("");
  const [q, setQ] = useState("");
  const [activeSlug, setActiveSlug] = useState<string | null>(null);

  const endpoint = useMemo(() => {
    const params = new URLSearchParams();
    if (categoria) params.set("categoria", categoria);
    if (publico) params.set("publico", publico);
    if (q.trim()) params.set("q", q.trim());
    const qs = params.toString();
    return `/juridico/contratos${qs ? "?" + qs : ""}`;
  }, [categoria, publico, q]);

  const { data, error, isLoading } = useSWR<{
    total: number;
    contratos: ContratoResumo[];
  }>(endpoint, swrFetcher, { revalidateOnFocus: false });

  const contratos = data?.contratos ?? [];

  return (
    <div className="space-y-5">
      {/* Filtros */}
      <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm flex flex-wrap items-end gap-3">
        <div className="flex-1 min-w-[220px]">
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Buscar
          </label>
          <div className="mt-1 relative">
            <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="título, sinopse…"
              className="w-full bg-input/40 border border-border rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>
        <div>
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Categoria
          </label>
          <select
            value={categoria}
            onChange={(e) => setCategoria(e.target.value)}
            className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm"
          >
            {CATEGORIAS.map((c) => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Público
          </label>
          <select
            value={publico}
            onChange={(e) => setPublico(e.target.value)}
            className="mt-1 bg-input/40 border border-border rounded-lg px-3 py-2 text-sm"
          >
            {PUBLICOS.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </div>
        <div className="ml-auto text-xs text-muted-foreground font-mono">
          {data?.total ?? 0} contrato(s)
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm">
          Erro ao carregar contratos.
        </div>
      )}

      {isLoading ? (
        <div className="p-10 text-center text-muted-foreground flex items-center justify-center gap-3">
          <Loader2 className="h-4 w-4 animate-spin" /> Carregando contratos…
        </div>
      ) : contratos.length === 0 ? (
        <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
          <FileSignature className="h-10 w-10 mx-auto mb-4 text-muted-foreground/50" />
          <div className="text-sm font-medium">
            Nenhum contrato encontrado com esses filtros.
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {contratos.map((c) => (
            <ContratoCard
              key={c.slug}
              contrato={c}
              onOpen={() => setActiveSlug(c.slug)}
            />
          ))}
        </div>
      )}

      {activeSlug && (
        <ContratoModal
          slug={activeSlug}
          onClose={() => setActiveSlug(null)}
        />
      )}
    </div>
  );
}

function ContratoCard({
  contrato,
  onOpen,
}: {
  contrato: ContratoResumo;
  onOpen: () => void;
}) {
  return (
    <button
      onClick={onOpen}
      className="text-left p-4 rounded-2xl border border-border bg-card/30 hover:bg-card/60 hover:border-primary/30 transition-all group"
    >
      <div className="flex items-start gap-2 mb-2">
        <FileSignature className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
        <div className="min-w-0 flex-1">
          <h3 className="text-sm font-semibold text-foreground group-hover:text-primary transition line-clamp-2">
            {contrato.titulo}
          </h3>
          <div className="text-[10px] text-muted-foreground uppercase tracking-wider mt-0.5">
            {contrato.categoria.replace(/_/g, " ")}
            {contrato.subcategoria && ` · ${contrato.subcategoria}`}
          </div>
        </div>
      </div>
      {contrato.sinopse && (
        <p className="text-xs text-muted-foreground line-clamp-3 mb-3">
          {contrato.sinopse}
        </p>
      )}
      <div className="flex flex-wrap gap-1.5 mt-auto">
        {contrato.publico_alvo?.slice(0, 3).map((p) => (
          <span
            key={p}
            className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-muted/60 text-muted-foreground border border-border uppercase tracking-wider"
          >
            {p}
          </span>
        ))}
        <span className="ml-auto text-[10px] text-muted-foreground font-mono">
          {contrato.n_campos} campos · {contrato.n_legislacao} leis
        </span>
      </div>
    </button>
  );
}

function ContratoModal({
  slug,
  onClose,
}: {
  slug: string;
  onClose: () => void;
}) {
  const { data: contrato, isLoading, error } = useSWR<ContratoDetalhe>(
    `/juridico/contratos/${slug}`,
    swrFetcher,
    { revalidateOnFocus: false },
  );

  const [values, setValues] = useState<Record<string, string>>({});
  const [copied, setCopied] = useState(false);

  const previewMd = useMemo(() => {
    if (!contrato) return "";
    return fillTemplate(contrato.texto_markdown, values);
  }, [contrato, values]);

  async function copyFilled() {
    try {
      await navigator.clipboard.writeText(previewMd);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* ignore */
    }
  }

  function downloadDocx() {
    if (!contrato) return;
    // Geramos um HTML básico e salvamos com extensão .docx —
    // Word abre HTML renomeado sem problemas, e evitamos dependência extra.
    const html = markdownToHtml(previewMd);
    const docHtml = `
<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns="http://www.w3.org/TR/REC-html40"
      lang="pt-BR">
<head>
<meta charset="utf-8"/>
<title>${escapeHtml(contrato.titulo)}</title>
<style>
  body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.5; }
  h1 { font-size: 16pt; text-align: center; margin: 0 0 20pt; }
  h2 { font-size: 13pt; margin-top: 20pt; }
  h3 { font-size: 12pt; margin-top: 14pt; }
  p { margin: 0 0 10pt; text-align: justify; }
  ol, ul { margin: 0 0 10pt 20pt; }
  li { margin-bottom: 4pt; }
  table { border-collapse: collapse; }
  td, th { border: 1px solid #888; padding: 4pt 8pt; }
</style>
</head>
<body>
<h1>${escapeHtml(contrato.titulo)}</h1>
${html}
</body>
</html>`.trim();

    const blob = new Blob(["\ufeff", docHtml], {
      type: "application/msword;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${contrato.slug}.doc`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadMd() {
    if (!contrato) return;
    const blob = new Blob([`# ${contrato.titulo}\n\n${previewMd}`], {
      type: "text/markdown;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${contrato.slug}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div
      className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-background border border-border rounded-2xl w-full max-w-6xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl"
      >
        <header className="flex items-start gap-3 px-5 py-4 border-b border-border">
          <FileSignature className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
          <div className="min-w-0 flex-1">
            <h2 className="font-heading font-bold text-lg">
              {contrato?.titulo ?? "Carregando…"}
            </h2>
            {contrato && (
              <div className="text-xs text-muted-foreground mt-1">
                {contrato.categoria.replace(/_/g, " ")}
                {contrato.versao && ` · versão ${contrato.versao}`}
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-muted rounded-lg transition"
          >
            <X className="h-5 w-5" />
          </button>
        </header>

        {isLoading && (
          <div className="p-10 flex items-center justify-center gap-3 text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" /> Carregando contrato…
          </div>
        )}
        {error && (
          <div className="p-6 text-rose-300">Erro ao carregar contrato.</div>
        )}

        {contrato && (
          <div className="grid grid-cols-1 lg:grid-cols-[340px_1fr] flex-1 min-h-0">
            {/* Painel esquerdo: campos + metadados */}
            <aside className="border-r border-border p-4 overflow-y-auto">
              {contrato.sinopse && (
                <p className="text-xs text-muted-foreground mb-4 italic">
                  {contrato.sinopse}
                </p>
              )}

              {contrato.campos.length > 0 && (
                <div className="mb-5">
                  <h3 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-2">
                    Campos preenchíveis
                  </h3>
                  <div className="space-y-2">
                    {contrato.campos.map((c) => (
                      <label key={c.nome} className="flex flex-col gap-1">
                        <span className="text-[11px] font-medium text-foreground">
                          {c.descricao || c.nome}
                          {c.obrigatorio && (
                            <span className="text-rose-400 ml-1">*</span>
                          )}
                        </span>
                        <input
                          value={values[c.nome] ?? ""}
                          onChange={(e) =>
                            setValues((prev) => ({
                              ...prev,
                              [c.nome]: e.target.value,
                            }))
                          }
                          placeholder={c.exemplo ?? `{{${c.nome}}}`}
                          className="bg-input/40 border border-border rounded px-2 py-1.5 text-xs font-mono focus:outline-none focus:ring-1 focus:ring-primary"
                        />
                      </label>
                    ))}
                  </div>
                </div>
              )}

              {contrato.legislacao_referencia &&
                contrato.legislacao_referencia.length > 0 && (
                  <div className="mb-5">
                    <h3 className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-2 flex items-center gap-1">
                      <BookOpen className="h-3 w-3" />
                      Legislação de referência
                    </h3>
                    <ul className="space-y-1 text-[11px] text-muted-foreground">
                      {contrato.legislacao_referencia.map((l, i) => (
                        <li key={i}>• {l}</li>
                      ))}
                    </ul>
                  </div>
                )}

              {contrato.cautelas && contrato.cautelas.length > 0 && (
                <div>
                  <h3 className="text-[10px] uppercase tracking-wider text-amber-400 font-semibold mb-2 flex items-center gap-1">
                    <AlertCircle className="h-3 w-3" />
                    Cautelas
                  </h3>
                  <ul className="space-y-1 text-[11px] text-amber-200/80">
                    {contrato.cautelas.map((c, i) => (
                      <li key={i}>• {c}</li>
                    ))}
                  </ul>
                </div>
              )}
            </aside>

            {/* Preview + ações */}
            <section className="flex flex-col min-h-0">
              <div className="flex items-center gap-2 px-4 py-2 border-b border-border bg-muted/20">
                <button
                  onClick={downloadDocx}
                  className="px-3 py-1.5 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition text-xs font-semibold inline-flex items-center gap-1.5"
                >
                  <Download className="h-3.5 w-3.5" /> Baixar .doc
                </button>
                <button
                  onClick={downloadMd}
                  className="px-3 py-1.5 rounded-lg border border-border hover:bg-muted transition text-xs font-medium inline-flex items-center gap-1.5"
                >
                  <FileText className="h-3.5 w-3.5" /> .md
                </button>
                <button
                  onClick={copyFilled}
                  className="px-3 py-1.5 rounded-lg border border-border hover:bg-muted transition text-xs font-medium inline-flex items-center gap-1.5"
                >
                  {copied ? (
                    <>
                      <Check className="h-3.5 w-3.5 text-emerald-400" /> Copiado
                    </>
                  ) : (
                    <>
                      <ClipboardCopy className="h-3.5 w-3.5" /> Copiar
                    </>
                  )}
                </button>
                <div className="ml-auto text-[10px] text-muted-foreground font-mono">
                  {Object.keys(values).length}/{contrato.campos.length} campos preenchidos
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-5 prose-agrojus">
                <MarkdownPreview markdown={previewMd} />
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Preview — usa utilitários de src/lib/markdown.ts
// ---------------------------------------------------------------------------

function MarkdownPreview({ markdown }: { markdown: string }) {
  const html = useMemo(() => markdownToHtml(markdown), [markdown]);
  return (
    <div
      className="text-sm leading-relaxed text-foreground/90"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
