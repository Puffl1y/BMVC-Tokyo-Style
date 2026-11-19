// Tokyo Style - interações compartilhadas e da loja
// Todos os blocos verificam se os elementos existem (o arquivo é usado em várias páginas).

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const brl = (n) => "R$ " + n.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  /* ---------- Menu mobile ---------- */
  const navToggle = $("#nav-toggle");
  const navLinks = $("#nav-links");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      const open = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    $$("a", navLinks).forEach((a) => a.addEventListener("click", () => {
      navLinks.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    }));
  }

  /* ---------- Mensagens flash somem sozinhas ---------- */
  $$("[data-autohide]").forEach(function (el) {
    setTimeout(function () {
      el.classList.add("is-leaving");
      setTimeout(() => el.remove(), 600);
    }, 5000);
  });

  /* ---------- Toast ---------- */
  const toastEl = $("#toast");
  let toastTimer;
  function toast(message) {
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("is-visible"), 2400);
  }

  /* ---------- Revelar elementos ao rolar ---------- */
  const revealTargets = $$(".card, .pillars article, .visit-box, .about-lead");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach((el) => { el.classList.add("reveal"); io.observe(el); });
  }

  /* =======================================================
     Catálogo: filtro, ordenação, tamanho
     ======================================================= */
  const grid = $("#product-grid");
  if (grid) {
    const cards = $$(".card", grid);
    const countEl = $("#result-count");
    const sortEl = $("#sort");
    let currentFilter = "all";

    function updateCount() {
      const visible = cards.filter((c) => !c.classList.contains("is-hidden")).length;
      countEl.textContent = visible + (visible === 1 ? " produto" : " produtos");
    }

    $$(".chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        $$(".chip").forEach((c) => c.classList.remove("is-active"));
        chip.classList.add("is-active");
        currentFilter = chip.dataset.filter;
        cards.forEach(function (card) {
          const show = currentFilter === "all" || card.dataset.category === currentFilter;
          card.classList.toggle("is-hidden", !show);
        });
        updateCount();
      });
    });

    if (sortEl) {
      const original = cards.slice();   // ordem "Destaques" (a do servidor)
      sortEl.addEventListener("change", function () {
        let ordered = original.slice();
        if (sortEl.value === "price-asc") ordered.sort((a, b) => a.dataset.price - b.dataset.price);
        if (sortEl.value === "price-desc") ordered.sort((a, b) => b.dataset.price - a.dataset.price);
        if (sortEl.value === "name") ordered.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name, "pt-BR"));
        ordered.forEach((c) => grid.appendChild(c));
      });
    }

    // seleção de tamanho (um por cartão)
    $$(".sizes").forEach(function (group) {
      group.addEventListener("click", function (ev) {
        const btn = ev.target.closest(".size");
        if (!btn || btn.disabled) return;
        $$(".size", group).forEach(function (s) {
          const on = s === btn;
          s.classList.toggle("is-selected", on);
          s.setAttribute("aria-checked", String(on));
        });
      });
    });
  }

  /* =======================================================
     Sacola (guardada no navegador via localStorage)
     ======================================================= */
  const bagToggle = $("#bag-toggle");
  if (bagToggle) {
    const drawer = $("#bag-drawer");
    const backdrop = $("#drawer-backdrop");
    const listEl = $("#bag-list");
    const emptyEl = $("#bag-empty");
    const totalEl = $("#bag-total");
    const countEl = $("#bag-count");
    const KEY = "tokyostyle.bag";

    function load() {
      try {
        const data = JSON.parse(localStorage.getItem(KEY) || "[]");
        return Array.isArray(data) ? data : [];
      } catch (e) { return []; }
    }
    function save(items) {
      try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { /* modo privado */ }
    }

    let bag = load();

    function render() {
      listEl.innerHTML = "";
      let total = 0, qty = 0;
      bag.forEach(function (item, index) {
        total += item.price * item.qty;
        qty += item.qty;
        const li = document.createElement("li");
        li.className = "bag-item";

        const info = document.createElement("div");
        const name = document.createElement("strong");
        name.textContent = item.name;
        const meta = document.createElement("small");
        meta.textContent = " · Tam. " + item.size + " · " + item.qty + "x";
        info.append(name, meta);

        const price = document.createElement("span");
        price.className = "bag-price";
        price.textContent = brl(item.price * item.qty);

        const remove = document.createElement("button");
        remove.type = "button";
        remove.className = "bag-remove";
        remove.textContent = "Remover";
        remove.addEventListener("click", function () {
          bag.splice(index, 1);
          save(bag);
          render();
        });

        li.append(info, price, remove);
        listEl.appendChild(li);
      });
      emptyEl.hidden = bag.length > 0;
      totalEl.textContent = brl(total);
      countEl.textContent = qty;
      $("#bag-checkout").disabled = bag.length === 0;
      $("#bag-clear").disabled = bag.length === 0;
    }

    function openDrawer() {
      drawer.classList.add("is-open");
      drawer.setAttribute("aria-hidden", "false");
      backdrop.hidden = false;
      $("#bag-close").focus();
    }
    function closeDrawer() {
      drawer.classList.remove("is-open");
      drawer.setAttribute("aria-hidden", "true");
      backdrop.hidden = true;
      bagToggle.focus();
    }

    bagToggle.addEventListener("click", openDrawer);
    $("#bag-close").addEventListener("click", closeDrawer);
    backdrop.addEventListener("click", closeDrawer);
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && drawer.classList.contains("is-open")) closeDrawer();
    });

    $$(".add-to-bag").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const card = btn.closest(".card");
        const sizeBtn = $(".size.is-selected", card);
        const size = sizeBtn ? sizeBtn.textContent.trim() : "Único";
        const id = btn.dataset.id;
        const existing = bag.find((i) => i.id === id && i.size === size);
        if (existing) existing.qty += 1;
        else bag.push({ id: id, name: btn.dataset.name, price: parseFloat(btn.dataset.price), size: size, qty: 1 });
        save(bag);
        render();
        bagToggle.classList.remove("bump");
        void bagToggle.offsetWidth;               // reinicia a animação
        bagToggle.classList.add("bump");
        toast(btn.dataset.name + " (" + size + ") foi para a sacola");
      });
    });

    $("#bag-clear").addEventListener("click", function () {
      bag = [];
      save(bag);
      render();
    });
    $("#bag-checkout").addEventListener("click", function () {
      toast("Obrigado! Esta é uma demonstração: o pagamento não está habilitado.");
    });

    render();
  }

  /* ---------- Newsletter (validação no cliente) ---------- */
  const news = $("#newsletter");
  if (news) {
    news.addEventListener("submit", function (ev) {
      ev.preventDefault();
      const input = $("#news-email");
      const msg = $("#news-msg");
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(input.value.trim());
      msg.classList.toggle("is-error", !ok);
      msg.textContent = ok ? "Pronto! Você vai receber nossos lançamentos. ありがとう!" : "Informe um e-mail válido.";
      if (ok) input.value = "";
    });
  }
});
