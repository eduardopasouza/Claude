"""Exporta uma campanha completa para markdown narrativo.

Lê current_state.json, event_log.jsonl, consolidated_summaries.json
(opcional) e diplomatic_log/*.json (opcional), e produz um único
markdown com:

- Cabeçalho: campanha, datas, polity jogador.
- Resumos consolidados (em ordem).
- Eventos brutos posteriores ao último resumo (em ordem cronológica).
- Estado final: polities, relações diplomáticas envolvendo o
  jogador, regiões e batalhões.
- Apêndice: histórico diplomático bilateral por polity (se houver).

Uso:
    python -m simengine.scripts.export_campaign <save-dir> [output.md]

Sem o segundo argumento, escreve em <save-dir>/CAMPAIGN.md.
Exit 0 em sucesso, 1 em erro de I/O ou validação, 2 em uso incorreto.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import ValidationError

from simengine.schemas import (
    ConsolidatedSummary,
    DiplomaticRelation,
    Event,
    GameState,
)


def _read_state(save_dir: Path) -> GameState:
    return GameState.model_validate_json(
        (save_dir / "current_state.json").read_text(encoding="utf-8")
    )


def _read_summaries(save_dir: Path) -> list[ConsolidatedSummary]:
    path = save_dir / "consolidated_summaries.json"
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    return [ConsolidatedSummary.model_validate(item) for item in json.loads(raw)]


def _read_events(save_dir: Path) -> list[Event]:
    path = save_dir / "event_log.jsonl"
    if not path.exists():
        return []
    out: list[Event] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(Event.model_validate_json(line))
    return out


def _read_diplomatic_log(save_dir: Path) -> dict[str, list[dict]]:
    log_dir = save_dir / "diplomatic_log"
    if not log_dir.exists():
        return {}
    out: dict[str, list[dict]] = {}
    for path in sorted(log_dir.glob("*.json")):
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            continue
        out[path.stem] = json.loads(raw)
    return out


def render(
    save_dir_name: str,
    state: GameState,
    summaries: list[ConsolidatedSummary],
    events: list[Event],
    diplomatic_log: dict[str, list[dict]],
) -> str:
    lines: list[str] = []
    lines.append(f"# Campanha `{save_dir_name}`")
    lines.append("")
    lines.append(f"- **Polity do jogador:** {state.player_polity}")
    lines.append(f"- **Data atual in-game:** {state.current_date.isoformat()}")
    lines.append(f"- **Polities no mundo:** {len(state.polities)}")
    lines.append(f"- **Regiões mapeadas:** {len(state.regions)}")
    lines.append(f"- **Resumos consolidados:** {len(summaries)}")
    lines.append(f"- **Eventos no log bruto:** {len(events)}")
    lines.append("")

    if summaries:
        lines.append("## Resumos consolidados")
        lines.append("")
        for s in sorted(summaries, key=lambda x: x.period_start):
            lines.append(
                f"### {s.period_start.isoformat()} → {s.period_end.isoformat()}"
            )
            lines.append("")
            lines.append(s.state_changes_summary)
            lines.append("")
            if s.key_events:
                lines.append("**Eventos-chave:**")
                for k in s.key_events:
                    lines.append(f"- {k}")
                lines.append("")
            if s.emerging_tensions:
                lines.append("**Tensões emergentes:**")
                for t in s.emerging_tensions:
                    lines.append(f"- {t}")
                lines.append("")

    cutoff = max((s.period_end for s in summaries), default=None)
    raw_events = [
        e for e in events if cutoff is None or e.date > cutoff
    ]
    if raw_events:
        lines.append("## Eventos recentes (não consolidados)")
        lines.append("")
        for e in sorted(raw_events, key=lambda x: x.date):
            polities = (
                f" — polities: {', '.join(e.affected_polities)}"
                if e.affected_polities else ""
            )
            regions = (
                f" — regiões: {', '.join(e.affected_regions)}"
                if e.affected_regions else ""
            )
            lines.append(
                f"- **{e.date.isoformat()}** [{e.category}/{e.caused_by}] "
                f"{e.description}{polities}{regions}"
            )
        lines.append("")

    lines.append("## Estado final")
    lines.append("")
    lines.append("### Polities")
    lines.append("")
    for name, polity in sorted(state.polities.items()):
        marker = " (jogador)" if name == state.player_polity else ""
        lines.append(f"- **{name}**{marker}")
        lines.append(
            f"  - Governo: {polity.government_type} · líder: {polity.leader}"
        )
        lines.append(f"  - Capital: {polity.capital_region}")
        lines.append(
            f"  - Regiões: {len(polity.owned_regions)} · "
            f"batalhões: {len(polity.military_units)} · "
            f"doutrinas: {len(polity.doctrines)} · "
            f"tensões: {len(polity.internal_tensions)}"
        )
    lines.append("")

    player_relations = [
        r for r in state.diplomatic_relations.values()
        if state.player_polity in (r.polity_a, r.polity_b)
    ]
    if player_relations:
        lines.append("### Relações diplomáticas do jogador")
        lines.append("")
        for r in sorted(
            player_relations, key=lambda x: (x.polity_a, x.polity_b)
        ):
            other = r.polity_b if r.polity_a == state.player_polity else r.polity_a
            if r.polity_a == state.player_polity:
                player_to_other = r.opinion_a_to_b
                other_to_player = r.opinion_b_to_a
            else:
                player_to_other = r.opinion_b_to_a
                other_to_player = r.opinion_a_to_b
            lines.append(
                f"- **{other}** — status `{r.status}` · "
                f"opinião {state.player_polity}→{other} = {player_to_other:+d}, "
                f"{other}→{state.player_polity} = {other_to_player:+d}"
            )
        lines.append("")

    lines.append("### Regiões")
    lines.append("")
    for name, region in sorted(state.regions.items()):
        owner = region.owner or "—"
        lines.append(
            f"- **{name}** ({region.type}) · dono: {owner} · "
            f"pop ~{region.population_estimate_thousands}k · "
            f"{region.economic_profile}"
        )
    lines.append("")

    if diplomatic_log:
        lines.append("## Apêndice: histórico diplomático")
        lines.append("")
        for polity, entries in sorted(diplomatic_log.items()):
            lines.append(f"### {polity}")
            lines.append("")
            for entry in entries:
                date = entry.get("date", "?")
                msg_in = entry.get("message_in", "").strip()
                msg_out = entry.get("message_out", "").strip()
                lines.append(f"**{date}**")
                lines.append("")
                if msg_in:
                    lines.append(f"> Brasil: {msg_in}")
                    lines.append("")
                if msg_out:
                    lines.append(f"> {polity}: {msg_out}")
                    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) not in (1, 2):
        print(
            "uso: python -m simengine.scripts.export_campaign "
            "<save-dir> [output.md]",
            file=sys.stderr,
        )
        return 2

    save_dir = Path(argv[0])
    output = Path(argv[1]) if len(argv) == 2 else save_dir / "CAMPAIGN.md"

    if not save_dir.is_dir():
        print(f"save-dir não é diretório: {save_dir}", file=sys.stderr)
        return 1

    try:
        state = _read_state(save_dir)
        summaries = _read_summaries(save_dir)
        events = _read_events(save_dir)
        diplomatic_log = _read_diplomatic_log(save_dir)
    except FileNotFoundError as exc:
        print(f"arquivo não encontrado: {exc.filename}", file=sys.stderr)
        return 1
    except (ValidationError, json.JSONDecodeError) as exc:
        print(f"falha lendo campanha: {exc}", file=sys.stderr)
        return 1

    rendered = render(save_dir.name, state, summaries, events, diplomatic_log)
    output.write_text(rendered, encoding="utf-8")
    print(f"OK: campanha exportada para {output} ({len(rendered)} bytes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
