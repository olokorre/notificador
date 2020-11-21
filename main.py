from flask import Flask, render_template, redirect, send_from_directory, request, make_response, session
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import db, hashlib, functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user = functions.user_db()
data_base = db.Data_Base(user[0], user[1])
data_base.return_classroom()

#Rotas principais
@app.route('/')
def index():
    user = session.get('user')
    if data_base.user_exist(user): resp = make_response(redirect('/login'))
    else:
        name = data_base.get_name(user)
        type_account = data_base.get_type_account(user)
        resp = make_response(render_template('index.html', name = name, type_account = type_account, user = user))
    return resp

@app.route('/panel', methods = ('GET', 'POST'))
def painel():
    user = session.get('user')
    name = data_base.get_name(user)
    type_account = data_base.get_type_account(user)
    if request.method == 'GET':
        if type_account == 'Professor': resp = make_response(render_template('panel/teacher_panel.html', questionnaires = data_base.list_questionnaires(), name = name, classroom = data_base.return_classroom()))
        elif type_account == 'Aluno': resp = make_response(render_template('panel/student_panel.html', name = name, grades = data_base.return_grades_to_studant(name)))
        elif type_account == 'Administrador': resp = make_response(render_template('panel/adm_panel.html', name = name, class_ = data_base.return_classroom()))
        else: resp = make_response(redirect('/'))
    return resp

@app.route('/view/<path:path>')
def view(path):
    user = session.get('user')
    if not path in data_base.return_classroom(): resp = make_response(redirect('/'))
    elif data_base.get_type_account(user) != 'Administrador': resp = make_response(redirect('/'))
    else:
        name = data_base.get_name(user)
        studants = data_base.return_studants_by_class(path)
        resp = make_response(render_template('/panel/view_class.html', name = name, class_ = path, studants = studants))
    return resp

@app.route('/add-studants-to-class', methods = ('GET', 'POST'))
def add_studant_to_class():
    user = session.get('user')
    if data_base.get_type_account(user) != "Administrador": resp = make_response(redirect('/'))
    elif request.method == 'GET':
        studants = data_base.return_studants_to_fix()
        class_ = data_base.return_classroom()
        resp = make_response(render_template('config/fix_studants.html', studants = studants, class_ = class_))
    elif request.method == 'POST':
        classroom = data_base.return_classroom()
        for i in data_base.return_studants_to_fix():
            class_ = request.form['%s' %(i)]
            if class_ in classroom: data_base.configure_classroom(i, class_)
            resp = make_response(redirect('/panel'))
    return resp

@app.route('/configure-class')
def configure_class():
    user = session.get('user')
    if data_base.get_type_account(user) != "Administrador": resp = make_response(redirect('/'))
    else:
        classroom = data_base.return_classroom()
        resp = make_response(render_template('config/select_class.html', classroom = classroom))
    return resp

@app.route('/configure/<path:path>', methods = ('GET', 'POST'))
def configure(path):
    user = session.get('user')
    if not path in data_base.return_classroom(): resp = make_response(redirect('/'))
    elif data_base.get_type_account(user) != "Administrador": resp = make_response(redirect('/'))
    elif request.method == 'GET':
        studants = data_base.return_studants_by_class(path)
        classroom = data_base.return_classroom()
        resp = make_response(render_template('config/class_config.html', studants = studants, class_ = path, classroom = classroom))
    elif request.method == 'POST':
        classroom = data_base.return_classroom()
        for i in data_base.return_studants_by_class(path):
            class_ = request.form['%s' %(i)]
            if class_ in classroom: data_base.configure_classroom(i, class_)
            resp = make_response(redirect('/panel'))
    return resp

