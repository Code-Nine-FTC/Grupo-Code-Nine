from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import datetime
import csv
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações para o upload de imagens
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#conecta ao banco de dados
db = {
    'host': "localhost", #host = ip, no caso localhost
    'user': "root", #usuario para logar
    'password': "fatec", #senha
    'database': "cianp", #qual banco de dados será utilizado
} 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] #requisita os valores dos campos usuario e password do form de login
        senha = request.form['senha']
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor(dictionary=True)
        # Checa se o e-mail e a senha batem
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha = %s", (email, senha,))
        user = cursor.fetchone() #verifica se os valores das variaveis usuario e password coincidem com os valores salvos no banco de dados
        #e insere na variavel user o valor True se os dados coincidirem, caso contrário insere False
        if email == 'ninecode.codek9@gmail.com' and senha == 'codenine123':
            session['admin'] = True
            return redirect('/admin')
        if user: #caso a variável user seja verdadeira
            session['email_usuario']=email
            session['nome_usuario']=user['usuario']
            return redirect(url_for('perfil'))
        else:
            flash('Dados inválidos.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST']) #inicia a rota de get e post de dados no form html
def cadastro():
    if request.method == 'POST': 
        usuario = request.form['usuario'] #adiciona o valor usuario do form para a variavel usuario
        senha = request.form['senha'] #adiciona o valor password do form para a variavel password
        email = request.form['email'] #adiciona o valor email do form para a variavel email
        cpf = request.form['cpf'] #adiciona o valor cpf do form para a variável cpf
        prof = request.form['prof'] #adiciona o valor prof do form para a variável prof
        data_nasc = request.form['data_nasc'] #adiciona o valor data do form para a variavel data
        parentesco = request.form['parentesco'] #adiciona o valor parentesco do form para a variavel parentesco
        conheceu = request.form['conheceu'] #adicionar o valor de onde conhece o site do form para a variavel conheceu

        if not cpf.isdigit or len(cpf) != 11:
            flash('CPF inválido. Deve ter exatamente 11 dígitos.')
            return redirect(url_for('cadastro'))
        if len(senha) > 15:
            flash('Senha inválida. Ela deve ter 15 dígitos no máximo.')
            return redirect(url_for('cadastro'))
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("SELECT * from usuario WHERE email = %s or cpf = %s", (email, cpf,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash('Endereço de e-mail e/ou CPF já estão em uso.')
            return redirect(url_for('cadastro')) 
        try:
            cursor.execute("INSERT INTO usuario (usuario, email, cpf, prof, data_nasc, parentesco, senha, conheceu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (usuario, email, cpf, prof, data_nasc, parentesco, senha, conheceu))
            conn.commit() #insere os valores das variaveis usuario e password para suas respectivas colunas na tabela users
            return redirect(url_for('login')) #retorna o usuário para a tela de login
        except mysql.connector.Error as err:
            print(f'Erro no banco de dados: {err}')
            return redirect('/')
        finally:
            cursor.close()
            conn.close()
    return render_template('cadastro.html')

@app.route('/senha', methods=['GET', 'POST'])
def senha():
    if request.method=='POST':
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("SELECT * from usuario WHERE email = %s and cpf = %s", (email, cpf,))
        user = cursor.fetchone()
        if user:
            cursor.execute("UPDATE usuario SET senha = %s WHERE email = %s and cpf = %s", (senha, email, cpf,))
            conn.commit()
            flash('Senha alterada')
        else:
            flash('Usuário não cadastrado')
        cursor.close()
        conn.close()
        return redirect('/login')
    return render_template('senha.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/dados',methods =['GET','POST'])
def dados():
    return render_template('dados.html')

@app.route('/dadoscsv', methods= ['GET', 'POST'])
def dadoscsv():
    tipo = request.form['dadosofc']
    if tipo:
        with open('../Docs/csv/' + tipo +'.csv', encoding='UTF-8') as file:
            df = pd.read_csv(file, delimiter=';')
            html_table = df.to_html(classes='table table-striped', index=False)
            response = {"table": html_table}
            return jsonify(response)
    else:
        return jsonify({'error': 'No file part'})
    
@app.route('/fontes')
def fontes():
    return render_template('fontes.html')

@app.route('/localizacao')
def localizacao():
    return render_template('localizacao.html')

@app.route('/loccsv', methods = ['POST', 'GET'])
def teste():
    regiao = request.form['regiao']
    if regiao:
        estado = request.form['estado']
        with open('../Docs/csv/' + estado +'.csv', encoding='UTF-8') as file:
            df = pd.read_csv(file, delimiter=';')
            html_table = df.to_html(classes='table table-striped', index=False)
            response = {"table": html_table}
            return jsonify(response)
    else:
        return jsonify({'error': 'No file part'})

@app.route('/forum')
def forum():
    try:
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM postagens")
        postagens = cursor.fetchall()
        return render_template('forum.html', postagens=postagens)
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
        perguntas = cursor.fetchall()
        return render_template('faq.html', perguntas=perguntas)
    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    finally:
        cursor.close()
        conn.close()
    return render_template('faq.html')


@app.route('/perfil', methods = ['POST', 'GET'])
def perfil():
    if is_admin():
        return redirect('/admin')
    if 'email_usuario' in session:
        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            email = session['email_usuario']
            cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            user = cursor.fetchone()
            return render_template('perfil.html', user=user)
        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return redirect('/')
        finally:
            cursor.close()
            conn.close()
    else:
        return redirect(url_for('login'))

def is_admin():
    return 'admin' in session and session['admin']

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    if not is_admin():
        return redirect('/login')
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'publicar_postagens':
            post_id = request.form.get('post_id')
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute('UPDATE postagens SET aprovado = True WHERE id = %s', (post_id,))
            conn.commit()
            cursor.close()
            conn.close()
        elif action == 'deletar_postagens':
            post_id = request.form.get('post_id')
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM comentarios WHERE post_id = %s', (post_id,))
            cursor.execute('DELETE FROM postagens WHERE id = %s', (post_id,))
            conn.commit()
            cursor.close()
            conn.close()

        elif action == 'publicar_perguntas':
            perg_id = request.form.get('perg_id')
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute('UPDATE perguntas SET aprovado = True WHERE id = %s', (perg_id,))
            conn.commit()
            cursor.close()
            conn.close()

        elif action == 'deletar_perguntas':
            perg_id = request.form.get('perg_id')
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM respostas WHERE perg_id = %s', (perg_id,))
            cursor.execute('DELETE FROM perguntas WHERE id = %s', (perg_id,))
            conn.commit()
            cursor.close()
            conn.close()

        elif action == 'deletar_usuario':
            email = request.form.get('email')
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM comentarios WHERE autor_email = %s', (email,))
            cursor.execute('DELETE FROM postagens WHERE autor_email = %s', (email,))
            cursor.execute('DELETE FROM respostas WHERE autor_email = %s', (email,))
            cursor.execute('DELETE FROM perguntas WHERE autor_email = %s', (email,))
            cursor.execute('DELETE FROM usuario WHERE email = %s', (email,))
            conn.commit()
            cursor.close()
            conn.close()
            
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM postagens ORDER BY id DESC')
    postagens = cursor.fetchall()
    cursor.execute('SELECT email, usuario FROM usuario ORDER BY email')
    usuarios = cursor.fetchall()
    cursor.execute('SELECT * FROM perguntas ORDER BY id DESC')
    perguntas = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin.html', postagens = postagens, usuarios = usuarios, perguntas = perguntas)

@app.route('/logout_admin', methods = ['POST', 'GET'])
def logout_admin():
    if is_admin():
        session.pop('admin', None)
        session.clear()
    return redirect(url_for('login'))

@app.route('/logout', methods= ['POST', 'GET'])
def logout():
    if 'email_usuario' in session:
        session.pop('email_usuario', None)
        session.clear()
    return redirect(url_for('login'))

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if 'email_usuario' in session:
        if request.method == 'POST':
            autor_email = session['email_usuario']
            nome_usuario = session['nome_usuario']
            texto = request.form['post_text']
            title = request.form['post_title']
            if len(texto) > 1500:
                flash('Tamanho inválido de texto. O máximo é de 1500 dígitos.')
                return redirect(url_for('create_post'))
            # Processar o upload de imagens
            image_urls = []
            for i in range(1, 4):
                image = request.files.get(f"imagem{i}")
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    file_path = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image.save(file_path)
                    image_url = f"/static/uploads/{filename}"
                    image_urls.append(image_url)

            # Resto do código para inserir no banco de dados
            timestamp_brasil = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            try:
                conn = mysql.connector.connect(**db)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO postagens (titulo, autor_email, nome_usuario, texto, imagem1, imagem2, imagem3, timestamp_brasil) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (title, autor_email, nome_usuario, texto, image_urls[0] if len(image_urls) > 0 else None, image_urls[1] if len(image_urls) > 1 else None, image_urls[2] if len(image_urls) > 2 else None, timestamp_brasil,))
                conn.commit()
                return redirect(url_for('forum'))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return redirect('/')
            finally:
                cursor.close()
                conn.close()
        # Resto do código para tratamento de erros e finalização
    else:
        flash('Você deve estar logado(a) para fazer uma postagem.')
        return redirect(url_for('forum'))

# Rota para a página de comentários de uma postagem
@app.route('/post/<int:post_id>')
def post_comments(post_id):
    if 'email_usuario' in session or is_admin():
        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM postagens WHERE id = %s", (post_id,))
            post = cursor.fetchone()
            cursor.execute("SELECT * FROM comentarios WHERE post_id = %s", (post_id,))
            comentarios = cursor.fetchall()
            return render_template('pcoments.html', post=post, comentarios=comentarios)
        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return redirect('/')
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Você precisa estar conectado para acessar os comentários.")
        return redirect(url_for('forum'))

# Rota para adicionar um comentário a uma postagem
@app.route('/add_comment/<int:post_id>', methods=['POST', 'GET'])
def add_comment(post_id):
    if 'email_usuario' in session:
        if request.method == 'POST':
            autor_email = session['email_usuario']
            nome_usuario = session['nome_usuario']
            texto = request.form['texto']  # Captura o conteúdo do comentário
            # Verificação do tamanho do comentário (até 300 caracteres)
            if len(texto) > 300:
                flash("O comentário excede o tamanho máximo de 300 caracteres.")
                return redirect(url_for('add_comment'))
            timestamp_brasil = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            try:
                conn = mysql.connector.connect(**db)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("INSERT INTO comentarios (post_id, autor_email, nome_usuario, texto, timestamp_brasil) VALUES (%s, %s, %s, %s, %s)",
                               (post_id, autor_email, nome_usuario, texto, timestamp_brasil,))
                conn.commit()
                return redirect(url_for('post_comments', post_id=post_id))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return redirect('/')
            finally:
                cursor.close()
                conn.close()

@app.route('/criar_pergunta', methods=['POST', 'GET'])
def criar_pergunta():
    if 'email_usuario' in session:
        if request.method == 'POST':
            autor_email = session['email_usuario']
            nome_usuario = session['nome_usuario']
            texto = request.form['texto']  # Captura o conteúdo da pergunta
            # Verificação do tamanho da pergunta (até 300 caracteres)
            if len(texto) > 500:
                flash("A pergunta excede o tamanho máximo de 500 caracteres.")
                return redirect(url_for('criar_pergunta'))
            timestamp_brasil = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            try:
                conn = mysql.connector.connect(**db)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO perguntas (autor_email, nome_usuario, texto, timestamp_brasil) VALUES (%s, %s, %s, %s)",
                               (autor_email, nome_usuario, texto, timestamp_brasil,))
                conn.commit()
                return redirect(url_for('faq'))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return redirect('/')
            finally:
                cursor.close()
                conn.close()
    else:
        flash("Você precisa estar conectado para fazer uma pergunta.")
        return redirect(url_for('faq'))

@app.route('/perg/<int:perg_id>')
def post_comments2(perg_id):
    if 'email_usuario' in session or is_admin():
        try:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM perguntas WHERE id = %s", (perg_id,))
            perg = cursor.fetchone()
            cursor.execute("SELECT * FROM respostas WHERE perg_id = %s", (perg_id,))
            respostas = cursor.fetchall()
            return render_template('pcoments2.html', perg=perg, respostas=respostas)
        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return redirect('/')
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Você precisa estar conectado para acessar as respostas.")
        return redirect(url_for('faq'))
    
# Rota para adicionar um comentário a uma pergunta
@app.route('/add_comment2/<int:perg_id>', methods=['POST'])
def add_comment2(perg_id):
    if 'email_usuario' in session:
        if request.method == 'POST':
            autor_email = session['email_usuario']
            nome_usuario = session['nome_usuario']
            texto = request.form['texto']  # Captura o conteúdo do comentário
            # Verificação do tamanho do comentário (até 300 caracteres)
            if len(texto) > 300:
                flash("O comentário excede o tamanho máximo de 300 caracteres.")
                return redirect('/perg/<int:perg_id>')
            timestamp_brasil = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            try:
                conn = mysql.connector.connect(**db)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("INSERT INTO respostas (perg_id, autor_email, nome_usuario, texto, timestamp_brasil) VALUES (%s, %s, %s, %s, %s)",
                               (perg_id, autor_email, nome_usuario, texto, timestamp_brasil,))
                conn.commit()
                return redirect(url_for('post_comments2', perg_id=perg_id))
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                return redirect('/')
            finally:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    app.secret_key = '8f2bdd84d7c4443215a42c84dabd52b21f9bdd596790cd61'
    app.run(debug=True)