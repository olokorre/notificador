from flask import Flask, render_template, redirect, send_from_directory, request, make_response
import db, hashlib, functions

app = Flask(__name__)
user = functions.user_db()
data_base = db.Data_Base(user[0], user[1])

@app.route('/')
def index():
    return redirect('/create')

@app.route('/create', methods = ('GET', 'POST'))
def create():
    type_account = request.cookies.get('type_account')
    if request.method == 'GET' and (type_account == None or type_account == 'None'):
        resp = make_response(render_template('set_type_account.html'))
    elif request.method == 'POST' and (type_account == None or type_account == 'None'):
        type_account = request.form['type-account']
        resp = make_response(redirect('/create'))
        resp.set_cookie('type_account', type_account)
    elif request.method == 'GET' and not (type_account == None or type_account == 'None'):
        resp = make_response(render_template('create_credentials.html', type_account = type_account))
    else:
        resp = 'top'
        user = request.form['user']
        name = request.form['real_name']
        passwd = hashlib.md5(request.form['passwd'].encode()).hexdigest()
        data_base.create_user(user, name, passwd, type_account)
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
    app.run(debug=True)