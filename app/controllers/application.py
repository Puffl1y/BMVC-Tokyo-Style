from app.controllers.datarecord import DataRecord
from app.controllers.stockrecord import StockRecord
from app.models.product import CATEGORIES, format_brl
from bottle import template, request
import re

# Mensagens (flash) identificadas por código na URL: /rota?msg=codigo
# Usar códigos (e não texto livre) evita refletir conteúdo arbitrário na página.
MESSAGES = {
    'bemvindo': ('ok', 'Login realizado com sucesso. Bem-vindo(a) à Tokyo Style!'),
    'saiu': ('ok', 'Você saiu da sua conta. Até logo!'),
    'credenciais': ('erro', 'Usuário ou senha incorretos.'),
    'login': ('erro', 'Faça login para continuar.'),
    'acesso': ('erro', 'Acesso restrito: somente administradores podem ver o estoque.'),
    'adicionado': ('ok', 'Produto cadastrado no estoque.'),
    'atualizado': ('ok', 'Quantidade atualizada.'),
    'removido': ('ok', 'Produto removido do estoque.'),
    'editado': ('ok', 'Produto atualizado com sucesso.'),
    'invalido': ('erro', 'Dados inválidos. Confira os campos e tente novamente.'),
    'inexistente': ('erro', 'Produto não encontrado.'),
}

HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{6}$')


class Application():

    def __init__(self):
        self.pages = {
            'helper': self.helper,
            'home': self.home,
            'portal': self.portal,
            'estoque': self.estoque,
            'editar': self.editar,
        }
        self.__users = DataRecord()
        self.__stock = StockRecord()

    # ------------------------------------------------------------- infra
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')

    def notice(self):
        """Mensagem flash (kind, texto) vinda de ?msg=codigo, ou None."""
        return MESSAGES.get(request.query.get('msg', ''))

    # ------------------------------------------------------------- páginas
    def helper(self):
        return template('app/views/html/helper')

    def home(self):
        products = self.__stock.all()
        present = {p.category for p in products}
        categories = [(slug, label) for slug, (label, _) in CATEGORIES.items()
                      if slug in present]
        return template('app/views/html/home',
                        products=products,
                        categories=categories,
                        current_user=self.current_user(),
                        notice=self.notice())

    def portal(self):
        # quem já está logado não precisa ver o formulário de novo
        return template('app/views/html/portal',
                        current_user=self.current_user(),
                        notice=self.notice())

    def estoque(self):
        """Página restrita ao administrador. Retorna (conteúdo, código)."""
        user = self.current_user()
        if not user:
            return None, 'login'
        if not user.is_admin:
            return None, 'acesso'
        summary = self.__stock.summary()
        summary['value_br'] = format_brl(summary['value'])
        page = template('app/views/html/estoque',
                        products=self.__stock.all(),
                        categories=list(CATEGORIES.items()),
                        summary=summary,
                        current_user=user,
                        notice=self.notice())
        return page, None

    def editar(self, product_id):
        """Formulário de edição (UPDATE). Retorna (conteúdo, código de erro)."""
        user = self.current_user()
        if not user:
            return None, 'login'
        if not user.is_admin:
            return None, 'acesso'
        product = self.__stock.get(product_id)
        if not product:
            return None, 'inexistente'
        page = template('app/views/html/editar',
                        product=product,
                        categories=list(CATEGORIES.items()),
                        current_user=user,
                        notice=self.notice())
        return page, None

    # ------------------------------------------------------- autenticação
    def current_user(self):
        return self.__users.getCurrentUser(self.get_session_id())

    def is_admin(self):
        user = self.current_user()
        return bool(user and user.is_admin)

    def authenticate_user(self, username, password):
        session_id = self.__users.checkUser(username, password)
        if session_id:
            self.logout_user()   # encerra uma sessão anterior, se existir
            user = self.__users.getCurrentUser(session_id)
            return session_id, user
        return None, None

    def logout_user(self):
        session_id = self.get_session_id()
        if session_id:
            self.__users.logout(session_id)

    # ----------------------------------------------- ações do estoque (admin)
    # Todas retornam (código_da_mensagem, produto_ou_None). O produto é usado
    # pela rota para avisar, via WebSocket, todos os navegadores conectados.
    def product_event(self, action, product):
        """Mensagem enviada pelo WebSocket (apenas dados públicos do produto)."""
        return {'action': action, 'id': product.id, 'name': product.name,
                'stock': product.stock, 'status': product.status,
                'status_label': product.status_label}

    def __parse_product_form(self, form):
        """Valida o formulário de produto. Retorna dict ou None se inválido."""
        name = (form.getunicode('name') or '').strip()
        category = form.get('category', '')
        sizes = [s.strip() for s in (form.getunicode('sizes') or '').split(',')
                 if s.strip()]
        color = form.get('color', '#222222')
        try:
            price = float((form.get('price') or '').replace(',', '.'))
            stock = int(form.get('stock') or '')
        except ValueError:
            return None
        if (not 2 <= len(name) <= 60 or category not in CATEGORIES
                or price < 0 or price > 99999 or not 0 <= stock <= 99999
                or not sizes or len(sizes) > 8
                or any(len(s) > 8 for s in sizes)
                or not HEX_COLOR.match(color)):
            return None
        return dict(name=name, category=category, price=round(price, 2),
                    stock=stock, sizes=sizes, color=color)

    def stock_add(self, form):                       # CREATE
        if not self.is_admin():
            return 'acesso', None
        data = self.__parse_product_form(form)
        if not data:
            return 'invalido', None
        return 'adicionado', self.__stock.add(**data)

    def stock_edit(self, product_id, form):          # UPDATE (todos os campos)
        if not self.is_admin():
            return 'acesso', None
        data = self.__parse_product_form(form)
        if not data:
            return 'invalido', None
        product = self.__stock.update(product_id, **data)
        return ('editado', product) if product else ('inexistente', None)

    def stock_update(self, product_id, form):        # UPDATE (só a quantidade)
        if not self.is_admin():
            return 'acesso', None
        try:
            quantity = int(form.get('stock') or '')
        except ValueError:
            return 'invalido', None
        if not 0 <= quantity <= 99999:
            return 'invalido', None
        product = self.__stock.set_stock(product_id, quantity)
        return ('atualizado', product) if product else ('inexistente', None)

    def stock_remove(self, product_id):              # DELETE
        if not self.is_admin():
            return 'acesso', None
        product = self.__stock.remove(product_id)
        return ('removido', product) if product else ('inexistente', None)
