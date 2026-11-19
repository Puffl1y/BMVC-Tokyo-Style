LOW_STOCK_LIMIT = 5

# slug -> (nome exibido, ícone do sprite static/img/icons.svg)
CATEGORIES = {
    'camisetas': ('Camisetas', 'tee'),
    'moletons': ('Moletons', 'hoodie'),
    'jaquetas': ('Jaquetas', 'jacket'),
    'calcas': ('Calças', 'pants'),
    'saias': ('Saias', 'skirt'),
    'vestidos': ('Vestidos', 'dress'),
    'acessorios': ('Acessórios', 'cap'),
    'calcados': ('Calçados', 'sneaker'),
}


def format_brl(value):
    """89.9 -> '89,90' | 1234.5 -> '1.234,50'"""
    text = f"{value:,.2f}"
    return text.replace(',', 'X').replace('.', ',').replace('X', '.')


class Product():
    """Peça de roupa/acessório do catálogo e do estoque."""

    def __init__(self, id, name, category, price, stock, sizes, color='#222222'):
        self.id = id
        self.name = name
        self.category = category
        self.price = float(price)
        self.stock = int(stock)
        self.sizes = list(sizes)
        self.color = color

    @property
    def category_label(self):
        return CATEGORIES.get(self.category, (self.category, 'tee'))[0]

    @property
    def icon(self):
        return CATEGORIES.get(self.category, (self.category, 'tee'))[1]

    @property
    def price_br(self):
        return format_brl(self.price)

    @property
    def total_br(self):
        return format_brl(self.price * self.stock)

    @property
    def status(self):
        if self.stock <= 0:
            return 'out'
        if self.stock <= LOW_STOCK_LIMIT:
            return 'low'
        return 'ok'

    @property
    def status_label(self):
        return {'out': 'Esgotado', 'low': 'Estoque baixo',
                'ok': 'Disponível'}[self.status]

    def to_dict(self):
        # só os atributos reais (as @property não entram no JSON)
        return dict(vars(self))
