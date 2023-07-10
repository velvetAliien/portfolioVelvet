import datetime
import hashlib

import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)

# Funzione per criptare la password utilizzando MD5
def encrypt_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

# Funzione per registrare un nuovo utente nel database
def register_user(username, password):
    encrypted_password = encrypt_password(password)

    # Connessione al database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='yourpasword',
        database='yourdatabasename'
    )
    cursor = connection.cursor()

    # Inserimento dei dati nel database
    insert_query = "INSERT INTO users (username, password, access_date) VALUES (%s, %s, %s)"
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(insert_query, (username, encrypted_password, current_date))
    connection.commit()

    cursor.close()
    connection.close()

# Funzione per effettuare il login dell'utente
def login(username, password):
    # Connessione al database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='yourpassword',
        database='yourdatabasename'
    )
    cursor = connection.cursor()

    # Verifica dell'utente nel database
    select_query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(select_query, (username,))
    user = cursor.fetchone()

    if user is None:
        return render_template('login3.html', message="L'utente non esiste.")
    else:
        stored_password = user[2]
        if encrypt_password(password) == stored_password:
            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return render_template('welcome2.html', username=username, access_date=current_date)
        else:
            return render_template('login3.html', message="Password errata.")

    cursor.close()
    connection.close()

@app.route('/')
def index():
    return render_template('login3.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    return login(username, password)

@app.route('/register')
def register():
    return render_template('register2.html')

@app.route('/register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']
    register_user(username, password)
    return render_template('registration_success.html')

if __name__ == '__main__':
    app.run()
