"use client";

/**
 * Aba Monitoramento do Hub Jurídico-Agro.
 *
 * GET /api/v1/juridico/monitoramento — lista dos monitoramentos ativos
 * POST /api/v1/juridico/monitoramento — cadastra novo
 * DELETE /api/v1/juridico/monitoramento/{id}
 *
 * Útil para acompanhamento contínuo de vendedores, fornecedores,
 * sócios, partes contrárias, etc.
 */

import { useState } from "react";
import useSWR from "swr";
import {
  Loader2,
  BellRing,
  Plus,
  Trash2,
  Check,
  Clock,
  Webhook,
  Tag as TagIcon,
  User2,
  AlertCircle,
  Calendar,
} from "lucide-react";
import { swrFetcher, fetchWithAuth } from "@/lib/api";

type Monitoramento = {
  id: number;
  cpf_cnpj: string;
  nome_sugerido?: string;
  contexto?: string;
  tags?: string[];
  eventos_monitorados: string[];
  frequencia: string;
  webhook_url: boolean;
  active: boolean;
  created_at?: string;
  last_checked_at?: string;
};

const EVENTOS_DISPONIVEIS = [
  { value: "datajud_novo_processo", label: "Novo processo (DataJud)" },
  { value: "ibama_auto", label: "Novo auto IBAMA" },
  { value: "ceis", label: "Sanção CEIS" },
  { value: "cnep", label: "Sanção CNEP" },
  { value: "lista_suja", label: "Lista Suja MTE" },
  { value: "djen", label: "Publicação DJEN" },
];

const FREQUENCIAS = [
  { value: "diaria", label: "Diária" },
  { value: "semanal", label: "Semanal" },
  { value: "mensal", label: "Mensal" },
];

