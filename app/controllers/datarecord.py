from app.models.user_account import UserAccount
import json
import os
import uuid

USERS_FILE = "app/controllers/db/user_accounts.json"

# Contas já cadastradas (usadas para criar o JSON na 1ª execução).
DEFAULT_USERS = [
    ('admin', 'tokyo@2025', 'admin', 'Administrador'),
    ('yuki', 'sakura123', 'cliente', 'Yuki'),
]


class DataRecord():
    """Banco de dados JSON para o recurso Usuários (+ sessões abertas)."""

    def __init__(self):
        self.__user_accounts = []
        self.__authenticated_users = {}   # session_id -> UserAccount
        self.read()

    # ------------------------------------------------------------------ I/O
    def read(self):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**d) for d in user_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__seed()

    def __seed(self):
        self.__user_accounts = [
            UserAccount.create(u, p, role, name)
            for u, p, role, name in DEFAULT_USERS
        ]
        self.__save()

    def __save(self):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as arquivo_json:
            json.dump([vars(u) for u in self.__user_accounts],
                      arquivo_json, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------- cadastro
    def book(self, username, password, role='cliente', display_name=None):
        if self.find(username):
            return None  # não permitimos dois usuários com o mesmo nome
        new_user = UserAccount.create(username, password, role, display_name)
        self.__user_accounts.append(new_user)
        self.__save()
        return new_user

    def find(self, username):
        username = (username or '').strip().lower()
        for user in self.__user_accounts:
            if user.username.lower() == username:
                return user
        return None

    # --------------------------------------------------------------- sessões
    def checkUser(self, username, password):
        user = self.find(username)
        if user and password and user.check_password(password):
            session_id = str(uuid.uuid4())   # ID de sessão único
            self.__authenticated_users[session_id] = user
            return session_id
        return None

    def getCurrentUser(self, session_id):
        return self.__authenticated_users.get(session_id)

    def getUserName(self, session_id):
        user = self.getCurrentUser(session_id)
        return user.username if user else None

    def getUserSessionId(self, username):
        for session_id, user in self.__authenticated_users.items():
            if user.username == username:
                return session_id
        return None

    def logout(self, session_id):
        self.__authenticated_users.pop(session_id, None)
