/**
 * AgroJus — GIS Engine v2
 *
 * Motor geoespacial completo com:
 *  - Multi-layer overlay (empilha camadas sem apagar)
 *  - Estilização dinâmica por tipo de camada
 *  - Base Map Switcher (Satélite / Terreno / OSM)
 *  - Right-click → Análise de Ponto (FUNAI, DETER, IBGE, Clima, Jurisdição)
 *  - Bounding Box Search (Shift+drag → busca retangular)
 *  - Coordenada Picker (click esquerdo → copia lat,lon)
 *  - Legenda dinâmica das camadas ativas
 *  - Feature counter no HUD
 */

import L from 'leaflet';

let map = null;
let layerGroup = null;
let activeLayers = {};   // { layerId: L.geoJSON instance }
let featureCount = 0;
let currentBasemap = 'satellite';

// ── Base Tiles ──────────────────────────────────────────────
const BASEMAPS = {
  satellite: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Esri, Maxar, Earthstar', maxZoom: 18,
  }),
  terrain: L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenTopoMap', maxZoom: 17,
  }),
  osm: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors', maxZoom: 19,
  }),
};

const LABELS = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
  maxZoom: 18, pane: 'overlayPane',
});

// ── Layer Styles ────────────────────────────────────────────
const LAYER_STYLES = {
  embargos:                { color: '#ef4444', weight: 2, fillOpacity: 0.4, fillColor: '#f87171' },
  terras_indigenas:        { color: '#f59e0b', weight: 2, fillOpacity: 0.3, fillColor: '#fbbf24', dashArray: '5,5' },
  desmatamento:            { color: '#dc2626', weight: 1, fillOpacity: 0.5, fillColor: '#ef4444' },
  desmatamento_cerrado:    { color: '#ea580c', weight: 1, fillOpacity: 0.5, fillColor: '#fb923c' },
  municipios:              { color: '#94a3b8', weight: 1, fillOpacity: 0.05, fillColor: '#e2e8f0' },
  parcelas_financiamento:  { color: '#10b981', weight: 2, fillOpacity: 0.3, fillColor: '#34d399' },
};

const LAYER_LABELS = {
  embargos:                '🔴 Embargos IBAMA',
  terras_indigenas:        '🟡 Terras Indígenas',
  desmatamento:            '🔥 Desmatamento Amazônia',
  desmatamento_cerrado:    '🔥 Desmatamento Cerrado',
  municipios:              '⬜ Malha Municipal',
  parcelas_financiamento:  '🟢 Crédito Rural',
};

const DEFAULT_STYLE = { color: '#8b5cf6', weight: 2, fillOpacity: 0.2 };

// ── Initialization ──────────────────────────────────────────
export function initMap(apiBaseUrl) {
  if (map) {
    map.invalidateSize();
    return;
  }

  map = L.map('gis-map', {
    center: [-14.0, -52.0],
    zoom: 5,
    zoomControl: false,
    attributionControl: false,
  });

  // Zoom control top-right
  L.control.zoom({ position: 'topright' }).addTo(map);

  // Attribution bottom-right (compact)
  L.control.attribution({ position: 'bottomright', prefix: false }).addTo(map);

  // Default basemap
  BASEMAPS.satellite.addTo(map);
  LABELS.addTo(map);

  layerGroup = L.layerGroup().addTo(map);

  // Wire everything
  setupRightClickAnalysis(apiBaseUrl);
  setupLayerControls(apiBaseUrl);
  setupBasemapSwitcher();
  setupCoordPicker();
  setupBboxSearch(apiBaseUrl);

  updateHUD('AgroJus GIS Engine v2 online. Click direito → Análise de ponto. Shift+drag → Busca retangular.');
}

