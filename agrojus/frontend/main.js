/**
 * AgroJus Frontend — Main Application Logic
 * Connects to FastAPI backend at localhost:8000
 */

import L from 'leaflet';

const API = 'http://localhost:8000';
let map = null;
let layerGroup = null;

// ════════════════════════════════════════
//  Navigation
// ════════════════════════════════════════

document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    const panel = document.getElementById(`panel-${btn.dataset.panel}`);
    if (panel) panel.classList.add('active');

    // Lazy-init map when mapa panel is opened
    if (btn.dataset.panel === 'mapa' && !map) initMap();
    if (btn.dataset.panel === 'mercado') loadMarket();
    if (btn.dataset.panel === 'noticias') loadNewsFull();
  });
});

// ════════════════════════════════════════
//  API Health & Dashboard
// ════════════════════════════════════════

async function checkAPI() {
  const dot = document.querySelector('.status-dot');
  const label = document.querySelector('.api-status span:last-child');
  const latencyEl = document.getElementById('api-latency');
  const versionEl = document.getElementById('api-version');

  try {
    const start = performance.now();
    const res = await fetch(`${API}/`);
    const ms = Math.round(performance.now() - start);
    const data = await res.json();

    dot.className = 'status-dot online';
    label.textContent = 'API Online';
    latencyEl.textContent = `${ms}ms`;
    versionEl.textContent = `v${data.version}`;
    return true;
  } catch {
    dot.className = 'status-dot offline';
    label.textContent = 'API Offline';
    latencyEl.textContent = '—';
    versionEl.textContent = 'Sem conexão';
    return false;
  }
}

async function loadDashboardNews() {
  try {
    const res = await fetch(`${API}/api/v1/news/latest?limit=5`);
    if (!res.ok) return;
    const data = await res.json();
    const list = document.getElementById('news-list');
    const articles = data.articles || data.data || [];
    if (articles.length === 0) {
      list.innerHTML = '<p style="color:var(--text-muted);font-size:13px;">Nenhuma notícia disponível</p>';
      return;
    }
    list.innerHTML = articles.slice(0, 5).map(a => `
      <a class="news-item" href="${a.url || '#'}" target="_blank" rel="noopener">
        <div>
          <span class="news-category ${a.category || ''}">${a.category || 'geral'}</span>
          <div class="news-title">${a.title}</div>
          <div class="news-meta">${a.source || ''} · ${a.published_at ? new Date(a.published_at).toLocaleDateString('pt-BR') : ''}</div>
        </div>
      </a>
    `).join('');
  } catch {
    document.getElementById('news-list').innerHTML = '<p style="color:var(--text-muted);font-size:13px;">Não foi possível carregar notícias</p>';
  }
}

// ════════════════════════════════════════
//  Quick Search
// ════════════════════════════════════════

document.getElementById('btn-quick-search')?.addEventListener('click', () => {
  const query = document.getElementById('input-quick-search').value.trim();
  if (!query) return;
  // Navigate to consulta panel and pre-fill
  document.getElementById('input-cpf-cnpj').value = query;
  document.querySelector('[data-panel="consulta"]').click();
});

document.getElementById('input-quick-search')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('btn-quick-search').click();
});

// ════════════════════════════════════════
//  Consulta Unificada
// ════════════════════════════════════════

document.getElementById('btn-consulta')?.addEventListener('click', async () => {
  const cpf = document.getElementById('input-cpf-cnpj').value.trim();
  if (!cpf) return;

  const btn = document.getElementById('btn-consulta');
  btn.classList.add('loading');
  btn.textContent = 'Consultando...';

  try {
    const res = await fetch(`${API}/api/v1/consulta/completa`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cpf_cnpj: cpf }),
    });

    const data = await res.json();
    renderConsultaResults(data);
  } catch (err) {
    alert(`Erro: ${err.message}. Verifique se o backend está rodando.`);
  } finally {
    btn.classList.remove('loading');
    btn.textContent = 'Executar Consulta Completa';
  }
});

