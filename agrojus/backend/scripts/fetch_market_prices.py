import httpx
from bs4 import BeautifulSoup
import datetime
import json
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

def fetch_agrolink_quotes():
    print(f"Buscando cotações públicas do Portal Agrolink...")
    url = "https://www.agrolink.com.br/cotacoes"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    results = []
    try:
        response = httpx.get(url, headers=headers, timeout=20.0, follow_redirects=True)
        if response.status_code != 200:
            print(f" Erro {response.status_code} ao acessar Agrolink.")
            return results
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procura as principais tabelas de cotação da home de cotações
        tables = soup.find_all('table', class_='table')
        
        today = datetime.date.today()
        
        # Simulando uma leitura caso as tabelas principais tenham nomes de produto
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                     # Formato comum: | Produto/Região | Preço(R$) | Var |
                     name = cols[0].text.strip()
                     
                     # Identificadores chave para nosso benchmark: Soja, Milho, Boi
                     if "soja" in name.lower() or "milho" in name.lower() or "boi" in name.lower():
                         try:
                             price_str = cols[1].text.strip().replace('R$', '').replace('.', '').replace(',', '.').strip()
                             price_val = float(price_str)
                             
                             results.append({
                                 'product': f"Agrolink: {name[:50]}",
                                 'date': today,
                                 'price_brl': price_val,
                                 'price_usd': 0.0,
                                 'index_name': 'AGROLINK'
                             })
                         except ValueError:
                             continue
                             
        return results
    except Exception as e:
        print(f"Erro no Scraper: {e}")
        return []

if __name__ == "__main__":
    session = setup_db()
    
    quotes = fetch_agrolink_quotes()
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
            print(f"✅ Inserido: {data['product']} - R$ {data['price_brl']}")
            
    session.commit()
    print(f"\nResumo: Foram salvas {saved} novas cotações do mercado agrícola.")
