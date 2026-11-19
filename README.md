# Tokyo Style — loja de roupas (BMVC / Bottle)

Projeto desenvolvido sobre a estrutura **BMVC** fornecida em aula
(Bottle + Model + View + Controller). A loja *Tokyo Style* vende streetwear
inspirado em Tóquio e possui:

| Rota | Página | Acesso |
|------|--------|--------|
| `/` ou `/home` | **Página estática da loja** (`home.tpl`): hero, catálogo com filtro/ordenação, sacola, sobre, loja física e newsletter | pública |
| `/portal` | **Login** (`portal.tpl`) | pública |
| `/estoque` | **Controle de estoque** (`estoque.tpl`): indicadores, busca, ajuste de quantidade, cadastro e remoção de peças | **somente administrador** |
| `/logout` (POST) | Encerra a sessão | logado |
| `/helper` | Página original do professor (mantida) | pública |

## Como executar

```bash
pip install bottle
python3 route.py        # abra http://localhost:8080
```

Com Docker (dentro da pasta do projeto):

```bash
docker build -t tokyostyle .
docker run --name tokyostyle -p 8080:8080 -v "$(pwd)":/bmeta tokyostyle
```

O volume deve ser montado em `/bmeta`, o `WORKDIR` do Dockerfile (a imagem
não copia o código, ela usa a pasta montada). Acesse http://localhost:8080.

## Contas já cadastradas

| Perfil | Usuário | Senha | O que acessa |
|--------|---------|-------|--------------|
| Administrador | `admin` | `tokyo@2025` | Loja + **Estoque** |
| Cliente | `yuki` | `sakura123` | Somente a loja (ao tentar `/estoque` é barrado) |

As contas ficam em `app/controllers/db/user_accounts.json`. As senhas **não são
guardadas em texto puro**: salvamos hash PBKDF2-SHA256 + *salt* por usuário.

## Estrutura (padrão BMVC)

```
route.py                          # rotas (GET/POST)
app/
├── controllers/
│   ├── application.py            # controlador: páginas, autenticação, regras do estoque
│   ├── datarecord.py             # "banco" JSON de usuários + sessões (uuid4)
│   ├── stockrecord.py            # "banco" JSON de produtos/estoque
│   └── db/
│       ├── user_accounts.json    # usuários cadastrados (hash)
│       └── products.json         # produtos e quantidades
├── models/
│   ├── user_account.py           # modelo UserAccount (hash, papel admin/cliente)
│   └── product.py                # modelo Product (preço BRL, situação do estoque)
├── views/html/
│   ├── home.tpl  portal.tpl  estoque.tpl  helper.tpl
│   └── partials/header.tpl  footer.tpl
└── static/
    ├── css/tokyo.css  portal.css  estoque.css
    ├── js/tokyo.js    portal.js   estoque.js
    └── img/icons.svg             # sprite SVG com as peças de roupa
```

## Detalhes de segurança

* Cookie de sessão `httponly` + `samesite=Lax`. Para HTTPS defina
  `TOKYO_SECURE_COOKIE=1` (em HTTP local o cookie `secure` não funcionaria).
* O servidor confere o papel **admin** em *toda* rota de estoque (inclusive nos
  POST de adicionar/atualizar/remover), não apenas ao exibir a página.
* Entradas do cadastro são validadas no servidor (tamanho, categoria, preço, cor).
* Mensagens de feedback usam códigos fixos na URL, evitando refletir texto arbitrário.
* O template escapa HTML por padrão (`{{ }}`).
