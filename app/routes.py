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
    rows = execute(
        "SELECT student_id, first_name, last_name, email, grad_year "
        "FROM Student ORDER BY student_id LIMIT 10",
        fetchall=True
    )
    return render_template('base.html', students=rows or [])