from flask import Blueprint, render_template
from .db import execute

bp = Blueprint('main', __name__)

@bp.route('/health')
def health():

    execute("SELECT 1")
    return "ok"

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route("/demo")
def demo():
    return render_template('demo.html')


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/register")
def register():
    return render_template("register.html")