function renderConsultaResults(data) {
  const container = document.getElementById('consulta-results');
  container.style.display = 'block';

  // Risk bar
  const riskBar = document.getElementById('risk-bar');
  if (data.risk_score) {
    const rs = data.risk_score;
    riskBar.innerHTML = `
      <div class="risk-badge ${rs.overall}">Risco Geral: ${rs.overall.toUpperCase()}</div>
      <div class="risk-badge ${rs.environmental}">Ambiental: ${rs.environmental}</div>
      <div class="risk-badge ${rs.labor}">Trabalhista: ${rs.labor}</div>
      <div class="risk-badge ${rs.legal}">Jurídico: ${rs.legal}</div>
      <div class="risk-badge ${rs.financial}">Financeiro: ${rs.financial}</div>
    `;
  } else if (data.error) {
    riskBar.innerHTML = `<div class="risk-badge high">${data.error}</div>`;
  }

  // Sections
  const grid = document.getElementById('sections-grid');
  if (data.sections) {
    grid.innerHTML = Object.entries(data.sections).map(([key, val]) => `
      <div class="section-card">
        <h4>${key.replace(/_/g, ' ')}</h4>
        <pre>${JSON.stringify(val, null, 2)}</pre>
      </div>
    `).join('');
  } else {
    grid.innerHTML = `<div class="section-card"><h4>Resposta</h4><pre>${JSON.stringify(data, null, 2)}</pre></div>`;
  }
}

// ════════════════════════════════════════
//  Mapa GIS (Leaflet)
// ════════════════════════════════════════

function initMap() {
  map = L.map('map-container').setView([-5.0, -44.0], 6);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Esri, Maxar, Earthstar',
    maxZoom: 18,
  }).addTo(map);

  // Labels overlay
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 18,
  }).addTo(map);

  layerGroup = L.layerGroup().addTo(map);

  // Right-click context menu
  map.on('contextmenu', async (e) => {
    const { lat, lng } = e.latlng;
    const infoEl = document.getElementById('map-info');
    infoEl.innerHTML = `<span>Analisando ${lat.toFixed(4)}, ${lng.toFixed(4)}...</span>`;

    try {
      const res = await fetch(`${API}/api/v1/geo/analyze-point?lat=${lat}&lon=${lng}&radius_km=5`);
      const data = await res.json();

      const risk = data.overall_risk || 'low';
      const muni = data.municipio?.municipio || '—';
      const estado = data.municipio?.estado || '—';
      const tis = data.summary?.terras_indigenas || 0;
      const alerts = data.summary?.alertas_desmatamento || 0;

      infoEl.innerHTML = `
        <strong>${muni}, ${estado}</strong> |
        Risco: <span class="risk-badge ${risk}" style="display:inline;padding:2px 8px;">${risk.toUpperCase()}</span> |
        TIs: ${tis} | Alertas: ${alerts} |
        ${data.risk_flags?.[0] || 'Nenhuma sobreposição'}
      `;

      // Add marker
      const color = risk === 'critical' ? '#ff4444' : risk === 'high' ? '#ff6b6b' : risk === 'medium' ? '#f0a030' : '#3ab874';
      L.circleMarker([lat, lng], { radius: 10, fillColor: color, color: '#fff', weight: 2, fillOpacity: 0.8 })
        .addTo(layerGroup)
        .bindPopup(`<b>${muni}</b><br>Risco: ${risk}<br>TIs: ${tis} | Desmat: ${alerts}`)
        .openPopup();
    } catch {
      infoEl.innerHTML = '<span style="color:var(--red-500);">Erro na análise — verifique se o backend está rodando</span>';
    }
  });
}

document.getElementById('btn-load-layer')?.addEventListener('click', async () => {
  const layer = document.getElementById('select-layer').value;
  const uf = document.getElementById('input-uf').value.toUpperCase();
  if (!layer) return;

  try {
    const params = new URLSearchParams({ max_features: '200' });
    if (uf) params.append('uf', uf);
    const res = await fetch(`${API}/api/v1/geo/layers/${layer}/geojson?${params}`);
    const data = await res.json();

    if (data.features && data.features.length > 0) {
      const geoLayer = L.geoJSON(data, {
        style: { color: '#3ab874', weight: 1, fillOpacity: 0.3 },
        onEachFeature: (f, l) => {
          const props = f.properties || {};
          const name = props.terrai_nom || props.nome || props.NM_MUN || 'Feature';
          l.bindPopup(`<b>${name}</b><br>${JSON.stringify(props).slice(0, 200)}`);
        }
      });
      layerGroup.clearLayers();
      geoLayer.addTo(layerGroup);
      map.fitBounds(geoLayer.getBounds());
      document.getElementById('map-info').innerHTML = `<span>Carregadas ${data.features.length} features — ${layer}</span>`;
    } else {
      document.getElementById('map-info').innerHTML = `<span>Nenhuma feature encontrada</span>`;
    }
  } catch {
    document.getElementById('map-info').innerHTML = '<span style="color:var(--red-500);">Erro ao carregar camada</span>';
  }
});

