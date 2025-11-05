# app/routes.py
from flask import Blueprint, render_template
from .db import execute

bp = Blueprint('main', __name__)

@bp.route('/health')
def health():
    # quick DB ping
    execute("SELECT 1")
    return "ok"

@bp.route('/')
def index():
    return render_template('index.html')