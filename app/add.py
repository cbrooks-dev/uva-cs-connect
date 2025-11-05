from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from .db import execute

bp = Blueprint('add', __name__)

bp.route("/student", methods=('POST'))
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        grad_year = request.form['grad_year']
        password = request.form['password']
        error = None
        
        if not first_name:
            error = 'First Name is required.'

        if not last_name:
            error = 'Last Name is required.'
        
        if not email:
            error = 'Email is required.'

        if not password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            execute(
                'INSERT INTO Student (student_id, first_name, last_name, email, grad_year, password)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.user['id'], first_name, last_name, email, grad_year if not None else None, generate_password_hash(password)),
                commit=True
            )
