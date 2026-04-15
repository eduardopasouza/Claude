from sqlalchemy import create_engine, text
e = create_engine('postgresql://agrojus:agrojus@db:5432/agrojus')
with e.connect() as conn:
    r = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='mapbiomas_irrigation_stats' ORDER BY ordinal_position LIMIT 10"))
    print([row[0] for row in r])
    # também verifica o erro do dashboard
    r2 = conn.execute(text("SELECT * FROM mapbiomas_irrigation_stats LIMIT 1"))
    print(r2.keys())
