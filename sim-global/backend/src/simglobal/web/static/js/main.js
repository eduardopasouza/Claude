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
    advisorAnswer: "",
    advisorPending: false,
    diplomaticDraft: "",
    diplomaticPending: false,
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
      { key: "advisor", label: "Advisor", icon: "💬" },
    ],

    init() {
      if (this.state) {
        const player = this.state.player_polity;
        this.selectedPolity = this.state.polities[player] ?? null;
      }
      // Mostra onboarding na primeira visita (localStorage).
      try {
        const seen = localStorage.getItem("simglobal-welcome-seen");
        if (!seen) this.showWelcome = true;
      } catch (e) {
        this.showWelcome = true;
      }
      // Alpine não aguarda promises do init síncrono. Disparamos o
      // load do mapa em background; recolorMap é chamado dentro do
      // próprio loadMap após a injeção.
      this.loadMap();
    },

    dismissWelcome() {
      this.showWelcome = false;
      try {
        localStorage.setItem("simglobal-welcome-seen", "1");
      } catch (e) {}
    },

    openAgentNotice(feature) {
      this.errorModal = {
        open: true,
        title: `${feature} indisponível`,
        body:
          "Este servidor está em modo leitura: não tem o motor narrativo Claude " +
          "Opus 4.7 configurado. Você pode navegar pelo mapa, ler atributos da " +
          "polity e o histórico do cenário, mas turnos, diplomacia e advisor " +
          "exigem o Claude Agent SDK rodando com seu token Pro/Max.\n\n" +
          "Para ativar: rode o servidor em Fly.io ou Docker (instruções no " +
          "README do projeto na raiz: sim-global/README.md → Deploy público).",
      };
    },

    showError(title, body) {
      this.errorModal = { open: true, title, body };
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
      if (!host) {
        console.warn("loadMap: #world-map não está no DOM");
        return;
      }
      host.innerHTML = '<p class="text-stone-500 text-xs italic">carregando mapa…</p>';
      try {
        const resp = await fetch("/assets/map/world-political.svg");
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const svgText = await resp.text();
        host.innerHTML = svgText;
        const svg = host.querySelector("svg");
        if (!svg) {
          host.innerHTML = '<p class="text-rose-400 text-xs">SVG inválido</p>';
          throw new Error("SVG raiz ausente após injeção");
        }
        svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
        svg.style.width = "100%";
        svg.style.height = "auto";
        svg.style.maxHeight = "70vh";
        svg.style.touchAction = "pinch-zoom";
        const paths = svg.querySelectorAll("path");
        paths.forEach((p) => {
          p.style.cursor = "pointer";
          p.addEventListener("click", () => this.selectByPath(p));
        });
        console.info(`loadMap: ${paths.length} países carregados`);
        this.mapLoaded = true;
        // Recolore imediatamente (não espera próxima chamada).
        this.recolorMap();
      } catch (err) {
        console.warn("loadMap falhou:", err);
        host.innerHTML = `<p class="text-rose-400 text-xs">mapa indisponível: ${err.message}</p>`;
      }
    },

    recolorMap() {
      if (!this.state || !this.mapLoaded) return;
      const host = document.getElementById("world-map");
      if (!host) return;
      const svg = host.querySelector("svg");
      if (!svg) return;
      // Reset completo: fill, stroke e stroke-width.
      svg.querySelectorAll("path").forEach((p) => {
        p.setAttribute("fill", "#444");
        p.setAttribute("stroke", "#222");
        p.setAttribute("stroke-width", "0.5");
      });
      let coloredCount = 0;
      let missingIso = [];
      Object.values(this.state.polities).forEach((polity) => {
        const iso = this.iso3Of(polity);
        if (!iso) {
          missingIso.push(polity.name);
          return;
        }
        // CSS.escape protege contra ids exóticos.
        const escapedIso = window.CSS && CSS.escape ? CSS.escape(iso) : iso;
        const path = svg.querySelector(`#${escapedIso}`);
        if (!path) {
          missingIso.push(`${polity.name}→${iso}`);
          return;
        }
        path.setAttribute("fill", this.colorFor(polity.name));
        if (polity.name === this.selectedPolity?.name) {
          path.setAttribute("stroke", "#fcd34d");
          path.setAttribute("stroke-width", "2.5");
        }
        coloredCount++;
      });
      if (missingIso.length) {
        console.info(
          `recolorMap: ${coloredCount} polities pintadas; sem path:`,
          missingIso,
        );
      }
    },

    selectByPath(pathEl) {
      const iso = pathEl.getAttribute("id");
      const polity = Object.values(this.state.polities).find(
        (p) => this.iso3Of(p) === iso,
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
      try {
        const resp = await fetch(
          `/api/campaigns/${encodeURIComponent(this.activeName)}/turn`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ months }),
          },
        );
        if (resp.status === 503) {
          this.openAgentNotice("Avançar tempo");
          this.status = "modo leitura";
          return;
        }
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          this.showError("Falha ao avançar tempo", err.detail || resp.statusText);
          this.status = "erro";
          return;
        }
        const payload = await resp.json();
        this.eventsFeed = [...payload.events, ...this.eventsFeed].slice(0, 50);
        this.status = `turno aplicado · ${payload.deltas_applied} deltas`;
        await this.loadCampaign(this.activeName);
      } catch (err) {
        this.showError("Erro de rede", String(err));
        this.status = "erro";
      }
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
        if (resp.status === 503) {
          this.openAgentNotice("Advisor");
          return;
        }
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          this.advisorAnswer = `erro: ${err.detail || resp.statusText}`;
          return;
        }
        const payload = await resp.json();
        this.advisorAnswer = payload.answer;
      } catch (err) {
        this.advisorAnswer = `erro de rede: ${err}`;
      } finally {
        this.advisorPending = false;
      }
    },

    async sendDiplomatic(counterparty, message) {
      if (!this.activeName) return null;
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
        if (resp.status === 503) {
          this.openAgentNotice("Diplomacia");
          return null;
        }
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          this.showError("Falha diplomática", err.detail || resp.statusText);
          return null;
        }
        return await resp.json();
      } catch (err) {
        this.showError("Erro de rede", String(err));
        return null;
      } finally {
        this.diplomaticPending = false;
      }
    },
  };
}
