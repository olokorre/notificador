from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Notificador 0.01'

if __name__ == "__main__":
    app.run()