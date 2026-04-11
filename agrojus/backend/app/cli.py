"""
CLI de importação e sincronização de dados.

Ferramentas para popular o banco de dados local com dados de fontes
que precisam de download periódico:
- IBAMA: embargos e autuações (CSV grandes)
- Lista Suja: trabalho escravo (CSV do Portal da Transparência)
- FUNAI: terras indígenas (shapefile)
- ICMBio: unidades de conservação (shapefile)
- INCRA: assentamentos (shapefile)
- INPE: desmatamento (shapefile)

Uso:
  python -m app.cli import-ibama
  python -m app.cli import-lista-suja
  python -m app.cli import-shapefile terras_indigenas /path/to/file.shp
  python -m app.cli sync-all
  python -m app.cli stats
"""

import sys
import csv
import io
from pathlib import Path
from datetime import datetime, timezone

from app.config import settings


def import_ibama_embargos(csv_path: str = None):
    """
    Importa embargos do IBAMA de CSV para o banco local.

    Se csv_path não for fornecido, baixa automaticamente do portal de dados abertos.
    Fonte: https://dadosabertos.ibama.gov.br/dados/SICAFI/embargo/Embargo.csv
    """
    import httpx
    from app.models.database import get_session, EnvironmentalAlert

    session = get_session()

    if csv_path and Path(csv_path).exists():
        print(f"[IBAMA] Importando de arquivo local: {csv_path}")
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
    else:
        print("[IBAMA] Baixando dados de embargos do portal de dados abertos...")
        url = "https://dadosabertos.ibama.gov.br/dados/SICAFI/embargo/Embargo.csv"
        response = httpx.get(url, timeout=300.0, follow_redirects=True)
        response.raise_for_status()
        content = response.text

        # Save locally for cache
        cache_path = Path(settings.cache_dir) / "ibama_embargos.csv"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[IBAMA] CSV salvo em: {cache_path}")

    reader = csv.DictReader(io.StringIO(content), delimiter=";")
    count = 0
    batch = []

    for row in reader:
        cpf_cnpj = row.get("CPF/CNPJ", "").replace(".", "").replace("/", "").replace("-", "")

        area_str = row.get("Área (ha)", "0").replace(",", ".")
        try:
            area = float(area_str) if area_str else None
        except ValueError:
            area = None

        alert = EnvironmentalAlert(
            property_car_code=None,
            cpf_cnpj=cpf_cnpj,
            alert_type="embargo",
            source="ibama",
            description=row.get("Infração", ""),
            area_ha=area,
            date_detected=parse_date_br(row.get("Data Embargo")),
            raw_data={
                "auto_infracao": row.get("Número TAD", ""),
                "nome": row.get("Nome", ""),
                "municipio": row.get("Município", ""),
                "uf": row.get("UF", ""),
                "situacao": row.get("Situação", ""),
            },
        )
        batch.append(alert)
        count += 1

        if len(batch) >= 1000:
            session.bulk_save_objects(batch)
            session.commit()
            batch = []
            print(f"  ... {count} registros importados")

    if batch:
        session.bulk_save_objects(batch)
        session.commit()

    session.close()
    print(f"[IBAMA] Importação concluída: {count} embargos importados")
    return count


def import_lista_suja(csv_path: str = None):
    """
    Importa dados da Lista Suja do Trabalho Escravo.

    Fonte: Portal da Transparência (download manual necessário).
    CSV deve estar em encoding UTF-8 com delimitador ';'.
    """
    from app.models.database import get_session, LegalRecord

    if not csv_path:
        # Try default cache location
        csv_path = str(Path(settings.cache_dir) / "lista_suja.csv")

    if not Path(csv_path).exists():
        print(f"[LISTA SUJA] Arquivo não encontrado: {csv_path}")
        print("  Baixe manualmente de: https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo")
        print(f"  Salve como: {csv_path}")
        return 0

    session = get_session()
    count = 0

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")

        batch = []
        for row in reader:
            cpf_cnpj = row.get("CPF/CNPJ", "").replace(".", "").replace("/", "").replace("-", "")

            workers = 0
            try:
                workers = int(row.get("TRABALHADORES ENVOLVIDOS", "0"))
            except ValueError:
                pass

            record = LegalRecord(
                cpf_cnpj=cpf_cnpj,
                record_type="slave_labour",
                source="MTE/Lista Suja",
                description=f"Empregador: {row.get('EMPREGADOR', '')}. Estabelecimento: {row.get('ESTABELECIMENTO', '')}",
                amount=None,
                status="ativo",
                municipality=row.get("MUNICÍPIO", ""),
                state=row.get("UF", ""),
                date_filed=parse_date_br(row.get("DATA DA FISCALIZAÇÃO")),
                raw_data={
                    "empregador": row.get("EMPREGADOR", ""),
                    "estabelecimento": row.get("ESTABELECIMENTO", ""),
                    "trabalhadores": workers,
                    "cnae": row.get("CNAE", ""),
                },
            )
            batch.append(record)
            count += 1

            if len(batch) >= 500:
                session.bulk_save_objects(batch)
                session.commit()
                batch = []

        if batch:
            session.bulk_save_objects(batch)
            session.commit()

    session.close()
    print(f"[LISTA SUJA] Importação concluída: {count} registros importados")
    return count


