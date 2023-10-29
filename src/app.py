from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)

#conecta ao banco de dados
db = {
    'host': "localhost", #host = ip, no caso localhost
    'user': "cianp", #usuario para logar
    'password': "codenine", #senha
    'database': "cianp", #qual banco de dados será utilizado
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] #requisita os valores dos campos username e password do form de login
        senha = request.form['senha']
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor(dictionary=True)
        # Check if the username and password match
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha = %s", (email, senha)) 
        user = cursor.fetchone() #verifica se os valores das variaveis username e password coincidem com os valores salvos no banco de dados
        #e insere na variavel user o valor True se os dados coincidirem, caso contrário insere False

        if user: #caso a variável user seja verdadeira
            session['user_email']=email
            return redirect('/perfil')
        else:
            return 'Inválido.'
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
        if not cpf.isdigit or len(cpf) != 11:
            return "CPF inválido"
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("SELECT * from usuario where email = %s or cpf = %s", (email, cpf))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return "CPF ou email já em uso"
        
        try:
            cursor.execute("INSERT INTO usuario (username, email, cpf, prof, data_nasc, parentesco, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, email, cpf, prof, data_nasc, parentesco, senha))
            conn.commit() #insere os valores das variaveis username e password para suas respectivas colunas na tabela users
            cursor.close()
            conn.close()
            #alert("Cadastro realizado, agora você pode logar.") #exibe um alerta de que a tarefa foi concluida
            return redirect(url_for('login')) #retorna o usuário para a tela de login
        except mysql.connector.Error as err:
            print(f'Erro no banco: {err}')
            cursor.close()
            conn.close()
            return 'Erro no cadastro'
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

@app.route('/postagem', methods = ['POST', 'GET'])
def postagem():
    if 'user_email' in session:
        #codigo da postagem
        return redirect ('/faq')
    return redirect('/login')

@app.route('/forum')
def forum():
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        return render_template('forum.html', posts=posts)
    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    finally:
        cursor.close()
        conn.close()
    return render_template('forum.html')

@app.route('/faq')
def faq():
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perguntas")
        perg = cursor.fetchall()
        return render_template('faq.html', perg=perg)
    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    finally:
        cursor.close()
        conn.close()
    return render_template('faq.html')


@app.route('/perfil', methods = ['POST', 'GET'])
def perfil():
    if 'user_email' in session:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        email = session['user_email']
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        return render_template('perfil.html', user=user)
    return redirect('/login')
    
@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('user_email', None)
    return redirect('/login')
    
# Rota para criar uma nova postagem
@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user_email' in session:
        if request.method == 'POST':
            user_email = session['user_email']
            content = request.form['post_text']  # Captura o conteúdo da postagem
            # Verificação do tamanho da postagem (até 1500 caracteres)
            if len(content) > 1500:
                return "A postagem excede o tamanho máximo de 1500 caracteres."
            if len(content) == 0:
                return "A postagem precisa de um conteúdo válido"
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO posts (user_email, content) VALUES (%s, %s)",
                               (user_email, content))
                conn.commit()
                return redirect(url_for('forum'))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return 'Erro, tente novamente'
            finally:
                cursor.close()
                conn.close()
    else:
        return "Você precisa estar conectado para fazer uma postagem."

# Rota para a página de comentários de uma postagem
@app.route('/post/<int:post_id>')
def post_comments(post_id):
    if 'user_email' in session:
        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
            post = cursor.fetchone()
            cursor.execute("SELECT * FROM coments WHERE post_id = %s", (post_id,))
            coments = cursor.fetchall()
            return render_template('pcoments.html', post=post, coments=coments)
        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return 'Erro, tente novamente'
        finally:
            cursor.close()
            conn.close()
    else:
        return "Você precisa estar conectado para acessar os comentários."

# Rota para adicionar um comentário a uma postagem
@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'user_email' in session:
        if request.method == 'POST':
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)
            user_email = session['user_email']
            content = request.form['content']  # Captura o conteúdo do comentário
            # Verificação do tamanho do comentário (até 300 caracteres)
            if len(content) > 300:
                return "O comentário excede o tamanho máximo de 300 caracteres."
            if len(content) == 0:
                return 'Insira um comentário válido'
            try:
                cursor.execute("INSERT INTO coments (post_id, user_email, content) VALUES (%s, %s, %s)",
                               (post_id, user_email, content))
                conn.commit()
                return redirect(url_for('post_comments', post_id=post_id))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return 'Erro, tente novamente'
            finally:
                cursor.close()
                conn.close()
    else:
        return "Você precisa estar conectado para fazer um comentário."

@app.route('/criar_pergunta', methods=['POST'])
def criar_pergunta():
    if 'user_email' in session:
        if request.method == 'POST':
            user_email = session['user_email']
            texto = request.form['perg_text']  # Captura o conteúdo da pergunta
            # Verificação do tamanho da pergunta (até 300 caracteres)
            if len(texto) > 300:
                return "A pergunta excede o tamanho máximo de 300 caracteres."
            if len(texto) == 0:
                return "A pergunta precisa de um conteúdo válido"
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO perguntas (user_email, texto) VALUES (%s, %s)",
                               (user_email, texto))
                conn.commit()
                return redirect(url_for('faq'))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return 'Erro, tente novamente'
            finally:
                cursor.close()
                conn.close()
    else:
        return "Você precisa estar conectado para fazer uma pergunta."

@app.route('/perg/<int:perg_id>')
def post_comments2(perg_id):
    if 'user_email' in session:
        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM perguntas WHERE id = %s", (perg_id,))
            perg = cursor.fetchone()
            cursor.execute("SELECT * FROM respostas_perguntas WHERE perg_id = %s", (perg_id,))
            coments2 = cursor.fetchall()
            return render_template('pcoments2.html', perg=perg, coments2=coments2)
        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return 'Erro, tente novamente'
        finally:
            cursor.close()
            conn.close()
    else:
        return "Você precisa estar conectado para acessar os comentários."
    
# Rota para adicionar um comentário a uma pergunta
@app.route('/add_comment2/<int:perg_id>', methods=['POST'])
def add_comment2(perg_id):
    if 'user_email' in session:
        if request.method == 'POST':
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)
            user_email = session['user_email']
            texto = request.form['texto']  # Captura o conteúdo do comentário
            # Verificação do tamanho do comentário (até 300 caracteres)
            if len(texto) > 300:
                return "O comentário excede o tamanho máximo de 300 caracteres."
            if len(texto) == 0:
                return 'Insira um comentário válido'
            try:
                cursor.execute("INSERT INTO respostas_perguntas (perg_id, user_email, texto) VALUES (%s, %s, %s)",
                               (perg_id, user_email, texto))
                conn.commit()
                return redirect(url_for('post_comments2', perg_id=perg_id))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return 'Erro, tente novamente'
            finally:
                cursor.close()
                conn.close()
    else:
        return "Você precisa estar conectado para fazer um comentário."

if __name__ == "__main__":
    app.secret_key = '8f2bdd84d7c4443215a42c84dabd52b21f9bdd596790cd61'
    app.run(debug=True)

