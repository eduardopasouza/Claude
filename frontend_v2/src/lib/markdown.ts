/**
 * Utilitários puros de markdown usados no Hub Jurídico-Agro.
 *
 * Funções 100% determinísticas, sem I/O. Fáceis de testar.
 * Foi extraído de `components/juridico/ContratosTab.tsx` para permitir
 * reuso (minutas, PDF client-side, outros tabs) e teste em isolamento.
 */

/**
 * Substitui `{{placeholder}}` pelo valor correspondente em `values`.
 * Se o valor está vazio ou ausente, mantém o placeholder visível (com as chaves)
 * — isso é intencional: contrato com campo não preenchido deve continuar visível.
 *
 * @example
 *   fillTemplate("Sr. {{nome}}", { nome: "Eduardo" }) === "Sr. Eduardo"
 *   fillTemplate("Sr. {{nome}}", {}) === "Sr. {{nome}}"
 *   fillTemplate("Sr. {{nome}}", { nome: "   " }) === "Sr. {{nome}}"   // whitespace = vazio
 */
export function fillTemplate(
  md: string,
  values: Record<string, string>,
): string {
  if (!md) return "";
  return md.replace(/\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}/g, (_match, key: string) => {
    const v = values[key];
    if (v && v.trim()) return v;
    return `{{${key}}}`;
  });
}

/**
 * Renderizador markdown mínimo.
 * Cobre só o que contratos/minutas agro realmente usam:
 *   - headings (#, ##, ###, #### …)
 *   - listas ordenadas e não ordenadas
 *   - **negrito**, *itálico*, `code inline`
 *   - parágrafos
 *   - highlight de `{{placeholder}}` não preenchido (span âmbar)
 *
 * Deliberadamente NÃO cobre: tabelas, links, blockquote, imagens, code fence.
 * Se precisar, migra pra `marked` ou `markdown-it` — mas hoje são ~60 linhas
 * controladas e zero dependência.
 */
export function markdownToHtml(md: string): string {
  if (!md) return "";
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const out: string[] = [];
  let inList: "ul" | "ol" | null = null;
  let paraBuf: string[] = [];

  function flushPara() {
    if (paraBuf.length) {
      out.push(`<p>${formatInline(paraBuf.join(" ").trim())}</p>`);
      paraBuf = [];
    }
  }
  function closeList() {
    if (inList) {
      out.push(`</${inList}>`);
      inList = null;
    }
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    if (!line.trim()) {
      flushPara();
      closeList();
      continue;
    }
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      flushPara();
      closeList();
      const level = h[1].length;
      out.push(`<h${level}>${formatInline(h[2])}</h${level}>`);
      continue;
    }
    const ol = line.match(/^\s*(\d+)\.\s+(.*)$/);
    const ul = line.match(/^\s*[-*]\s+(.*)$/);
    if (ol) {
      flushPara();
      if (inList !== "ol") {
        closeList();
        out.push("<ol>");
        inList = "ol";
      }
      out.push(`<li>${formatInline(ol[2])}</li>`);
      continue;
    }
    if (ul) {
      flushPara();
      if (inList !== "ul") {
        closeList();
        out.push("<ul>");
        inList = "ul";
      }
      out.push(`<li>${formatInline(ul[1])}</li>`);
      continue;
    }
    closeList();
    paraBuf.push(line);
  }
  flushPara();
  closeList();
  return out.join("\n");
}

function formatInline(s: string): string {
  let t = escapeHtml(s);
  t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  t = t.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
  t = t.replace(
    /\{\{([^}]+)\}\}/g,
    '<span style="background:#3f2c0a;color:#f5c678;padding:1px 4px;border-radius:3px;font-family:monospace;font-size:0.9em;">{{$1}}</span>',
  );
  return t;
}

export function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
