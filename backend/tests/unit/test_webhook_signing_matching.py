"""
Testes unit das primitivas de dispatch de webhooks.

Funções sob teste:
  app.services.webhook_dispatcher._sign_payload(secret, payload_bytes) -> str
  app.services.webhook_dispatcher._matches(webhook, event_type, car, cpf) -> bool
  EVENT_TYPES constante

Importante: NÃO testa o POST HTTP — isso é contract test ou e2e.
"""

from __future__ import annotations

import hashlib
import hmac
from types import SimpleNamespace

import pytest

from app.services.webhook_dispatcher import (
    EVENT_TYPES,
    _matches,
    _sign_payload,
)


# ---------------------------------------------------------------------------
# _sign_payload
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSignPayload:
    def test_formato_do_header_e_sha256_hex(self):
        sig = _sign_payload("segredo", b'{"event": "test"}')
        assert sig.startswith("sha256=")
        hex_part = sig.removeprefix("sha256=")
        # SHA-256 tem 64 chars hex
        assert len(hex_part) == 64
        assert all(c in "0123456789abcdef" for c in hex_part)

    def test_assinatura_bate_com_hmac_sha256_independente(self):
        """Double-check: reimplementa o cálculo e compara."""
        secret = "meu-segredo-123"
        payload = b'{"hello": "world"}'

        sig = _sign_payload(secret, payload)

        expected = hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()
        assert sig == f"sha256={expected}"

    def test_payloads_diferentes_geram_assinaturas_diferentes(self):
        a = _sign_payload("s", b'{"a": 1}')
        b = _sign_payload("s", b'{"a": 2}')
        assert a != b

    def test_secrets_diferentes_geram_assinaturas_diferentes(self):
        a = _sign_payload("secret-1", b'{"a": 1}')
        b = _sign_payload("secret-2", b'{"a": 1}')
        assert a != b

    def test_mesmo_input_sempre_mesma_assinatura(self):
        """Determinístico."""
        a = _sign_payload("s", b'{"a": 1}')
        b = _sign_payload("s", b'{"a": 1}')
        assert a == b

    def test_secret_com_caracteres_unicode(self):
        sig = _sign_payload("çãõ-segredo", b"payload")
        assert sig.startswith("sha256=")


# ---------------------------------------------------------------------------
# _matches
# ---------------------------------------------------------------------------


def webhook(
    *,
    active: bool = True,
    event_types: list[str] | None = None,
    car_filter: str | None = None,
    cpf_cnpj_filter: str | None = None,
) -> SimpleNamespace:
    """Helper: cria um mock de webhook com os campos usados por _matches."""
    return SimpleNamespace(
        active=active,
        event_types=event_types or [],
        car_filter=car_filter,
        cpf_cnpj_filter=cpf_cnpj_filter,
    )


@pytest.mark.unit
class TestMatches:
    # --- active ---
    def test_webhook_inativo_nunca_da_match(self):
        w = webhook(active=False, event_types=["ibama_auto"])
        assert _matches(w, "ibama_auto", None, None) is False

    # --- event_types ---
    def test_event_em_lista_da_match(self):
        w = webhook(event_types=["ibama_auto", "ceis"])
        assert _matches(w, "ibama_auto", None, None) is True

    def test_event_fora_da_lista_nao_da_match(self):
        w = webhook(event_types=["ceis"])
        assert _matches(w, "ibama_auto", None, None) is False

    def test_wildcard_asterisco_da_match_em_qualquer_evento(self):
        w = webhook(event_types=["*"])
        assert _matches(w, "ibama_auto", None, None) is True
        assert _matches(w, "mapbiomas_alert", None, None) is True
        assert _matches(w, "evento_hipotetico_futuro", None, None) is True

    def test_lista_vazia_de_eventos_nunca_da_match(self):
        w = webhook(event_types=[])
        assert _matches(w, "ibama_auto", None, None) is False

    # --- car_filter ---
    def test_car_filter_bate_com_car_do_evento(self):
        w = webhook(event_types=["*"], car_filter="MA-2100055-ABC")
        assert _matches(w, "ibama_auto", "MA-2100055-ABC", None) is True

    def test_car_filter_nao_bate_com_outro_car(self):
        w = webhook(event_types=["*"], car_filter="MA-2100055-ABC")
        assert _matches(w, "ibama_auto", "SP-1234567-XYZ", None) is False

    def test_car_filter_sem_car_no_evento_passa(self):
        """Se webhook filtra por CAR mas o evento não tem CAR, não bloqueia."""
        w = webhook(event_types=["*"], car_filter="MA-2100055-ABC")
        assert _matches(w, "ibama_auto", None, None) is True

    # --- cpf_cnpj_filter ---
    def test_cpf_cnpj_filter_bate(self):
        w = webhook(event_types=["*"], cpf_cnpj_filter="11111111111")
        assert _matches(w, "ibama_auto", None, "11111111111") is True

    def test_cpf_cnpj_filter_ignora_formatacao(self):
        """Máscara no filter e doc limpo no evento — devem bater."""
        w = webhook(event_types=["*"], cpf_cnpj_filter="111.111.111-11")
        assert _matches(w, "ibama_auto", None, "11111111111") is True

    def test_cpf_cnpj_filter_nao_bate_com_outro_doc(self):
        w = webhook(event_types=["*"], cpf_cnpj_filter="11111111111")
        assert _matches(w, "ibama_auto", None, "22222222222") is False

    # --- combinações ---
    def test_filtros_combinados_exigem_todos_baterem(self):
        w = webhook(
            event_types=["ibama_auto"],
            car_filter="MA-2100055-ABC",
            cpf_cnpj_filter="11111111111",
        )
        # todos batem
        assert _matches(w, "ibama_auto", "MA-2100055-ABC", "11111111111") is True
        # event errado
        assert _matches(w, "ceis", "MA-2100055-ABC", "11111111111") is False
        # car errado
        assert _matches(w, "ibama_auto", "SP-1234567-XYZ", "11111111111") is False
        # cpf errado
        assert _matches(w, "ibama_auto", "MA-2100055-ABC", "22222222222") is False


# ---------------------------------------------------------------------------
# Constante EVENT_TYPES
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEventTypes:
    def test_contem_todos_eventos_suportados_pelo_hub(self):
        # Hub Jurídico espera que estes eventos existam como event types válidos
        for evt in ["ibama_auto", "mapbiomas_alert", "djen_publicacao"]:
            assert evt in EVENT_TYPES

    def test_sem_duplicatas(self):
        assert len(EVENT_TYPES) == len(set(EVENT_TYPES))

    def test_todos_em_snake_case(self):
        for evt in EVENT_TYPES:
            assert evt.islower()
            assert " " not in evt
            assert "-" not in evt
