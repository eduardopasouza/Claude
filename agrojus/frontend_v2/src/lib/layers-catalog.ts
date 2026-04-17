/**
 * Catálogo declarativo de camadas geoespaciais do AgroJus.
 *
 * EXPANSÃO MASSIVA v2: ~70 camadas organizadas em 15 temas.
 * Cobre TUDO discutido ao longo do projeto:
 *   - 6 plataformas MapBiomas completas (Cobertura, Alertas, Fogo, Mineração, Recuperação, Crédito Rural)
 *   - Registros cartoriais (ONR matrículas, SNCI legado)
 *   - Fundiário completo (CAR, SIGEF, assentamentos, quilombolas, terras União, faixa fronteira)
 *   - Ambiental (UCs federal+estadual, embargos/autos IBAMA+ICMBio, DETER, PRODES, CTF IBAMA, ZEE)
 *   - IBGE como choropleth por município (PAM soja/milho/cana/café/algodão/arroz, PPM bovino/ovino,
 *     Censo Agropecuário, IDHM, PIB municipal, REGIC hierarquia urbana)
 *   - Hidrografia (ANA BHO, outorgas, HidroWeb, Atlas Irrigação)
 *   - Clima (INMET estações, NASA POWER, CHIRPS, ZARC aptidão)
 *   - Solos (SmartSolos Embrapa, aptidão IBGE, carbono MapBiomas)
 *   - Infraestrutura (rodovias federais+estaduais, ferrovias, portos, aeroportos, armazéns,
 *     frigoríficos, energia ANEEL, terminais intermodais)
 *   - Mineração (SIGMINE ANM, MapBiomas mineração legal/ilegal)
 *   - Jurídico georreferenciado (autos IBAMA pontos, embargos, processos DataJud)
 *   - Fiscal (CEIS/CNEP por município, CNDT)
 *   - Urbano (MapBiomas urbanização anual, limites municipais/estaduais)
 *   - Agricultura especializada (MapBiomas cultura específica)
 *   - Atmosfera (MapBiomas temperatura, precipitação, qualidade ar)
 *   - Degradação (MapBiomas borda, fragmento, frequência fogo)
 *   - Risco climático (deslizamentos, inundação, segurança hídrica)
 *
 * Status de cada camada:
 *   "postgis"  → dados já carregados no PostgreSQL (17 camadas)
 *   "geo"      → endpoint legado /geo/layers (WFS externo)
 *   "ibge"     → choropleth IBGE (endpoint a criar)
 *   "gee"      → Earth Engine (GCP Project já configurado)
 *   "external" → API externa a integrar
 *   "stub"     → placeholder sem dados ainda (comingSoon)
 */

import {
  Droplets,
  FileWarning,
  Flame,
  Landmark,
  LucideIcon,
  Map as MapIcon,
  Mountain,
  Pickaxe,
  ShieldAlert,
  Sprout,
  TreePine,
  Truck,
  Waves,
  Wheat,
  Building2,
  Users,
  ScrollText,
  Gavel,
  Thermometer,
  Zap,
  Scroll,
  Building,
  Wind,
  Factory,
  CloudRain,
  MoveVertical,
  AlertTriangle,
} from "lucide-react";

export type LayerCategory =
  | "fundiario"
  | "ambiental"
  | "desmatamento"
  | "fogo"
  | "vegetacao_sec"
  | "degradacao"
  | "agricultura"
  | "pastagem"
  | "agua"
  | "solo"
  | "mineracao"
  | "infraestrutura"
  | "energia"
  | "credito"
  | "producao_ibge"
  | "pecuaria_ibge"
  | "socioeconomico"
  | "clima"
  | "atmosfera"
  | "risco_climatico"
  | "urbano"
  | "juridico"
  | "fiscal";

export type LayerEndpoint = "postgis" | "geo" | "ibge" | "ibge_choropleth" | "gee" | "external" | "stub";

export type LayerConfig = {
  id: string;
  name: string;
  description: string;
  category: LayerCategory;
  color: string;
  endpoint: LayerEndpoint;
  endpointId?: string;
  minZoom: number;
  maxFeatures: number;
  inspectorFields?: string[];
  fieldLabels?: Record<string, string>;
  comingSoon?: boolean;
  geometryType?: "polygon" | "line" | "point" | "raster" | "choropleth" | "mixed";
  /** Fonte original humano-legível */
  source?: string;
};

export type ThemeGroup = {
  id: LayerCategory;
  label: string;
  icon: LucideIcon;
  description: string;
  color: string;
};

