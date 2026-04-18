from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "AgroJus API"
    app_version: str = "0.5.0"
    debug: bool = True

    # Database
    database_url: str = "postgresql://agrojus:agrojus@localhost:5432/agrojus"

    # JWT Auth — MUST be overridden via JWT_SECRET env var in production
    jwt_secret: str = "agrojus-dev-secret-change-in-production"
    jwt_secret_min_length: int = 32

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

    # DataJud/CNJ — API key publica universal (nao requer cadastro)
    datajud_api_key: str = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

    # Google Cloud / BigQuery (BasedosDados)
    gcp_project_id: str = "agrojus"
    gcp_project_number: str = ""

    # MapBiomas Alerta GraphQL (credenciais via .env em producao)
    mapbiomas_email: str = ""
    mapbiomas_password: str = ""

    # Embrapa AgroAPI — 9 APIs assinadas (Agritec, AGROFIT, AgroTermos,
    # Bioinsumos, BovTrace, PlantAnnot, RespondeAgro, SmartSolosExpert, Sting)
    embrapa_consumer_key: str = ""
    embrapa_consumer_secret: str = ""
    embrapa_access_token: str = ""
    embrapa_base_url: str = "https://api.cnptia.embrapa.br"

    # dados.gov.br (CKAN federal)
    dados_gov_token: str = ""
    dados_gov_base_url: str = "https://dados.gov.br/api/publico"

    # Portal da Transparência (CEIS, CNEP, Garantia-Safra, Servidores)
    portal_transparencia_token: str = ""
    portal_transparencia_base_url: str = "https://api.portaldatransparencia.gov.br/api-de-dados"

    # SERPRO API (CPF/CNPJ premium)
    serpro_api_token: str = ""

    # OpenAI — Codex 5.4 (Code Reviewer agent)
    openai_api_key: str = ""

    # Anthropic Claude API — gerador de minutas jurídicas
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-4-7"

    # Webhooks — timeout HTTP para entrega
    webhook_timeout_seconds: int = 10
    webhook_max_retries: int = 3

    # Data directories
    data_dir: str = "data"
    shapefile_dir: str = "data/shapefiles"
    cache_dir: str = "data/cache"

    # Cache TTL (seconds)
    cache_ttl: int = 86400  # 24 hours


settings = Settings()