def import_shapefile(layer_name: str, shapefile_path: str):
    """
    Importa shapefile para o banco PostGIS.

    Camadas suportadas:
    - terras_indigenas (FUNAI)
    - unidades_conservacao (ICMBio)
    - assentamentos (INCRA)
    - desmatamento (INPE/PRODES)
    - quilombos (INCRA)
    """
    try:
        import geopandas as gpd
    except ImportError:
        print("[GEO] GeoPandas não instalado. Instale com: pip install geopandas")
        return 0

    from app.models.database import get_engine

    if not Path(shapefile_path).exists():
        print(f"[GEO] Arquivo não encontrado: {shapefile_path}")
        return 0

    print(f"[GEO] Lendo shapefile: {shapefile_path}")
    gdf = gpd.read_file(shapefile_path)

    # Ensure CRS is WGS84
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        print(f"[GEO] Reprojetando de {gdf.crs} para EPSG:4326")
        gdf = gdf.to_crs(epsg=4326)

    table_name = f"layer_{layer_name}"

    engine = get_engine()
    print(f"[GEO] Importando {len(gdf)} features para tabela '{table_name}'...")

    gdf.to_postgis(
        table_name,
        engine,
        if_exists="replace",
        index=True,
    )

    print(f"[GEO] Importação concluída: {len(gdf)} features em '{table_name}'")
    return len(gdf)


def show_stats():
    """Mostra estatísticas do banco de dados local."""
    from app.models.database import get_session
    from sqlalchemy import text

    session = get_session()

    tables = [
        ("properties", "Imóveis"),
        ("persons", "Pessoas"),
        ("environmental_alerts", "Alertas Ambientais"),
        ("legal_records", "Registros Jurídicos"),
        ("rural_credits", "Créditos Rurais"),
        ("land_prices", "Preços de Terra"),
        ("market_data", "Dados de Mercado"),
        ("monitoring_alerts", "Alertas de Monitoramento"),
        ("cached_queries", "Consultas em Cache"),
    ]

    print("\n=== AgroJus - Estatísticas do Banco de Dados ===\n")
    total = 0

    for table, label in tables:
        try:
            result = session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            total += count
            print(f"  {label:.<35} {count:>8} registros")
        except Exception:
            print(f"  {label:.<35} {'(tabela não existe)':>20}")

    # Check for imported layers
    try:
        result = session.execute(text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_name LIKE 'layer_%'"
        ))
        layers = [row[0] for row in result]
        if layers:
            print("\n  Camadas geoespaciais importadas:")
            for layer in layers:
                result = session.execute(text(f"SELECT COUNT(*) FROM {layer}"))
                count = result.scalar()
                total += count
                print(f"    {layer:.<33} {count:>8} features")
    except Exception:
        pass

    print(f"\n  {'TOTAL':.<35} {total:>8} registros")
    print()

    session.close()


def parse_date_br(date_str: str) -> datetime | None:
    """Parse data no formato brasileiro (DD/MM/YYYY)."""
    if not date_str:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def main():
    """Entry point do CLI."""
    if len(sys.argv) < 2:
        print("Uso: python -m app.cli <comando> [argumentos]")
        print()
        print("Comandos:")
        print("  import-ibama [csv_path]       Importa embargos IBAMA")
        print("  import-lista-suja [csv_path]  Importa Lista Suja")
        print("  import-shapefile <nome> <path> Importa shapefile para PostGIS")
        print("  create-tables                 Cria tabelas no banco")
        print("  stats                         Mostra estatísticas do banco")
        print("  sync-all                      Importa todos os dados disponíveis")
        return

    command = sys.argv[1]

    if command == "import-ibama":
        csv_path = sys.argv[2] if len(sys.argv) > 2 else None
        import_ibama_embargos(csv_path)

    elif command == "import-lista-suja":
        csv_path = sys.argv[2] if len(sys.argv) > 2 else None
        import_lista_suja(csv_path)

    elif command == "import-shapefile":
        if len(sys.argv) < 4:
            print("Uso: python -m app.cli import-shapefile <nome_camada> <path.shp>")
            print("Camadas: terras_indigenas, unidades_conservacao, assentamentos, desmatamento, quilombos")
            return
        import_shapefile(sys.argv[2], sys.argv[3])

    elif command == "create-tables":
        from app.models.database import create_tables
        create_tables()
        print("[DB] Tabelas criadas com sucesso")

    elif command == "stats":
        show_stats()

    elif command == "sync-all":
        print("=== Sincronização completa ===")
        from app.models.database import create_tables
        create_tables()
        import_ibama_embargos()
        import_lista_suja()
        print("=== Sincronização concluída ===")

    else:
        print(f"Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
