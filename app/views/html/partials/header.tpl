<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>

<header class="site-header">
  <div class="announce" role="note">
    <span>新作 NOVA COLEÇÃO OUTONO/INVERNO</span>
    <span class="dot">●</span>
    <span>FRETE GRÁTIS ACIMA DE R$ 299</span>
    <span class="dot">●</span>
    <span>TROCA FÁCIL EM 30 DIAS</span>
  </div>

  <nav class="navbar" aria-label="Navegação principal">
    <a class="logo" href="/" aria-label="Tokyo Style - página inicial">
      <span class="logo-kanji" lang="ja">東京</span>
      <span class="logo-text">TOKYO&nbsp;STYLE</span>
    </a>

    <button class="nav-toggle" id="nav-toggle" type="button"
            aria-expanded="false" aria-controls="nav-links">
      <span class="sr-only">Abrir menu</span>
      <span class="bars" aria-hidden="true"></span>
    </button>

    <ul class="nav-links" id="nav-links">
      <li><a href="/#colecao" class="{{'is-active' if active == 'home' else ''}}">Coleção</a></li>
      <li><a href="/#sobre">Sobre</a></li>
      <li><a href="/#visite">Visite</a></li>
      % if current_user and current_user.is_admin:
      <li><a href="/estoque" class="{{'is-active' if active == 'estoque' else ''}}">Estoque</a></li>
      % end
    </ul>

    <div class="nav-actions">
      % if show_bag:
      <button class="bag-btn" id="bag-toggle" type="button" aria-label="Abrir sacola">
        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M5 8h14l-1 12H6L5 8Z M9 8V6a3 3 0 0 1 6 0v2" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>
        <span class="bag-count" id="bag-count">0</span>
      </button>
      % end

      % if current_user:
      <span class="hello">Olá, <strong>{{current_user.display_name}}</strong></span>
      <form action="/logout" method="post" class="inline-form">
        <button type="submit" class="btn btn-ghost btn-sm">Sair</button>
      </form>
      % else:
      <a href="/portal" class="btn btn-ink btn-sm">Entrar</a>
      % end
    </div>
  </nav>
</header>
