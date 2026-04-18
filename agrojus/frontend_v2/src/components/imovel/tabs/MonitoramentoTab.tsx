"use client";

import { useState } from "react";
import useSWR, { mutate } from "swr";
import {
  Bell,
  Plus,
  Trash2,
  Play,
  CheckCircle2,
  XCircle,
  Activity,
  Copy,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Loader2,
} from "lucide-react";
import { fetchWithAuth, swrFetcher } from "@/lib/api";
import type { PropertyData } from "../PropertyHeader";

type Webhook = {
  id: number;
  name: string;
  url: string;
  event_types: string[];
  car_filter: string | null;
  cpf_cnpj_filter: string | null;
  secret: string | null;
  active: boolean;
  created_at: string | null;
  last_delivery_at: string | null;
  last_delivery_status: string | null;
};

type WebhookDelivery = {
  id: number;
  event_type: string;
  success: boolean;
  status_code: number | null;
  attempt: number;
  attempted_at: string;
  duration_ms: number | null;
  error: string | null;
  response_body: string | null;
  payload: unknown;
};

const EVENT_LABELS: Record<string, string> = {
  mapbiomas_alert: "MapBiomas Alerta (desmate)",
  deter_alert: "DETER (alerta INPE)",
  prodes_alert: "PRODES (desmate consolidado)",
  ibama_embargo: "Embargo IBAMA",
  ibama_auto: "Auto de infração IBAMA",
  djen_publicacao: "Publicação DJEN",
  datajud_movimento: "Movimento processual (DataJud)",
  car_status_change: "Mudança status CAR",
  slave_labour: "Lista suja (MTE)",
};

const ALL_EVENTS = Object.keys(EVENT_LABELS);


export function MonitoramentoTab({ property }: { property: PropertyData }) {
  const [showForm, setShowForm] = useState(false);

  const { data, error, isLoading } = useSWR<{ total: number; webhooks: Webhook[] }>(
    `/webhooks?active_only=false`,
    swrFetcher,
    { revalidateOnFocus: false }
  );

  // Só webhooks deste CAR ou globais (car_filter = null OU = este car)
  const webhooksDoImovel = (data?.webhooks || []).filter(
    (w) => !w.car_filter || w.car_filter === property.car_code
  );

  return (
    <div className="p-6 space-y-5">
      <header className="flex flex-wrap items-center gap-3 justify-between">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Bell className="w-5 h-5 text-emerald-400" />
          Monitoramento do imóvel
        </h2>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm rounded-lg transition"
        >
          <Plus className="w-4 h-4" />
          Novo webhook
        </button>
      </header>

      <p className="text-sm text-slate-400 leading-relaxed">
        Cadastre URLs que receberão <code className="text-xs bg-slate-800 px-1.5 py-0.5 rounded">POST JSON</code> em
        tempo real quando eventos de interesse ocorrerem: novos alertas
        MapBiomas/DETER/PRODES, embargos IBAMA, publicações DJEN, mudanças no CAR
        ou inclusão na lista suja. Ideal para integrar com Slack, Zapier, n8n ou
        um bot interno.
      </p>

      {showForm && (
        <WebhookForm
          carCode={property.car_code}
          onCreated={() => {
            setShowForm(false);
            mutate(`/webhooks?active_only=false`);
          }}
          onCancel={() => setShowForm(false)}
        />
      )}

      {isLoading && (
        <div className="p-8 flex items-center justify-center text-slate-500 text-sm">
          <Loader2 className="w-4 h-4 animate-spin mr-2" /> Carregando…
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-950/30 border border-red-900/40 rounded text-red-300 text-sm">
          Erro: {String(error)}
        </div>
      )}

      {!isLoading && webhooksDoImovel.length === 0 && !showForm && (
        <div className="p-8 border border-dashed border-slate-800 rounded-xl text-center text-slate-500 text-sm">
          Nenhum webhook cadastrado para este imóvel.
        </div>
      )}

      {webhooksDoImovel.length > 0 && (
        <div className="space-y-3">
          {webhooksDoImovel.map((w) => (
            <WebhookRow key={w.id} webhook={w} />
          ))}
        </div>
      )}
    </div>
  );
}

// --------------------------------------------------------------------------
// Form de criação
// --------------------------------------------------------------------------

