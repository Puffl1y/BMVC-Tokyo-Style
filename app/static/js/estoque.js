// Tokyo Style - painel de estoque (administrador)

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
  const rows = $$("#stock-table tbody tr");
  const search = $("#search");
  const status = $("#filter-status");
  const counter = $("#result-count");
  const empty = $("#empty-row");

  function applyFilters() {
    const term = search.value.trim().toLowerCase();
    const st = status.value;
    let visible = 0;
    rows.forEach(function (row) {
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
  $$(".qty-form").forEach(function (form) {
    const input = $("input", form);
    const original = input.value;
    const mark = () => form.classList.toggle("is-dirty", input.value !== original);

    $$(".step", form).forEach(function (btn) {
      btn.addEventListener("click", function () {
        const next = (parseInt(input.value, 10) || 0) + parseInt(btn.dataset.step, 10);
        input.value = Math.max(0, Math.min(99999, next));
        mark();
      });
    });
    input.addEventListener("input", mark);
  });

  /* ---------- Confirmação antes de remover ---------- */
  $$("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      if (!window.confirm(form.dataset.confirm)) ev.preventDefault();
    });
  });
});
