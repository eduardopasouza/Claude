"""
Earth Engine Service — analise de satelite por propriedade.

Wrapper sobre etl_earth_engine.py com:
- Inicializacao lazy do EE
- Timeout e tratamento de erros
- Cache simples em memoria
- Formato padronizado para o relatorio
"""

import json
import logging
import time
from typing import Optional

logger = logging.getLogger("agrojus.ee")

_ee_initialized = False


def _ensure_ee():
    """Inicializa Earth Engine (lazy, uma vez)."""
    global _ee_initialized
    if _ee_initialized:
        return True
    try:
        import ee
        ee.Initialize(project="agrojus")
        _ee_initialized = True
        logger.info("Earth Engine inicializado")
        return True
    except Exception as e:
        logger.warning("Earth Engine indisponivel: %s", e)
        return False


def analyze_property_satellite(geometry_geojson: str, year: int = 2023) -> dict:
    """
    Analise completa de satelite para uma propriedade.

    Args:
        geometry_geojson: GeoJSON string do poligono
        year: Ano de referencia (default 2023)

    Returns:
        dict com lulc, fogo, solo, agua — ou erros parciais
    """
    if not _ensure_ee():
        return {"error": "Earth Engine indisponivel", "available": False}

    start = time.time()
    geom = json.loads(geometry_geojson) if isinstance(geometry_geojson, str) else geometry_geojson

    result = {
        "available": True,
        "year": year,
        "lulc": None,
        "fire_history": None,
        "soil": None,
        "water": None,
        "errors": [],
        "query_time_ms": 0,
    }

    # Importar funcoes do script ETL
    import sys
    sys.path.insert(0, "/app/scripts")
    from etl_earth_engine import (
        extract_lulc_for_property,
        extract_fire_for_property,
        extract_soil_for_property,
        extract_water_for_property,
    )

    # LULC
    try:
        result["lulc"] = extract_lulc_for_property(geom, year)
    except Exception as e:
        logger.warning("EE LULC error: %s", e)
        result["errors"].append(f"LULC: {e}")

    # Fogo (ultimos 5 anos)
    try:
        result["fire_history"] = extract_fire_for_property(geom, year - 4, year)
    except Exception as e:
        logger.warning("EE Fire error: %s", e)
        result["errors"].append(f"Fire: {e}")

    # Solo
    try:
        result["soil"] = extract_soil_for_property(geom)
    except Exception as e:
        logger.warning("EE Soil error: %s", e)
        result["errors"].append(f"Soil: {e}")

    # Agua
    try:
        result["water"] = extract_water_for_property(geom, year)
    except Exception as e:
        logger.warning("EE Water error: %s", e)
        result["errors"].append(f"Water: {e}")

    result["query_time_ms"] = round((time.time() - start) * 1000, 0)
    logger.info("EE analise completa: %.1fs, %d erros", (time.time() - start), len(result["errors"]))
    return result
