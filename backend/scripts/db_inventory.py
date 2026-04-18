"""Inventário completo de todas as tabelas e contagens no banco AgroJus."""
from sqlalchemy import create_engine, text, inspect

DB_URL = "postgresql://agrojus:agrojus@db:5432/agrojus"
engine = create_engine(DB_URL)
insp   = inspect(engine)
tables = sorted(insp.get_table_names())

print("=" * 55)
print(f"{'TABELA':<38} {'REGISTROS':>12}")
print("=" * 55)

with engine.connect() as conn:
    for t in tables:
        try:
            n = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar()
            flag = "✅" if n and n > 0 else "⭕"
            print(f"{flag} {t:<36} {n:>12,}")
        except Exception as e:
            print(f"❌ {t:<36} ERRO: {e}")

print("=" * 55)
print(f"Total de tabelas: {len(tables)}")
