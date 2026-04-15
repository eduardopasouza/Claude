import pandas as pd
import json

files = [
    'data/mapbiomas_stats/AGRICULTURA_COL9.xlsx',
    'data/mapbiomas_stats/PASTAGEM_COL9.xlsx',
    'data/mapbiomas_stats/MINERACAO_COL9.xlsx'
]

results = {}
for f in files:
    try:
        df = pd.read_excel(f, nrows=0)
        results[f] = df.columns.tolist()
    except Exception as e:
        results[f] = str(e)

print(json.dumps(results, indent=2))
