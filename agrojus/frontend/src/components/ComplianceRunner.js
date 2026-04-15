export function initComplianceRunner(API) {
    const btnMcr29 = document.getElementById('btn-run-mcr29');
    const btnEudr = document.getElementById('btn-run-eudr');
  
    if (!btnMcr29 || !btnEudr) return;
  
    const runCompliance = async (type) => {
      const doc = document.getElementById('comp-doc').value.trim();
      const car = document.getElementById('comp-car').value.trim();
      const lat = document.getElementById('comp-lat').value;
      const lon = document.getElementById('comp-lon').value;
  
      const payload = {
        radius_km: 10.0
      };
      
      if (doc) payload.cpf_cnpj = doc;
      if (car) payload.car_code = car;
      if (lat && lon) {
          payload.latitude = parseFloat(lat);
          payload.longitude = parseFloat(lon);
      }
  
      const btn = type === 'mcr29' ? btnMcr29 : btnEudr;
      const originalText = btn.textContent;
  
      // Loading state
      btn.textContent = 'Processando Regulamentos...';
      btn.style.opacity = '0.7';
  
      try {
        const res = await fetch(`${API}/api/v1/compliance/${type}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
  
        const data = await res.json();
        renderComplianceResults(data, type);
      } catch (err) {
        alert(`Erro na avaliação de compliance: ${err.message}`);
      } finally {
        btn.textContent = originalText;
        btn.style.opacity = '1';
      }
    };
  
    btnMcr29.addEventListener('click', () => runCompliance('mcr29'));
    btnEudr.addEventListener('click', () => runCompliance('eudr'));
  }
  
  function renderComplianceResults(data, type) {
    const box = document.getElementById('compliance-results-box');
    box.style.display = 'grid'; // .data-blocks-grid rules
  
    // Determine overall color
    let statusColor = 'var(--slate-500)';
    let statusLabel = 'EM ANÁLISE';
    
    if (data.overall_status === 'approved' || data.overall_status === 'compliant') {
        statusColor = 'var(--emerald-500)';
        statusLabel = 'APROVADO CÓD. VERDE';
    } else if (data.overall_status === 'blocked' || data.overall_status === 'non_compliant') {
        statusColor = 'var(--rose-500)';
        statusLabel = 'BLOQUEADO / CRÍTICO';
    } else if (data.overall_status === 'restricted') {
        statusColor = 'var(--amber-500)';
        statusLabel = 'RESTRITO / ATENÇÃO';
    }
  
    let html = `
       <div class="section-block full" style="border-top: 4px solid ${statusColor}">
          <div style="display:flex; justify-content:space-between; align-items:center;">
             <h5>Laudo Oficial: ${type.toUpperCase()}</h5>
             <strong style="color:${statusColor}">${statusLabel}</strong>
          </div>
          <p style="font-size:14px; margin-top:10px; line-height:1.5;">${data.recommendation}</p>
          <div style="font-size:11px; color:var(--text-muted); margin-top:10px">
              ID: ${data.compliance_id} | Ref: ${new Date(data.generated_at).toLocaleString()}
          </div>
       </div>
    `;
  
    // Render individual checks
    if (data.checks && Array.isArray(data.checks)) {
        data.checks.forEach(chk => {
            let chkColor = 'var(--slate-400)';
            if (chk.status === 'blocked') chkColor = 'var(--rose-400)';
            if (chk.status === 'approved') chkColor = 'var(--emerald-400)';
            if (chk.status === 'restricted') chkColor = 'var(--amber-400)';
            
            html += `
            <div class="section-block">
               <strong style="color:${chkColor}; font-size:12px;">[${chk.status.toUpperCase()}]</strong>
               <h5 style="margin-top:5px; margin-bottom:5px;">${chk.check}</h5>
               <p style="font-size:12px; color:var(--text-muted);">${chk.detail}</p>
               ${chk.regulation ? `<div style="margin-top:10px; font-size:10px; color:#183b2b; background:#e2ede6; padding:5px; border-radius:4px;">${chk.regulation}</div>` : ''}
            </div>
            `;
        });
    }
  
    box.innerHTML = html;
  }