@app.route('/grades/<path:path>', methods = ('GET', 'POST'))
def grade(path):
    user = session.get('user')
    if data_base.get_type_account(user) != 'Professor' or path not in data_base.return_classroom() : resp = make_response(redirect('/'))
    elif request.method == 'GET': resp = make_response(render_template('config/grades.html', class_ = path, grades = data_base.return_grades_to_teacher(path)))
    else:
        for i in data_base.return_studants_by_class(path):
            for l in range(1, 4):
                grade = request.form['%s' %(i + 'N' + str(l))]
                data_base.mycursor.execute('update %s set N%s = %s where studant = "%s"' %(path, l, grade, i))
        data_base.mydb.commit()
        resp = make_response(redirect('/panel'))
    return resp

@app.route('/questionnaires', methods = ('GET', 'POST'))
def create_questionnaires():
    user = session.get('user')
    if data_base.get_type_account(user) != 'Professor': resp = make_response(redirect('/'))
    elif request.method == 'GET': resp = make_response(render_template('/questionnaires/new.html'))
    elif request.method == 'POST':
        name_form = request.form['name_form']
        id_form = functions.md5_hash(name_form)
        if data_base.create_quiz(name_form, id_form): resp = make_response(redirect('/questionnaires/%s' %(id_form)))
        else: resp = make_response(redirect('/'))
    return resp

@app.route('/questionnaires/<path:path>', methods = ('GET', 'POST'))
def questionnaires(path):
    user = session.get('user')
    if not data_base.is_questionnaires(path): resp = make_response(redirect('/'))
    elif data_base.get_type_account(user) == 'Professor':
        if request.method == 'GET':
            data = data_base.get_data_by_quiz(path)
            resp = make_response(render_template('/questionnaires/edit_quiz.html', name = data[0][0], detais = data[0][1]))
        else:
            detais = request.form['detais']
            data_base.save_data_by_quiz(path, detais)
            resp = redirect('/questionnaires/%s' %(path))
    return resp

@app.route('/questionnaires/delete/<path:path>', methods = ('GET','POST'))
def delete_questionnaires(path):
    user = session.get('user')
    if data_base.get_type_account(user) == "Professor" and data_base.is_questionnaires(path): data_base.delete_quiz(path)
    return redirect('/panel')

#rotas websocket
@socketio.on('joined')
def joined(message):
    room = 'main_room'
    session['room'] = room
    join_room(room)
    menssage = data_base.get_menssage(room)
    emit('status', {'msg': '%s' %(menssage), 'session': '%s' %(session.get('user'))}, room = room)

@socketio.on('text')
def text(message):
    now = datetime.now()
    resp = '<%s> %s: %s' %(now.strftime("%d/%m/%Y %H:%M"), session.get('user'), message['msg'])
    data_base.store_menssage(session.get('room'), resp)
    emit('message', {'msg': '%s' %(resp)}, room = session.get('room'))

#rotas de login
@app.route('/login', methods = ('GET', 'POST'))
def login():
    user = session.get('user')
    if not (user == None or user == 'None'): return redirect('/')
    if request.method == 'GET': resp = make_response(render_template('login/login.html'))
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
    if (user == None or user == 'None'): resp = make_response(redirect('/login'))
    elif request.method == 'GET': resp = make_response(render_template('login/logout.html'))
    else:
        resp = make_response(redirect('/login'))
        session['user'] = None
    return resp

@app.route('/sign-up', methods = ('GET', 'POST'))
def sign_up():
    user = session.get('user')
    if not (user == None or user == 'None'): return redirect('/')
    elif request.method == 'GET': resp = make_response(render_template('login/create_credentials.html'))
    else:
        users = []
        user = request.form['user']
        name = request.form['real_name']
        passwd = request.form['passwd']
        data_base.mycursor.execute('select user from users')
        for i in data_base.mycursor: users.append(i[0])
        if len(users) == len([]): type_account = 'Administrador'
        elif len(users) == len(['hmm']): type_account = 'Professor'
        else: type_account = 'Aluno'
        if data_base.create_user(user, name, passwd, type_account):
            session['user'] = user
            resp = make_response(redirect('/'))
        else: resp = 'Usuário já existe...'
    return resp

#rotas para retono de conteudo
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