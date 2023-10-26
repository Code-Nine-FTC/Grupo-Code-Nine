from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "codenine"  # Change this to a strong, random key

#conecta ao banco de dados
db = mysql.connector.connect(
    host="localhost", #host = ip, no caso localhost
    user="root", #usuario para logar
    password="fatec", #senha
    database="cianp" #qual banco de dados será utilizado
)

cursor = db.cursor(buffered=True) #ativa a biblioteca cursor para acessar o banco de dados

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] #requisita os valores dos campos username e password do form de login
        senha = request.form['senha']

        # Check if the username and password match
        cursor.execute("SELECT * FROM usuario WHERE username = %s AND senha = %s", (email, senha)) 
        user = cursor.fetchone() #verifica se os valores das variaveis username e password coincidem com os valores salvos no banco de dados
        #e insere na variavel user o valor True se os dados coincidirem, caso contrário insere False

        if user: #caso a variável user seja verdadeira
            flash("Logado com sucesso") #exibe o alerta de login concluído
            session['logged_in'] = True #define o status da sessão como True
            return redirect(url_for('/')) #retorna o usuário para a tela home
        else:
            flash("Dados errados, tente novamente") #caso a variável user seja falsa
            #exibe um alerta de que os dados estão errados
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST']) #inicia a rota de get e post de dados no form html
def cadastro():
    if request.method == 'POST': 
        username = request.form['username'] #adiciona o valor username do form para a variavel username
        senha = request.form['senha'] #adiciona o valor password do form para a variavel password
        email = request.form['email'] #adiciona o valor email do form para a variavel email
        cpf = request.form['cpf'] #adiciona o valor cpf do form para a variável cpf
        prof = request.form['prof'] #adiciona o valor prof do form para a variável prof
        data_nasc = request.form['data_nasc'] #adiciona o valor data do form para a variavel data
        parentesco = request.form['parentesco'] #adiciona o valor parentesco do form para a variavel parentesco

        try:
            cursor.execute("INSERT INTO usuario (username, senha, email, cpf, prof, data_nasc, parentesco) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, senha, email, cpf, prof, data_nasc, parentesco))
            db.commit() #insere os valores das variaveis username e password para suas respectivas colunas na tabela users
            flash("Cadastro realizado, agora você pode logar.") #exibe um alerta de que a tarefa foi concluida
            return redirect(url_for('login')) #retorna o usuário para a tela de login
        except mysql.connector.Error as err:
            flash(f"Error: {err}") #caso um erro ocorra, ele é armazenado na variavel err, e um alerta é exibido na tela informando o erro
            db.rollback() #cancela a conexão ao banco de dados

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

@app.route('/perfil')
def perfil():
    if 'logged_in' in session and session['logged_in']: #caso a variável dde sessão seja definida como logada
        return render_template('perfil.html')
    else:
        return redirect(url_for('login')) #caso contrário, redireciona o usuário para a tela de login

if __name__ == "__main__":
    app.run(debug=True)