from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

pages = Blueprint('pages', __name__)

@pages.route("/")
def home():
    return render_template("login.html")

@pages.route("/signup")
def signup_page():
    return render_template("signup.html")

@pages.route("/login")
def login_page():
    return render_template("login.html")

@pages.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')
