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

function campaign(initialState, examples, activeName) {
  return {
    examples,
    activeName,
    state: initialState,
    selectedPolity: null,
    actionDraft: "",
    actionOpen: false,
    pendingActions: initialState?.pending_actions ?? [],
    eventsFeed: [],
    advisorAnswer: "",
    advisorPending: false,
    diplomaticDraft: "",
    diplomaticPending: false,
    status: "pronto",
    tab: "mapa",
    mapLoaded: false,
    tabs: [
      { key: "mapa", label: "Mapa", icon: "🗺" },
      { key: "polity", label: "Polity", icon: "📋" },
      { key: "eventos", label: "Eventos", icon: "📜" },
      { key: "diplo", label: "Diplo", icon: "🤝" },
      { key: "advisor", label: "Advisor", icon: "💬" },
    ],

    async init() {
      if (this.state) {
        const player = this.state.player_polity;
        this.selectedPolity = this.state.polities[player] ?? null;
      }
      await this.loadMap();
      this.recolorMap();
    },

    get regionList() {
      if (!this.state) return [];
      return Object.values(this.state.regions);
    },

    get internalRegionList() {
      if (!this.state) return [];
      return Object.values(this.state.regions).filter(
        (r) => r.owner === this.state.player_polity,
      );
    },

    get polityList() {
      if (!this.state) return [];
      return Object.values(this.state.polities);
    },

    flagFor(polityName) {
      const iso = POLITY_TO_ISO3[polityName];
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
      try {
        const resp = await fetch("/assets/map/world-political.svg");
        if (!resp.ok) throw new Error("mapa não encontrado");
        const svgText = await resp.text();
        const host = document.getElementById("world-map");
        if (!host) return;
        host.innerHTML = svgText;
        const svg = host.querySelector("svg");
        if (svg) {
          svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
          svg.style.width = "100%";
          svg.style.height = "auto";
          svg.style.maxHeight = "70vh";
          svg.querySelectorAll("path").forEach((p) => {
            p.style.cursor = "pointer";
            p.addEventListener("click", () => this.selectByPath(p));
          });
        }
        this.mapLoaded = true;
      } catch (err) {
        console.warn("loadMap falhou:", err);
      }
    },

    recolorMap() {
      if (!this.state || !this.mapLoaded) return;
      const host = document.getElementById("world-map");
      if (!host) return;
      const svg = host.querySelector("svg");
      if (!svg) return;
      // Reset
      svg.querySelectorAll("path").forEach((p) => {
        p.setAttribute("fill", "#444");
        p.setAttribute("stroke-width", "0.5");
      });
      // Aplica cor por dono.
      Object.values(this.state.polities).forEach((polity) => {
        const iso = POLITY_TO_ISO3[polity.name];
        if (!iso) return;
        const path = svg.querySelector(`#${iso}`);
        if (!path) return;
        path.setAttribute("fill", this.colorFor(polity.name));
        if (polity.name === this.selectedPolity?.name) {
          path.setAttribute("stroke", "#fcd34d");
          path.setAttribute("stroke-width", "2");
        }
      });
    },

    selectByPath(pathEl) {
      const iso = pathEl.getAttribute("id");
      const polity = Object.values(this.state.polities).find(
        (p) => POLITY_TO_ISO3[p.name] === iso,
      );
      if (polity) {
        this.selectedPolity = polity;
        this.tab = "polity";
        this.recolorMap();
      }
    },

    selectByRegion(region) {
      if (!region.owner || !this.state) return;
      this.selectedPolity = this.state.polities[region.owner] ?? null;
      this.recolorMap();
    },

    selectByPolityName(name) {
      this.selectedPolity = this.state.polities[name] ?? null;
      this.recolorMap();
    },

    submitAction() {
      const description = this.actionDraft.trim();
      if (!description) return;
      this.pendingActions.push({
        description,
        submitted_on: this.state?.current_date ?? null,
        target_polities: [],
        target_regions: [],
        category: null,
      });
      this.actionDraft = "";
      this.status = `ação enfileirada (${this.pendingActions.length} pendentes)`;
    },

    async loadCampaign(name) {
      this.status = `carregando ${name}…`;
      const resp = await fetch(`/api/campaigns/${encodeURIComponent(name)}/state`);
      if (!resp.ok) {
        this.status = `falha ao carregar ${name}`;
        return;
      }
      const payload = await resp.json();
      this.state = payload.state;
      this.activeName = payload.campaign;
      this.selectedPolity = this.state.polities[this.state.player_polity] ?? null;
      this.pendingActions = this.state.pending_actions ?? [];
      this.eventsFeed = [];
      this.recolorMap();
      this.status = payload.invariant_violations.length
        ? `carregado com ${payload.invariant_violations.length} violações`
        : "carregado";
    },

    async advanceTime(months = 6) {
      if (!this.activeName) return;
      this.status = `avançando ${months} meses…`;
      const resp = await fetch(
        `/api/campaigns/${encodeURIComponent(this.activeName)}/turn`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ months }),
        },
      );
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({ detail: resp.statusText }));
        this.status = `turn falhou: ${err.detail}`;
        return;
      }
      const payload = await resp.json();
      this.eventsFeed = [...payload.events, ...this.eventsFeed].slice(0, 50);
      this.status = `turno aplicado · ${payload.deltas_applied} deltas`;
      // Recarrega estado do servidor.
      await this.loadCampaign(this.activeName);
    },

    async askAdvisor(question) {
      if (!this.activeName) return;
      this.advisorPending = true;
      this.advisorAnswer = "";
      try {
        const resp = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/advise`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
          },
        );
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          this.advisorAnswer = `erro: ${err.detail}`;
          return;
        }
        const payload = await resp.json();
        this.advisorAnswer = payload.answer;
      } finally {
        this.advisorPending = false;
      }
    },

    async sendDiplomatic(counterparty, message) {
      if (!this.activeName) return;
      this.diplomaticPending = true;
      try {
        const resp = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/dm`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ counterparty, message }),
          },
        );
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          this.status = `dm falhou: ${err.detail}`;
          return null;
        }
        return await resp.json();
      } finally {
        this.diplomaticPending = false;
      }
    },
  };
}
