# Flask Backend with HTML Integration
# Database: SQLite

from flask import Flask, request, render_template
import sqlite3
import bcrypt

app = Flask(__name__)

# Create Database and Table
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

# Render HTML Page
@app.route('/')
def index():
    return render_template('authenticate.html')  # Place your HTML file in a 'templates' folder

# User Authentication Route
@app.route('/authenticate', methods=['POST'])
def authenticate():
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

if __name__ == '__main__':
    app.run(debug=True)

# HTML Link: Place 'index.html' in a folder named 'templates' next to 'app.py'.
# Access the page at http://127.0.0.1:5000/
