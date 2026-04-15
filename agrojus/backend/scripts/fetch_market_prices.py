"""
fetch_market_prices.py — Coletor diário de cotações agrícolas
Fontes:
  1. Yahoo Finance API (futuros CBOT/CME em USD) — sem autenticação, sem scraping JS
  2. HG Brasil Finance API (câmbio USD/BRL em tempo real)
Resultado: insere/atualiza tabela `market_quotes` com preços em BRL e USD.
Execução diária recomendada via cron: 09h e 18h (horário de Brasília).
"""
import httpx
import datetime
import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
Base = declarative_base()
TODAY = datetime.date.today()

# ──────────────────────────────────────────────────────────────────────────────
# Mapeamento: nome interno → ticker Yahoo Finance
# Fonte: Chicago Board of Trade (CBOT) / CME
# Unidade original do ticker indicada para conversão correta
# ──────────────────────────────────────────────────────────────────────────────
COMMODITIES = [
    # (produto, ticker_yahoo, unidade_original, fator_conversao)
    # ──────────────────────────────────────────────────────────
    # Soja CBOT: USX/bushel (1 bu = 27.2 kg → fator = 60/27.2 = 2.2059 sacas 60kg/bu)
    # price_brl = (USX / 100) * usd_brl * (60/27.2)
    ("Soja CBOT (R$/sc 60kg)",   "ZS=F", "USX/bu",  60/27.2  ),
    # Milho CBOT: USX/bushel (1 bu milho = 25.4 kg → 60/25.4 = 2.362 sacas/bu)
    ("Milho CBOT (R$/sc 60kg)",  "ZC=F", "USX/bu",  60/25.4  ),
    # Trigo CBOT: USX/bushel (1 bu = 27.2 kg → 60/27.2 = 2.2059)
    ("Trigo CBOT (R$/sc 60kg)",  "ZW=F", "USX/bu",  60/27.2  ),
    # Algodão ICE: USX/lb  (1 arroba = 15 kg = 33.069 lbs → fator = 33.069)
    ("Algodão ICE (R$/@)",       "CT=F", "USX/lb",  33.069   ),
    # Café Arábica NY: USX/lb (saca 60 kg = 132.277 lbs → fator = 132.277)
    ("Café Arábica NY (R$/sc)",  "KC=F", "USX/lb",  132.277  ),
    # Açúcar bruto ICE: USX/lb (saca 50 kg = 110.231 lbs → fator = 110.231)
    ("Açúcar NY (R$/sc 50kg)",   "SB=F", "USX/lb",  110.231  ),
    # Boi Gordo CME: USD/cwt (1 cwt = 45.359 kg; 1 arroba = 15 kg = 0.3307 cwt)
    # price_brl = USD/cwt * usd_brl * (15/45.359)
    ("Boi Gordo CME (R$/@)",     "LE=F", "USD/cwt", 15/45.359),
    # Cacau ICE: USD/ton → R$/ton (fator = 1, já na mesma unidade por tonelada)
    ("Cacau ICE (R$/ton)",       "CC=F", "USD/ton", 1.0      ),
    # Suco de Laranja FCOJ: USX/lb (cx 40.8 kg = 89.949 lbs → fator = 89.949)
    ("Laranja FCOJ (R$/cx)",     "OJ=F", "USX/lb",  89.949   ),
    # Petróleo WTI: USD/barril (energia, referência fertilizantes)
    ("Petróleo WTI (USD/bbl)",   "CL=F", "USD/bbl", None     ),  # mantém em USD
]

YAHOO_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"
YAHOO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


class MarketQuote(Base):
    __tablename__ = "market_quotes"
    id         = Column(Integer, primary_key=True)
    date       = Column(Date,    nullable=False)
    product    = Column(String,  nullable=False)
    index_name = Column(String,  nullable=False)
    price_brl  = Column(Float,   nullable=False)
    price_usd  = Column(Float,   nullable=True)


def setup_db():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def fetch_usd_brl(client: httpx.Client) -> float:
    """Cotação USD/BRL atual via HG Brasil (API pública, sem chave)."""
    try:
        r = client.get(
            "https://api.hgbrasil.com/finance?format=json&key=free",
            timeout=15
        )
        rate = r.json()["results"]["currencies"]["USD"]["buy"]
        logger.info("USD/BRL atual: %.4f", rate)
        return float(rate)
    except Exception as exc:
        logger.warning("Câmbio não obtido (usando fallback 5.0): %s", exc)
        return 5.0   # fallback razoável


def fetch_yahoo_quote(client: httpx.Client, ticker: str) -> float | None:
    """Retorna o último preço de fechamento de um ticker Yahoo Finance."""
    try:
        url = f"{YAHOO_BASE}/{ticker}?interval=1d&range=2d"
        r = client.get(url, timeout=15)
        r.raise_for_status()
        result = r.json()["chart"]["result"][0]
        meta   = result["meta"]
        price  = meta.get("regularMarketPrice") or meta.get("previousClose")
        return float(price) if price else None
    except Exception as exc:
        logger.error("Erro Yahoo Finance [%s]: %s", ticker, exc)
        return None


def to_brl(raw_price: float, unit: str, factor: float, usd_brl: float) -> float:
    """Converte preço bruto para BRL/unidade-BR conforme unidade original."""
    if unit in ("USX/bu", "USX/lb"):
        # USX = centavos de USD → divide por 100 → USD, depois * usd_brl * fator
        return (raw_price / 100) * usd_brl * factor
    elif unit in ("USD/cwt", "USD/bbl", "USD/ton"):
        return raw_price * usd_brl * factor
    return raw_price   # já em BRL ou desconhecido


def main():
    logger.info("=== Coletor de Cotações Agrícolas — %s ===", TODAY)
    session = setup_db()
    all_quotes = []

    with httpx.Client(headers=YAHOO_HEADERS, verify=False, follow_redirects=True) as client:
        usd_brl = fetch_usd_brl(client)

        for produto, ticker, unit, factor in COMMODITIES:
            raw = fetch_yahoo_quote(client, ticker)
            if raw is None:
                logger.warning("Sem preço para %s (%s)", produto, ticker)
                continue

            if factor is None:
                # Mantém em USD (ex: Petróleo)
                price_brl = raw * usd_brl
                price_usd = raw
            else:
                price_brl = round(to_brl(raw, unit, factor, usd_brl), 2)
                price_usd = round(raw / 100 if unit.startswith("USX") else raw, 4)

            logger.info("  %-40s | raw=%-10.2f | R$ %.2f | USD %.4f",
                        produto, raw, price_brl, price_usd or 0)

            all_quotes.append({
                "product":    produto,
                "date":       TODAY,
                "price_brl":  price_brl,
                "price_usd":  price_usd,
                "index_name": f"YAHOO/{ticker}",
            })

    if not all_quotes:
        logger.error("Nenhuma cotação coletada.")
        return

    saved = updated = 0
    for data in all_quotes:
        existing = session.query(MarketQuote).filter_by(
            date=data["date"], product=data["product"]
        ).first()
        if existing:
            existing.price_brl  = data["price_brl"]
            existing.price_usd  = data["price_usd"]
            existing.index_name = data["index_name"]
            updated += 1
        else:
            session.add(MarketQuote(**data))
            saved += 1

    session.commit()
    session.close()
    logger.info(
        "✅ Cotações finalizadas: %d produtos | %d novos | %d atualizados.",
        len(all_quotes), saved, updated
    )


if __name__ == "__main__":
    main()
