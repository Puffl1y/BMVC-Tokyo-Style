<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Tokyo Style - streetwear inspirado em Tóquio: camisetas, moletons, jaquetas, calças e acessórios.">
  <title>Tokyo Style | Streetwear inspirado em Tóquio</title>
  <link rel="stylesheet" type="text/css" href="/static/css/tokyo.css">
  <script src="/static/js/tokyo.js" defer></script>
</head>
<body class="page-home">

  % include('app/views/html/partials/header', current_user=current_user, active='home', show_bag=True)

  % if notice:
  <div class="flash flash-{{notice[0]}}" role="status" data-autohide>{{notice[1]}}</div>
  % end

  <main id="conteudo">

    <!-- ===================== HERO ===================== -->
    <section class="hero">
      <div class="hero-text">
        <p class="eyebrow">東京スタイル · Outono/Inverno 2025</p>
        <h1>As ruas de Tóquio,<br>no seu <em>guarda-roupa</em>.</h1>
        <p class="lead">Peças oversized, cortes limpos e detalhes que nascem em Shibuya, Harajuku e Shinjuku.
          Visual urbano, confortável e cheio de personalidade.</p>
        <div class="hero-cta">
          <a href="#colecao" class="btn btn-red">Ver coleção</a>
          <a href="#sobre" class="btn btn-ghost">Conheça a marca</a>
        </div>
        <dl class="hero-stats">
          <div><dt>{{len(products)}}</dt><dd>peças na coleção</dd></div>
          <div><dt>30</dt><dd>dias para trocar</dd></div>
          <div><dt>4,9</dt><dd>nota dos clientes</dd></div>
        </dl>
      </div>

      <div class="hero-art" aria-hidden="true">
        <div class="sun"></div>
        <span class="vertical-kanji" lang="ja">東京スタイル</span>
        <div class="hero-card c1"><svg><use href="/static/img/icons.svg#hoodie"/></svg></div>
        <div class="hero-card c2"><svg><use href="/static/img/icons.svg#jacket"/></svg></div>
        <div class="hero-card c3"><svg><use href="/static/img/icons.svg#cap"/></svg></div>
      </div>
    </section>

    <div class="marquee" aria-hidden="true">
      <div class="marquee-track">
        <span>STREETWEAR</span><span lang="ja">渋谷</span><span>OVERSIZED</span><span lang="ja">原宿</span>
        <span>NEW DROP</span><span lang="ja">新宿</span><span>URBAN MOOD</span><span lang="ja">秋葉原</span>
        <span>STREETWEAR</span><span lang="ja">渋谷</span><span>OVERSIZED</span><span lang="ja">原宿</span>
        <span>NEW DROP</span><span lang="ja">新宿</span><span>URBAN MOOD</span><span lang="ja">秋葉原</span>
      </div>
    </div>

    <!-- ===================== COLEÇÃO ===================== -->
    <section class="section" id="colecao">
      <header class="section-head">
        <div>
          <p class="eyebrow">コレクション</p>
          <h2>Coleção</h2>
        </div>
        <div class="tools">
          <label class="sr-only" for="sort">Ordenar produtos</label>
          <select id="sort" class="select">
            <option value="default">Destaques</option>
            <option value="price-asc">Menor preço</option>
            <option value="price-desc">Maior preço</option>
            <option value="name">Nome (A-Z)</option>
          </select>
        </div>
      </header>

      <div class="filters" role="group" aria-label="Filtrar por categoria">
        <button type="button" class="chip is-active" data-filter="all">Tudo</button>
        % for slug, label in categories:
        <button type="button" class="chip" data-filter="{{slug}}">{{label}}</button>
        % end
      </div>
      <p class="result-count" id="result-count" aria-live="polite">{{len(products)}} produtos</p>

      <div class="grid" id="product-grid">
        % for p in products:
        <article class="card status-{{p.status}}" data-category="{{p.category}}"
                 data-price="{{p.price}}" data-name="{{p.name}}">
          <div class="card-media" style="--garment: {{p.color}}">
            <svg class="garment" aria-hidden="true"><use href="/static/img/icons.svg#{{p.icon}}"/></svg>
            % if p.status == 'out':
            <span class="badge badge-out">Esgotado</span>
            % elif p.status == 'low':
            <span class="badge badge-low">Últimas {{p.stock}}</span>
            % end
          </div>
          <div class="card-body">
            <p class="card-cat">{{p.category_label}}</p>
            <h3>{{p.name}}</h3>
            <p class="price">R$ {{p.price_br}}</p>
            <div class="sizes" role="radiogroup" aria-label="Tamanho de {{p.name}}">
              % for i, s in enumerate(p.sizes):
              <button type="button" class="size {{'is-selected' if i == 0 else ''}}"
                      role="radio" aria-checked="{{'true' if i == 0 else 'false'}}"
                      {{'disabled' if p.status == 'out' else ''}}>{{s}}</button>
              % end
            </div>
            <button type="button" class="btn btn-ink btn-block add-to-bag"
                    data-id="{{p.id}}" data-name="{{p.name}}" data-price="{{p.price}}"
                    {{'disabled' if p.status == 'out' else ''}}>
              {{'Indisponível' if p.status == 'out' else 'Adicionar à sacola'}}
            </button>
          </div>
        </article>
        % end
      </div>
    </section>

    <!-- ===================== SOBRE ===================== -->
    <section class="section about" id="sobre">
      <header class="section-head">
        <div>
          <p class="eyebrow">私たちについて</p>
          <h2>Sobre a Tokyo Style</h2>
        </div>
      </header>
      <p class="about-lead">A Tokyo Style nasceu da vontade de trazer para o Brasil a liberdade criativa da moda de rua japonesa.
        Misturamos silhuetas amplas, tons sóbrios, toques de vermelho e estampas gráficas para criar looks que funcionam
        do trabalho ao rolê.</p>
      <div class="pillars">
        <article>
          <span class="pillar-kanji" lang="ja">質</span>
          <h3>Qualidade</h3>
          <p>Algodão de gramatura alta, costuras reforçadas e acabamento pensado para durar muitas lavagens.</p>
        </article>
        <article>
          <span class="pillar-kanji" lang="ja">形</span>
          <h3>Modelagem</h3>
          <p>Cortes oversized e wide leg inspirados em Harajuku, com tabela de medidas fiel ao caimento real.</p>
        </article>
        <article>
          <span class="pillar-kanji" lang="ja">心</span>
          <h3>Atendimento</h3>
          <p>Troca em até 30 dias, frete grátis acima de R$ 299 e time pronto para ajudar a montar o seu look.</p>
        </article>
      </div>
    </section>

    <!-- ===================== VISITE / NEWSLETTER ===================== -->
    <section class="section visit" id="visite">
      <div class="visit-box">
        <div>
          <p class="eyebrow eyebrow-light">店舗 · Loja física</p>
          <h2>Visite a Tokyo Style</h2>
          <p>CLS 109, Bloco A, Loja 12 - Asa Sul, Brasília/DF<br>
             Segunda a sábado, das 10h às 20h</p>
        </div>
        <form class="newsletter" id="newsletter" novalidate>
          <label for="news-email">Receba os próximos drops em primeira mão</label>
          <div class="news-row">
            <input id="news-email" type="email" placeholder="seu@email.com" autocomplete="email" required>
            <button type="submit" class="btn btn-red">Quero receber</button>
          </div>
          <p class="news-msg" id="news-msg" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>
  </main>

  % include('app/views/html/partials/footer')

  <!-- ===================== SACOLA (gaveta lateral) ===================== -->
  <div class="drawer-backdrop" id="drawer-backdrop" hidden></div>
  <aside class="drawer" id="bag-drawer" aria-label="Sacola de compras" aria-hidden="true">
    <header>
      <h2>Sua sacola</h2>
      <button type="button" class="icon-btn" id="bag-close" aria-label="Fechar sacola">✕</button>
    </header>
    <ul class="bag-list" id="bag-list"></ul>
    <p class="bag-empty" id="bag-empty">Sua sacola está vazia.</p>
    <footer>
      <p class="bag-total">Total <strong id="bag-total">R$ 0,00</strong></p>
      <button type="button" class="btn btn-red btn-block" id="bag-checkout">Finalizar compra</button>
      <button type="button" class="btn btn-ghost btn-block" id="bag-clear">Esvaziar sacola</button>
    </footer>
  </aside>

  <div class="toast" id="toast" role="status" aria-live="polite"></div>
</body>
</html>
