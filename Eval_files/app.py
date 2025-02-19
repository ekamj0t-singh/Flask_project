from flask import Flask, render_template, redirect, url_for, request
import bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Create database
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

@app.route('/authenticate', methods=["GET", 'POST'])
def authenticate():
    if request.method == 'GET':
        return render_template('authenticate.html')  # Ensure authenticate.html exists

    # For POST method (handling login/signup)
    
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()

    if record:
        if bcrypt.checkpw(password.encode('utf-8'), record[0]):
            return "Login Successful"
        else:
            return "Invalid Password"
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return "Signup Successful"

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  

@app.route("/zephyrus")
def zephyrus():
    return render_template("zephyrus.html")

@app.route("/zenbook")
def zenbook():
    return render_template("zenbook.html")

@app.route("/vivobook")
def vivobook():
    return render_template("vivobook.html")

@app.route("/tuf")
def tuf():
    return render_template("tuf.html")

@app.route("/strix")
def strix():
    return render_template("strix.html")


if __name__ == '__main__':
    app.run(debug=True)