export const THEMES: ThemeGroup[] = [
  { id: "fundiario",        label: "Fundiário",             icon: Landmark,       description: "CAR, SIGEF, SNCI, terras União, quilombolas, TIs",       color: "#10B981" },
  { id: "ambiental",        label: "Ambiental",             icon: TreePine,       description: "UCs, embargos, autos, CTF IBAMA, ZEE",                   color: "#22C55E" },
  { id: "desmatamento",     label: "Desmatamento",          icon: FileWarning,    description: "PRODES, DETER, MapBiomas desmatamento anual/acumulado",  color: "#DC2626" },
  { id: "fogo",             label: "Fogo & Queimadas",      icon: Flame,          description: "MapBiomas cicatrizes mensais/anuais, frequência",        color: "#EF4444" },
  { id: "vegetacao_sec",    label: "Vegetação Secundária",  icon: Sprout,         description: "Regeneração, idade — MapBiomas Recuperação",             color: "#4ADE80" },
  { id: "degradacao",       label: "Degradação Florestal",  icon: AlertTriangle,  description: "Borda, fragmento, freq. fogo — MapBiomas",                color: "#F97316" },
  { id: "agricultura",      label: "Agricultura",           icon: Wheat,          description: "MapBiomas culturas (soja, milho, cana, café, algodão)",  color: "#F59E0B" },
  { id: "pastagem",         label: "Pastagem & Pecuária",   icon: Sprout,         description: "Vigor, idade, biomassa — MapBiomas",                     color: "#84CC16" },
  { id: "agua",             label: "Água & Hidrografia",    icon: Droplets,       description: "ANA BHO, outorgas, estações, Atlas Irrigação",           color: "#06B6D4" },
  { id: "solo",             label: "Solo & Aptidão",        icon: Mountain,       description: "SmartSolos Embrapa, aptidão, carbono MapBiomas",         color: "#92400E" },
  { id: "mineracao",        label: "Mineração",             icon: Pickaxe,        description: "SIGMINE ANM + MapBiomas mineração legal/ilegal",         color: "#A78BFA" },
  { id: "infraestrutura",   label: "Logística",             icon: Truck,          description: "Rodovias, ferrovias, portos, armazéns, frigoríficos",    color: "#FBBF24" },
  { id: "energia",          label: "Energia",               icon: Zap,            description: "ANEEL usinas, linhas transmissão, subestações",           color: "#FACC15" },
  { id: "credito",          label: "Crédito & Finanças",    icon: Landmark,       description: "SICOR, parcelas financiadas, inadimplência",             color: "#3B82F6" },
  { id: "producao_ibge",    label: "Produção Agrícola (PAM)", icon: Wheat,        description: "IBGE SIDRA: soja, milho, cana, café, algodão (choropleth)", color: "#EAB308" },
  { id: "pecuaria_ibge",    label: "Pecuária (PPM)",        icon: Factory,        description: "IBGE SIDRA: bovino, ovino, suíno, leite (choropleth)",    color: "#BE123C" },
  { id: "socioeconomico",   label: "Socioeconômico",        icon: Users,          description: "IDHM, PIB municipal, REGIC, população — IBGE+PNUD",      color: "#8B5CF6" },
  { id: "clima",            label: "Clima",                 icon: CloudRain,      description: "INMET, NASA POWER, CHIRPS, ZARC aptidão",                color: "#0EA5E9" },
  { id: "atmosfera",        label: "Atmosfera",             icon: Wind,           description: "Temperatura, precipitação, qualidade ar — MapBiomas",    color: "#38BDF8" },
  { id: "risco_climatico",  label: "Risco Climático",       icon: AlertTriangle,  description: "Deslizamentos, inundação, segurança hídrica",            color: "#F43F5E" },
  { id: "urbano",           label: "Urbano",                icon: Building,       description: "MapBiomas urbanização anual, limites",                   color: "#94A3B8" },
  { id: "juridico",         label: "Jurídico",              icon: Gavel,          description: "Autos IBAMA pontos, processos DataJud por município",    color: "#EC4899" },
  { id: "fiscal",           label: "Fiscal/Compliance",     icon: ShieldAlert,    description: "CEIS, CNEP, CNDT, Lista Suja MTE por CNPJ",              color: "#DB2777" },
];

// =============================================================================
// CATÁLOGO COMPLETO — ~70 camadas
// =============================================================================

