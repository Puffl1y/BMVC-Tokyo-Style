// Tokyo Style - cliente WebSocket (tempo real)
// Conecta em ws://host/ws. Quando o servidor avisa que o estoque mudou,
// dispara o evento "tokyo:stock" no document (a loja e o painel escutam).
// Se a conexão cair, tenta reconectar sozinho e pede uma atualização.

(function () {
  "use strict";
  if (!("WebSocket" in window)) return;

  let retries = 0;
  let firstConnection = true;

  function setStatus(state, text) {
    const el = document.getElementById("live-status");
    if (!el) return;
    el.dataset.state = state;                       // on | off
    el.querySelector(".live-text").textContent = text;
  }

  function connect() {
    const proto = location.protocol === "https:" ? "wss://" : "ws://";
    const socket = new WebSocket(proto + location.host + "/ws");

    socket.addEventListener("open", function () {
      retries = 0;
      setStatus("on", "Ao vivo");
      // numa reconexão, pode ter havido mudanças enquanto estávamos offline
      document.dispatchEvent(new CustomEvent("tokyo:ws-open", { detail: { reconnect: !firstConnection } }));
      firstConnection = false;
    });

    socket.addEventListener("message", function (ev) {
      let data;
      try { data = JSON.parse(ev.data); } catch (e) { return; }
      document.dispatchEvent(new CustomEvent("tokyo:stock", { detail: data }));
    });

    socket.addEventListener("close", function () {
      setStatus("off", "Reconectando…");
      const wait = Math.min(10000, 1000 * Math.pow(2, retries++));
      setTimeout(connect, wait);
    });

    socket.addEventListener("error", function () { socket.close(); });
  }

  connect();
})();