function WebhookForm({
  carCode,
  onCreated,
  onCancel,
}: {
  carCode: string;
  onCreated: () => void;
  onCancel: () => void;
}) {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [selected, setSelected] = useState<string[]>([...ALL_EVENTS]);
  const [restrictToCar, setRestrictToCar] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [created, setCreated] = useState<Webhook | null>(null);

  function toggle(evt: string) {
    setSelected((s) => (s.includes(evt) ? s.filter((x) => x !== evt) : [...s, evt]));
  }

  async function submit() {
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetchWithAuth("/webhooks", {
        method: "POST",
        body: JSON.stringify({
          name,
          url,
          event_types: selected,
          car_filter: restrictToCar ? carCode : null,
          active: true,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const w = (await res.json()) as Webhook;
      setCreated(w);
    } catch (e) {
      setError(String(e));
    } finally {
      setSubmitting(false);
    }
  }

  if (created) {
    return (
      <div className="border border-emerald-900/40 bg-emerald-950/20 rounded-xl p-5 space-y-4">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <h3 className="font-semibold text-emerald-300">Webhook criado</h3>
        </div>
        <div className="text-sm text-slate-300 space-y-2">
          <p>
            Guarde o <strong>secret</strong> abaixo — ele é mostrado apenas uma
            vez e será usado como assinatura HMAC-SHA256 no header{" "}
            <code className="text-xs bg-slate-800 px-1.5 py-0.5 rounded">
              X-AgroJus-Signature
            </code>{" "}
            para validar que o POST veio do AgroJus.
          </p>
          <div className="bg-slate-900 border border-slate-800 p-3 rounded flex items-center gap-2">
            <code className="text-xs text-emerald-300 break-all flex-1">
              {created.secret}
            </code>
            <button
              onClick={() => navigator.clipboard.writeText(created.secret || "")}
              className="p-1.5 hover:bg-slate-800 rounded transition"
              title="Copiar"
            >
              <Copy className="w-3.5 h-3.5 text-slate-400" />
            </button>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={onCreated}
            className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm rounded-lg transition"
          >
            Concluir
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="border border-slate-800 bg-slate-900/40 rounded-xl p-5 space-y-4">
      <h3 className="font-semibold text-slate-100">Novo webhook</h3>

      <div className="grid gap-3 sm:grid-cols-2">
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">Nome</span>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Slack alerts, n8n fluxo X..."
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-xs text-slate-400">URL</span>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://hooks.slack.com/..."
            className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-slate-100"
          />
        </label>
      </div>

      <div>
        <p className="text-xs text-slate-400 mb-2">Eventos monitorados</p>
        <div className="grid gap-1.5 sm:grid-cols-2 md:grid-cols-3">
          {ALL_EVENTS.map((evt) => {
            const on = selected.includes(evt);
            return (
              <button
                key={evt}
                onClick={() => toggle(evt)}
                className={`text-xs px-2.5 py-1.5 rounded border text-left transition ${
                  on
                    ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300"
                    : "border-slate-800 text-slate-500 hover:text-slate-300"
                }`}
              >
                {EVENT_LABELS[evt] || evt}
              </button>
            );
          })}
        </div>
      </div>

      <label className="flex items-center gap-2 text-sm text-slate-300">
        <input
          type="checkbox"
          checked={restrictToCar}
          onChange={(e) => setRestrictToCar(e.target.checked)}
          className="accent-emerald-500"
        />
        Restringir a este imóvel ({carCode.slice(0, 12)}…)
      </label>

      {error && (
        <div className="p-3 bg-red-950/30 border border-red-900/40 rounded text-red-300 text-xs">
          {error}
        </div>
      )}

      <div className="flex gap-2 pt-2">
        <button
          onClick={submit}
          disabled={submitting || !name || !url || selected.length === 0}
          className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {submitting ? "Salvando…" : "Criar"}
        </button>
        <button
          onClick={onCancel}
          className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm rounded-lg transition"
        >
          Cancelar
        </button>
      </div>
    </div>
  );
}

// --------------------------------------------------------------------------
// Linha do webhook (expansível)
// --------------------------------------------------------------------------

function WebhookRow({ webhook }: { webhook: Webhook }) {
  const [expanded, setExpanded] = useState(false);
  const [testing, setTesting] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [toggleLoading, setToggleLoading] = useState(false);

  const { data: deliveriesData } = useSWR<{
    total: number;
    deliveries: WebhookDelivery[];
  }>(
    expanded ? `/webhooks/${webhook.id}/deliveries?limit=20` : null,
    swrFetcher,
    { refreshInterval: 15_000 }
  );

  async function test() {
    setTesting(true);
    try {
      const res = await fetchWithAuth(`/webhooks/${webhook.id}/test`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(await res.text());
      mutate(`/webhooks/${webhook.id}/deliveries?limit=20`);
      mutate(`/webhooks?active_only=false`);
    } catch (e) {
      alert(`Falha ao testar: ${e}`);
    } finally {
      setTesting(false);
    }
  }

  async function toggleActive() {
    setToggleLoading(true);
    try {
      const res = await fetchWithAuth(`/webhooks/${webhook.id}`, {
        method: "PUT",
        body: JSON.stringify({ active: !webhook.active }),
      });
      if (!res.ok) throw new Error(await res.text());
      mutate(`/webhooks?active_only=false`);
    } finally {
      setToggleLoading(false);
    }
  }

  async function del() {
    if (!confirm(`Remover webhook "${webhook.name}"?`)) return;
    setDeleting(true);
    try {
      const res = await fetchWithAuth(`/webhooks/${webhook.id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error(await res.text());
      mutate(`/webhooks?active_only=false`);
    } finally {
      setDeleting(false);
    }
  }

  const statusColor = webhook.last_delivery_status === "success"
    ? "text-emerald-400"
    : webhook.last_delivery_status === "failed"
    ? "text-red-400"
    : "text-slate-500";

  return (
    <div className="border border-slate-800 rounded-xl bg-slate-900/20">
      <div className="p-4 flex items-start gap-3">
        <div
          className={`w-2 h-2 mt-2 rounded-full flex-shrink-0 ${
            webhook.active ? "bg-emerald-400" : "bg-slate-600"
          }`}
        />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <h3 className="font-medium text-slate-100 truncate">
              {webhook.name}
            </h3>
            {webhook.car_filter && (
              <span className="text-[10px] uppercase bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">
                imóvel
              </span>
            )}
            {!webhook.active && (
              <span className="text-[10px] uppercase bg-slate-800 text-slate-500 px-1.5 py-0.5 rounded">
                pausado
              </span>
            )}
          </div>
          <p className="text-xs text-slate-400 truncate mt-0.5">{webhook.url}</p>
          <div className="text-xs text-slate-500 mt-1.5 flex flex-wrap gap-x-4 gap-y-1">
            <span>{webhook.event_types.length} eventos</span>
            {webhook.last_delivery_at && (
              <span className={statusColor}>
                Última entrega: {new Date(webhook.last_delivery_at).toLocaleString("pt-BR")}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1 flex-shrink-0">
          <button
            onClick={test}
            disabled={testing}
            className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-slate-200 transition disabled:opacity-50"
            title="Disparar teste"
          >
            {testing ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5" />}
          </button>
          <button
            onClick={toggleActive}
            disabled={toggleLoading}
            className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-slate-200 transition disabled:opacity-50"
            title={webhook.active ? "Pausar" : "Ativar"}
          >
            <Activity className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setExpanded((v) => !v)}
            className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-slate-200 transition"
            title="Ver logs"
          >
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
          <button
            onClick={del}
            disabled={deleting}
            className="p-1.5 hover:bg-red-950/40 rounded text-slate-500 hover:text-red-400 transition disabled:opacity-50"
            title="Remover"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {expanded && (
        <div className="border-t border-slate-800 p-4 bg-slate-950/40">
          <h4 className="text-xs uppercase text-slate-500 font-medium mb-2">
            Últimas 20 entregas
          </h4>
          {!deliveriesData && (
            <div className="text-slate-500 text-sm py-2 flex items-center gap-2">
              <Loader2 className="w-3.5 h-3.5 animate-spin" /> Carregando logs…
            </div>
          )}
          {deliveriesData && deliveriesData.deliveries.length === 0 && (
            <p className="text-slate-500 text-sm py-2">
              Nenhuma entrega registrada ainda.
            </p>
          )}
          {deliveriesData && deliveriesData.deliveries.length > 0 && (
            <div className="space-y-1.5">
              {deliveriesData.deliveries.map((d) => (
                <DeliveryRow key={d.id} delivery={d} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function DeliveryRow({ delivery }: { delivery: WebhookDelivery }) {
  const [expanded, setExpanded] = useState(false);

  const Icon = delivery.success ? CheckCircle2 : XCircle;
  const color = delivery.success ? "text-emerald-400" : "text-red-400";

  return (
    <div className="border border-slate-800 rounded bg-slate-900/40 text-xs">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full p-2.5 flex items-center gap-2 hover:bg-slate-900 transition text-left"
      >
        <Icon className={`w-3.5 h-3.5 flex-shrink-0 ${color}`} />
        <span className="text-slate-300 font-mono">
          {delivery.event_type}
        </span>
        <span className="text-slate-500">
          {delivery.status_code ? `HTTP ${delivery.status_code}` : "sem resposta"}
        </span>
        {delivery.duration_ms !== null && (
          <span className="text-slate-500">{delivery.duration_ms}ms</span>
        )}
        <span className="text-slate-500 ml-auto">
          {new Date(delivery.attempted_at).toLocaleString("pt-BR")}
        </span>
      </button>
      {expanded && (
        <div className="border-t border-slate-800 p-3 space-y-2">
          {delivery.error && (
            <div className="bg-red-950/20 border border-red-900/40 text-red-300 p-2 rounded">
              <AlertCircle className="w-3.5 h-3.5 inline mr-1" />
              {delivery.error}
            </div>
          )}
          {delivery.response_body && (
            <details>
              <summary className="text-slate-500 cursor-pointer">
                Resposta do destino
              </summary>
              <pre className="mt-2 p-2 bg-slate-950 rounded text-slate-400 overflow-auto max-h-40 text-[10px]">
                {delivery.response_body}
              </pre>
            </details>
          )}
          <details>
            <summary className="text-slate-500 cursor-pointer">
              Payload enviado
            </summary>
            <pre className="mt-2 p-2 bg-slate-950 rounded text-slate-400 overflow-auto max-h-60 text-[10px]">
              {JSON.stringify(delivery.payload, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}
