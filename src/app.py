from flask import Flask
from flask import render_template
    
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/dados')
def dados():
    return render_template('dados.html')

@app.route('/localizacao')
def localizacao():
    return render_template('localizacao.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == "__main__":
    app.run(debug=True)