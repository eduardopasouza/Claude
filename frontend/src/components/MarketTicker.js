/**
 * MarketTicker — Cotações Agropecuárias em Tempo Real e Histórico
 * 
 * Conecta com:
 *  GET /api/v1/market/quotes
 *  GET /api/v1/market/quotes/history/{ticker}
 */

const COMMODITY_ICONS = {
  'soja': '🌱', 'milho': '🌽', 'boi': '🐂',
  'bezerro': '🐄', 'leite': '🥛', 'café': '☕',
  'açúcar': '🍬', 'trigo': '🌾', 'frango': '🐔',
  'suíno': '🐷', 'arroz': '🍚', 'algodão': '🧶',
  'laranja': '🍊', 'citros': '🍊', 'piscicultura': '🐟',
  'tilápia': '🐟', 'etanol': '⛽', 'petróleo': '🛢️'
};

function getIcon(commodity) {
  const lc = (commodity || '').toLowerCase();
  for (const [key, icon] of Object.entries(COMMODITY_ICONS)) {
    if (lc.includes(key)) return icon;
  }
  return '📊';
}

let chartInstance = null;
let candlestickSeries = null;
let smaSeries = null;

// Extracted from ticker string (e.g., "YAHOO/ZS=F") -> "ZS=F"
function extractTicker(index_name) {
  if (!index_name) return null;
  const parts = index_name.split('/');
  return parts[parts.length - 1];
}

