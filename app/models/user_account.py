import hashlib
import hmac
import secrets


class UserAccount():
    """Conta de usuário da Tokyo Style.

    A senha NUNCA é guardada em texto puro: salvamos apenas o hash
    (PBKDF2-SHA256) e o 'salt' aleatório de cada usuário.
    role: 'admin' (acessa o estoque) ou 'cliente'.
    """

    ITERATIONS = 120_000

    def __init__(self, username, password_hash, salt, role='cliente',
                 display_name=None):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.role = role
        self.display_name = display_name or username

    @staticmethod
    def hash_password(password, salt):
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                     bytes.fromhex(salt),
                                     UserAccount.ITERATIONS)
        return digest.hex()

    @classmethod
    def create(cls, username, password, role='cliente', display_name=None):
        salt = secrets.token_hex(16)
        return cls(username, cls.hash_password(password, salt), salt, role,
                   display_name)

    def check_password(self, password):
        candidate = self.hash_password(password, self.salt)
        return hmac.compare_digest(candidate, self.password_hash)

    @property
    def is_admin(self):
        return self.role == 'admin'