export function MonitoramentoTab() {
  const [showForm, setShowForm] = useState(false);

  const { data, error, isLoading, mutate } = useSWR<{
    total: number;
    monitoramentos: Monitoramento[];
  }>(`/juridico/monitoramento`, swrFetcher, { revalidateOnFocus: false });

  const monits = data?.monitoramentos ?? [];

  async function handleDelete(id: number) {
    if (!confirm("Remover este monitoramento?")) return;
    try {
      const res = await fetchWithAuth(`/juridico/monitoramento/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error(await res.text());
      await mutate();
    } catch (err) {
      alert(`Erro ao remover: ${String(err)}`);
    }
  }

  return (
    <div className="space-y-5">
      {/* Banner + ação */}
      <div className="p-4 rounded-2xl border border-border bg-card/50 backdrop-blur-sm flex items-start gap-4">
        <BellRing className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold mb-1">
            Acompanhamento contínuo de partes
          </h3>
          <p className="text-xs text-muted-foreground">
            Cadastre CPFs/CNPJs que você precisa acompanhar (vendedor,
            fornecedor, sócio, parte contrária). A plataforma varre as bases
            oficiais na frequência escolhida e alerta quando surgem novos
            eventos relevantes.
          </p>
        </div>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition font-semibold text-sm inline-flex items-center gap-2 flex-shrink-0"
        >
          <Plus className="h-4 w-4" />
          {showForm ? "Cancelar" : "Cadastrar"}
        </button>
      </div>

      {showForm && (
        <MonitoramentoForm
          onClose={() => setShowForm(false)}
          onSaved={async () => {
            setShowForm(false);
            await mutate();
          }}
        />
      )}

      {error && !isLoading && (
        <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm flex items-start gap-2">
          <AlertCircle className="h-4 w-4 flex-shrink-0 mt-0.5" />
          <div>
            Erro ao carregar monitoramentos. Se o endpoint exige autenticação,
            verifique se você está logado.
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="p-10 text-center text-muted-foreground flex items-center justify-center gap-3">
          <Loader2 className="h-4 w-4 animate-spin" /> Carregando
          monitoramentos…
        </div>
      ) : monits.length === 0 && !showForm ? (
        <div className="p-10 text-center text-muted-foreground border border-dashed border-border rounded-2xl">
          <BellRing className="h-10 w-10 mx-auto mb-4 text-muted-foreground/50" />
          <div className="text-sm font-medium mb-2">
            Nenhum monitoramento ativo.
          </div>
          <div className="text-xs max-w-md mx-auto">
            Clique em “Cadastrar” acima para começar a acompanhar novos
            eventos de uma parte específica.
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {monits.map((m) => (
            <MonitoramentoCard
              key={m.id}
              monit={m}
              onDelete={() => handleDelete(m.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function MonitoramentoForm({
  onClose,
  onSaved,
}: {
  onClose: () => void;
  onSaved: () => void | Promise<void>;
}) {
  const [cpfCnpj, setCpfCnpj] = useState("");
  const [nome, setNome] = useState("");
  const [contexto, setContexto] = useState("");
  const [tags, setTags] = useState("");
  const [eventos, setEventos] = useState<string[]>(
    EVENTOS_DISPONIVEIS.map((e) => e.value),
  );
  const [frequencia, setFrequencia] = useState("diaria");
  const [webhookUrl, setWebhookUrl] = useState("");
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  function toggleEvento(v: string) {
    setEventos((prev) =>
      prev.includes(v) ? prev.filter((e) => e !== v) : [...prev, v],
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    const clean = cpfCnpj.replace(/\D/g, "");
    if (clean.length !== 11 && clean.length !== 14) {
      setErr("CPF (11) ou CNPJ (14) inválido.");
      return;
    }
    if (eventos.length === 0) {
      setErr("Selecione ao menos um tipo de evento.");
      return;
    }

    setSaving(true);
    try {
      const payload = {
        cpf_cnpj: clean,
        nome_sugerido: nome || undefined,
        contexto: contexto || undefined,
        tags: tags.trim()
          ? tags.split(",").map((t) => t.trim()).filter(Boolean)
          : undefined,
        eventos_monitorados: eventos,
        frequencia,
        webhook_url: webhookUrl || undefined,
      };
      const res = await fetchWithAuth("/juridico/monitoramento", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(await res.text());
      await onSaved();
    } catch (error) {
      setErr(String(error));
    } finally {
      setSaving(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="p-5 rounded-2xl border border-primary/30 bg-primary/5 space-y-4"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label className="flex flex-col gap-1">
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            CPF ou CNPJ *
          </span>
          <input
            required
            value={cpfCnpj}
            onChange={(e) => setCpfCnpj(e.target.value)}
            placeholder="000.000.000-00 ou 00.000.000/0000-00"
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Nome sugerido (opcional)
          </span>
          <input
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            placeholder="ex. Vendedor — Fazenda Rio Verde"
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </label>
        <label className="flex flex-col gap-1 md:col-span-2">
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Contexto (opcional)
          </span>
          <input
            value={contexto}
            onChange={(e) => setContexto(e.target.value)}
            placeholder="Descreva o motivo do monitoramento"
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Tags (separadas por vírgula)
          </span>
          <input
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="aquisição, due-diligence"
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Frequência
          </span>
          <select
            value={frequencia}
            onChange={(e) => setFrequencia(e.target.value)}
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm"
          >
            {FREQUENCIAS.map((f) => (
              <option key={f.value} value={f.value}>
                {f.label}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 md:col-span-2">
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            Webhook URL (opcional)
          </span>
          <input
            value={webhookUrl}
            onChange={(e) => setWebhookUrl(e.target.value)}
            placeholder="https://exemplo.com/hook"
            className="bg-input/40 border border-border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </label>
      </div>

      <div>
        <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-1.5">
          Eventos monitorados
        </div>
        <div className="flex flex-wrap gap-1.5">
          {EVENTOS_DISPONIVEIS.map((e) => {
            const on = eventos.includes(e.value);
            return (
              <button
                type="button"
                key={e.value}
                onClick={() => toggleEvento(e.value)}
                className={`
                  inline-flex items-center gap-1 px-2.5 py-1 rounded-lg border text-xs font-medium transition
                  ${
                    on
                      ? "bg-primary/10 text-primary border-primary/30"
                      : "bg-muted/30 text-muted-foreground border-border hover:bg-muted/50"
                  }
                `}
              >
                {on && <Check className="h-3 w-3" />}
                {e.label}
              </button>
            );
          })}
        </div>
      </div>

      {err && (
        <div className="p-3 rounded-lg border border-rose-500/30 bg-rose-500/10 text-rose-300 text-xs flex items-start gap-2">
          <AlertCircle className="h-4 w-4 flex-shrink-0 mt-0.5" />
          {err}
        </div>
      )}

      <div className="flex items-center gap-2">
        <button
          type="submit"
          disabled={saving}
          className="px-5 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition font-semibold text-sm disabled:opacity-40 disabled:cursor-not-allowed inline-flex items-center gap-2"
        >
          {saving ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Salvando…
            </>
          ) : (
            <>
              <Plus className="h-4 w-4" /> Criar monitoramento
            </>
          )}
        </button>
        <button
          type="button"
          onClick={onClose}
          className="px-4 py-2 rounded-lg border border-border hover:bg-muted transition text-sm"
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}

function MonitoramentoCard({
  monit,
  onDelete,
}: {
  monit: Monitoramento;
  onDelete: () => void;
}) {
  return (
    <div className="p-4 rounded-2xl border border-border bg-card/30">
      <div className="flex items-start gap-3 mb-3">
        <User2 className="h-4 w-4 text-primary flex-shrink-0 mt-0.5" />
        <div className="min-w-0 flex-1">
          <div className="text-sm font-medium">
            {monit.nome_sugerido || "Parte sem nome"}
          </div>
          <div className="text-xs font-mono text-muted-foreground">
            {monit.cpf_cnpj}
          </div>
        </div>
        <span
          className={`text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border ${
            monit.active
              ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/30"
              : "bg-muted text-muted-foreground border-border"
          }`}
        >
          {monit.active ? "ativo" : "inativo"}
        </span>
        <button
          onClick={onDelete}
          className="p-1 hover:bg-rose-500/10 hover:text-rose-400 rounded transition text-muted-foreground"
          title="Remover"
        >
          <Trash2 className="h-3.5 w-3.5" />
        </button>
      </div>

      {monit.contexto && (
        <p className="text-xs text-muted-foreground italic mb-2">
          {monit.contexto}
        </p>
      )}

      <div className="flex flex-wrap gap-1.5 mb-2">
        {monit.eventos_monitorados.map((ev) => {
          const meta = EVENTOS_DISPONIVEIS.find((e) => e.value === ev);
          return (
            <span
              key={ev}
              className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-muted/60 border border-border uppercase tracking-wider"
            >
              {meta?.label ?? ev}
            </span>
          );
        })}
      </div>

      {monit.tags && monit.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {monit.tags.map((t) => (
            <span
              key={t}
              className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20"
            >
              <TagIcon className="h-2.5 w-2.5" /> {t}
            </span>
          ))}
        </div>
      )}

      <div className="flex flex-wrap items-center gap-3 text-[11px] text-muted-foreground mt-2 pt-2 border-t border-border">
        <span className="flex items-center gap-1">
          <Clock className="h-3 w-3" /> {monit.frequencia}
        </span>
        {monit.webhook_url && (
          <span className="flex items-center gap-1 text-primary">
            <Webhook className="h-3 w-3" /> webhook
          </span>
        )}
        {monit.created_at && (
          <span className="flex items-center gap-1 ml-auto">
            <Calendar className="h-3 w-3" /> criado em{" "}
            {new Date(monit.created_at).toLocaleDateString("pt-BR")}
          </span>
        )}
        {monit.last_checked_at && (
          <span className="flex items-center gap-1">
            última checagem{" "}
            {new Date(monit.last_checked_at).toLocaleDateString("pt-BR")}
          </span>
        )}
      </div>
    </div>
  );
}
