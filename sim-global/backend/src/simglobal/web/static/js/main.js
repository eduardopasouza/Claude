// sim-global frontend — Alpine.js component principal.

const POLITY_TO_ISO3 = {
  Brasil: "BRA",
  Argentina: "ARG",
  Uruguai: "URY",
  Paraguai: "PRY",
  Chile: "CHL",
  "Bolívia": "BOL",
  EUA: "USA",
  "Reino Unido": "GBR",
  Alemanha: "DEU",
  "Itália": "ITA",
  "Japão": "JPN",
};

const LS_TAB_KEY = "simglobal-tab";
const LS_POLITY_KEY = "simglobal-selected-polity";

function campaign(initialState, examples, activeName, agentReady) {
  return {
    examples,
    activeName,
    state: initialState,
    agentReady: !!agentReady,
    selectedPolity: null,
    actionDraft: "",
    actionOpen: false,
    pendingActions: initialState?.pending_actions ?? [],
    eventsFeed: [],
    advisorThread: [],   // [{id, in_game_date, question, answer}]
    advisorDraft: "",
    advisorPending: false,
    diplomaticThreads: {}, // {polityName: [{date, message_in, message_out}]}
    diplomaticPolity: null,
    diplomaticDraft: "",
    diplomaticPending: false,
    turnMonths: 6,
    turnPending: false,
    turnProgress: "",
    turnLastNarrative: "",
    status: "pronto",
    tab: "mapa",
    mapLoaded: false,
    showWelcome: false,
    errorModal: { open: false, title: "", body: "" },
    tabs: [
      { key: "mapa", label: "Mapa", icon: "🗺" },
      { key: "polity", label: "Polity", icon: "📋" },
      { key: "eventos", label: "Eventos", icon: "📜" },
      { key: "diplo", label: "Diplo", icon: "🤝" },
      { key: "advisor", label: "Conselho", icon: "💬" },
    ],

    init() {
      // Restaura tab e polity selecionada do localStorage.
      try {
        const savedTab = localStorage.getItem(LS_TAB_KEY);
        if (savedTab && this.tabs.some(t => t.key === savedTab)) this.tab = savedTab;
      } catch (e) {}
      if (this.state) {
        const savedPolity = (() => {
          try { return localStorage.getItem(LS_POLITY_KEY); } catch (e) { return null; }
        })();
        const player = this.state.player_polity;
        const target = (savedPolity && this.state.polities[savedPolity]) || this.state.polities[player];
        this.selectedPolity = target ?? null;
      }
      try {
        if (!localStorage.getItem("simglobal-welcome-seen")) this.showWelcome = true;
      } catch (e) { this.showWelcome = true; }

      this.loadMap();
      this.refreshHistory();
    },

    persistTab() { try { localStorage.setItem(LS_TAB_KEY, this.tab); } catch (e) {} },
    setTab(key) { this.tab = key; this.persistTab(); },

    persistPolity() {
      try {
        if (this.selectedPolity?.name) {
          localStorage.setItem(LS_POLITY_KEY, this.selectedPolity.name);
        }
      } catch (e) {}
    },

    dismissWelcome() {
      this.showWelcome = false;
      try { localStorage.setItem("simglobal-welcome-seen", "1"); } catch (e) {}
    },

    openAgentNotice(feature) {
      this.errorModal = {
        open: true,
        title: `${feature} indisponível`,
        body:
          "Este servidor está em modo leitura: não tem o motor narrativo Claude " +
          "Opus 4.7 configurado. A versão completa está em https://sim-global.fly.dev " +
          "(login: eduardosouza).",
      };
    },

    showError(title, body) {
      this.errorModal = { open: true, title, body };
    },

    async refreshHistory() {
      if (!this.activeName) return;
      const enc = encodeURIComponent(this.activeName);
      try {
        const [advR, evR, actR] = await Promise.all([
          fetch(`/api/campaigns/${enc}/advisor/history`),
          fetch(`/api/campaigns/${enc}/events?limit=200`),
          fetch(`/api/campaigns/${enc}/actions`),
        ]);
        if (advR.ok) this.advisorThread = await advR.json();
        if (evR.ok) this.eventsFeed = (await evR.json()).reverse();
        if (actR.ok) this.pendingActions = await actR.json();
      } catch (e) { console.warn("refreshHistory:", e); }
    },

    async loadDmHistory(polityName) {
      if (!this.activeName || !polityName) return;
      const enc = encodeURIComponent(this.activeName);
      const polEnc = encodeURIComponent(polityName);
      try {
        const r = await fetch(`/api/campaigns/${enc}/dm/${polEnc}/history`);
        if (r.ok) this.diplomaticThreads[polityName] = await r.json();
      } catch (e) { console.warn("loadDmHistory:", e); }
    },

    selectDiplomatic(polityName) {
      this.diplomaticPolity = polityName;
      if (!this.diplomaticThreads[polityName]) this.loadDmHistory(polityName);
    },

    backFromDiplomatic() { this.diplomaticPolity = null; },

    get regionList() {
      if (!this.state) return [];
      return Object.values(this.state.regions);
    },

    get internalRegionList() {
      if (!this.state) return [];
      return Object.values(this.state.regions).filter(r => r.owner === this.state.player_polity);
    },

    get polityList() {
      if (!this.state) return [];
      return Object.values(this.state.polities);
    },

    get foreignPolityList() {
      return this.polityList.filter(p => p.name !== this.state?.player_polity);
    },

    iso3Of(polity) {
      if (!polity) return null;
      return polity.iso3 || POLITY_TO_ISO3[polity.name] || null;
    },

    flagFor(polityName) {
      const polity = this.state?.polities?.[polityName];
      const iso = polity?.iso3 || POLITY_TO_ISO3[polityName];
      return iso ? `/assets/catalog/flags/${iso}.svg` : null;
    },

    colorFor(owner) {
      if (!owner) return "#3f3f3f";
      let h = 0;
      for (const c of owner) h = (h * 31 + c.charCodeAt(0)) | 0;
      const hue = ((h % 360) + 360) % 360;
      return `hsl(${hue}, 55%, 35%)`;
    },

    severityBorder(severity) {
      switch (severity) {
        case "critical": return "border-rose-500";
        case "major": return "border-amber-500";
        case "moderate": return "border-stone-500";
        case "minor": return "border-stone-700";
        default: return "border-stone-700";
      }
    },

    async loadMap() {
      const host = document.getElementById("world-map");
      if (!host) return;
      host.innerHTML = '<p class="text-stone-500 text-xs italic p-4">carregando mapa…</p>';
      try {
        const resp = await fetch("/assets/map/world-political.svg");
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        host.innerHTML = await resp.text();
        const svg = host.querySelector("svg");
        if (!svg) throw new Error("SVG raiz ausente");
        svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
        svg.style.width = "100%";
        svg.style.height = "auto";
        svg.style.maxHeight = "60vh";
        svg.style.touchAction = "pinch-zoom";
        svg.querySelectorAll("path").forEach(p => {
          p.style.cursor = "pointer";
          p.addEventListener("click", () => this.selectByPath(p));
        });
        this.mapLoaded = true;
        this.recolorMap();
      } catch (err) {
        host.innerHTML = `<p class="text-rose-400 text-xs p-4">mapa indisponível: ${err.message}</p>`;
      }
    },

    recolorMap() {
      if (!this.state || !this.mapLoaded) return;
      const svg = document.querySelector("#world-map svg");
      if (!svg) return;
      svg.querySelectorAll("path").forEach(p => {
        p.setAttribute("fill", "#444");
        p.setAttribute("stroke", "#222");
        p.setAttribute("stroke-width", "0.5");
      });
      Object.values(this.state.polities).forEach(polity => {
        const iso = this.iso3Of(polity);
        if (!iso) return;
        const escapedIso = window.CSS && CSS.escape ? CSS.escape(iso) : iso;
        const path = svg.querySelector(`#${escapedIso}`);
        if (!path) return;
        path.setAttribute("fill", this.colorFor(polity.name));
        if (polity.name === this.selectedPolity?.name) {
          path.setAttribute("stroke", "#fcd34d");
          path.setAttribute("stroke-width", "2.5");
        }
      });
    },

    selectByPath(pathEl) {
      const iso = pathEl.getAttribute("id");
      const polity = Object.values(this.state.polities).find(p => this.iso3Of(p) === iso);
      if (polity) {
        this.selectedPolity = polity;
        this.persistPolity();
        this.setTab("polity");
        this.recolorMap();
      }
    },

    selectByRegion(region) {
      if (!region.owner || !this.state) return;
      this.selectedPolity = this.state.polities[region.owner] ?? null;
      this.persistPolity();
      this.recolorMap();
    },

    selectByPolityName(name) {
      this.selectedPolity = this.state.polities[name] ?? null;
      this.persistPolity();
      this.recolorMap();
    },

    async submitAction() {
      const description = this.actionDraft.trim();
      if (!description || !this.activeName) return;
      try {
        const r = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/actions`,
          { method: "POST", headers: {"Content-Type":"application/json"},
            body: JSON.stringify({description}) }
        );
        if (!r.ok) {
          const err = await r.json().catch(() => ({detail: r.statusText}));
          this.showError("Falha ao enfileirar ação", err.detail || r.statusText);
          return;
        }
        const action = await r.json();
        this.pendingActions.push(action);
        this.actionDraft = "";
        this.status = `ação enfileirada (${this.pendingActions.length})`;
      } catch (err) {
        this.showError("Erro de rede", String(err));
      }
    },

    async deleteAction(actionId) {
      if (!this.activeName) return;
      try {
        const r = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/actions/${actionId}`,
          { method: "DELETE" }
        );
        if (r.ok || r.status === 404) {
          this.pendingActions = this.pendingActions.filter(a => a.id !== actionId);
        }
      } catch (e) { console.warn("deleteAction:", e); }
    },

    async refreshPendingActions() {
      if (!this.activeName) return;
      try {
        const r = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/actions`
        );
        if (r.ok) this.pendingActions = await r.json();
      } catch (e) { console.warn("refreshPendingActions:", e); }
    },

    async loadCampaign(name) {
      this.status = `carregando ${name}…`;
      const resp = await fetch(`/api/campaigns/${encodeURIComponent(name)}/state`);
      if (!resp.ok) { this.status = `falha ao carregar ${name}`; return; }
      const payload = await resp.json();
      this.state = payload.state;
      this.activeName = payload.campaign;
      this.selectedPolity = this.state.polities[this.state.player_polity] ?? null;
      this.pendingActions = this.state.pending_actions ?? [];
      this.recolorMap();
      await this.refreshHistory();
      this.status = "carregado";
    },

    async advanceTime() {
      if (!this.activeName) return;
      if (!this.agentReady) { this.openAgentNotice("Avançar tempo"); return; }
      const months = Math.max(1, Math.min(120, parseInt(this.turnMonths, 10) || 6));
      this.turnPending = true;
      this.turnProgress = "submetendo turno…";
      try {
        const subResp = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/turn`,
          { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({months}) }
        );
        if (subResp.status === 503) { this.openAgentNotice("Avançar tempo"); return; }
        if (!subResp.ok) {
          const err = await subResp.json().catch(() => ({detail: subResp.statusText}));
          this.showError("Falha ao submeter turno", err.detail || subResp.statusText);
          return;
        }
        const {job_id} = await subResp.json();
        // Polling
        const enc = encodeURIComponent(this.activeName);
        for (let i = 0; i < 360; i++) {  // 360 * 2s = 12min máx
          await new Promise(r => setTimeout(r, 2000));
          const stR = await fetch(`/api/campaigns/${enc}/turn/${job_id}`);
          if (!stR.ok) continue;
          const job = await stR.json();
          this.turnProgress = job.progress_message || job.status;
          if (job.status === "done") {
            this.turnLastNarrative = job.result?.narrative || "";
            this.eventsFeed = [...(job.result?.events || []), ...this.eventsFeed].slice(0, 200);
            await this.loadCampaign(this.activeName);
            this.status = `turno aplicado · ${job.result?.deltas_applied} deltas`;
            return;
          }
          if (job.status === "failed") {
            this.showError("Turno falhou", job.error || "erro desconhecido");
            return;
          }
        }
        this.showError("Turno demorou demais", "polling >12min sem resposta. O job pode estar travado.");
      } catch (err) {
        this.showError("Erro de rede", String(err));
      } finally {
        this.turnPending = false;
        this.turnProgress = "";
      }
    },

    async askAdvisor() {
      const question = this.advisorDraft.trim();
      if (!this.activeName || !question) return;
      if (!this.agentReady) { this.openAgentNotice("Conselheiro"); return; }
      this.advisorPending = true;
      try {
        const resp = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/advise`,
          { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({question}) }
        );
        if (resp.status === 503) { this.openAgentNotice("Conselheiro"); return; }
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({detail: resp.statusText}));
          this.showError("Conselheiro falhou", err.detail || resp.statusText);
          return;
        }
        const payload = await resp.json();
        this.advisorThread.push({
          id: payload.id,
          in_game_date: payload.in_game_date,
          question: question,
          answer: payload.answer,
        });
        this.advisorDraft = "";
      } catch (err) {
        this.showError("Erro de rede", String(err));
      } finally {
        this.advisorPending = false;
      }
    },

    async sendDiplomatic() {
      if (!this.activeName || !this.diplomaticPolity) return;
      const message = this.diplomaticDraft.trim();
      if (!message) return;
      if (!this.agentReady) { this.openAgentNotice("Diplomacia"); return; }
      this.diplomaticPending = true;
      try {
        const resp = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/dm`,
          {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({counterparty: this.diplomaticPolity, message}),
          }
        );
        if (resp.status === 503) { this.openAgentNotice("Diplomacia"); return; }
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({detail: resp.statusText}));
          this.showError("Diplomacia falhou", err.detail || resp.statusText);
          return;
        }
        const reply = await resp.json();
        const thread = this.diplomaticThreads[this.diplomaticPolity] || [];
        thread.push({
          date: this.state?.current_date,
          from_polity: this.state?.player_polity,
          to_polity: this.diplomaticPolity,
          message_in: message,
          message_out: reply.message_out,
          proposed_deltas: reply.proposed_deltas || [],
        });
        this.diplomaticThreads[this.diplomaticPolity] = thread;
        this.diplomaticDraft = "";
      } catch (err) {
        this.showError("Erro de rede", String(err));
      } finally {
        this.diplomaticPending = false;
      }
    },
  };
}