// ── Right-Click → Full Point Analysis ───────────────────────
function setupRightClickAnalysis(API) {
  map.on('contextmenu', async (e) => {
    const { lat, lng } = e.latlng;
    updateHUD(`<span class="hud-loading">⏳</span> Interrogando <b>${lat.toFixed(5)}, ${lng.toFixed(5)}</b> …`);

    // Pulse marker imediato (feedback visual)
    const pulseMarker = L.circleMarker([lat, lng], {
      radius: 14, fillColor: '#3b82f6', color: '#fff', weight: 2, fillOpacity: 0.5,
      className: 'pulse-ring-marker',
    }).addTo(layerGroup);

    try {
      const res = await fetch(`${API}/api/v1/geo/analyze-point?lat=${lat}&lon=${lng}&radius_km=5`);
      const data = await res.json();

      const risk    = data.overall_risk || 'low';
      const muni    = data.municipio?.municipio || '—';
      const estado  = data.municipio?.estado || '';
      const ts      = data.summary?.terras_indigenas || 0;
      const alerts  = data.summary?.alertas_desmatamento || 0;
      const clima   = data.clima;
      const jur     = data.jurisdicao;
      const rl      = data.reserva_legal;

      // Color by risk
      const riskColors = { critical: '#e11d48', high: '#f97316', medium: '#eab308', low: '#10b981' };
      const color = riskColors[risk] || '#10b981';
      pulseMarker.setStyle({ fillColor: color, radius: 10, fillOpacity: 0.8 });

      // Rich popup
      let popup = `
        <div style="font-family:'Inter',sans-serif; font-size:13px; min-width:260px; max-width:340px;">
          <div style="font-size:16px; font-weight:800; margin-bottom:8px; color:${color}">
            ■ Risco ${risk.toUpperCase()}
          </div>
          <div style="margin-bottom:6px"><b>📍 ${muni}</b> — ${estado}</div>
          <div style="margin-bottom:6px">🛡 Terras Indígenas: <b>${ts}</b> | 🌳 Alertas DETER: <b>${alerts}</b></div>`;

      if (clima) {
        popup += `<hr style="border:none;border-top:1px solid #e5e7eb;margin:8px 0">
          <div style="font-size:11px;color:#6b7280">
            🌡 Temp: <b>${clima.temp_media_c?.toFixed(1) || '—'}°C</b> |
            🌧 Chuva: <b>${clima.chuva_acumulada_mm?.toFixed(0) || '—'}mm</b> (${clima.dias_chuva || '—'} dias)
          </div>`;
      }

      if (jur) {
        popup += `<hr style="border:none;border-top:1px solid #e5e7eb;margin:8px 0">
          <div style="font-size:11px;color:#6b7280">
            ⚖ Justiça: <b>${jur.justica_estadual || ''}</b><br>
            📋 ITERUF: ${jur.orgao_terras || '—'}
          </div>`;
      }

      if (rl) {
        popup += `<div style="font-size:11px;margin-top:4px;color:#6b7280">
          🌿 Reserva Legal: <b>${rl.percentual_minimo || '—'}%</b> (${rl.bioma || ''})
        </div>`;
      }

      popup += `<div style="font-size:9px;color:#9ca3af;margin-top:8px">
        Coord: ${lat.toFixed(6)}, ${lng.toFixed(6)} | Fontes: FUNAI, INPE, IBGE, NASA
      </div></div>`;

      pulseMarker.bindPopup(popup, { maxWidth: 360 }).openPopup();

      // HUD summary
      updateHUD(`<b>${muni}</b> (${estado}) — Risco: <span style="color:${color};font-weight:800">${risk.toUpperCase()}</span> | TI: ${ts} | DETER: ${alerts}`);

    } catch (err) {
      pulseMarker.remove();
      updateHUD(`<span style="color:#ef4444">❌ Falha na análise: ${err.message}</span>`);
    }
  });
}

// ── Layer Controls ──────────────────────────────────────────
function setupLayerControls(API) {
  const btn = document.getElementById('gis-load-btn');
  if (!btn) return;

  btn.addEventListener('click', async () => {
    const layerId = document.getElementById('gis-layer').value;
    const uf      = document.getElementById('gis-uf').value.toUpperCase();
    if (!layerId) return;

    btn.textContent = 'Carregando...';
    btn.disabled = true;
    updateHUD(`⏳ Requisitando camada <b>${LAYER_LABELS[layerId] || layerId}</b>…`);

    try {
      const params = new URLSearchParams({ max_features: '500' });
      if (uf) params.append('uf', uf);

      const res = await fetch(`${API}/api/v1/geo/layers/${layerId}/geojson?${params}`);
      const data = await res.json();

      if (data.error) {
        updateHUD(`⚠️ ${data.error}`);
        return;
      }

      if (data.features && data.features.length > 0) {
        addGeoJSONLayer(layerId, data);
        updateHUD(`✅ <b>${LAYER_LABELS[layerId] || layerId}</b> — ${data.features.length} features renderizadas`);
      } else {
        updateHUD('⚠️ 0 features retornadas para a consulta.');
      }
    } catch (err) {
      updateHUD(`<span style="color:#ef4444">❌ Falha ao carregar camada: ${err.message}</span>`);
    } finally {
      btn.textContent = 'Renderizar';
      btn.disabled = false;
    }
  });

  // Clear button
  const clearBtn = document.getElementById('gis-clear-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      layerGroup.clearLayers();
      activeLayers = {};
      featureCount = 0;
      updateLegend();
      updateHUD('🧹 Todas as camadas limpas.');
    });
  }
}

