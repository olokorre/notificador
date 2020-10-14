from flask import Flask, render_template, redirect, send_from_directory, request

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/create')

@app.route('/create', methods = ('GET', 'POST'))
def create():
    if request.method == 'GET': return render_template('create.html')
    else:
        pass

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