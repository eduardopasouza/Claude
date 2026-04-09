"""
Rotas do portal de notícias do agronegócio.

Quando os feeds RSS reais nao estiverem disponiveis,
retorna dados de referencia para desenvolvimento do frontend.
"""

from fastapi import APIRouter

from app.collectors.news_aggregator import NewsAggregator
from app.models.schemas import NewsArticle

router = APIRouter()

# Noticias de referencia para quando RSS nao estiver disponivel
_REFERENCE_NEWS = [
    NewsArticle(title="Safra de soja 2025/26 deve atingir recorde de 170 milhoes de toneladas", url="https://example.com/1", source="Canal Rural", published_at="2026-04-09T10:30:00", summary="A CONAB revisou para cima a estimativa de producao de soja, impulsionada pelo clima favoravel no Centro-Oeste e expansao de area plantada no MATOPIBA.", category="mercado", image_url=None),
    NewsArticle(title="IBAMA intensifica fiscalizacao de desmatamento ilegal no Cerrado", url="https://example.com/2", source="Agrolink", published_at="2026-04-09T09:15:00", summary="Operacao Bioma Vivo embargou 15 mil hectares em Mato Grosso e Goias. Proprietarios podem consultar situacao no CAR.", category="juridico", image_url=None),
    NewsArticle(title="Preco do boi gordo sobe 3% na semana com demanda aquecida", url="https://example.com/3", source="Noticias Agricolas", published_at="2026-04-08T16:45:00", summary="Indicador CEPEA/B3 do boi gordo atingiu R$ 312/@ em Sao Paulo, maior patamar desde fevereiro. Exportacoes para China seguem em alta.", category="mercado", image_url=None),
    NewsArticle(title="Nova regulamentacao do Codigo Florestal entra em vigor em maio", url="https://example.com/4", source="Embrapa", published_at="2026-04-08T14:20:00", summary="Decreto federal define novas regras para compensacao de Reserva Legal e regularizacao de APP em propriedades rurais com CAR ativo.", category="juridico", image_url=None),
    NewsArticle(title="Credito rural do Plano Safra 2025/26 ultrapassa R$ 400 bilhoes", url="https://example.com/5", source="Portal do Agronegocio", published_at="2026-04-08T11:00:00", summary="PRONAF e PRONAMP concentram 45% dos recursos. Taxa de juros para agricultura familiar permanece em 5% ao ano.", category="mercado", image_url=None),
    NewsArticle(title="STJ decide sobre usucapiao de terras publicas em area rural", url="https://example.com/6", source="Canal Rural", published_at="2026-04-07T17:30:00", summary="Decisao da Segunda Turma do STJ estabelece novo entendimento sobre prescricao aquisitiva em glebas devolutas estaduais.", category="juridico", image_url=None),
    NewsArticle(title="Exportacoes do agro brasileiro batem US$ 15 bi em marco", url="https://example.com/7", source="Agrolink", published_at="2026-04-07T10:15:00", summary="Soja, carne bovina e celulose lideram as exportacoes. China continua como principal destino com 35% do total.", category="mercado", image_url=None),
    NewsArticle(title="MTE atualiza Lista Suja do trabalho escravo com 47 novos empregadores", url="https://example.com/8", source="Noticias Agricolas", published_at="2026-04-06T15:00:00", summary="Atualizacao semestral inclui fazendas em 12 estados. Plataforma AgroJus permite consulta automatizada por CPF/CNPJ.", category="juridico", image_url=None),
    NewsArticle(title="FIAGRO captam R$ 8 bilhoes no primeiro trimestre de 2026", url="https://example.com/9", source="Portal do Agronegocio", published_at="2026-04-06T09:45:00", summary="Fundos do agronegocio registram crescimento de 25% na captacao. CRAs e CRIs agro dominam as carteiras.", category="mercado", image_url=None),
    NewsArticle(title="Georreferenciamento obrigatorio: prazo para imoveis acima de 25ha encerra em dezembro", url="https://example.com/10", source="Embrapa", published_at="2026-04-05T13:30:00", summary="INCRA reforça que propriedades acima de 25 hectares devem ter certificacao SIGEF ate dezembro de 2026 para transacoes imobiliarias.", category="juridico", image_url=None),
    NewsArticle(title="Milho safrinha tem desenvolvimento comprometido por seca no Parana", url="https://example.com/11", source="Canal Rural", published_at="2026-04-05T08:20:00", summary="Falta de chuvas nas ultimas 3 semanas preocupa produtores do norte do Parana e sul do Mato Grosso do Sul.", category="mercado", image_url=None),
    NewsArticle(title="Funai delimita nova terra indigena em area de expansao agricola no MA", url="https://example.com/12", source="Agrolink", published_at="2026-04-04T16:00:00", summary="A TI Arariboia, com 413 mil hectares, afeta 12 municipios no sul do Maranhao. Produtores podem verificar sobreposicao via consulta geoespacial.", category="juridico", image_url=None),
]


def _paginate(items: list, skip: int, limit: int) -> tuple[list, int]:
    """Aplica paginacao offset-based."""
    total = len(items)
    return items[skip:skip + limit], total


@router.get("/")
async def get_latest_news(limit: int = 30, skip: int = 0):
    """Retorna as ultimas noticias do agronegocio (curadoria de multiplas fontes)."""
    aggregator = NewsAggregator()
    articles = await aggregator.fetch_all_news(limit=200)

    if articles:
        page, total = _paginate(articles, skip, limit)
        return {"articles": page, "total": total, "skip": skip, "limit": limit, "is_reference": False}

    page, total = _paginate(_REFERENCE_NEWS, skip, limit)
    return {"articles": page, "total": total, "skip": skip, "limit": limit, "is_reference": True}


@router.get("/legal")
async def get_legal_news(limit: int = 20, skip: int = 0):
    """Retorna noticias com relevancia juridica."""
    aggregator = NewsAggregator()
    articles = await aggregator.fetch_legal_news(limit=200)

    if articles:
        page, total = _paginate(articles, skip, limit)
        return {"articles": page, "total": total, "skip": skip, "limit": limit, "category": "juridico", "is_reference": False}

    legal = [a for a in _REFERENCE_NEWS if a.category == "juridico"]
    page, total = _paginate(legal, skip, limit)
    return {"articles": page, "total": total, "skip": skip, "limit": limit, "category": "juridico", "is_reference": True}


@router.get("/market")
async def get_market_news(limit: int = 20, skip: int = 0):
    """Retorna noticias de mercado (cotacoes, safras, commodities)."""
    aggregator = NewsAggregator()
    articles = await aggregator.fetch_market_news(limit=200)

    if articles:
        page, total = _paginate(articles, skip, limit)
        return {"articles": page, "total": total, "skip": skip, "limit": limit, "category": "mercado", "is_reference": False}

    market = [a for a in _REFERENCE_NEWS if a.category == "mercado"]
    page, total = _paginate(market, skip, limit)
    return {"articles": page, "total": total, "skip": skip, "limit": limit, "category": "mercado", "is_reference": True}
