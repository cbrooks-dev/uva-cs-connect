from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db import execute, get_db, close_db
from app.sort import sort_users

bp = Blueprint("main", __name__)


@bp.route("/health")
def health():

    execute("SELECT 1")
    return "ok"


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@bp.route("/events")
def events():
    search = request.args.get("q", "").strip()
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute(
            """
            SELECT event_id, title, description, type, start_datetime, end_datetime, location
            FROM `Event`
            WHERE title LIKE %s OR description LIKE %s OR type LIKE %s OR location LIKE %s
            ORDER BY start_datetime ASC
        """,
            (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"),
        )
    else:
        cursor.execute(
            """
            SELECT event_id, title, description, type, start_datetime, end_datetime, location
            FROM `Event`
            ORDER BY start_datetime ASC
        """
        )

    events = cursor.fetchall()
    cursor.close()
    close_db()
    return render_template("events.html", events=events)


@bp.route("/users")
def users():
    sort = request.args.get("sort", "alpha")
    search = request.args.get("q", "").strip()
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Base query
    query = "SELECT student_id, first_name, last_name, email, grad_year FROM Student"
    params = ()

    # Search filter
    if search:
        query += " WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s"
        params = (f"%{search}%", f"%{search}%", f"%{search}%")

    # Sorting
    if sort == "year":
        query += " ORDER BY grad_year ASC, last_name ASC, first_name ASC"
    else:
        query += " ORDER BY last_name ASC, first_name ASC"

    cursor.execute(query, params)
    users = cursor.fetchall()
    cursor.close()
    close_db()
    return render_template("users.html", users=users, search=search, sort=sort)

@bp.route("/demo")
def demo():
    return render_template("demo.html")
