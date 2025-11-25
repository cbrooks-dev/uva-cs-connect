from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db import execute

bp = Blueprint('main', __name__)

@bp.route('/health')
def health():

    execute("SELECT 1")
    return "ok"

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        grad_year = request.form.get('grad_year')
        password = request.form['password']

        existing = execute(
            "SELECT * FROM Student WHERE email = %s",
            (email,),
            fetchone=True
        )

        if existing:
            flash("An account with that email already exists.")
            return redirect(url_for('main.register'))

        execute(
            """
            INSERT INTO Student (first_name, last_name, email, grad_year, password)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (first_name, last_name, email, grad_year, generate_password_hash(password)),
            commit=True
        )

        flash("Registration successful! You can now log in.")
        return redirect(url_for('main.login'))

    return render_template('register.html')


@bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@bp.route('/events')
def events():
    return render_template('events.html')

@bp.route("/demo")
def demo():
    return render_template('demo.html')

@bp.route("/about")
def about():
    return render_template("about.html")