// ── Add GeoJSON to Map ──────────────────────────────────────
function addGeoJSONLayer(layerId, data) {
  const style = LAYER_STYLES[layerId] || DEFAULT_STYLE;

  const geoLayer = L.geoJSON(data, {
    style,
    pointToLayer: (feature, latlng) => {
      return L.circleMarker(latlng, { ...style, radius: 6 });
    },
    onEachFeature: (feature, layer) => {
      const p = feature.properties || {};

      // Smart popup per layer type
      let html = `<div style="font-family:'Inter',sans-serif;font-size:13px;">`;
      html += `<div style="font-weight:700;margin-bottom:6px;color:${style.color}">${LAYER_LABELS[layerId] || layerId.toUpperCase()}</div>`;

      if (layerId === 'embargos') {
        html += `<b>CPF/CNPJ:</b> ${p.cpf_cnpj || 'N/A'}<br>`;
        html += `<b>Tipo:</b> ${p.alert_type || 'Embargo'}<br>`;
        html += `<b>Fonte:</b> ${p.source || 'IBAMA'}`;
      } else if (layerId === 'parcelas_financiamento') {
        const val = p.valor_financiado
          ? parseFloat(p.valor_financiado).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
          : 'R$ —';
        html += `<b>Financiamento:</b> ${val}<br>`;
        html += `<b>Cultura:</b> ${p.cultura || 'Agrícola'}<br>`;
        html += `<b>CPF/CNPJ:</b> ${p.cpf_cnpj || 'N/A'}`;
      } else if (layerId === 'terras_indigenas') {
        html += `<b>Nome:</b> ${p.terrai_nom || p.nome || 'TI'}<br>`;
        html += `<b>Etnia:</b> ${p.etnia_nome || p.etnias || 'Diversas'}<br>`;
        html += `<b>Fase:</b> ${p.fase_ti || p.situacao || 'Em demarcação'}<br>`;
        html += `<b>Área:</b> ${p.superficie_ha ? parseFloat(p.superficie_ha).toLocaleString('pt-BR') + ' ha' : '—'}`;
      } else if (layerId.startsWith('desmatamento')) {
        html += `<b>Classe:</b> ${p.classname || p.class_name || 'Desmatamento'}<br>`;
        html += `<b>Data:</b> ${p.view_date || p.date || '—'}<br>`;
        html += `<b>Área:</b> ${p.areamunkm || p.area_km2 ? (p.areamunkm || p.area_km2) + ' km²' : '—'}<br>`;
        html += `<b>Sensor:</b> ${p.sensor || '—'}`;
      } else if (layerId === 'municipios') {
        html += `<b>${p.NM_MUN || p.nome || 'Município'}</b><br>`;
        html += `Cód. IBGE: ${p.CD_MUN || p.codarea || '—'}`;
      } else {
        // Genérico
        const keys = Object.keys(p).slice(0, 6);
        keys.forEach(k => { html += `<b>${k}:</b> ${p[k]}<br>`; });
      }

      html += `</div>`;
      layer.bindPopup(html, { maxWidth: 320 });

      // Hover interaction
      layer.on('mouseover', function () { this.setStyle({ fillOpacity: 0.7, weight: 4 }); });
      layer.on('mouseout',  function () { geoLayer.resetStyle(this); });
    },
  });

  // Remove existing same layer if present, then add new
  if (activeLayers[layerId]) {
    layerGroup.removeLayer(activeLayers[layerId]);
    featureCount -= activeLayers[layerId].getLayers().length;
  }

  geoLayer.addTo(layerGroup);
  activeLayers[layerId] = geoLayer;
  featureCount += data.features.length;

  // Fit view
  try { map.fitBounds(geoLayer.getBounds(), { padding: [30, 30] }); } catch {}

  updateLegend();
}

