from sqlalchemy import create_engine, text
e = create_engine('postgresql://agrojus:agrojus@db:5432/agrojus')
c = e.connect()
r1 = c.execute(text("SELECT count(*) FROM environmental_alerts WHERE source='IBAMA'"))
r2 = c.execute(text("SELECT count(*) FROM environmental_alerts WHERE source='MTE'"))
r3 = c.execute(text("SELECT count(*) FROM market_quotes"))
r4 = c.execute(text("SELECT count(*) FROM mapbiomas_credito_rural"))

print(f"IBAMA alerts: {r1.fetchone()[0]}")
print(f"MTE alerts: {r2.fetchone()[0]}")
print(f"Market quotes: {r3.fetchone()[0]}")
try:
    print(f"Credito Rural parcelas: {r4.fetchone()[0]}")
except:
    print("Credito Rural: tabela nao carregada ainda")
c.close()
