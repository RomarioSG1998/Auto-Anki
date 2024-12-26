from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os

# Inicialize o aplicativo Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use uma chave secreta para gerenciar sessões

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test1'

# Inicializa a conexão MySQL
mysql = MySQL(app)

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')  # Usando 'senha'

        # Verificar se o usuário existe no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE email = %s AND senha = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['user'] = email  # Armazena o email na sessão
            return redirect(url_for('welcome'))

        return 'Credenciais inválidas, por favor, tente novamente.'

    return render_template_string(''' 
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form method="POST">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Seu email" required>
            
            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" placeholder="Sua senha" required>
            
            <input type="submit" value="Login">
        </form>
        <div class="link">
            <a href="/register">Cadastrar-se</a>
        </div>
    </body>
    </html>
    ''')

# Rota para a página de boas-vindas
@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
            <title>Bem-vindo</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #eaeaea;
                }
                .fade-in {
                    opacity: 0; /* Inicialmente invisível */
                    animation: fadeIn 1s forwards; /* Animação que irá fazer a transição */
                }
                @keyframes fadeIn {
                    to {
                        opacity: 1; /* Finaliza a animação tornando o elemento visível */
                    }
                }
            </style>
        </head>
        <body>
            <div class="fade-in">
                <h1>Bem-vindo, {{ session['user'] }}!</h1>
                <a href="/logout">Logout</a>
            </div>
        </body>
        </html>
        ''')
    return redirect(url_for('login'))

# Rota para cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('senha')

        # Inserir dados do formulário no banco de dados MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (name, email, senha) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template_string(''' 
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>Cadastro</title>
    </head>
    <body>
        <h1>Cadastrar</h1>
        <form method="POST">
            <label for="name">Nome:</label>
            <input type="text" id="name" name="name" placeholder="Seu nome" required>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Seu email" required>
            
            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" placeholder="Sua senha" required>
            
            <input type="submit" value="Cadastrar">
        </form>
    </body>
    </html>
    ''')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Cria a pasta static caso não exista
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
