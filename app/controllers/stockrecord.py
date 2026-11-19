from app.models.product import Product
import json
import os
import threading

PRODUCTS_FILE = "app/controllers/db/products.json"

DEFAULT_PRODUCTS = [
    ("Camiseta Oversized Sakura", "camisetas", 89.90, 24, ["P", "M", "G", "GG"], "#f2b8c6"),
    ("Camiseta Kanji Preta", "camisetas", 79.90, 31, ["P", "M", "G", "GG"], "#161616"),
    ("Hoodie Shibuya", "moletons", 219.90, 12, ["M", "G", "GG"], "#6b7280"),
    ("Moletom Harajuku Rosa", "moletons", 229.90, 4, ["P", "M", "G"], "#e8a0bf"),
    ("Jaqueta Bomber Tokyo Night", "jaquetas", 349.90, 8, ["M", "G", "GG"], "#1d2b53"),
    ("Jaqueta Coach Shinjuku", "jaquetas", 299.90, 0, ["M", "G"], "#3d4a3a"),
    ("Calça Cargo Akihabara", "calcas", 259.90, 15, ["38", "40", "42", "44"], "#8a7f68"),
    ("Calça Wide Leg Ginza", "calcas", 239.90, 18, ["38", "40", "42", "44"], "#262626"),
    ("Saia Plissada Kawaii", "saias", 169.90, 10, ["P", "M", "G"], "#b3202a"),
    ("Vestido Kimono Wrap", "vestidos", 279.90, 7, ["P", "M", "G"], "#e9e2d0"),
    ("Boné Tokyo Club", "acessorios", 99.90, 40, ["Único"], "#d9261c"),
    ("Tênis Shinkansen", "calcados", 399.90, 3, ["37", "39", "41", "43"], "#f1f1f1"),
]


class StockRecord():
    """Banco de dados JSON para o recurso Produtos / Estoque."""

    def __init__(self):
        self.__lock = threading.Lock()
        self.__products = []
        self.read()

    # ------------------------------------------------------------------ I/O
    def read(self):
        try:
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as arquivo_json:
                self.__products = [Product(**d) for d in json.load(arquivo_json)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__products = [
                Product(f"TKS-{i:03d}", *item)
                for i, item in enumerate(DEFAULT_PRODUCTS, start=1)
            ]
            self.__save()

    def __save(self):
        os.makedirs(os.path.dirname(PRODUCTS_FILE), exist_ok=True)
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as arquivo_json:
            json.dump([p.to_dict() for p in self.__products],
                      arquivo_json, indent=2, ensure_ascii=False)

    # --------------------------------------------------------------- leitura
    def all(self):
        return list(self.__products)

    def get(self, product_id):
        for product in self.__products:
            if product.id == product_id:
                return product
        return None

    def summary(self):
        products = self.__products
        return {
            'skus': len(products),
            'units': sum(p.stock for p in products),
            'low': sum(1 for p in products if p.status == 'low'),
            'out': sum(1 for p in products if p.status == 'out'),
            'value': sum(p.price * p.stock for p in products),
        }

    # ----------------------------------------------------------- manutenção
    def __next_id(self):
        numbers = [int(p.id.split('-')[1]) for p in self.__products
                   if p.id.startswith('TKS-') and p.id.split('-')[1].isdigit()]
        return f"TKS-{(max(numbers) if numbers else 0) + 1:03d}"

    def add(self, name, category, price, stock, sizes, color):
        with self.__lock:
            product = Product(self.__next_id(), name, category, price, stock,
                              sizes, color)
            self.__products.append(product)
            self.__save()
            return product

    def update(self, product_id, name, category, price, stock, sizes, color):
        """UPDATE completo: altera todos os campos de um produto."""
        with self.__lock:
            product = self.get(product_id)
            if not product:
                return None
            product.name = name
            product.category = category
            product.price = float(price)
            product.stock = int(stock)
            product.sizes = list(sizes)
            product.color = color
            self.__save()
            return product

    def set_stock(self, product_id, quantity):
        with self.__lock:
            product = self.get(product_id)
            if not product:
                return None
            product.stock = max(0, int(quantity))
            self.__save()
            return product

    def remove(self, product_id):
        with self.__lock:
            product = self.get(product_id)
            if not product:
                return None
            self.__products.remove(product)
            self.__save()
            return product
