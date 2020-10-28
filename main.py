from flask import Flask, render_template, redirect, send_from_directory, request, make_response, session
from flask_socketio import SocketIO, emit, join_room
import db, hashlib, functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user = functions.user_db()
data_base = db.Data_Base(user[0], user[1])

@app.route('/')
def index():
    user = session.get('user')
    name = data_base.get_name(user)
    type_account = data_base.get_type_account(user)
    if user == None: resp = make_response(redirect('/login'))
    else: resp = make_response(render_template('index.html', name = name, type_account = type_account))
    return resp

@app.route('/panel', methods = ('GET', 'POST'))
def painel():
    user = session.get('user')
    name = data_base.get_name(user)
    type_account = data_base.get_type_account(user)
    if request.method == 'GET':
        if type_account == 'Professor': resp = make_response(render_template('teacher_panel.html', name = name))
        elif type_account == 'Aluno': resp = make_response(render_template('student_panel.html', name = name))
    return resp

@socketio.on('joined')
def joined(message):
    join_room('main_room')
    emit('status', {'msg': '%s entrou no chat!' %(session.get('user'))}, room = 'main_room')

@socketio.on('text')
def text(message):
    emit('message', {'msg': '%s: %s' %(session.get('user'), message['msg'])}, room = 'main_room')

@app.route('/login', methods = ('GET', 'POST'))
def login():
    user = session.get('user')
    if not (user == None): return redirect('/')
    if request.method == 'GET': resp = make_response(render_template('login.html'))
    else:
        user = request.form['user']
        passwd = request.form['passwd']
        if data_base.user_check(user, passwd):
            resp = make_response(redirect('/'))
            session['user'] = user
        else: resp = 'usuário ou senha incorretos'
    return resp

@app.route('/logout', methods = ('GET', 'POST'))
def logout():
    user = session.get('user')
    if (user == None): return redirect('/login')
    if request.method == 'GET': resp = render_template('logout.html')
    else:
        resp = make_response(redirect('/login'))
        session['user'] = None
        session['type_account'] = None
    return resp

@app.route('/create', methods = ('GET', 'POST'))
def create():
    user = session.get('user')
    if not (user == None): return redirect('/')
    type_account = session.get('type_account')
    if request.method == 'GET' and type_account == None:
        resp = make_response(render_template('set_type_account.html'))
    elif request.method == 'POST' and type_account == None:
        type_account = request.form['type-account']
        resp = make_response(redirect('/create'))
        session['type_account'] = type_account
    elif request.method == 'GET' and not type_account == None:
        resp = make_response(render_template('create_credentials.html', type_account = type_account))
    else:
        user = request.form['user']
        name = request.form['real_name']
        passwd = request.form['passwd']
        if data_base.create_user(user, name, passwd, type_account):
            resp = make_response(redirect('/'))
            session['user'] = user
        else: resp = 'algo deu errado :/'
    return resp

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('static/css', path)

@app.route('/image/<path:path>')
def send_image(path):
	return send_from_directory('static/image', path)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')