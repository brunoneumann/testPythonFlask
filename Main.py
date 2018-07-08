#coding=UTF8
import psycopg2

from flask import Flask, flash, Markup
from flask import render_template
from flask import session
from flask import request
from flask import redirect

app = Flask(__name__)

con = psycopg2.connect(
         host='localhost',
         database='dados666',
         user='postgres',
         password='postgres'
)

@app.route('/')
def index():
    if not 'LOGGGED' in session:
        return render_template('login.html')
    return rented_template('dashboard.html')

@app.route('/index')
def root():
    if not 'LOGGED' in session:
        return render_template('login.html')
    # endif
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None

        email = request.form['email']
        password = request.form['password']

        cur = con.cursor()

        sql  = "SELECT usuario "
        sql += "FROM login "
        sql += "WHERE usuario = '" + email + "'"
        sql += " and senha = '" + password + "'"

        cur.execute(sql)

        dados = cur.fetchall()

        if dados:
            session['LOGGED'] = True
            session['email'] = email
            session['password'] = password

            return redirect('/dashboard')
        else:
            flash('Usuario nao encontrado')
        # endif
    # endif
    return render_template('login.html')

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not 'LOGGED' in session:
        return render_template('dasboard.html')

    cur = con.cursor();
    sql = "SELECT * FROM cpu";
    cur.execute(sql);
    dados = cur.fetchall();

    return render_template('dashboard.html', data=dados)


# USUARIOS
@app.route("/usuarios")
def usuarios():
    if not 'LOGGED' in session:
        return render_template('login.html')

    cur = con.cursor();

    sql = "SELECT id,usuario,senha FROM login ORDER BY id DESC";

    cur.execute(sql)

    dados = cur.fetchall()

    return render_template('usuarios.html', data=dados)
def excluir():
    alert('excluir');


# USUARIO
@app.route("/usuario")
def usuario():
    if not 'LOGGED' in session:
        return render_template('login.html')

    _id = request.args.get('id')

    if _id == "0":
        return render_template('usuario.html')

    cur = con.cursor();
    sql = "SELECT id,usuario,senha FROM login WHERE id="+_id+"";
    cur.execute(sql)
    dados = cur.fetchall()

    return render_template('usuario.html', data=dados)


@app.route("/salvar_usuario", methods=['POST'])
def salvar_usuario():
    if not 'LOGGED' in session:
        return render_template('login.html')

    _id = request.args.get('id');
    email = request.form['email']
    senha = request.form['senha']
    cur = con.cursor();

    if _id == "0":
        sql = "INSERT INTO login(usuario,senha) VALUES('"+email+"','"+senha+"')";
    else:
        sql = "UPDATE login set usuario='"+email+"', senha='"+senha+"' WHERE id="+_id;

    cur.execute(sql)
    con.commit()

    return redirect('/usuarios')

@app.route("/excluir_usuario", methods=['GET','POST'])
def excluir_usuario():
    if not 'LOGGED' in session:
        return render_template('login.html')

    _id = request.args.get('id');
    cur = con.cursor();

    sql = "DELETE FROM login WHERE id="+_id;
    cur.execute(sql);
    con.commit();

    return redirect('/usuarios');


@app.route("/logout")
def logout():
    session.pop('LOGGED', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'sadkljsdakljfsdsdfds'
    app.session_type = 'memcache'
    app.run(host='0.0.0.0', port=8099, debug=True)
