from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

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

# Database Setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    """Home page should always be accessible"""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for user authentication"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):  # user[3] is the hashed password
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!', 'success')

            # Redirect user to their intended page
            next_page = session.pop('next', None)  # Get the page they tried to visit
            return redirect(f'/{next_page}') if next_page else redirect('/')

        flash('Invalid credentials, please try again.', 'danger')

    return render_template('loginpage.html')

@app.route('/signup', methods=['POST'])
def signup():
    """User sign-up functionality"""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        flash('All fields are required!', 'danger')
        return redirect('/')

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        conn.commit()
        conn.close()
        flash('Sign-up successful! You can now log in.', 'success')
    except sqlite3.IntegrityError:
        flash('Email already exists. Please log in.', 'warning')

    return redirect('/login')

@app.route('/logout')
def logout():
    """Logout functionality"""
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect('/')

@app.route('/<page>')
def navigate(page):
    """Restrict access to pages other than home"""
    if page == 'home':
        return render_template('home.html')  # Allow home page access without login

    if 'user_id' not in session:
        flash('You need to log in first!', 'warning')
        session['next'] = page  # Store the intended page before login
        return redirect('/login')

    # Ensure the requested page exists before rendering
    template_path = os.path.join("templates", f"{page}.html")
    if os.path.exists(template_path):
        return render_template(f"{page}.html")
    else:
        flash("Page not found!", "danger")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
