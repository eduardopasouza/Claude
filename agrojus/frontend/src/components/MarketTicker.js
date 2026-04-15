/**
 * MarketTicker — Cotações Agropecuárias em Tempo Real (Conectado ao PostGIS)
 * 
 * Puxa dados de: GET /api/v1/market/quotes
 * Renderiza cards visuais para as 14 cadeias agrárias monitoradas.
 */

// Ícones emoji para cada commodity — visual rápido
const COMMODITY_ICONS = {
  'soja':     '🌱', 'milho':    '🌽', 'boi':      '🐂',
  'bezerro':  '🐄', 'leite':    '🥛', 'café':     '☕',
  'açúcar':   '🍬', 'trigo':    '🌾', 'frango':   '🐔',
  'suíno':    '🐷', 'arroz':    '🍚', 'algodão':  '🧶',
  'laranja':  '🍊', 'citros':   '🍊', 'piscicultura': '🐟',
  'tilápia':  '🐟', 'etanol':   '⛽',
};

function getIcon(commodity) {
  const lc = (commodity || '').toLowerCase();
  for (const [key, icon] of Object.entries(COMMODITY_ICONS)) {
    if (lc.includes(key)) return icon;
  }
  return '📊';
}

export async function loadMarketTicker(API) {
  const grid = document.getElementById('market-ticker-grid');
  if (!grid) return;

  grid.innerHTML = '<div class="loading-text">Conectando ao Banco de Cotações...</div>';

  try {
    const res = await fetch(`${API}/api/v1/market/quotes`);
    const data = await res.json();

    if (!data.quotes || data.quotes.length === 0) {
      grid.innerHTML = '<div class="loading-text">Nenhuma cotação disponível. Execute o Scraper CEPEA primeiro.</div>';
      return;
    }

    let html = '';

    // Badge de fonte
    const sourceBadge = data.is_reference
      ? '<span class="source-badge mock">MOCK</span>'
      : '<span class="source-badge live">LIVE DB</span>';

    html += `<div class="market-source-header">${sourceBadge} ${data.total} commodities · Fonte: ${data.source}</div>`;

    for (const q of data.quotes) {
      const icon = getIcon(q.commodity);
      const variation = q.variation_pct || 0;
      const variationClass = variation > 0 ? 'positive' : variation < 0 ? 'negative' : 'neutral';
      const variationArrow = variation > 0 ? '▲' : variation < 0 ? '▼' : '●';

      html += `
      <div class="market-card">
        <div class="market-card-icon">${icon}</div>
        <div class="market-card-body">
          <div class="market-card-name">${q.commodity}</div>
          <div class="market-card-price">R$ ${typeof q.price === 'number' ? q.price.toLocaleString('pt-BR', {minimumFractionDigits: 2}) : q.price}</div>
          <div class="market-card-meta">
            <span class="market-variation ${variationClass}">${variationArrow} ${Math.abs(variation).toFixed(2)}%</span>
            <span class="market-date">${q.date || ''}</span>
          </div>
        </div>
      </div>`;
    }

    grid.innerHTML = html;

  } catch (err) {
    grid.innerHTML = `<div class="loading-text" style="color:var(--rose-500)">Erro ao carregar cotações: ${err.message}</div>`;
  }
}
