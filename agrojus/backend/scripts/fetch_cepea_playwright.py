import asyncio
from playwright.async_api import async_playwright
import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrojus:agrojus@db:5432/agrojus")
Base = declarative_base()

class MarketQuote(Base):
    __tablename__ = 'market_quotes'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    product = Column(String, nullable=False)
    index_name = Column(String, nullable=False)
    price_brl = Column(Float, nullable=False)
    price_usd = Column(Float, nullable=True)

def setup_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

async def fetch_cepea_prices():
    sources = [
        ("https://www.cepea.esalq.usp.br/br/indicador/soja.aspx", "Soja (Saca 60kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/milho.aspx", "Milho (Saca 60kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/boi-gordo.aspx", "Boi Gordo (Arroba)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/bezerro.aspx", "Bezerro (Reposição/Cabeça)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/leite.aspx", "Leite Fresco (Litro)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/cafe.aspx", "Café Arábica (Saca 60kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/acucar.aspx", "Açúcar Cristal (Saca 50kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/trigo.aspx", "Trigo (Tonelada)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/frango.aspx", "Frango Vivo (Kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/suino.aspx", "Suíno Vivo (Kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/arroz.aspx", "Arroz em Casca (Saca 50kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/algodao.aspx", "Algodão Pluma (Libra-Peso)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/citros.aspx", "Laranja/Citros Pera (Caixa 40,8kg)"),
        ("https://www.cepea.esalq.usp.br/br/indicador/tilapia.aspx", "Piscicultura/Tilápia (Kg)"),
    ]

    print("Iniciando motor de extração Playwright (Bypass WAF)...")
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for url, name in sources:
            print(f"Coletando: {name}...")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # A tabela de indicadores do Cepea usa o id 'imagenet-indicador1'
                # Vamos pegar as células da primeira linha do tbody
                row = page.locator("#imagenet-indicador1 tbody tr").first
                
                if await row.count() > 0:
                    cols = row.locator("td")
                    date_str = await cols.nth(0).text_content()
                    price_brl_str = await cols.nth(1).text_content()
                    
                    try:
                        price_usd_str = await cols.nth(2).text_content()
                    except:
                        price_usd_str = "0"
                        
                    date_str = date_str.strip()
                    price_brl = float(price_brl_str.strip().replace('.', '').replace(',', '.'))
                    price_usd = float(price_usd_str.strip().replace('.', '').replace(',', '.'))
                    
                    d, m, y = date_str.split('/')
                    if len(y) == 2:
                        y = "20" + y
                    date_obj = datetime.date(int(y), int(m), int(d))
                    
                    results.append({
                        "product": name,
                        "date": date_obj,
                        "price_brl": price_brl,
                        "price_usd": price_usd,
                        "index_name": "CEPEA"
                    })
                    print(f"✅ {name}: R$ {price_brl} ({date_str})")
                else:
                    print(f"⚠️ {name}: Tabela não encontrada na página.")
            except Exception as e:
                print(f"❌ Falha em {name}: {e}")
                
        await browser.close()
    return results

if __name__ == "__main__":
    session = setup_db()
    quotes = asyncio.run(fetch_cepea_prices())
    saved = 0
    
    for data in quotes:
        existing = session.query(MarketQuote).filter_by(date=data['date'], product=data['product']).first()
        if not existing:
            quote = MarketQuote(
                date=data['date'],
                product=data['product'],
                index_name=data['index_name'],
                price_brl=data['price_brl'],
                price_usd=data['price_usd']
            )
            session.add(quote)
            saved += 1
            
    session.commit()
    print(f"\nResumo: Foram gravadas {saved} cotações da CEPEA no Banco de Dados.")
