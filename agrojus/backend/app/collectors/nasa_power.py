"""
Coletor de dados climaticos da NASA POWER.

API publica, gratuita, sem autenticacao.
Fonte: https://power.larc.nasa.gov/

Dados disponiveis para qualquer ponto do planeta:
- Temperatura (T2M, T2M_MAX, T2M_MIN)
- Precipitacao (PRECTOTCORR)
- Radiacao solar (ALLSKY_SFC_SW_DWN)
- Umidade relativa (RH2M)
- Velocidade do vento (WS2M)
- Evapotranspiracao
"""

import logging
from typing import Optional
from datetime import datetime, timedelta

from app.collectors.base import BaseCollector

logger = logging.getLogger("agrojus")


class NASAPowerCollector(BaseCollector):
    """Dados climaticos reais da NASA POWER — funciona para qualquer coordenada."""

    API_URL = "https://power.larc.nasa.gov/api/temporal"

    PARAMETERS = {
        "temperature": "T2M,T2M_MAX,T2M_MIN",
        "precipitation": "PRECTOTCORR",
        "solar": "ALLSKY_SFC_SW_DWN",
        "humidity": "RH2M",
        "wind": "WS2M",
        "complete": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN,RH2M,WS2M",
    }

    def __init__(self):
        super().__init__("nasa_power")

    async def get_climate_data(
        self,
        lat: float,
        lon: float,
        days: int = 30,
        parameters: str = "complete",
    ) -> dict:
        """
        Busca dados climaticos para uma coordenada.

        Retorna dados diarios dos ultimos N dias.
        """
        cache_key = f"climate:{lat}:{lon}:{days}:{parameters}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        end = datetime.now()
        start = end - timedelta(days=days)
        params_str = self.PARAMETERS.get(parameters, parameters)

        try:
            response = await self._http_get(
                f"{self.API_URL}/daily/point",
                params={
                    "start": start.strftime("%Y%m%d"),
                    "end": end.strftime("%Y%m%d"),
                    "latitude": lat,
                    "longitude": lon,
                    "community": "ag",
                    "parameters": params_str,
                    "format": "json",
                },
                timeout=30.0,
            )
            data = response.json()

            # Processar e simplificar
            properties = data.get("properties", {}).get("parameter", {})
            result = {
                "coordinates": {"lat": lat, "lon": lon},
                "period": {"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d"), "days": days},
                "parameters": {},
                "summary": {},
                "source": "NASA POWER (Prediction Of Worldwide Energy Resources)",
            }

            for param_name, values in properties.items():
                # Filtrar valores invalidos (-999)
                valid_values = [v for v in values.values() if v != -999.0 and v is not None]
                result["parameters"][param_name] = values

                if valid_values:
                    result["summary"][param_name] = {
                        "mean": round(sum(valid_values) / len(valid_values), 2),
                        "min": round(min(valid_values), 2),
                        "max": round(max(valid_values), 2),
                        "days_with_data": len(valid_values),
                    }

            # Calcular precipitacao acumulada
            if "PRECTOTCORR" in properties:
                precip_values = [v for v in properties["PRECTOTCORR"].values() if v != -999.0 and v is not None]
                if precip_values:
                    result["summary"]["precipitation_total_mm"] = round(sum(precip_values), 1)
                    result["summary"]["rainy_days"] = sum(1 for v in precip_values if v > 1.0)

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.warning("NASA POWER failed: %s", e)
            return {"error": str(e), "source": "NASA POWER"}

    async def get_climate_summary(self, lat: float, lon: float) -> dict:
        """Resumo climatico dos ultimos 30 dias para uma coordenada."""
        return await self.get_climate_data(lat, lon, days=30, parameters="complete")