// ── Basemap Switcher ────────────────────────────────────────
function setupBasemapSwitcher() {
  const switcher = document.getElementById('gis-basemap');
  if (!switcher) return;

  switcher.addEventListener('change', (e) => {
    const val = e.target.value;
    // Remove current basemap
    Object.values(BASEMAPS).forEach(layer => { if (map.hasLayer(layer)) map.removeLayer(layer); });
    // Add new
    if (BASEMAPS[val]) {
      BASEMAPS[val].addTo(map);
      map.removeLayer(LABELS);
      if (val !== 'osm') LABELS.addTo(map);
      currentBasemap = val;
    }
  });
}

// ── Coord Picker (Left Click) ───────────────────────────────
function setupCoordPicker() {
  map.on('click', (e) => {
    const { lat, lng } = e.latlng;
    const coordStr = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;

    // Copy to clipboard
    navigator.clipboard.writeText(coordStr).catch(() => {});

    updateHUD(`📋 Coordenada copiada: <b>${coordStr}</b> — Click direito para análise completa`);
  });
}

// ── Bounding Box Search (Shift+drag) ────────────────────────
function setupBboxSearch(API) {
  let bboxRect = null;

  map.on('boxzoomend', async (e) => {
    const bounds = e.boxZoomBounds;
    const sw = bounds.getSouthWest();
    const ne = bounds.getNorthEast();
    const bbox = `${sw.lng},${sw.lat},${ne.lng},${ne.lat}`;

    if (bboxRect) map.removeLayer(bboxRect);
    bboxRect = L.rectangle(bounds, {
      color: '#3b82f6', weight: 2, fillOpacity: 0.08, dashArray: '6,4',
    }).addTo(map);

    updateHUD(`⏳ Buscando features na BBox: <code>${bbox}</code>…`);

    // Search DETER alerts inside the bounding box
    try {
      const res = await fetch(`${API}/api/v1/geo/layers/desmatamento/geojson?bbox=${bbox}&max_features=300`);
      const data = await res.json();

      if (data.features && data.features.length > 0) {
        addGeoJSONLayer('desmatamento', data);
        updateHUD(`🔍 BBox Search: <b>${data.features.length}</b> alertas de desmatamento encontrados na região`);
      } else {
        updateHUD('✅ BBox Search: nenhum alerta de desmatamento na região selecionada');
      }
    } catch (err) {
      updateHUD(`<span style="color:#ef4444">❌ BBox search falhou: ${err.message}</span>`);
    }
  });
}

// ── Dynamic Legend ──────────────────────────────────────────
function updateLegend() {
  let legendEl = document.getElementById('gis-legend');
  if (!legendEl) {
    legendEl = document.createElement('div');
    legendEl.id = 'gis-legend';
    legendEl.className = 'gis-legend glass-hud';
    const overlay = document.querySelector('.map-hud-overlay');
    if (overlay) overlay.appendChild(legendEl);
  }

  const keys = Object.keys(activeLayers);
  if (keys.length === 0) {
    legendEl.style.display = 'none';
    return;
  }

  legendEl.style.display = 'block';
  let html = `<div class="legend-title">Camadas Ativas (${featureCount} features)</div>`;
  keys.forEach(k => {
    const style = LAYER_STYLES[k] || DEFAULT_STYLE;
    const label = LAYER_LABELS[k] || k;
    const count = activeLayers[k].getLayers().length;
    html += `
      <div class="legend-item">
        <span class="legend-swatch" style="background:${style.fillColor || style.color};border:2px solid ${style.color}"></span>
        <span class="legend-label">${label}</span>
        <span class="legend-count">${count}</span>
        <button class="legend-remove" data-layer="${k}" title="Remover camada">✕</button>
      </div>`;
  });
  legendEl.innerHTML = html;

  // Wire remove buttons
  legendEl.querySelectorAll('.legend-remove').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = e.target.dataset.layer;
      if (activeLayers[id]) {
        featureCount -= activeLayers[id].getLayers().length;
        layerGroup.removeLayer(activeLayers[id]);
        delete activeLayers[id];
        updateLegend();
        updateHUD(`🗑 Camada ${LAYER_LABELS[id] || id} removida`);
      }
    });
  });
}

// ── HUD Helper ──────────────────────────────────────────────
function updateHUD(html) {
  const el = document.getElementById('gis-hud-info');
  if (el) el.innerHTML = html;
}
