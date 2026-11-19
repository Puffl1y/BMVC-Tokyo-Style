import json


class Realtime():
    """Comunicação WebSocket (servidor -> navegadores) usando eventlet.

    * Cada navegador abre uma conexão em  ws://host:8080/ws
    * Quando o administrador cria/edita/remove um produto ou muda a
      quantidade, o servidor faz broadcast() de um evento JSON para TODOS os
      clientes conectados, que atualizam a página sem recarregar.
    * Se o eventlet não estiver instalado, o site continua funcionando
      normalmente (apenas sem tempo real): available == False.
    """

    def __init__(self):
        self.clients = set()
        self.available = False
        try:
            from eventlet import websocket
            self.__ws_app = websocket.WebSocketWSGI(self.__handle)
            self.available = True
        except ImportError:
            self.__ws_app = None

    def __handle(self, ws):
        """Uma chamada por conexão aberta; fica ativa até o cliente sair."""
        self.clients.add(ws)
        try:
            while True:
                if ws.wait() is None:     # None = conexão fechada
                    break                 # mensagens do cliente são ignoradas
        finally:
            self.clients.discard(ws)

    def broadcast(self, event):
        """Envia um dicionário (como JSON) a todos os clientes conectados."""
        data = json.dumps(event, ensure_ascii=False)
        for ws in list(self.clients):
            try:
                ws.send(data)
            except Exception:
                self.clients.discard(ws)

    def wsgi(self, app):
        """Envolve o app Bottle: /ws vira WebSocket, o resto segue normal."""
        def dispatcher(environ, start_response):
            if self.available and environ.get('PATH_INFO') == '/ws':
                return self.__ws_app(environ, start_response)
            return app(environ, start_response)
        return dispatcher
