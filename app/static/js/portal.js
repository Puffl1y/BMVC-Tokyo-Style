// Tokyo Style - comportamento da página de login

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  const form = document.getElementById("login-form");
  if (!form) return;   // usuário já logado: não há formulário

  const user = document.getElementById("username");
  const pass = document.getElementById("password");
  const toggle = document.getElementById("toggle-pass");
  const error = document.getElementById("form-error");
  const submit = document.getElementById("login-submit");

  // mostrar / ocultar senha
  toggle.addEventListener("click", function () {
    const show = pass.type === "password";
    pass.type = show ? "text" : "password";
    toggle.textContent = show ? "Ocultar" : "Mostrar";
    toggle.setAttribute("aria-pressed", String(show));
    toggle.setAttribute("aria-label", show ? "Ocultar senha" : "Mostrar senha");
  });

  // validação simples antes de enviar
  form.addEventListener("submit", function (ev) {
    const problems = [];
    if (user.value.trim().length < 3) problems.push("O usuário deve ter ao menos 3 caracteres.");
    if (pass.value.length < 4) problems.push("A senha deve ter ao menos 4 caracteres.");
    if (problems.length) {
      ev.preventDefault();
      error.textContent = problems[0];
      error.hidden = false;
      (user.value.trim().length < 3 ? user : pass).focus();
      return;
    }
    error.hidden = true;
    submit.disabled = true;
    submit.textContent = "Entrando…";
  });

  // preenchimento rápido da conta de demonstração
  const fill = document.getElementById("fill-admin");
  if (fill) {
    fill.addEventListener("click", function () {
      user.value = "admin";
      pass.value = "tokyo@2025";
      pass.focus();
    });
  }
});
