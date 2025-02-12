from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure random key
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

# Route for Login Page
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
    return render_template("loginpage.html")

# Home Route (Accessible without login)
@app.route("/")
def home():
    return render_template("home.html", name=session.get("user_name"))

# Route for Sign-up Page
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered!", "danger")
        return redirect(url_for("login"))

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for("login"))

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# Product Routes (Inline Login Check)
@app.route("/zephyrus")
def zephyrus():
    if "user_id" not in session:
        flash("Please log in to view this page!", "danger")
        return redirect(url_for("login"))
    return render_template("zephyrus.html")

@app.route("/zenbook")
def zenbook():
    if "user_id" not in session:
        flash("Please log in to view this page!", "danger")
        return redirect(url_for("login"))
    return render_template("zenbook.html")

@app.route("/vivobook")
def vivobook():
    if "user_id" not in session:
        flash("Please log in to view this page!", "danger")
        return redirect(url_for("login"))
    return render_template("vivobook.html")

@app.route("/tuf")
def tuf():
    if "user_id" not in session:
        flash("Please log in to view this page!", "danger")
        return redirect(url_for("login"))
    return render_template("tuf.html")

@app.route("/strix")
def strix():
    if "user_id" not in session:
        flash("Please log in to view this page!", "danger")
        return redirect(url_for("login"))
    return render_template("strix.html")

if __name__ == "__main__":
    app.run(debug=True)