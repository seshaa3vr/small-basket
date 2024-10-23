from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
app = Flask(__name__)
  
app.secret_key = 'xyzsdfg'
  
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'seshaa3'
app.config['MYSQL_DB'] = 'smallbasket'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = user['username']
            mesage = 'Logged in successfully!'
            return redirect(url_for('dashboard'))  # Assuming you'll redirect to a dashboard or another page
        else:
            mesage = 'Incorrect username or password!'
    return render_template('login.html', mesage=mesage)
  
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        email = request.form['email']
        username = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address!'
        elif not username or not password or not email:
            mesage = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            mesage = 'You have successfully registered!'
            return redirect(url_for('login'))  # Redirect to login after successful registration
    elif request.method == 'POST':
        mesage = 'Please fill out the form!'
    return render_template('signup.html', mesage=mesage)

if __name__ == "__main__":
    app.run()
