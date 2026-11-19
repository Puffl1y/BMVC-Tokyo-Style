<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Estoque | Tokyo Style</title>
  <link rel="stylesheet" type="text/css" href="/static/css/tokyo.css">
  <link rel="stylesheet" type="text/css" href="/static/css/estoque.css">
  <script src="/static/js/tokyo.js" defer></script>
  <script src="/static/js/realtime.js" defer></script>
  <script src="/static/js/estoque.js" defer></script>
</head>
<body class="page-estoque">

  % include('app/views/html/partials/header', current_user=current_user, active='estoque', show_bag=False)

  % if notice:
  <div class="flash flash-{{notice[0]}}" role="status" data-autohide>{{notice[1]}}</div>
  % end

  <main id="conteudo" class="admin">
    <header class="admin-head">
      <div>
        <p class="eyebrow">在庫 · Painel do administrador</p>
        <h1>Controle de estoque</h1>
        <p class="lead">Consulte, ajuste quantidades e cadastre novas peças. As alterações aparecem na loja imediatamente.</p>
      </div>
      <div class="head-side">
        <p class="live" id="live-status" data-state="off"><span class="dot" aria-hidden="true"></span><span class="live-text">Conectando…</span></p>
        <button type="button" class="btn btn-red" id="toggle-add" aria-expanded="false" aria-controls="add-panel">+ Nova peça</button>
      </div>
    </header>

    <!-- ---------- Indicadores ---------- -->
    <section class="kpis" aria-label="Resumo do estoque">
      <article class="kpi">
        <p class="kpi-label">Produtos (SKUs)</p>
        <p class="kpi-value">{{summary['skus']}}</p>
      </article>
      <article class="kpi">
        <p class="kpi-label">Unidades em estoque</p>
        <p class="kpi-value">{{summary['units']}}</p>
      </article>
      <article class="kpi kpi-warn">
        <p class="kpi-label">Estoque baixo</p>
        <p class="kpi-value">{{summary['low']}}</p>
      </article>
      <article class="kpi kpi-danger">
        <p class="kpi-label">Esgotados</p>
        <p class="kpi-value">{{summary['out']}}</p>
      </article>
      <article class="kpi kpi-wide">
        <p class="kpi-label">Valor do estoque (preço de venda)</p>
        <p class="kpi-value">R$ {{summary['value_br']}}</p>
      </article>
    </section>

    <!-- ---------- Atividade em tempo real (WebSocket) ---------- -->
    <section class="feed" aria-label="Atividade em tempo real">
      <h2>Atividade em tempo real</h2>
      <ol id="live-feed" aria-live="polite"><li class="feed-empty">Aguardando alterações…</li></ol>
    </section>

    <!-- ---------- Cadastro ---------- -->
    <section class="add-panel" id="add-panel" hidden>
      <h2>Cadastrar nova peça</h2>
      <form action="/estoque/add" method="post" class="add-form" id="add-form">
        <div class="field span-2">
          <label for="f-name">Nome</label>
          <input id="f-name" name="name" type="text" minlength="2" maxlength="60" required>
        </div>
        <div class="field">
          <label for="f-category">Categoria</label>
          <select id="f-category" name="category" required>
            % for slug, (label, icon) in categories:
            <option value="{{slug}}">{{label}}</option>
            % end
          </select>
        </div>
        <div class="field">
          <label for="f-price">Preço (R$)</label>
          <input id="f-price" name="price" type="number" min="0" max="99999" step="0.01" inputmode="decimal" required>
        </div>
        <div class="field">
          <label for="f-stock">Quantidade</label>
          <input id="f-stock" name="stock" type="number" min="0" max="99999" step="1" value="0" required>
        </div>
        <div class="field">
          <label for="f-sizes">Tamanhos (separados por vírgula)</label>
          <input id="f-sizes" name="sizes" type="text" placeholder="P, M, G" maxlength="60" required>
        </div>
        <div class="field">
          <label for="f-color">Cor principal</label>
          <input id="f-color" name="color" type="color" value="#d9261c">
        </div>
        <div class="add-actions span-2">
          <button type="submit" class="btn btn-ink">Salvar peça</button>
          <button type="button" class="btn btn-ghost" id="cancel-add">Cancelar</button>
        </div>
      </form>
    </section>

    <!-- ---------- Tabela ---------- -->
    <section class="table-section" aria-label="Lista de produtos">
      <div class="toolbar">
        <div class="field grow">
          <label class="sr-only" for="search">Buscar</label>
          <input id="search" type="search" placeholder="Buscar por código, nome ou categoria…" autocomplete="off">
        </div>
        <div class="field">
          <label class="sr-only" for="filter-status">Situação</label>
          <select id="filter-status">
            <option value="all">Todas as situações</option>
            <option value="ok">Disponível</option>
            <option value="low">Estoque baixo</option>
            <option value="out">Esgotado</option>
          </select>
        </div>
        <p class="result-count" id="result-count" aria-live="polite">{{len(products)}} itens</p>
      </div>

      <div class="table-wrap">
        <table class="stock-table" id="stock-table">
          <thead>
            <tr>
              <th scope="col">Código</th>
              <th scope="col">Produto</th>
              <th scope="col">Categoria</th>
              <th scope="col">Tamanhos</th>
              <th scope="col" class="num">Preço</th>
              <th scope="col">Quantidade</th>
              <th scope="col">Situação</th>
              <th scope="col" class="num">Valor em estoque</th>
              <th scope="col"><span class="sr-only">Ações</span></th>
            </tr>
          </thead>
          <tbody>
            % for p in products:
            <tr data-id="{{p.id}}" data-status="{{p.status}}" data-search="{{(p.id + ' ' + p.name + ' ' + p.category_label).lower()}}">
              <td class="mono">{{p.id}}</td>
              <td>
                <span class="swatch" style="background: {{p.color}}" aria-hidden="true"></span>
                <strong>{{p.name}}</strong>
              </td>
              <td>{{p.category_label}}</td>
              <td>{{', '.join(p.sizes)}}</td>
              <td class="num">R$ {{p.price_br}}</td>
              <td>
                <form action="/estoque/update/{{p.id}}" method="post" class="qty-form">
                  <button type="button" class="step" data-step="-1" aria-label="Diminuir">−</button>
                  <input type="number" name="stock" min="0" max="99999" value="{{p.stock}}" data-original="{{p.stock}}"
                         aria-label="Quantidade de {{p.name}}" required>
                  <button type="button" class="step" data-step="1" aria-label="Aumentar">+</button>
                  <button type="submit" class="btn btn-ink btn-sm">Salvar</button>
                </form>
              </td>
              <td><span class="pill pill-{{p.status}}">{{p.status_label}}</span></td>
              <td class="num">R$ {{p.total_br}}</td>
              <td>
                <div class="row-actions">
                  <a class="btn btn-ghost btn-sm" href="/estoque/edit/{{p.id}}">Editar</a>
                  <form action="/estoque/delete/{{p.id}}" method="post" data-confirm="Remover {{p.name}} do estoque?">
                    <button type="submit" class="btn btn-danger btn-sm">Remover</button>
                  </form>
                </div>
              </td>
            </tr>
            % end
          </tbody>
        </table>
        <p class="empty-row" id="empty-row" hidden>Nenhum item encontrado com esses filtros.</p>
      </div>
    </section>
  </main>

  % include('app/views/html/partials/footer')
</body>
</html>
