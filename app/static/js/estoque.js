// Tokyo Style - painel de estoque (administrador)
// Usa delegação de eventos para continuar funcionando quando a tabela é
// atualizada em tempo real (WebSocket).

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---------- Painel "Nova peça" ---------- */
  const panel = $("#add-panel");
  const toggleBtn = $("#toggle-add");
  function setPanel(open) {
    panel.hidden = !open;
    toggleBtn.setAttribute("aria-expanded", String(open));
    toggleBtn.textContent = open ? "Fechar" : "+ Nova peça";
    if (open) { $("#f-name").focus(); panel.scrollIntoView({ behavior: "smooth", block: "center" }); }
  }
  toggleBtn.addEventListener("click", () => setPanel(panel.hidden));
  $("#cancel-add").addEventListener("click", () => { $("#add-form").reset(); setPanel(false); });

  /* ---------- Busca e filtro por situação ---------- */
  const tbody = $("#stock-table tbody");
  const search = $("#search");
  const status = $("#filter-status");
  const counter = $("#result-count");
  const empty = $("#empty-row");

  function applyFilters() {
    const term = search.value.trim().toLowerCase();
    const st = status.value;
    let visible = 0;
    $$("tr", tbody).forEach(function (row) {
      const okTerm = !term || row.dataset.search.includes(term);
      const okStatus = st === "all" || row.dataset.status === st;
      const show = okTerm && okStatus;
      row.hidden = !show;
      if (show) visible++;
    });
    counter.textContent = visible + (visible === 1 ? " item" : " itens");
    empty.hidden = visible > 0;
  }
  search.addEventListener("input", applyFilters);
  status.addEventListener("change", applyFilters);

  /* ---------- Botões − / + e marcação de campo alterado ---------- */
  function markDirty(form) {
    const input = $("input", form);
    form.classList.toggle("is-dirty", input.value !== input.dataset.original);
  }
  tbody.addEventListener("click", function (ev) {
    const btn = ev.target.closest(".step");
    if (!btn) return;
    const form = btn.closest(".qty-form");
    const input = $("input", form);
    const next = (parseInt(input.value, 10) || 0) + parseInt(btn.dataset.step, 10);
    input.value = Math.max(0, Math.min(99999, next));
    markDirty(form);
  });
  tbody.addEventListener("input", function (ev) {
    const form = ev.target.closest(".qty-form");
    if (form) markDirty(form);
  });

  /* ---------- Confirmação antes de remover ---------- */
  tbody.addEventListener("submit", function (ev) {
    const form = ev.target.closest("form[data-confirm]");
    if (form && !window.confirm(form.dataset.confirm)) ev.preventDefault();
  });

  /* =======================================================
     TEMPO REAL (WebSocket)
     ======================================================= */
  const feed = $("#live-feed");

  function addFeed(text) {
    const first = $(".feed-empty", feed);
    if (first) first.remove();
    const li = document.createElement("li");
    const time = document.createElement("time");
    time.textContent = new Date().toLocaleTimeString("pt-BR");
    li.append(time, " " + text);        // textContent/append: sem risco de XSS
    feed.prepend(li);
    while (feed.children.length > 8) feed.lastElementChild.remove();
  }

  let refreshing = false;
  async function refreshTable(changedId) {
    if (refreshing) return;
    refreshing = true;
    try {
      const resp = await fetch("/estoque", { credentials: "same-origin" });
      // sessão expirada: o servidor redireciona ao login; nesse caso não mexemos na tela
      if (!resp.ok || new URL(resp.url).pathname !== "/estoque") return;
      const doc = new DOMParser().parseFromString(await resp.text(), "text/html");
      const freshBody = doc.querySelector("#stock-table tbody");
      const freshKpis = doc.querySelector(".kpis");
      if (!freshBody || !freshKpis) return;

      // não perde o que o admin está digitando em outras linhas
      const pending = {};
      $$(".qty-form.is-dirty", tbody).forEach(function (f) {
        pending[f.closest("tr").dataset.id] = $("input", f).value;
      });

      tbody.innerHTML = freshBody.innerHTML;
      $(".kpis").innerHTML = freshKpis.innerHTML;

      Object.keys(pending).forEach(function (id) {
        const row = $('tr[data-id="' + id + '"]', tbody);
        if (!row) return;
        $("input", row).value = pending[id];
        markDirty($(".qty-form", row));
      });

      applyFilters();
      const row = changedId && $('tr[data-id="' + changedId + '"]', tbody);
      if (row) { row.classList.add("updated"); setTimeout(() => row.classList.remove("updated"), 2000); }
    } catch (e) { /* tentamos de novo no próximo evento */ }
    finally { refreshing = false; }
  }

  document.addEventListener("tokyo:stock", function (ev) {
    const d = ev.detail || {};
    const texts = {
      atualizado: d.name + ": quantidade alterada para " + d.stock + " (" + d.status_label + ")",
      editado: d.name + " foi editado",
      adicionado: "Nova peça cadastrada: " + d.name,
      removido: d.name + " foi removido",
    };
    if (texts[d.action]) addFeed(texts[d.action]);
    refreshTable(d.id);
  });
  document.addEventListener("tokyo:ws-open", function (ev) {
    if (ev.detail && ev.detail.reconnect) refreshTable();
  });
});