export const LAYERS: LayerConfig[] = [
  // ============== FUNDIÁRIO (10) ==============
  { id: "sicar_completo", name: "CAR Nacional (SICAR)", description: "352k+ imóveis cadastrados — corte MCR 2.9", category: "fundiario", color: "#10B981", endpoint: "postgis", minZoom: 10, maxFeatures: 500, geometryType: "polygon", source: "SICAR/SFB/MMA",
    inspectorFields: ["cod_imovel","municipio","uf","area","modulos_fiscais","status_imovel","tipo_imovel","condicao"],
    fieldLabels: { cod_imovel:"Código CAR", area:"Área (ha)", modulos_fiscais:"Módulos fiscais", status_imovel:"Status CAR" } },
  { id: "geo_car", name: "CAR via WFS (MA)", description: "135k imóveis Maranhão — WFS oficial", category: "fundiario", color: "#059669", endpoint: "postgis", minZoom: 10, maxFeatures: 500, geometryType: "polygon", source: "SICAR WFS",
    inspectorFields: ["cod_imovel","municipio","uf","area","status_imovel","tipo_imovel","m_fiscal","condicao"] },
  { id: "sigef_parcelas", name: "SIGEF (parcelas certificadas)", description: "1.7M+ parcelas georreferenciadas INCRA (pós-2013)", category: "fundiario", color: "#EC4899", endpoint: "postgis", minZoom: 11, maxFeatures: 300, geometryType: "polygon", source: "INCRA/SIGEF",
    inspectorFields: ["parcela_co","nome_area","situacao_i","status","data_aprov","rt","art","uf_id"] },
  { id: "snci_imoveis", name: "SNCI (imóveis certificados legado)", description: "Imóveis certificados pré-2013 (antes do SIGEF)", category: "fundiario", color: "#DB2777", endpoint: "stub", minZoom: 11, maxFeatures: 300, comingSoon: true, source: "INCRA/SNCI" },
  { id: "terras_indigenas", name: "Terras Indígenas", description: "655 TIs demarcadas — FUNAI", category: "fundiario", color: "#6366F1", endpoint: "postgis", minZoom: 4, maxFeatures: 1000, geometryType: "polygon", source: "FUNAI",
    inspectorFields: ["terrai_nom","etnia_nome","fase_ti","modalidade","superficie","uf_sigla"] },
  { id: "quilombolas_incra", name: "Territórios Quilombolas", description: "Comunidades tituladas + em processo", category: "fundiario", color: "#D97706", endpoint: "stub", minZoom: 5, maxFeatures: 500, comingSoon: true, source: "INCRA/Palmares" },
  { id: "assentamentos_incra", name: "Assentamentos INCRA", description: "Projetos de reforma agrária", category: "fundiario", color: "#CA8A04", endpoint: "stub", minZoom: 6, maxFeatures: 1000, comingSoon: true, source: "INCRA" },
  { id: "terras_uniao_spu", name: "Terras da União (SPU)", description: "Terrenos de marinha, várzeas, imóveis da União", category: "fundiario", color: "#65A30D", endpoint: "stub", minZoom: 6, maxFeatures: 500, comingSoon: true, source: "SPU/ME" },
  { id: "faixa_fronteira", name: "Faixa de Fronteira (150km)", description: "Restrição Lei 6.634/79 a imóveis de estrangeiros", category: "fundiario", color: "#9333EA", endpoint: "stub", minZoom: 4, maxFeatures: 100, comingSoon: true, source: "IBGE" },
  { id: "glebas_federais", name: "Glebas Federais", description: "Terras devolutas federais (Amazônia Legal)", category: "fundiario", color: "#7C3AED", endpoint: "stub", minZoom: 6, maxFeatures: 500, comingSoon: true, source: "INCRA" },

  // Nota: "Cartório (ONR)" foi removido do catálogo de camadas — dados de
  // matrícula e cadeia dominial NÃO são de acesso público; exigem pagamento
  // por consulta (ONR/e-CRI/InfoSimples R$ 0,10-0,50/consulta) ou convênio
  // institucional. Não há como renderizar como "camada de mapa".
  //
  // O tratamento desses dados no AgroJus acontece em:
  //   - Ficha do imóvel /imoveis/[car] aba "Cadeia Dominial" (consulta paga on-demand)
  //   - Upload manual de PDF de matrícula com OCR + análise documental
  //   - Campo de texto livre onde usuário cola teor da matrícula
  // Ver docs/research/catalog-layers-complete.md seção "Cartorial".

  // ============== AMBIENTAL (8) ==============
  { id: "unidades_conservacao", name: "UCs Federais (ICMBio)", description: "346 UCs — parques, APAs, reservas biológicas", category: "ambiental", color: "#0EA5E9", endpoint: "postgis", minZoom: 6, maxFeatures: 500, geometryType: "polygon", source: "ICMBio/MMA",
    inspectorFields: ["nomeuc","siglacateg","grupouc","esferaadm","criacaoano","areahaalb","biomas","ufabrang"] },
  { id: "ucs_estaduais", name: "UCs Estaduais", description: "Parques e APAs estaduais (complementa federais)", category: "ambiental", color: "#06B6D4", endpoint: "stub", minZoom: 6, maxFeatures: 500, comingSoon: true, source: "SEMAS estaduais" },
  { id: "embargos_icmbio", name: "Embargos ICMBio", description: "Embargos em UCs federais", category: "ambiental", color: "#EF4444", endpoint: "postgis", minZoom: 7, maxFeatures: 500, geometryType: "polygon", source: "ICMBio",
    inspectorFields: ["numero_emb","data","nome_uc","municipio","uf","area","desc_infra","julgamento","autuado","cpf_cnpj"] },
  { id: "autos_icmbio", name: "Autos de Infração ICMBio", description: "Autos ambientais em UCs federais", category: "ambiental", color: "#F43F5E", endpoint: "postgis", minZoom: 7, maxFeatures: 500, geometryType: "polygon", source: "ICMBio",
    inspectorFields: ["numero_ai","data","autuado","cpf_cnpj","nome_uc","municipio","uf","tipo_infra","valor_mult","julgamento"] },
  { id: "embargos_ibama_pontos", name: "Áreas Embargadas IBAMA", description: "104k embargos com CPF/CNPJ autuados — IBAMA", category: "ambiental", color: "#B91C1C", endpoint: "stub", minZoom: 6, maxFeatures: 2000, comingSoon: true, source: "IBAMA dados abertos" },
  { id: "autos_ibama", name: "Autos de Infração IBAMA (pontos)", description: "16k+ autos georreferenciados — dados abertos SIFISC 2026", category: "ambiental", color: "#DC2626", endpoint: "postgis", minZoom: 5, maxFeatures: 3000, geometryType: "point", source: "IBAMA SIFISC",
    inspectorFields: ["num_auto","data_auto","nome","cpf_cnpj","descricao","valor","municipio","uf"] },
  { id: "ctf_ibama", name: "CTF/APP IBAMA", description: "Cadastro Técnico Federal — atividades poluidoras registradas", category: "ambiental", color: "#DC2626", endpoint: "stub", minZoom: 8, maxFeatures: 1000, comingSoon: true, source: "IBAMA CTF" },
  { id: "zee_estaduais", name: "Zoneamento Ecológico-Econômico", description: "ZEE por estado — zonas de uso e restrição", category: "ambiental", color: "#15803D", endpoint: "stub", minZoom: 5, maxFeatures: 500, comingSoon: true, source: "Governos estaduais" },
  { id: "biomas_brasil", name: "Biomas Brasileiros", description: "6 biomas + Zona Costeira — limites IBGE", category: "ambiental", color: "#16A34A", endpoint: "stub", minZoom: 3, maxFeatures: 10, comingSoon: true, source: "IBGE" },

  // ============== DESMATAMENTO (5) ==============
  { id: "prodes", name: "PRODES (desmatamento anual consolidado)", description: "Desmatamento anual 2000-2024 — INPE. Corte MCR 2.9", category: "desmatamento", color: "#7E22CE", endpoint: "postgis", minZoom: 6, maxFeatures: 500, geometryType: "polygon", source: "INPE/TerraBrasilis",
    inspectorFields: ["class_name","main_class","year","state","area_km","image_date","satellite","sensor"] },
  { id: "deter_amazonia", name: "DETER Amazônia (tempo real)", description: "Alertas diários DETER — bioma Amazônia", category: "desmatamento", color: "#F59E0B", endpoint: "postgis", minZoom: 6, maxFeatures: 1000, geometryType: "polygon", source: "INPE",
    inspectorFields: ["classname","view_date","sensor","satellite","areamunkm","municipali","uf"] },
  { id: "deter_cerrado", name: "DETER Cerrado (tempo real)", description: "Alertas diários DETER — bioma Cerrado", category: "desmatamento", color: "#F97316", endpoint: "postgis", minZoom: 6, maxFeatures: 1000, geometryType: "polygon", source: "INPE",
    inspectorFields: ["classname","view_date","sensor","satellite","areatotalkm","municipality","uf"] },
  { id: "mapbiomas_alertas", name: "MapBiomas Alertas (validados)", description: "515k+ alertas cruzados com CAR — todas fontes integradas", category: "desmatamento", color: "#DC2626", endpoint: "postgis", minZoom: 7, maxFeatures: 1000, geometryType: "polygon", source: "MapBiomas Alerta",
    inspectorFields: ["CODEALERTA","DATADETEC","BIOMA","ESTADO","MUNICIPIO","AREAHA","FONTE","VPRESSAO"] },
  { id: "mapbiomas_desmat_acumulado", name: "MapBiomas Desmatamento Acumulado", description: "Perda acumulada 1985-2024 — histórico total", category: "desmatamento", color: "#991B1B", endpoint: "gee", minZoom: 5, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Coleção 10 via GEE" },

  // ============== FOGO (4) ==============
  { id: "mapbiomas_fogo_anual", name: "Cicatrizes de Fogo Anuais", description: "Áreas queimadas por ano desde 1985", category: "fogo", color: "#DC2626", endpoint: "gee", minZoom: 6, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Fogo" },
  { id: "mapbiomas_fogo_mensal", name: "Cicatrizes de Fogo Mensais", description: "Áreas queimadas mês-a-mês desde 2019 (Sentinel)", category: "fogo", color: "#EF4444", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Fogo" },
  { id: "mapbiomas_fogo_frequencia", name: "Frequência de Fogo", description: "Nº de vezes que o pixel queimou em 40 anos", category: "fogo", color: "#F43F5E", endpoint: "gee", minZoom: 6, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Fogo" },
  { id: "focos_inpe", name: "Focos de Calor INPE (BDQueimadas)", description: "Focos diários via satélite — antes do mapeamento consolidado", category: "fogo", color: "#FB923C", endpoint: "stub", minZoom: 7, maxFeatures: 2000, comingSoon: true, source: "INPE BDQueimadas" },

  // ============== VEGETAÇÃO SECUNDÁRIA (3) ==============
  { id: "mapbiomas_vegsec_anual", name: "Vegetação Secundária Anual", description: "Áreas em regeneração por ano", category: "vegetacao_sec", color: "#4ADE80", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Recuperação" },
  { id: "mapbiomas_vegsec_idade", name: "Idade da Vegetação Secundária", description: "Anos desde abandono/plantio (restauração ativa ou natural)", category: "vegetacao_sec", color: "#22C55E", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Recuperação" },
  { id: "prad_cumprimento", name: "PRAD — Cumprimento", description: "Cruzamento PRAD registrado × vegetação secundária detectada", category: "vegetacao_sec", color: "#16A34A", endpoint: "stub", minZoom: 10, maxFeatures: 200, comingSoon: true, source: "AgroJus (derivado)" },

  // ============== DEGRADAÇÃO (3) ==============
  { id: "mapbiomas_degrad_borda", name: "Degradação — Tamanho de Borda", description: "Efeito borda florestal acumulado", category: "degradacao", color: "#FB923C", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Degradação" },
  { id: "mapbiomas_degrad_fragmento", name: "Degradação — Tamanho Fragmento", description: "Fragmentação florestal (isolamento)", category: "degradacao", color: "#F97316", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Degradação" },
  { id: "mapbiomas_degrad_freq_fogo", name: "Degradação — Frequência Fogo", description: "Frequência de fogo como proxy de degradação", category: "degradacao", color: "#EA580C", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Degradação" },

  // ============== AGRICULTURA (MapBiomas + derivados) (14) ==============
  { id: "mapbiomas_agri_soja", name: "Soja (MapBiomas)", description: "Área de soja mapeada anualmente 1985-2024", category: "agricultura", color: "#FBBF24", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_milho", name: "Milho (1ª e 2ª safra)", description: "Diferencia primeira e segunda safra", category: "agricultura", color: "#F59E0B", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_cana", name: "Cana-de-Açúcar", description: "Área canavieira mapeada", category: "agricultura", color: "#CA8A04", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_cafe", name: "Café", description: "Lavouras permanentes de café", category: "agricultura", color: "#78350F", endpoint: "gee", minZoom: 9, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_algodao", name: "Algodão", description: "Área algodoeira mapeada", category: "agricultura", color: "#F3F4F6", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_arroz", name: "Arroz", description: "Arroz inundado + sequeiro", category: "agricultura", color: "#D4D4D4", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_citrus", name: "Citrus (laranja, limão)", description: "Lavoura perene citrus — MapBiomas", category: "agricultura", color: "#FB923C", endpoint: "gee", minZoom: 9, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_silvicultura", name: "Silvicultura", description: "Eucalipto + pinus + outras — MapBiomas", category: "agricultura", color: "#22C55E", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_irrigacao", name: "Sistemas de Irrigação", description: "Pivôs centrais + outras técnicas detectados", category: "agricultura", color: "#38BDF8", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_2safra", name: "Uso Agrícola 2ª Safra", description: "Áreas que fazem safrinha (milho, soja 2ª, etc.)", category: "agricultura", color: "#EAB308", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "mapbiomas_agri_rotacao", name: "Rotação de Cultivos (derivado)", description: "Sequência detectada ano-a-ano (ex: soja 3a → milho 2a → pousio)", category: "agricultura", color: "#65A30D", endpoint: "stub", minZoom: 10, maxFeatures: 0, comingSoon: true, source: "AgroJus derivado MapBiomas" },
  { id: "mapbiomas_agri_frequencia", name: "Frequência Média de Cultivo", description: "Pixels com mais anos sob agricultura", category: "agricultura", color: "#F59E0B", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Agricultura" },
  { id: "satveg_ndvi", name: "NDVI Histórico (SATVeg Embrapa)", description: "Vigor vegetativo por pixel 250m desde 2000", category: "agricultura", color: "#16A34A", endpoint: "external", endpointId: "satveg", minZoom: 9, maxFeatures: 0, comingSoon: true, source: "Embrapa SATVeg MODIS" },
  { id: "mapbiomas_expansao_fronteira", name: "Expansão da Fronteira Agrícola", description: "Áreas convertidas de natural para agrícola ano a ano", category: "agricultura", color: "#F97316", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "AgroJus derivado MapBiomas" },

  // ============== PASTAGEM (4) ==============
  { id: "mapbiomas_past_vigor", name: "Vigor da Pastagem", description: "Qualidade via NDVI: alto/médio/baixo vigor", category: "pastagem", color: "#84CC16", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Pastagem" },
  { id: "mapbiomas_past_idade", name: "Idade da Pastagem", description: "Anos desde conversão → proxy de degradação", category: "pastagem", color: "#65A30D", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Pastagem" },
  { id: "mapbiomas_past_biomassa", name: "Biomassa da Pastagem", description: "Produção estimada ton/ha", category: "pastagem", color: "#4D7C0F", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Pastagem" },
  { id: "mapbiomas_past_transicao", name: "Transições de Pastagem", description: "Pasto ↔ agricultura ↔ floresta", category: "pastagem", color: "#3F6212", endpoint: "gee", minZoom: 8, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Pastagem" },

  // ============== ÁGUA (5) ==============
  { id: "ana_bho", name: "BHO — Rios e Bacias (ANA)", description: "Base Hidrográfica Ottocodificada 12 níveis", category: "agua", color: "#06B6D4", endpoint: "stub", minZoom: 7, maxFeatures: 2000, comingSoon: true, source: "ANA/SNIRH" },
  { id: "ana_outorgas", name: "Outorgas ANA", description: "Direitos de uso de água registrados", category: "agua", color: "#0891B2", endpoint: "stub", minZoom: 8, maxFeatures: 1000, comingSoon: true, source: "ANA" },
  { id: "ana_hidroweb_estacoes", name: "Estações Fluviométricas", description: "Rede de monitoramento de rios", category: "agua", color: "#0E7490", endpoint: "stub", minZoom: 8, maxFeatures: 500, comingSoon: true, source: "ANA Hidroweb" },
  { id: "atlas_irrigacao_ana", name: "Atlas de Irrigação 2021", description: "Pivôs centrais catalogados pela ANA", category: "agua", color: "#22D3EE", endpoint: "stub", minZoom: 9, maxFeatures: 500, comingSoon: true, source: "ANA" },
  { id: "mapbiomas_agua_anual", name: "Superfície d'Água (MapBiomas)", description: "Permanente vs sazonal, série 1985+", category: "agua", color: "#67E8F9", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Água" },

  // ============== SOLO (5) ==============
  { id: "embrapa_solos", name: "SmartSolos (Embrapa)", description: "Classificação + textura + carbono via AgroAPI", category: "solo", color: "#78350F", endpoint: "external", endpointId: "smartsolos", minZoom: 8, maxFeatures: 0, comingSoon: true, source: "Embrapa AgroAPI" },
  { id: "aptidao_agricola_ibge", name: "Aptidão Agrícola das Terras", description: "Classes 1-6 por vocação agrícola", category: "solo", color: "#92400E", endpoint: "stub", minZoom: 7, maxFeatures: 0, comingSoon: true, source: "EMBRAPA/IBGE" },
  { id: "mapbiomas_solo_carbono", name: "Carbono Orgânico no Solo", description: "Estoque de carbono por pixel — MapBiomas Solo", category: "solo", color: "#451A03", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Solo" },
  { id: "mapbiomas_solo_textura", name: "Textura do Solo", description: "Fração areia/silte/argila — MapBiomas", category: "solo", color: "#A16207", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Solo" },
  { id: "ibge_pedologia", name: "Pedologia IBGE", description: "Mapa de solos oficial do IBGE", category: "solo", color: "#854D0E", endpoint: "stub", minZoom: 5, maxFeatures: 0, comingSoon: true, source: "IBGE" },

  // ============== MINERAÇÃO (3) ==============
  { id: "sigmine_anm", name: "SIGMINE (processos minerários)", description: "Pesquisa, lavra, concessão — ANM", category: "mineracao", color: "#A78BFA", endpoint: "stub", minZoom: 7, maxFeatures: 2000, comingSoon: true, source: "ANM" },
  { id: "mapbiomas_mineracao_industrial", name: "Mineração Industrial", description: "Áreas mineradoras legais mapeadas", category: "mineracao", color: "#8B5CF6", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Mineração" },
  { id: "mapbiomas_garimpo", name: "Garimpos (MapBiomas)", description: "Garimpo detectado — cruza com ANM p/ legalidade", category: "mineracao", color: "#7C3AED", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Mineração" },

  // ============== INFRAESTRUTURA (9) ==============
  { id: "rodovias_federais", name: "Rodovias Federais", description: "Malha BRs — DNIT", category: "infraestrutura", color: "#FBBF24", endpoint: "postgis", minZoom: 6, maxFeatures: 3000, geometryType: "line", source: "DNIT",
    inspectorFields: ["tipovia","jurisdicao","revestimen","operaciona"] },
  { id: "rodovias_estaduais", name: "Rodovias Estaduais", description: "Malha estadual — DERs", category: "infraestrutura", color: "#FDE047", endpoint: "stub", minZoom: 7, maxFeatures: 3000, comingSoon: true, source: "DERs" },
  { id: "ferrovias", name: "Ferrovias", description: "Malha ferroviária — ANTT", category: "infraestrutura", color: "#A78BFA", endpoint: "postgis", minZoom: 6, maxFeatures: 2000, geometryType: "line", source: "ANTT/DNIT",
    inspectorFields: ["SIGLA","BITOLA","CATEGORIA","NAME","TIP_SITUAC"] },
  { id: "portos", name: "Portos", description: "Marítimos e fluviais — ANTAQ", category: "infraestrutura", color: "#38BDF8", endpoint: "postgis", minZoom: 4, maxFeatures: 200, geometryType: "point", source: "ANTAQ",
    inspectorFields: ["nome","tipo","cidade","estado","modalidade","situacao"] },
  { id: "aeroportos", name: "Aeroportos", description: "ANAC — aeródromos homologados", category: "infraestrutura", color: "#60A5FA", endpoint: "stub", minZoom: 5, maxFeatures: 500, comingSoon: true, source: "ANAC" },
  { id: "terminais_intermodais", name: "Terminais Intermodais", description: "Nós logísticos ANTT/ANTAQ", category: "infraestrutura", color: "#818CF8", endpoint: "stub", minZoom: 7, maxFeatures: 200, comingSoon: true, source: "ANTT/ANTAQ" },
  { id: "armazens_silos", name: "Armazéns e Silos", description: "~16k unidades — CONAB SICARM", category: "infraestrutura", color: "#F59E0B", endpoint: "postgis", minZoom: 8, maxFeatures: 3000, geometryType: "point", source: "CONAB SICARM" },
  { id: "frigorificos", name: "Frigoríficos (SIF)", description: "Frigoríficos habilitados — MAPA SIF", category: "infraestrutura", color: "#F87171", endpoint: "postgis", minZoom: 6, maxFeatures: 500, geometryType: "point", source: "MAPA SIF" },
  { id: "cnt_condicao_rodovias", name: "Condição das Rodovias (CNT)", description: "Nota CNT por trecho (pavimento, sinalização)", category: "infraestrutura", color: "#FCD34D", endpoint: "stub", minZoom: 6, maxFeatures: 5000, comingSoon: true, source: "CNT Pesquisa Rodovias" },

  // ============== ENERGIA (3) ==============
  { id: "aneel_usinas", name: "Usinas Elétricas (ANEEL)", description: "Hidro, termo, solar, eólica — ANEEL BIG", category: "energia", color: "#FACC15", endpoint: "stub", minZoom: 5, maxFeatures: 2000, comingSoon: true, source: "ANEEL" },
  { id: "aneel_linhas_transmissao", name: "Linhas de Transmissão", description: "Alta tensão — ONS/ANEEL", category: "energia", color: "#EAB308", endpoint: "stub", minZoom: 5, maxFeatures: 2000, comingSoon: true, source: "ONS/ANEEL" },
  { id: "aneel_subestacoes", name: "Subestações Elétricas", description: "Nós da rede — ANEEL", category: "energia", color: "#CA8A04", endpoint: "stub", minZoom: 7, maxFeatures: 1000, comingSoon: true, source: "ANEEL" },

  // ============== CRÉDITO (3) ==============
  { id: "mapbiomas_credito_rural", name: "Crédito Rural (MapBiomas)", description: "5.6M+ parcelas financiadas — SICOR×MapBiomas", category: "credito", color: "#3B82F6", endpoint: "postgis", minZoom: 12, maxFeatures: 300, geometryType: "polygon", source: "SICOR×MapBiomas",
    inspectorFields: ["order_number","year","car_code","vl_parc_credito","vl_area_financ","dt_emissao","cnpj_if"] },
  { id: "bcb_sicor_choropleth", name: "SICOR por Município (choropleth)", description: "Volume de crédito rural por município — BCB SICOR", category: "credito", color: "#2563EB", endpoint: "stub", minZoom: 4, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "BCB SICOR OData" },
  { id: "garantia_safra", name: "Garantia-Safra (beneficiários)", description: "Semiárido — Portal Transparência", category: "credito", color: "#1D4ED8", endpoint: "stub", minZoom: 5, maxFeatures: 5000, comingSoon: true, source: "Portal da Transparência" },

  // ============== PRODUÇÃO AGRÍCOLA IBGE (choropleth via SIDRA t.1612) (10) ==============
  // Endpoint: /api/v1/geo/ibge/choropleth/{metric_id}/{ano}?uf=<UF>
  { id: "ibge_pam_soja", name: "Produção Soja (IBGE PAM)", description: "Quantidade produzida (ton) por município — SIDRA Tabela 1612", category: "producao_ibge", color: "#EAB308", endpoint: "ibge_choropleth", endpointId: "pam_soja", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA 1612" },
  { id: "ibge_pam_milho", name: "Produção Milho", description: "IBGE PAM — SIDRA Tabela 1612", category: "producao_ibge", color: "#FBBF24", endpoint: "ibge_choropleth", endpointId: "pam_milho", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_cana", name: "Produção Cana-de-Açúcar", description: "IBGE PAM — ton", category: "producao_ibge", color: "#CA8A04", endpoint: "ibge_choropleth", endpointId: "pam_cana", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_cafe", name: "Produção Café", description: "IBGE PAM — ton", category: "producao_ibge", color: "#78350F", endpoint: "ibge_choropleth", endpointId: "pam_cafe", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_algodao", name: "Produção Algodão", description: "IBGE PAM — ton", category: "producao_ibge", color: "#F3F4F6", endpoint: "ibge_choropleth", endpointId: "pam_algodao", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_arroz", name: "Produção Arroz", description: "IBGE PAM — ton", category: "producao_ibge", color: "#FEF3C7", endpoint: "ibge_choropleth", endpointId: "pam_arroz", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_feijao", name: "Produção Feijão", description: "IBGE PAM — ton", category: "producao_ibge", color: "#A16207", endpoint: "ibge_choropleth", endpointId: "pam_feijao", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_trigo", name: "Produção Trigo", description: "IBGE PAM — ton", category: "producao_ibge", color: "#D97706", endpoint: "ibge_choropleth", endpointId: "pam_trigo", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_area_soja", name: "Área Colhida Soja", description: "Hectares colhidos de soja por município", category: "producao_ibge", color: "#65A30D", endpoint: "ibge_choropleth", endpointId: "pam_area_soja", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pam_valor_soja", name: "Valor Produção Soja", description: "R$ mil por município — IBGE PAM", category: "producao_ibge", color: "#84CC16", endpoint: "ibge_choropleth", endpointId: "pam_valor_soja", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },

  // ============== PECUÁRIA IBGE (choropleth via SIDRA t.3939) (4) ==============
  { id: "ibge_ppm_bovino", name: "Rebanho Bovino (IBGE PPM)", description: "Efetivo bovino por município — Tabela 3939", category: "pecuaria_ibge", color: "#BE123C", endpoint: "ibge_choropleth", endpointId: "ppm_bovinos", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA PPM" },
  { id: "ibge_ppm_ovino", name: "Rebanho Ovino", description: "IBGE PPM 3939", category: "pecuaria_ibge", color: "#E11D48", endpoint: "ibge_choropleth", endpointId: "ppm_ovinos", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_ppm_suino", name: "Rebanho Suíno", description: "IBGE PPM 3939", category: "pecuaria_ibge", color: "#F43F5E", endpoint: "ibge_choropleth", endpointId: "ppm_suinos", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_ppm_bubalinos", name: "Rebanho Bubalino", description: "IBGE PPM 3939", category: "pecuaria_ibge", color: "#FB7185", endpoint: "ibge_choropleth", endpointId: "ppm_bubalinos", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },

  // ============== SOCIOECONÔMICO (5) ==============
  { id: "idhm_pnud", name: "IDHM (PNUD/IPEA/FJP)", description: "Índice de Desenvolvimento Humano Municipal", category: "socioeconomico", color: "#8B5CF6", endpoint: "stub", minZoom: 4, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "PNUD/IPEA" },
  { id: "ibge_pib_municipal", name: "PIB Total Municipal", description: "IBGE SIDRA 5938 — R$ mil", category: "socioeconomico", color: "#A78BFA", endpoint: "ibge_choropleth", endpointId: "pib_total", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_pib_per_capita", name: "PIB per capita", description: "IBGE SIDRA 5938 — R$ per capita", category: "socioeconomico", color: "#7C3AED", endpoint: "ibge_choropleth", endpointId: "pib_per_capita", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_populacao", name: "População Estimada", description: "IBGE SIDRA 6579 — habitantes", category: "socioeconomico", color: "#C084FC", endpoint: "ibge_choropleth", endpointId: "populacao", minZoom: 4, maxFeatures: 5570, geometryType: "choropleth", source: "IBGE SIDRA" },
  { id: "ibge_regic_2018", name: "REGIC — Hierarquia Urbana", description: "Metrópole → Capital Reg. → Centro Local — influência urbana", category: "socioeconomico", color: "#9333EA", endpoint: "stub", minZoom: 4, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "IBGE REGIC 2018" },
  { id: "cnes_estabelecimentos", name: "Estabelecimentos de Saúde (CNES)", description: "Hospitais, postos, leitos — DataSUS", category: "socioeconomico", color: "#D946EF", endpoint: "stub", minZoom: 7, maxFeatures: 2000, comingSoon: true, source: "DataSUS CNES" },

  // ============== CLIMA (7) ==============
  { id: "inmet_estacoes", name: "Estações INMET", description: "~600 estações automáticas + convencionais", category: "clima", color: "#0EA5E9", endpoint: "stub", minZoom: 6, maxFeatures: 700, comingSoon: true, source: "INMET APITempo" },
  { id: "nasa_power_overlay", name: "Clima NASA POWER (overlay)", description: "Temperatura, precipitação por grid 0.5° — global 1981+", category: "clima", color: "#38BDF8", endpoint: "stub", minZoom: 5, maxFeatures: 0, comingSoon: true, source: "NASA POWER" },
  { id: "chirps_precipitacao", name: "CHIRPS Precipitação", description: "Precipitação 5km diária 1981+ via GEE", category: "clima", color: "#06B6D4", endpoint: "gee", minZoom: 5, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "UCSB CHIRPS" },
  { id: "zarc_aptidao", name: "ZARC — Aptidão Climática", description: "Zoneamento Agrícola de Risco por cultura/município — Embrapa", category: "clima", color: "#F97316", endpoint: "external", endpointId: "zarc", minZoom: 5, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "Embrapa AgroAPI ZARC" },
  { id: "zarc_janela_plantio", name: "Janela de Plantio (ZARC)", description: "Dekêndios aptos por cultura/município — Portaria MAPA", category: "clima", color: "#EA580C", endpoint: "external", endpointId: "zarc_janela", minZoom: 5, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "Embrapa AgroAPI + MAPA" },
  { id: "climapi_embrapa", name: "ClimAPI Embrapa", description: "Clima histórico 6h resolução — Embrapa AgroAPI", category: "clima", color: "#0284C7", endpoint: "external", endpointId: "climapi", minZoom: 6, maxFeatures: 0, comingSoon: true, source: "Embrapa ClimAPI" },
  { id: "agritec_embrapa", name: "Agritec — Recomendação Cultivo", description: "Recomendações de cultivo por coordenada — Embrapa", category: "clima", color: "#0369A1", endpoint: "external", endpointId: "agritec", minZoom: 7, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "Embrapa Agritec v2" },

  // ============== ATMOSFERA (MapBiomas) (3) ==============
  { id: "mapbiomas_atmo_temp", name: "Temperatura (MapBiomas)", description: "Série temperatura atmosférica", category: "atmosfera", color: "#DC2626", endpoint: "gee", minZoom: 5, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Atmosfera" },
  { id: "mapbiomas_atmo_precip", name: "Precipitação e Água (MapBiomas)", description: "Mapeamento de precipitação", category: "atmosfera", color: "#06B6D4", endpoint: "gee", minZoom: 5, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Atmosfera" },
  { id: "mapbiomas_atmo_qual_ar", name: "Qualidade do Ar", description: "MapBiomas Atmosfera qualidade do ar", category: "atmosfera", color: "#6B7280", endpoint: "gee", minZoom: 5, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Atmosfera" },

  // ============== RISCO CLIMÁTICO (3) ==============
  { id: "mapbiomas_risco_deslizamento", name: "Áreas Suscetíveis a Deslizamentos", description: "Áreas urbanas — MapBiomas Risco", category: "risco_climatico", color: "#EA580C", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Risco Climático" },
  { id: "mapbiomas_risco_inundacao", name: "Áreas de Inundação/Enxurrada", description: "Áreas urbanas suscetíveis — MapBiomas Risco", category: "risco_climatico", color: "#0284C7", endpoint: "gee", minZoom: 7, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Risco Climático" },
  { id: "mapbiomas_seguranca_hidrica", name: "Índice de Segurança Hídrica", description: "Mapa nacional de estresse hídrico", category: "risco_climatico", color: "#0369A1", endpoint: "gee", minZoom: 5, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Risco Climático" },

  // ============== URBANO (3) ==============
  { id: "mapbiomas_urbano", name: "Urbanização Anual (MapBiomas)", description: "Expansão urbana 1985-2024", category: "urbano", color: "#94A3B8", endpoint: "gee", minZoom: 6, maxFeatures: 0, geometryType: "raster", comingSoon: true, source: "MapBiomas Urbano" },
  { id: "ibge_malha_municipal", name: "Limites Municipais", description: "5.570 municípios brasileiros", category: "urbano", color: "#64748B", endpoint: "stub", minZoom: 5, maxFeatures: 5570, comingSoon: true, source: "IBGE Malhas" },
  { id: "ibge_malha_estadual", name: "Limites Estaduais", description: "27 estados + DF", category: "urbano", color: "#475569", endpoint: "stub", minZoom: 3, maxFeatures: 28, comingSoon: true, source: "IBGE Malhas" },

  // ============== JURÍDICO (3) ==============
  { id: "autos_ibama_pontos", name: "Autos de Infração IBAMA (pontos)", description: "Georreferenciados a partir de municípios/CPFs", category: "juridico", color: "#EC4899", endpoint: "stub", minZoom: 6, maxFeatures: 2000, comingSoon: true, source: "IBAMA dados abertos" },
  { id: "datajud_por_municipio", name: "Processos DataJud por Município", description: "Choropleth — densidade processual agrária/ambiental", category: "juridico", color: "#DB2777", endpoint: "stub", minZoom: 4, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "DataJud CNJ" },
  { id: "djen_por_oab", name: "Publicações DJEN por OAB", description: "Agregação de intimações dos clientes da carteira", category: "juridico", color: "#BE185D", endpoint: "stub", minZoom: 5, maxFeatures: 1000, comingSoon: true, source: "DJEN Comunica.PJe" },

  // ============== FISCAL / COMPLIANCE (4) ==============
  { id: "ceis_por_municipio", name: "CEIS (Empresas Inidôneas)", description: "Cadastro Nacional de Inidôneas — Portal Transparência", category: "fiscal", color: "#DB2777", endpoint: "stub", minZoom: 4, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "Portal da Transparência" },
  { id: "cnep_por_municipio", name: "CNEP (Empresas Punidas Anticorrupção)", description: "Lei 12.846 — Portal Transparência", category: "fiscal", color: "#BE185D", endpoint: "stub", minZoom: 4, maxFeatures: 5570, comingSoon: true, geometryType: "choropleth", source: "Portal da Transparência" },
  { id: "lista_suja_mte", name: "Lista Suja MTE (Trabalho Escravo)", description: "Pontos de CPF/CNPJ autuados", category: "fiscal", color: "#9F1239", endpoint: "stub", minZoom: 5, maxFeatures: 1000, comingSoon: true, source: "MTE" },
  { id: "cndt_por_uf", name: "CNDT (Débitos Trabalhistas)", description: "Choropleth por UF — TST", category: "fiscal", color: "#881337", endpoint: "stub", minZoom: 4, maxFeatures: 27, comingSoon: true, geometryType: "choropleth", source: "TST CNDT" },
];

// =============================================================================
// Helpers
// =============================================================================

export function layersByCategory(cat: LayerCategory): LayerConfig[] {
  return LAYERS.filter((l) => l.category === cat);
}

export function getLayer(id: string): LayerConfig | undefined {
  return LAYERS.find((l) => l.id === id);
}

export function countByTheme(): Record<LayerCategory, number> {
  return LAYERS.reduce(
    (acc, l) => {
      acc[l.category] = (acc[l.category] || 0) + 1;
      return acc;
    },
    {} as Record<LayerCategory, number>
  );
}

export function countActiveLayers(): number {
  return LAYERS.filter((l) => !l.comingSoon).length;
}

export function countComingSoonLayers(): number {
  return LAYERS.filter((l) => l.comingSoon).length;
}
