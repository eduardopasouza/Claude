// sim-global frontend — Alpine.js component principal.

function campaign(initialState, examples, activeName) {
  return {
    examples,
    activeName,
    state: initialState,
    selectedPolity: null,
    actionDraft: "",
    pendingActions: initialState?.pending_actions ?? [],
    eventsFeed: [],
    status: "pronto",

    init() {
      if (this.state) {
        const player = this.state.player_polity;
        this.selectedPolity = this.state.polities[player] ?? null;
      }
    },

    get regionList() {
      if (!this.state) return [];
      return Object.values(this.state.regions);
    },

    colorFor(owner) {
      if (!owner) return "#3f3f3f";
      // hash do nome do dono em uma cor estável
      let h = 0;
      for (const c of owner) h = (h * 31 + c.charCodeAt(0)) | 0;
      const hue = ((h % 360) + 360) % 360;
      return `hsl(${hue}, 55%, 30%)`;
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

    selectByRegion(region) {
      if (!region.owner || !this.state) return;
      this.selectedPolity = this.state.polities[region.owner] ?? null;
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
      const resp = await fetch(`/api/state/${encodeURIComponent(name)}`);
      if (!resp.ok) {
        this.status = `falha ao carregar ${name}`;
        return;
      }
      const payload = await resp.json();
      this.state = payload.state;
      this.activeName = payload.campaign;
      this.selectedPolity = this.state.polities[this.state.player_polity] ?? null;
      this.pendingActions = this.state.pending_actions ?? [];
      this.status = payload.invariant_violations.length
        ? `carregado com ${payload.invariant_violations.length} violações`
        : "carregado";
    },

    advanceTime() {
      // stub: integração com /api/turn vem na fase do Agent SDK.
      this.status =
        "avançar tempo: stub. Integração game_master vem na próxima fase.";
    },
  };
}
