from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash

from .db import execute

bp = Blueprint('add', __name__)


@bp.route("/student", methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')  # TODO: ensure unique email
        grad_year = request.form.get('grad_year')
        password = request.form.get('password')
        error = None

        if not student_id:
            error = 'Student ID is required.'
        if not first_name:
            error = 'First Name is required.'
        elif not last_name:
            error = 'Last Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            execute(
                '''
                INSERT INTO Student (student_id, first_name, last_name, email, grad_year, password)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (
                    student_id,
                    first_name,
                    last_name,
                    email,
                    grad_year if grad_year else None,
                    generate_password_hash(password)
                ),
                commit=True
            )
            flash('Student added successfully!')
            return redirect(url_for('some_page'))  # TODO: replace with actual route

    return render_template('something.html')  # TODO: handle non-POST or return something after flash


@bp.route("/course", methods=['POST'])
def add_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        title = request.form.get('title')
        year = request.form.get('year')
        section = request.form.get('section')
        error = None

        if not course_id:
            error = 'Course ID is required.'
        elif not title:
            error = 'Title is required.'
        elif not year:
            error = 'Year is required.'

        if error is not None:
            flash(error)
        else:
            execute(
                '''
                INSERT INTO Course (course_id, title, year, section)
                VALUES (?, ?, ?, ?)
                ''',
                (
                    course_id,
                    title,
                    year,
                    section if section else None
                ),
                commit=True
            )
            flash('Course added successfully!')
            return redirect(url_for('some_page'))  # TODO: replace with actual route

    return render_template('something.html')  # TODO: handle non-POST or return something after flash


@bp.route("/event", methods=['POST'])
def add_event():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        title = request.form.get('title')
        description = request.form.get('description')
        event_type = request.form.get('event_type')
        start_datetime = request.form.get('start_datetime')
        end_datetime = request.form.get('end_datetime')
        location =request.form.get('location')
        error = None

        if not event_id:
            error = 'Event ID is required.'
        elif not title:
            error = 'Title is required.'
        elif not start_datetime:
            error = 'Start Date and Time is required.'
        elif not end_datetime:
            error = 'End Date and Time is required.'

        if error is not None:
            flash(error)
        else:
            execute(
                '''
                INSERT INTO Event (event_id, title, description, type, start_datetime, end_datetime, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    event_id,
                    title,
                    description if description else None,
                    event_type if event_type else None,
                    start_datetime,
                    end_datetime,
                    location if location else None
                ),
                commit=True
            )
            flash('Event added successfully!')
            return redirect(url_for('some_page'))  # TODO: replace with actual route

    return render_template('something.html')  # TODO: handle non-POST or return something after flash


# TODO: add experience route


@bp.route("/skill", methods=['POST'])
def add_skill():
    if request.method == 'POST':
        skill_id = request.form.get('skill_id')
        name = request.form.get('name')  # TODO: ensure unique name
        error = None

        if not skill_id:
            error = 'Skill ID is required.'
        elif not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            execute(
                '''
                INSERT INTO Skill (skill_id, name)
                VALUES (?, ?)
                ''',
                (
                    skill_id,
                    name
                ),
                commit=True
            )
            flash('Skill added successfully!')
            return redirect(url_for('some_page'))  # TODO: replace with actual route

    return render_template('something.html')  # TODO: handle non-POST or return something after flash
