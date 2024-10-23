from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'seshaa3'
app.config['MYSQL_DB'] = 'smallbasket'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Message to show if login fails
    message = ''
    
    if request.method == 'POST':
        # Get the form inputs
        username = request.form['firstname']
        password = request.form['password']
        
        # Connect to MySQL and verify the user's credentials
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            # Set session variables
            session['loggedin'] = True
            session['username'] = account['username']
            
            # Redirect to the main page after successful login
            return redirect(url_for('main'))
        else:
            message = 'Incorrect username or password. Please try again.'
    
    # If it's a GET request or login fails, render the login page
    return render_template('login.html', message=message)

@app.route('/main')
def main():
    if 'loggedin' in session:
        # User is logged in, render the main page
        return f"Hello, {session['username']}! Welcome to the main page."
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear session data and redirect to login
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
