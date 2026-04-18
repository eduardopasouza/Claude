"""
Gerador de minutas jurídicas via Claude API (Anthropic).

Recebe:
  - contexto do imóvel (dict com CAR, área, UF, overlaps, processos, etc.)
  - tipo_minuta: "notificacao_extrajudicial" | "peticao_inicial_anulacao_auto"
                 | "defesa_administrativa" | "contrarrazoes" | "livre"
  - observacoes opcionais do advogado

Retorna:
  - título, corpo (markdown), fundamentação, avisos
  - tokens_used, model

Se ANTHROPIC_API_KEY não estiver setada, devolve 501 com instrução.
"""

from __future__ import annotations

import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger("agrojus.minuta")


MINUTA_PROMPTS = {
    "notificacao_extrajudicial": (
        "Redija uma **notificação extrajudicial** civil na qualidade de advogado "
        "do proprietário do imóvel rural abaixo, solicitando providência ao "
        "destinatário em função das circunstâncias apresentadas. Use linguagem "
        "formal, terceira pessoa, fundamentada no Código Civil e no CPC quando "
        "aplicável. Inclua: qualificação (com campos em branco [NOME], [CPF] "
        "quando faltar dado), fatos, direito aplicável, requerimento, prazo "
        "de resposta (15 dias úteis). Final com local/data e assinatura."
    ),
    "peticao_inicial_anulacao_auto": (
        "Redija uma **petição inicial** para ação anulatória de auto de infração "
        "ambiental (IBAMA/órgão estadual). Estrutura ABNT: endereçamento, "
        "qualificação das partes, dos fatos, do direito (incluindo nulidades "
        "processuais se cabíveis), dos pedidos (tutela provisória se justificar), "
        "do valor da causa e das provas. Fundamente em Lei 9.605/98, Decreto "
        "6.514/08, CF/88, jurisprudência do STJ."
    ),
    "defesa_administrativa": (
        "Redija uma **defesa administrativa** contra auto de infração ambiental, "
        "dirigida à autoridade autuante. Estrutura: endereçamento, qualificação, "
        "tempestividade, preliminares (nulidades se cabíveis), mérito com "
        "contraprova dos fatos imputados, pedido de arquivamento ou conversão "
        "de multa em serviços ambientais quando aplicável (art. 140 Dec 6.514/08)."
    ),
    "contrarrazoes": (
        "Redija **contrarrazões** ao recurso interposto pela parte adversa, "
        "rebatendo os argumentos apresentados. Estrutura: endereçamento, breve "
        "síntese do recurso, dos fatos e do direito, preliminar (se cabível), "
        "do mérito, dos pedidos."
    ),
    "livre": (
        "Redija a peça jurídica conforme solicitado nas observações do advogado, "
        "usando linguagem formal e fundamentação legal sempre que possível."
    ),
}


def _render_context(ctx: dict) -> str:
    """Converte dict de contexto em bloco markdown para enviar ao Claude."""
    lines = ["## CONTEXTO DO IMÓVEL\n"]
    if ctx.get("car_code"):
        lines.append(f"- **Código CAR:** {ctx['car_code']}")
    if ctx.get("property_name"):
        lines.append(f"- **Nome:** {ctx['property_name']}")
    if ctx.get("municipality") or ctx.get("uf"):
        lines.append(f"- **Município/UF:** {ctx.get('municipality','')}/{ctx.get('uf','')}")
    if ctx.get("area_ha"):
        lines.append(f"- **Área:** {ctx['area_ha']} ha")
    if ctx.get("status"):
        lines.append(f"- **Status CAR:** {ctx['status']}")
    if ctx.get("owner_name") or ctx.get("owner_cpf_cnpj"):
        lines.append(f"- **Proprietário:** {ctx.get('owner_name','')} ({ctx.get('owner_cpf_cnpj','')})")

    overlaps = ctx.get("overlaps") or {}
    if overlaps:
        lines.append("\n### Sobreposições detectadas\n")
        for k, v in overlaps.items():
            if v:
                lines.append(f"- {k}: {v}")

    if ctx.get("compliance"):
        lines.append("\n### Compliance\n")
        c = ctx["compliance"]
        lines.append(f"- Score: {c.get('score','N/A')}/1000 — Risco {c.get('risk','N/A')}")

    if ctx.get("processos"):
        lines.append("\n### Processos vinculados\n")
        for p in (ctx["processos"] or [])[:10]:
            lines.append(f"- {p}")

    if ctx.get("extra"):
        lines.append("\n### Observações Adicionais\n")
        lines.append(str(ctx["extra"]))

    return "\n".join(lines)


def generate_minuta(
    tipo: str,
    property_context: dict,
    observacoes: Optional[str] = None,
    destinatario: Optional[str] = None,
) -> dict:
    """
    Gera minuta via Claude API. Síncrono (a API é rápida com streaming=False).
    Raises:
      RuntimeError com detalhe se a chave não estiver configurada ou SDK ausente.
    """
    if not settings.anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não configurada no backend/.env. "
            "Sem a chave, a geração de minutas via Claude não está disponível. "
            "Adicione ANTHROPIC_API_KEY=sk-ant-... ao .env e reinicie o container."
        )

    try:
        from anthropic import Anthropic
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "SDK `anthropic` não instalada. Rode: pip install anthropic>=0.45.0"
        ) from e

    client = Anthropic(api_key=settings.anthropic_api_key)

    role_prompt = MINUTA_PROMPTS.get(tipo, MINUTA_PROMPTS["livre"])

    system_message = (
        "Você é um redator jurídico sênior com 20 anos de experiência em direito "
        "agrário, ambiental e fundiário brasileiro. Escreve em português formal, "
        "cita legislação vigente (CF/88, Código Civil, CPC, Lei 9.605/98, Dec 6.514/08, "
        "Código Florestal Lei 12.651/12), jurisprudência do STJ e STF quando relevante. "
        "NUNCA inventa números de acórdãos ou ementas — use apenas aqueles que o usuário "
        "fornecer no contexto. Se precisar citar jurisprudência mas o contexto não traz, "
        "deixe lacuna marcada com [buscar precedente]. Retorne markdown limpo."
    )

    user_message = (
        f"{role_prompt}\n\n"
        f"{_render_context(property_context)}\n"
    )
    if destinatario:
        user_message += f"\n**Destinatário:** {destinatario}\n"
    if observacoes:
        user_message += f"\n### Observações do Advogado\n{observacoes}\n"

    user_message += (
        "\n---\n"
        "**Formato da saída:**\n"
        "1. Linha 1 = título da peça.\n"
        "2. Em seguida, o corpo completo em markdown pronto para revisão.\n"
        "3. Ao fim, seção `### Fundamentação Jurídica Mobilizada` listando os "
        "dispositivos citados.\n"
        "4. Seção `### Avisos para o Advogado` listando lacunas e itens que "
        "requerem verificação humana (ex: números de processo, datas específicas).\n"
    )

    message = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=4096,
        system=system_message,
        messages=[{"role": "user", "content": user_message}],
    )

    # Extrai texto
    text_blocks = [b.text for b in message.content if getattr(b, "type", "") == "text"]
    body = "\n\n".join(text_blocks).strip()

    # Heurística: primeira linha = título
    lines = body.splitlines()
    title = lines[0].lstrip("#").strip() if lines else "Minuta"

    return {
        "tipo": tipo,
        "title": title,
        "body_markdown": body,
        "model": message.model,
        "tokens_input": message.usage.input_tokens if message.usage else None,
        "tokens_output": message.usage.output_tokens if message.usage else None,
        "context_summary": _render_context(property_context),
    }
