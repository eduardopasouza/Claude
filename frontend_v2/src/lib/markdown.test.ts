/**
 * Testes unit de src/lib/markdown.ts
 *
 * Funções puras, sem I/O — arquétipo do que é fácil de testar.
 * Template para outros utilitários que a gente venha a criar.
 */

import { describe, expect, it } from "vitest";
import { fillTemplate, markdownToHtml, escapeHtml } from "./markdown";

describe("fillTemplate", () => {
  it("substitui placeholder simples", () => {
    expect(fillTemplate("Sr. {{nome}}", { nome: "Eduardo" })).toBe("Sr. Eduardo");
  });

  it("substitui múltiplos placeholders", () => {
    expect(
      fillTemplate("{{saudacao}}, {{nome}}!", {
        saudacao: "Olá",
        nome: "Eduardo",
      }),
    ).toBe("Olá, Eduardo!");
  });

  it("mantém placeholder quando valor está ausente", () => {
    expect(fillTemplate("Sr. {{nome}}", {})).toBe("Sr. {{nome}}");
  });

  it("mantém placeholder quando valor é string vazia", () => {
    expect(fillTemplate("Sr. {{nome}}", { nome: "" })).toBe("Sr. {{nome}}");
  });

  it("mantém placeholder quando valor é só whitespace", () => {
    expect(fillTemplate("Sr. {{nome}}", { nome: "   " })).toBe("Sr. {{nome}}");
  });

  it("aceita espaços dentro das chaves", () => {
    expect(fillTemplate("Sr. {{ nome }}", { nome: "Eduardo" })).toBe(
      "Sr. Eduardo",
    );
  });

  it("aceita nomes com underscore, ponto e dígitos", () => {
    expect(
      fillTemplate("{{user_name}} · {{meta.id}} · {{valor_1}}", {
        user_name: "ana",
        "meta.id": "42",
        valor_1: "100",
      }),
    ).toBe("ana · 42 · 100");
  });

  it("string vazia retorna string vazia", () => {
    expect(fillTemplate("", { nome: "x" })).toBe("");
  });

  it("sem placeholder retorna input literal", () => {
    expect(fillTemplate("Nenhum placeholder aqui.", { nome: "x" })).toBe(
      "Nenhum placeholder aqui.",
    );
  });

  it("não expande placeholder inexistente no values", () => {
    expect(fillTemplate("{{a}} e {{b}}", { a: "ok" })).toBe("ok e {{b}}");
  });
});

describe("escapeHtml", () => {
  it("escapa & < > e aspas duplas", () => {
    expect(escapeHtml('<b class="x">A & B</b>')).toBe(
      "&lt;b class=&quot;x&quot;&gt;A &amp; B&lt;/b&gt;",
    );
  });

  it("string sem caracteres especiais passa intacta", () => {
    expect(escapeHtml("texto normal")).toBe("texto normal");
  });
});

describe("markdownToHtml", () => {
  it("string vazia retorna string vazia", () => {
    expect(markdownToHtml("")).toBe("");
  });

  it("parágrafo simples vira <p>", () => {
    expect(markdownToHtml("Olá mundo.")).toBe("<p>Olá mundo.</p>");
  });

  it("heading # vira <h1>", () => {
    expect(markdownToHtml("# Título")).toBe("<h1>Título</h1>");
  });

  it("heading ### vira <h3>", () => {
    expect(markdownToHtml("### Cláusula")).toBe("<h3>Cláusula</h3>");
  });

  it("negrito **x**", () => {
    expect(markdownToHtml("**forte**")).toBe("<p><strong>forte</strong></p>");
  });

  it("itálico *x*", () => {
    expect(markdownToHtml("*ênfase*")).toBe("<p><em>ênfase</em></p>");
  });

  it("code inline `x`", () => {
    expect(markdownToHtml("use `npm run dev`")).toBe(
      "<p>use <code>npm run dev</code></p>",
    );
  });

  it("lista não-ordenada com -", () => {
    expect(markdownToHtml("- a\n- b\n- c")).toBe(
      "<ul>\n<li>a</li>\n<li>b</li>\n<li>c</li>\n</ul>",
    );
  });

  it("lista não-ordenada com *", () => {
    expect(markdownToHtml("* a\n* b")).toBe(
      "<ul>\n<li>a</li>\n<li>b</li>\n</ul>",
    );
  });

  it("lista ordenada", () => {
    expect(markdownToHtml("1. um\n2. dois")).toBe(
      "<ol>\n<li>um</li>\n<li>dois</li>\n</ol>",
    );
  });

  it("parágrafos separados por linha em branco", () => {
    expect(markdownToHtml("A\n\nB")).toBe("<p>A</p>\n<p>B</p>");
  });

  it("heading seguido de parágrafo", () => {
    expect(markdownToHtml("# Título\n\nConteúdo.")).toBe(
      "<h1>Título</h1>\n<p>Conteúdo.</p>",
    );
  });

  it("escapa HTML no conteúdo", () => {
    expect(markdownToHtml("Use <script>alert(1)</script>")).toBe(
      "<p>Use &lt;script&gt;alert(1)&lt;/script&gt;</p>",
    );
  });

  it("placeholder não preenchido vira span destacado em âmbar", () => {
    const html = markdownToHtml("Sr. {{nome}}");
    expect(html).toContain("<span");
    expect(html).toContain("background:#3f2c0a");
    expect(html).toContain("{{nome}}");
  });

  it("placeholder já substituído (sem chaves) não cria span", () => {
    const html = markdownToHtml("Sr. Eduardo");
    expect(html).not.toContain("<span");
  });

  it("lista intercalada com parágrafo", () => {
    expect(markdownToHtml("Intro\n\n- a\n- b\n\nFim.")).toBe(
      "<p>Intro</p>\n<ul>\n<li>a</li>\n<li>b</li>\n</ul>\n<p>Fim.</p>",
    );
  });

  it("troca de lista ol → ul fecha e abre corretamente", () => {
    expect(markdownToHtml("1. um\n- dois")).toBe(
      "<ol>\n<li>um</li>\n</ol>\n<ul>\n<li>dois</li>\n</ul>",
    );
  });
});

describe("integração fillTemplate + markdownToHtml", () => {
  it("contrato com placeholder preenchido mostra valor sem destaque", () => {
    const template = "Sr. {{nome}}, **contrato** de arrendamento.";
    const preenchido = fillTemplate(template, { nome: "Eduardo" });
    const html = markdownToHtml(preenchido);
    expect(html).toBe("<p>Sr. Eduardo, <strong>contrato</strong> de arrendamento.</p>");
    expect(html).not.toContain("<span");
  });

  it("contrato com placeholder vazio mostra valor destacado em âmbar", () => {
    const template = "Sr. {{nome}}, **contrato** de arrendamento.";
    const preenchido = fillTemplate(template, {});
    const html = markdownToHtml(preenchido);
    expect(html).toContain("<span");
    expect(html).toContain("{{nome}}");
  });
});
