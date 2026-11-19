<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Entrar | Tokyo Style</title>
  <link rel="stylesheet" type="text/css" href="/static/css/tokyo.css">
  <link rel="stylesheet" type="text/css" href="/static/css/portal.css">
  <script src="/static/js/tokyo.js" defer></script>
  <script src="/static/js/portal.js" defer></script>
</head>
<body class="page-portal">

  % include('app/views/html/partials/header', current_user=current_user, active='portal', show_bag=False)

  <main id="conteudo" class="portal">
    <section class="login-card">
      <div class="login-side" aria-hidden="true">
        <div class="sun"></div>
        <span class="vertical-kanji" lang="ja">ログイン</span>
      </div>

      <div class="login-form-wrap">
        <p class="eyebrow">ポータル · Área restrita</p>
        <h1>Entrar</h1>

        % if notice:
        <div class="flash flash-{{notice[0]}} flash-inline" role="alert">{{notice[1]}}</div>
        % end

        % if current_user:
        <p class="lead">Você já está conectado como <strong>{{current_user.display_name}}</strong>.</p>
        <div class="login-actions">
          % if current_user.is_admin:
          <a class="btn btn-red" href="/estoque">Ir para o estoque</a>
          % end
          <a class="btn btn-ghost" href="/">Voltar à loja</a>
        </div>
        % else:
        <p class="lead">Acesse sua conta Tokyo Style. Administradores têm acesso ao controle de estoque.</p>

        <form action="/portal" method="post" id="login-form" autocomplete="on">
          <div class="field">
            <label for="username">Usuário</label>
            <input id="username" name="username" type="text" autocomplete="username"
                   autocapitalize="none" spellcheck="false" maxlength="40" required autofocus>
          </div>

          <div class="field">
            <label for="password">Senha</label>
            <div class="password-row">
              <input id="password" name="password" type="password"
                     autocomplete="current-password" maxlength="80" required>
              <button type="button" class="toggle-pass" id="toggle-pass"
                      aria-label="Mostrar senha" aria-pressed="false">Mostrar</button>
            </div>
          </div>

          <p class="form-error" id="form-error" role="alert" hidden></p>

          <button type="submit" class="btn btn-red btn-block" id="login-submit">Entrar</button>
        </form>

        <details class="demo">
          <summary>Contas de demonstração</summary>
          <table>
            <thead><tr><th>Perfil</th><th>Usuário</th><th>Senha</th></tr></thead>
            <tbody>
              <tr><td>Administrador</td><td><code>admin</code></td><td><code>tokyo@2025</code></td></tr>
              <tr><td>Cliente</td><td><code>yuki</code></td><td><code>sakura123</code></td></tr>
            </tbody>
          </table>
          <button type="button" class="btn btn-ghost btn-sm" id="fill-admin">Preencher como admin</button>
        </details>
        % end

        <p class="back-link"><a href="/">← Voltar para a loja</a></p>
      </div>
    </section>
  </main>

  % include('app/views/html/partials/footer')
</body>
</html>
