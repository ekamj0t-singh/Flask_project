from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure random key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize database properly for Flask 2.3+
with app.app_context():
    db.create_all()

# Ensure login is required for all pages except login/signup
@app.before_request
def require_login():
    allowed_routes = ["login", "signup", "static"]
    if "user_id" not in session and request.endpoint not in allowed_routes:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash("Login successful!", "success")
            return redirect(url_for("home"))  
        else:
            flash("Invalid email or password", "danger")
    return render_template("loginpage.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("signup"))  # Redirect to signup instead of login

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# Dynamic Route for Product Pages
@app.route("/product/<model>")
def product_page(model):
    valid_models = ["zephyrus", "zenbook", "vivobook", "tuf", "strix"]
    if model in valid_models:
        return render_template(f"{model}.html")
    else:
        flash("Product not found", "danger")  # Flash message for product not found
        return redirect(url_for("home"))  # Redirect to home instead of returning 404

if __name__ == "__main__":
    app.run(debug=True)