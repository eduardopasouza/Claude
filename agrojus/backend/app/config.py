from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "AgroJus API"
    app_version: str = "0.4.0"
    debug: bool = True

    # Database
    database_url: str = "postgresql://agrojus:agrojus@localhost:5432/agrojus"

    # JWT Auth
    jwt_secret: str = "agrojus-dev-secret-change-in-production"

    # External APIs
    receita_federal_url: str = "https://brasilapi.com.br/api/cnpj/v1"

    # SICAR/CAR
    sicar_wfs_url: str = "https://car.gov.br/geoserver/wfs"
    sicar_public_url: str = "https://consultapublica.car.gov.br"

    # SIGEF/INCRA
    sigef_wfs_url: str = "https://acervofundiario.incra.gov.br/geoserver/wfs"
    sigef_api_url: str = "https://sigef.incra.gov.br/api/v1"

    # IBAMA
    ibama_embargos_url: str = "https://dadosabertos.ibama.gov.br"

    # DataJud/CNJ
    datajud_api_key: str = ""

    # SERPRO API (CPF/CNPJ premium)
    serpro_api_token: str = ""

    # Data directories
    data_dir: str = "data"
    shapefile_dir: str = "data/shapefiles"
    cache_dir: str = "data/cache"

    # Cache TTL (seconds)
    cache_ttl: int = 86400  # 24 hours


settings = Settings()
