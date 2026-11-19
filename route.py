from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
import os


app = Bottle()
ctl = Application()

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


@app.route('/estoque', method='GET')
def action_estoque():
    page, error = ctl.render('estoque')
    if error:
        redirect('/portal?msg=' + error)
    return page


@app.route('/estoque/add', method='POST')
def action_estoque_add():
    redirect('/estoque?msg=' + ctl.stock_add(request.forms))


@app.route('/estoque/update/<product_id>', method='POST')
def action_estoque_update(product_id):
    redirect('/estoque?msg=' + ctl.stock_update(product_id, request.forms))


@app.route('/estoque/delete/<product_id>', method='POST')
def action_estoque_delete(product_id):
    redirect('/estoque?msg=' + ctl.stock_remove(product_id))


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
