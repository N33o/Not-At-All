from flask import Flask, render_template, request, make_response, redirect, session, render_template_string,  flash
import sqlite3
from hashlib import md5



app = Flask(__name__)
app.secret_key = 'SoSecret_DoYouKnowThat?'
conn = sqlite3.connect('example.db')
db = conn.cursor()


def hash_string(s):
    return md5(s.encode()).hexdigest()


@app.route('/')
def index():
    return render_template('index.html')

def check_login(user):
    query = 'SELECT * FROM users WHERE login = "{}"'.format(user)
    db.execute(query)
    exist = db.fetchone()
    if exist is None:
        return False
    else:
        return True


@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        if login == '' or password == '':
            #ТУТ ФЛАШ!!!
            flash("Login or password is missing. Try Again")
            return render_template('login.html')

        password = hash_string(password)
        #query = 'SELECT * FROM users WHERE login = ? and password = ?'
        query = 'SELECT * FROM users WHERE (login,password) VALUES ("{}","{}")'.format(login, password)
        db.execute(query, [login, password])
        result = db.fetchone()
        if result is None:
            # ТУТ ФЛАШ!!!
            flash("User doesn't exist or password is incorrect. Try again")
        #Тут должна быть сессия, но у меня не получается ! :с
        # ТУТ ФЛАШ!!!
        flash('You were successfully logged in')
        return render_template('company.html')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')

        if login == '' or password == '':
            flash("Login or password is missing")
            render_template('register.html')

        if check_login(login):
            # ТУТ ФЛАШ!!!
            flash("This login already exist")
            return render_template('register.html')
        password = hash_string(password)
        query = 'INSERT INTO users (login,password) VALUES ("{}","{}")'.format(login, password)
        db.execute(query)
        conn.commit()
        # ТУТ ФЛАШ!!!
        flash("Success! Now you can login in.")
        return render_template('login.html')

if __name__ == '__main__':
    init_query = 'CREATE TABLE IF NOT EXISTS users(id  integer NOT NULL PRIMARY KEY AUTOINCREMENT,login text,password text)'
    db.execute(init_query)
    conn.commit()
    app.run(port=5000)