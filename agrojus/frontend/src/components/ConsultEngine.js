export function initConsultEngine(API) {
  const btn = document.getElementById('deep-search-btn');
  if(!btn) return;

  btn.addEventListener('click', async () => {
    const docInput = document.getElementById('deep-cpf-input').value.trim();
    if (!docInput) return;

    // Loading State
    btn.textContent = 'Tracionando Dados...';
    btn.style.opacity = '0.7';

    try {
      const res = await fetch(`${API}/api/v1/consulta/completa`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
           cpf_cnpj: docInput,
           include_cadastral: true,
           include_environmental: true,
           include_labour: true,
           include_legal: true,
           include_financial: true,
           include_protests: true
        }),
      });

      const data = await res.json();
      renderDeepResults(data);
    } catch (err) {
      alert(`Erro na busca profunda: ${err.message}`);
    } finally {
      btn.textContent = 'Auditar (Real)';
      btn.style.opacity = '1';
    }
  });
}

function renderDeepResults(data) {
  document.getElementById('deep-results-area').style.display = 'block';

  // Render Risk Matrix
  if (data.risk_score) {
    const setRisk = (id, val) => {
      const el = document.getElementById(id);
      if(!el) return;
      el.className = `matrix-cell risk-${val.toUpperCase()}`;
      el.querySelector('.val').textContent = val.toUpperCase();
    };
    
    setRisk('risk-overall', data.risk_score.overall || 'LOW');
    setRisk('risk-env', data.risk_score.environmental || 'LOW');
    setRisk('risk-legal', data.risk_score.legal || 'LOW');
    setRisk('risk-fin', data.risk_score.financial || 'LOW');
  }

  // Render Sections cleanly
  const grid = document.getElementById('deep-sections-grid');
  let html = '';

  const s = data.sections || {};

  // 1. Cadastral (Receita Federal)
  if (s.cadastral && s.cadastral.status !== 'error') {
     const c = s.cadastral;
     html += `
     <div class="section-block">
        <h5>Receita Federal Oficial</h5>
        <div style="font-size:14px; margin-bottom:8px"><strong>Razão:</strong> ${c.razao_social || 'N/A'}</div>
        <div style="font-size:14px; margin-bottom:8px"><strong>CNAE:</strong> ${c.cnae_principal || 'N/A'}</div>
        <div style="font-size:14px; margin-bottom:8px"><strong>Situação:</strong> <span style="color:var(--emerald-400); font-weight:bold">${c.situacao_cadastral || 'N/A'}</span></div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:10px">Endereço: ${c.endereco || ''}</div>
     </div>`;
  }

  // 2. IBAMA / Ambiental
  if (s.embargos_ibama && s.embargos_ibama.status !== 'error') {
     const env = s.embargos_ibama;
     const hasEmbargo = env.total > 0;
     const color = hasEmbargo ? 'var(--rose-500)' : 'var(--emerald-400)';
     html += `
     <div class="section-block" style="border-left: 4px solid ${color}">
        <h5>Ambiental (IBAMA)</h5>
        <h2 style="font-size:24px; color:${color}">${env.total} Autuações/Embargos</h2>
        <p style="font-size:12px; color:var(--text-muted); margin-top:8px">Base pública processada localmente baseada em auto de infrações e áreas embargadas em TIs.</p>
     </div>`;
  }

  // 3. MTE Trabalho Escravo
  if (s.lista_suja && s.lista_suja.status !== 'error') {
     const te = s.lista_suja;
     const isDirty = te.found;
     const color = isDirty ? 'var(--rose-500)' : 'var(--emerald-400)';
     html += `
     <div class="section-block" style="border-left: 4px solid ${color}">
        <h5>Trabalhista (Lista Suja MTE)</h5>
        <h2 style="font-size:24px; color:${color}">${te.total} Ocorrências</h2>
        <p style="font-size:12px; color:var(--text-muted); margin-top:8px">Consulta de resgate em condições análogas à escravidão segundo portaria MTE.</p>
     </div>`;
  }

  // 4. DataJud
  if (s.processos_judiciais && s.processos_judiciais.status !== 'error') {
      const jud = s.processos_judiciais;
      html += `
      <div class="section-block">
        <h5>Processos Judiciais (DataJud)</h5>
        <h2 style="font-size:24px; color:var(--amber-400)">${jud.total} Processos</h2>
        <ul style="list-style:none; padding:0; margin-top:10px; font-size:12px">
           ${jud.records ? jud.records.slice(0,3).map(r => `<li>• ${r.tribunal || r.numero}: ${r.assunto || 'Cível'}</li>`).join('') : ''}
        </ul>
      </div>`;
  }

  // 5. Crédito Rural SICOR
  if (s.credito_rural && s.credito_rural.status !== 'error') {
     const cred = s.credito_rural;
     html += `
     <div class="section-block">
        <h5>Crédito Rural SICOR</h5>
        <h2 style="font-size:24px; color:var(--emerald-400)">R$ ${cred.total_amount ? cred.total_amount.toLocaleString('pt-BR') : '0,00'}</h2>
        <p style="font-size:12px; color:var(--text-muted); margin-top:8px">${cred.total_operations} operações financiadas via Cédula de Produto Rural / BCB.</p>
     </div>`;
  }

  // Erros/Dumps Crudos em caso de debug
  Object.entries(s).forEach(([key, val]) => {
     if (val.status === 'error') {
        html += `<div class="section-block"><h5 style="color:var(--rose-500)">Falha: ${key}</h5><p style="font-size:12px; color:var(--text-muted)">${val.message}</p></div>`;
     }
  });

  if(!html) {
      grid.innerHTML = `<div class="section-block full"><h5>Nenhum Dossiê processado</h5><p>Backend retornou estrutura vazia.</p></div>`;
  } else {
      grid.innerHTML = html;
  }
}
