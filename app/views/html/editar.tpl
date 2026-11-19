<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Editar {{product.name}} | Tokyo Style</title>
  <link rel="stylesheet" type="text/css" href="/static/css/tokyo.css">
  <link rel="stylesheet" type="text/css" href="/static/css/estoque.css">
  <script src="/static/js/tokyo.js" defer></script>
</head>
<body class="page-estoque">

  % include('app/views/html/partials/header', current_user=current_user, active='estoque', show_bag=False)

  % if notice:
  <div class="flash flash-{{notice[0]}}" role="status" data-autohide>{{notice[1]}}</div>
  % end

  <main id="conteudo" class="admin">
    <header class="admin-head">
      <div>
        <p class="eyebrow">編集 · {{product.id}}</p>
        <h1>Editar produto</h1>
        <p class="lead">Altere qualquer informação da peça. A loja e o painel de todos os usuários conectados são atualizados em tempo real.</p>
      </div>
    </header>

    <section class="add-panel">
      <form action="/estoque/edit/{{product.id}}" method="post" class="add-form">
        <div class="field span-2">
          <label for="f-name">Nome</label>
          <input id="f-name" name="name" type="text" minlength="2" maxlength="60" value="{{product.name}}" required>
        </div>
        <div class="field">
          <label for="f-category">Categoria</label>
          <select id="f-category" name="category" required>
            % for slug, (label, icon) in categories:
            <option value="{{slug}}" {{'selected' if slug == product.category else ''}}>{{label}}</option>
            % end
          </select>
        </div>
        <div class="field">
          <label for="f-price">Preço (R$)</label>
          <input id="f-price" name="price" type="number" min="0" max="99999" step="0.01" inputmode="decimal" value="{{product.price}}" required>
        </div>
        <div class="field">
          <label for="f-stock">Quantidade</label>
          <input id="f-stock" name="stock" type="number" min="0" max="99999" step="1" value="{{product.stock}}" required>
        </div>
        <div class="field">
          <label for="f-sizes">Tamanhos (separados por vírgula)</label>
          <input id="f-sizes" name="sizes" type="text" maxlength="60" value="{{', '.join(product.sizes)}}" required>
        </div>
        <div class="field">
          <label for="f-color">Cor principal</label>
          <input id="f-color" name="color" type="color" value="{{product.color}}">
        </div>
        <div class="add-actions span-2">
          <button type="submit" class="btn btn-ink">Salvar alterações</button>
          <a href="/estoque" class="btn btn-ghost">Cancelar</a>
        </div>
      </form>
    </section>
  </main>

  % include('app/views/html/partials/footer')
</body>
</html>
