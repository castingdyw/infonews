from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    a = 1
    return 'index123'


if __name__ == '__main__':
    app.run(debug=True)
