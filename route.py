try:                      # WebSocket: o eventlet precisa ser "patcheado" primeiro
    import eventlet
    eventlet.monkey_patch()
except ImportError:
    eventlet = None

from app.controllers.application import Application
from app.controllers.realtime import Realtime
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response, debug
import os


app = Bottle()
ctl = Application()
realtime = Realtime()

# Em produção (HTTPS) defina TOKYO_SECURE_COOKIE=1 para enviar o cookie
# de sessão somente por conexões seguras. Em HTTP local, fica desligado.
SECURE_COOKIE = os.environ.get('TOKYO_SECURE_COOKIE') == '1'


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Tokyo Style - página estática da loja:

@app.route('/', method='GET')
@app.route('/home', method='GET')
def action_home():
    return ctl.render('home')


#-----------------------------------------------------------------------------
# Tokyo Style - login (portal), logout e estoque:

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.getunicode('username')
    password = request.forms.getunicode('password')
    session_id, user = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True,
                            secure=SECURE_COOKIE, samesite='Lax',
                            max_age=3600, path='/')
        if user.is_admin:
            redirect('/estoque?msg=bemvindo')
        redirect('/?msg=bemvindo')
    else:
        redirect('/portal?msg=credenciais')


@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id', path='/')
    redirect('/?msg=saiu')


def finish(result):
    """Redireciona com a mensagem e avisa todos os navegadores (WebSocket)."""
    code, product = result
    if product is not None:
        realtime.broadcast(ctl.product_event(code, product))
    redirect('/estoque?msg=' + code)


@app.route('/estoque', method='GET')
def action_estoque():
    page, error = ctl.render('estoque')
    if error:
        redirect('/portal?msg=' + error)
    return page


@app.route('/estoque/add', method='POST')                       # CREATE
def action_estoque_add():
    finish(ctl.stock_add(request.forms))


@app.route('/estoque/edit/<product_id>', method='GET')          # UPDATE (form)
def action_estoque_edit_form(product_id):
    page, error = ctl.render('editar', product_id)
    if error in ('login', 'acesso'):
        redirect('/portal?msg=' + error)
    if error:
        redirect('/estoque?msg=' + error)
    return page


@app.route('/estoque/edit/<product_id>', method='POST')         # UPDATE (salvar)
def action_estoque_edit(product_id):
    finish(ctl.stock_edit(product_id, request.forms))


@app.route('/estoque/update/<product_id>', method='POST')       # UPDATE (qtd.)
def action_estoque_update(product_id):
    finish(ctl.stock_update(product_id, request.forms))


@app.route('/estoque/delete/<product_id>', method='POST')       # DELETE
def action_estoque_delete(product_id):
    finish(ctl.stock_remove(product_id))


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    debug(True)
    if realtime.available:
        # Servidor do eventlet: atende HTTP e WebSocket (/ws) na porta 8080
        from eventlet import wsgi
        print('Tokyo Style em http://localhost:8080  (WebSocket em /ws)')
        wsgi.server(eventlet.listen(('0.0.0.0', 8080)), realtime.wsgi(app))
    else:
        print('eventlet nao encontrado: iniciando SEM WebSocket')
        run(app, host='0.0.0.0', port=8080)
