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

@bp.route("/about")
def about():
    return render_template("about.html")
