/**
 * AgroJus Enterprise — Kernel
 * Initializes all view engines and checks heartbeat.
 */

import { initMap } from './src/components/GisMap.js';
import { initConsultEngine } from './src/components/ConsultEngine.js';
import { initComplianceRunner } from './src/components/ComplianceRunner.js';
import { loadMarketTicker } from './src/components/MarketTicker.js';

const API = 'http://localhost:8000';

// View Router
function setupNavigation() {
  document.querySelectorAll('.nav-action').forEach(btn => {
    btn.addEventListener('click', () => {
      // Clean UI states
      document.querySelectorAll('.nav-action').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
      
      // Paint active state
      btn.classList.add('active');
      const targetView = document.getElementById(`view-${btn.dataset.view}`);
      if (targetView) targetView.classList.add('active');

      // Lazy load engines if needed
      if (btn.dataset.view === 'mapa') {
        initMap(API);
        // Force Leaflet to recalculate container dimensions when the tab is exposed
        setTimeout(() => {
          if (window.dispatchEvent) {
            window.dispatchEvent(new Event('resize'));
          }
        }, 150);
      }
      if (btn.dataset.view === 'mercado') {
        loadMarketTicker(API);
      }
    });
  });
}

// API Heartbeat
async function startHeartbeat() {
  const orb = document.querySelector('.status-orb');
  const txt = document.querySelector('.status-text');
  const ping = document.querySelector('.status-ping');

  const check = async () => {
    try {
      const start = performance.now();
      const res = await fetch(`${API}/`);
      if(!res.ok) throw new Error('Bad Gateway');
      
      const ms = Math.round(performance.now() - start);
      
      orb.className = 'status-orb online';
      txt.textContent = 'SYSTEM ONLINE';
      ping.textContent = `Latency: ${ms}ms`;
      
      // Update Dashboard Metric if active
      const dLat = document.getElementById('dash-latency');
      if(dLat) dLat.innerHTML = `${ms}<span class="kpi-sub">ms</span>`;
      
    } catch {
      orb.className = 'status-orb offline';
      txt.textContent = 'BACKBONE OFFLINE';
      ping.textContent = 'Waiting connection...';
    }
  };

  await check();
  setInterval(check, 10000);
}

// Sub-Engine: Quick Search OmniBar
function setupOmniBar() {
  const btn = document.getElementById('omni-btn');
  const input = document.getElementById('omni-input');
  
  if(!btn || !input) return;

  const trigger = () => {
     if(!input.value.trim()) return;
     document.getElementById('deep-cpf-input').value = input.value.trim();
     document.querySelector('.nav-action[data-view="consulta"]').click();
  };

  btn.addEventListener('click', trigger);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') trigger(); });
}

// Load Dashboard data on startup
async function loadDashboardFeed() {
  const newsList = document.getElementById('dash-news-list');
  if (!newsList) return;
  try {
    const res = await fetch(`${API}/api/v1/news/feed`);
    const data = await res.json();
    if (data.articles && data.articles.length > 0) {
      newsList.innerHTML = data.articles.slice(0, 6).map(a => `
        <div class="news-item">
          <div class="news-cat">${a.source || 'AGRO'}</div>
          <div class="news-title">${a.title}</div>
          <div class="news-meta">${a.published || ''}</div>
        </div>
      `).join('');
    }
  } catch { /* silent news feed fail */ }
}

// ──────────────────────────────────────────────────────────────────────────
// Dashboard KPI Metrics → /api/v1/dashboard/metrics
// Popula todos os cards com dados reais do PostgreSQL. Sem mock.
// ──────────────────────────────────────────────────────────────────────────
function fmt(n) {
  if (n == null) return '—';
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000)     return (n / 1_000).toFixed(0) + 'k';
  return String(n);
}

async function loadDashboardMetrics() {
  try {
    const res  = await fetch(`${API}/api/v1/dashboard/metrics`);
    if (!res.ok) return;
    const data = await res.json();
    const k    = data.kpis;

    // IBAMA
    const ibamaEl = document.getElementById('kpi-ibama');
    const ibamaTr = document.getElementById('kpi-ibama-trend');
    if (ibamaEl) ibamaEl.textContent = fmt(k.ibama_embargos?.total);
    if (ibamaTr) ibamaTr.textContent = `+${fmt(k.ibama_embargos?.last_30d)} nos últimos 30 dias`;

    // MTE Lista Suja
    const mteEl = document.getElementById('kpi-mte');
    const mteTr = document.getElementById('kpi-mte-trend');
    if (mteEl) mteEl.textContent = fmt(k.mte_lista_suja?.total);
    if (mteTr) {
      const n = k.mte_lista_suja?.total || 0;
      mteTr.textContent  = n > 0 ? `${n} empregadores na lista` : 'ETL pendente';
      mteTr.className    = `kpi-trend ${n > 0 ? 'warning' : ''}`;
    }

    // Cotações
    const mktEl = document.getElementById('kpi-market');
    const mktTr = document.getElementById('kpi-market-trend');
    if (mktEl) mktEl.textContent = fmt(k.market_quotes?.products) + ' cadeias';
    if (mktTr) {
      const d = k.market_quotes?.last_date;
      mktTr.textContent = d ? `Última coleta: ${d}` : 'Aguardando scraper';
    }

    // Crédito Rural
    const credEl = document.getElementById('kpi-credito');
    if (credEl) credEl.textContent = fmt(k.credito_rural?.total);

    // DB Latência
    const latEl = document.getElementById('dash-latency');
    if (latEl) latEl.innerHTML = `${data.db_latency_ms}<span class="kpi-sub">ms</span>`;

    // Timestamp
    const tsEl = document.getElementById('kpi-updated-at');
    const dtEl = document.getElementById('kpi-market-date');
    if (tsEl) {
      const ts = new Date(data.generated_at);
      tsEl.textContent = ts.toLocaleTimeString('pt-BR');
    }
    if (dtEl) dtEl.textContent = `Última cotação: ${k.market_quotes?.last_date || '—'}`;

  } catch(e) {
    console.warn('[AgroJus] Métricas indisponíveis:', e);
  }
}

// Run Engine
(() => {
  setupNavigation();
  initConsultEngine(API);
  initComplianceRunner(API);
  setupOmniBar();
  startHeartbeat();
  loadDashboardFeed();
  loadDashboardMetrics();
  // Refresh KPIs a cada 60s
  setInterval(loadDashboardMetrics, 60_000);
})();