// ════════════════════════════════════════
//  Compliance
// ════════════════════════════════════════

async function runCompliance(type) {
  const cpf = document.getElementById('comp-cpf').value.trim();
  const car = document.getElementById('comp-car').value.trim();
  const lat = parseFloat(document.getElementById('comp-lat').value) || -5;
  const lon = parseFloat(document.getElementById('comp-lon').value) || -44;

  const body = { cpf_cnpj: cpf, property_car: car, lat, lon };
  if (type === 'eudr') body.product = 'soja';

  try {
    const res = await fetch(`${API}/api/v1/compliance/${type}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    const el = document.getElementById('compliance-results');
    el.style.display = 'block';
    el.innerHTML = `<h4>${type.toUpperCase()} — Resultado</h4><pre style="color:var(--text-secondary);font-size:12px;white-space:pre-wrap;">${JSON.stringify(data, null, 2)}</pre>`;
  } catch (err) {
    alert(`Erro: ${err.message}`);
  }
}

document.getElementById('btn-mcr29')?.addEventListener('click', () => runCompliance('mcr29'));
document.getElementById('btn-eudr')?.addEventListener('click', () => runCompliance('eudr'));

// ════════════════════════════════════════
//  Market
// ════════════════════════════════════════

async function loadMarket() {
  const grid = document.getElementById('market-grid');
  try {
    const res = await fetch(`${API}/api/v1/market/quotes`);
    const data = await res.json();
    const quotes = data.quotes || {};

    grid.innerHTML = Object.entries(quotes).map(([name, info]) => {
      const val = typeof info === 'object' ? (info.value || info.buy || '—') : info;
      return `
        <div class="market-card">
          <h4>${name}</h4>
          <div class="market-value">${typeof val === 'number' ? val.toFixed(2) : val}</div>
        </div>
      `;
    }).join('');

    if (Object.keys(quotes).length === 0) {
      grid.innerHTML = '<div class="market-card"><h4>Sem dados</h4><div class="market-value">—</div></div>';
    }
  } catch {
    grid.innerHTML = '<div class="market-card"><h4>Erro</h4><p style="color:var(--text-muted);">Backend offline</p></div>';
  }
}

// ════════════════════════════════════════
//  News
// ════════════════════════════════════════

async function loadNewsFull(filter = 'all') {
  const list = document.getElementById('news-full-list');
  try {
    const endpoint = filter === 'juridico' ? 'legal' : filter === 'mercado' ? 'market' : 'latest';
    const res = await fetch(`${API}/api/v1/news/${endpoint}?limit=20`);
    const data = await res.json();
    const articles = data.articles || data.data || [];

    if (articles.length === 0) {
      list.innerHTML = '<p style="color:var(--text-muted);">Nenhuma notícia encontrada</p>';
      return;
    }

    list.innerHTML = articles.map(a => `
      <a class="news-item" href="${a.url || '#'}" target="_blank" rel="noopener">
        <div>
          <span class="news-category ${a.category || ''}">${a.category || 'geral'}</span>
          <div class="news-title">${a.title}</div>
          <div class="news-meta">${a.source || ''} · ${a.published_at ? new Date(a.published_at).toLocaleDateString('pt-BR') : ''}</div>
          ${a.summary ? `<p style="font-size:12px;color:var(--text-muted);margin-top:4px;">${a.summary.slice(0, 150)}...</p>` : ''}
        </div>
      </a>
    `).join('');
  } catch {
    list.innerHTML = '<p style="color:var(--text-muted);">Não foi possível carregar notícias</p>';
  }
}

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    loadNewsFull(btn.dataset.filter);
  });
});

// ════════════════════════════════════════
//  Init
// ════════════════════════════════════════

async function init() {
  const online = await checkAPI();
  if (online) {
    loadDashboardNews();
  }
  // Re-check every 30s
  setInterval(checkAPI, 30000);
}

init();
