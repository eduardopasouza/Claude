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

// Run Engine
(() => {
  setupNavigation();
  initConsultEngine(API);
  initComplianceRunner(API);
  setupOmniBar();
  startHeartbeat();
  loadDashboardFeed();
})();
