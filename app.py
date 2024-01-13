import random
import secrets
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

app.config['MYSQL_HOST'] = 'DESKTOP-2QT7FQE'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'example_project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def check_user(username, password):
    with mysql.connection.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND pass = %s", (username, password))
        user = cur.fetchone()
    return user

def add_user(id, username, email, password, hobby):
    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO users VALUES(%s, %s, %s, %s, %s)",
                    (id, username, email, password, hobby))
    mysql.connection.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']

        user = check_user(username, password)

        if user:
            flash("Login Successful", 'success')
            user_data = print_data(username, password)
            return render_template('index.html', data=user_data)
            # return render_template('index.html', user_data=user_data)
        else:
            flash("Login Failed | User does not exist!", "error")

    return render_template('login.html')

def generate_id():
    return random.randint(1, 100)

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['NewUsername']
        password = request.form['NewPassword']
        hobby = request.form['NewHobby']

        add_user(generate_id(), username, email, password, hobby)
        return redirect(url_for('login'))

    return render_template('signup.html')

def print_data(uname, pwd):
    with mysql.connection.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND pass = %s", (uname, pwd))
        result = cur.fetchone()
    return result

if __name__ == '__main__':
    app.run(port=5000, debug=True)