export async function loadMarketTicker(API) {
  // Replace the default grid with a proper dashboard layout
  const viewMercado = document.getElementById('view-mercado');
  if (!viewMercado) return;
  
  // Create layout once
  if (!document.getElementById('market-dashboard-layout')) {
    viewMercado.innerHTML = `
      <header class="view-heading">
        <h2>Commodities & Câmbio</h2>
        <div class="ribbon-btn">TradingView Analytics</div>
      </header>
      <div id="market-dashboard-layout" style="display:flex; gap:20px; height: calc(100vh - 160px);">
        <div id="market-ticker-list" style="width: 320px; overflow-y: auto; display:flex; flex-direction: column; gap:10px; padding-right:5px;">
          <div class="loading-text">Conectando ao Banco de Cotações...</div>
        </div>
        <div class="glass-card" style="flex:1; display:flex; flex-direction:column; padding: 20px;">
           <div id="market-chart-header" style="margin-bottom:15px; display:flex; align-items:center; justify-content:space-between;">
             <h3 id="market-chart-title" style="margin:0; font-size:1.5rem; font-weight:700;">Selecione um ativo</h3>
             <div id="market-chart-legend" style="font-size:14px; color:var(--slate-500); font-weight:600;"></div>
           </div>
           <div id="market-chart-container" style="flex:1; width:100%; position:relative;"></div>
        </div>
      </div>
    `;
    
    // Initialize Lightweight Chart
    setTimeout(() => initChart(), 50);
  }

  const listContainer = document.getElementById('market-ticker-list');

  try {
    const res = await fetch(`${API}/api/v1/market/quotes`);
    const data = await res.json();

    if (!data.quotes || data.quotes.length === 0) {
      listContainer.innerHTML = '<div class="loading-text">Nenhuma cotação disponível.</div>';
      return;
    }

    let html = '';
    const sourceBadge = data.is_reference
      ? '<span class="source-badge mock" style="background:#f59e0b;color:#fff;padding:2px 6px;border-radius:4px;font-size:10px;">MOCK</span>'
      : '<span class="source-badge live" style="background:#10b981;color:#fff;padding:2px 6px;border-radius:4px;font-size:10px;">LIVE DB</span>';

    html += `<div style="font-size:12px;color:var(--slate-400);margin-bottom:10px;">${sourceBadge} Fonte: ${data.source}</div>`;

    let firstTicker = null;

    for (const q of data.quotes) {
      const icon = getIcon(q.commodity);
      const variation = q.variation_pct || 0;
      const variationClass = variation > 0 ? 'color: #10b981' : variation < 0 ? 'color: #ef4444' : 'color: #94a3b8';
      const variationArrow = variation > 0 ? '▲' : variation < 0 ? '▼' : '●';
      const ticker = extractTicker(q.source);

      if (ticker && !firstTicker) firstTicker = { ticker, name: q.commodity };

      html += `
      <div class="market-card" data-ticker="${ticker || ''}" data-name="${q.commodity}" style="cursor:pointer; display:flex; padding: 15px; background:var(--glass-bg); border:1px solid var(--glass-border); border-radius:12px; align-items:center; transition: all 0.2s;">
        <div style="font-size:24px; margin-right:15px; background:var(--slate-100); width:40px; height:40px; display:flex; align-items:center; justify-content:center; border-radius:8px;">${icon}</div>
        <div style="flex:1;">
          <div style="font-weight:700; font-size:14px; color:var(--text-main);">${q.commodity}</div>
          <div style="font-size:18px; font-weight:800; color:var(--indigo-800); margin:4px 0;">R$ ${typeof q.price === 'number' ? q.price.toLocaleString('pt-BR', {minimumFractionDigits: 2}) : q.price}</div>
          <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:600;">
            <span style="${variationClass}">${variationArrow} ${Math.abs(variation).toFixed(2)}%</span>
            <span style="color:var(--slate-400)">${q.date || ''}</span>
          </div>
        </div>
      </div>`;
    }

    listContainer.innerHTML = html;

    // Attach Click Events
    document.querySelectorAll('.market-card').forEach(card => {
      card.addEventListener('click', () => {
        document.querySelectorAll('.market-card').forEach(c => c.style.borderColor = 'var(--glass-border)');
        card.style.borderColor = 'var(--indigo-500)';
        const tk = card.dataset.ticker;
        const name = card.dataset.name;
        if (tk) loadChartData(API, tk, name);
      });
      
      // Hover effects
      card.addEventListener('mouseover', () => { if(card.style.borderColor !== 'var(--indigo-500)') card.style.borderColor = 'var(--indigo-300)'; });
      card.addEventListener('mouseout', () => { if(card.style.borderColor !== 'var(--indigo-500)') card.style.borderColor = 'var(--glass-border)'; });
    });

    // Auto-load first chart
    if (firstTicker) {
      const firstCard = document.querySelector(\`.market-card[data-ticker="\${firstTicker.ticker}"]\`);
      if (firstCard) firstCard.style.borderColor = 'var(--indigo-500)';
      loadChartData(API, firstTicker.ticker, firstTicker.name);
    }

  } catch (err) {
    listContainer.innerHTML = \`<div class="loading-text" style="color:#ef4444">Erro ao carregar cotações: \${err.message}</div>\`;
  }
}

function initChart() {
  const container = document.getElementById('market-chart-container');
  if (!container || !window.LightweightCharts) return;
  
  container.innerHTML = '';
  
  chartInstance = LightweightCharts.createChart(container, {
    width: container.clientWidth,
    height: container.clientHeight || 400,
    layout: {
      background: { type: 'solid', color: 'transparent' },
      textColor: '#64748b',
    },
    grid: {
      vertLines: { color: 'rgba(226, 232, 240, 0.5)' },
      horzLines: { color: 'rgba(226, 232, 240, 0.5)' },
    },
    rightPriceScale: {
      borderColor: 'rgba(226, 232, 240, 0.8)',
    },
    timeScale: {
      borderColor: 'rgba(226, 232, 240, 0.8)',
      timeVisible: true,
    },
  });

  candlestickSeries = chartInstance.addCandlestickSeries({
    upColor: '#10b981',
    downColor: '#ef4444',
    borderDownColor: '#ef4444',
    borderUpColor: '#10b981',
    wickDownColor: '#ef4444',
    wickUpColor: '#10b981',
  });

  smaSeries = chartInstance.addLineSeries({
    color: '#8b5cf6',
    lineWidth: 2,
    title: 'SMA 20',
  });

  // Handle resizing manually
  window.addEventListener('resize', () => {
    if (chartInstance && container) {
      chartInstance.applyOptions({ width: container.clientWidth, height: container.clientHeight });
    }
  });

  // Crosshair legend event
  chartInstance.subscribeCrosshairMove((param) => {
    const legend = document.getElementById('market-chart-legend');
    if (!param.time || !param.seriesData.size) {
      legend.innerHTML = '';
      return;
    }
    const candleData = param.seriesData.get(candlestickSeries);
    if (candleData) {
      const date = new Date(param.time * 1000).toLocaleDateString('pt-BR');
      legend.innerHTML = \`<span style="margin-right:8px">Data: \${date}</span>
                          <span style="color:#64748b; margin-right:8px">A: \${candleData.open.toFixed(2)}</span>
                          <span style="color:#10b981; margin-right:8px">M: \${candleData.high.toFixed(2)}</span>
                          <span style="color:#ef4444; margin-right:8px">m: \${candleData.low.toFixed(2)}</span>
                          <span style="color:#0f172a">F: \${candleData.close.toFixed(2)}</span>\`;
    }
  });
}

function calculateSMA(data, period) {
  const sma = [];
  for (let i = 0; i < data.length; i++) {
    if (i < period - 1) continue;
    let sum = 0;
    for (let j = 0; j < period; j++) {
      sum += data[i - j].close;
    }
    sma.push({ time: data[i].time, value: sum / period });
  }
  return sma;
}

async function loadChartData(API, ticker, name) {
  const title = document.getElementById('market-chart-title');
  if (title) title.textContent = \`\${name} (\${ticker})\`;
  
  if (!chartInstance) return;

  try {
    const res = await fetch(\`\${API}/api/v1/market/quotes/history/\${ticker}?range=2y&interval=1d\`);
    const data = await res.json();

    if (data.history && data.history.length > 0) {
      candlestickSeries.setData(data.history);
      
      const smaData = calculateSMA(data.history, 20);
      smaSeries.setData(smaData);
      
      chartInstance.timeScale().fitContent();
    } else {
      console.warn("Sem histórico para:", ticker);
      candlestickSeries.setData([]);
      smaSeries.setData([]);
    }
  } catch (err) {
    console.error("Failed to load history for", ticker, err);
  }
}
