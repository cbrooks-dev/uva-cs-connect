from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from .db import execute, get_db, close_db
from app.sort import sort_users, sort_events
from datetime import datetime

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
    sort_key = request.args.get("sort", "")
    search = request.args.get("q", "").strip()
    order_clause = sort_events(sort_key)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Get events with organizer_id
    query = """
        SELECT 
            e.event_id, e.title, e.description, e.type, e.start_datetime, e.end_datetime,
            e.location, e.created_by AS organizer_id
        FROM Event e
    """
    params = ()

    if search:
        query += " WHERE e.title LIKE %s OR e.description LIKE %s OR e.type LIKE %s OR e.location LIKE %s"
        params = (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%")

    query += f" {order_clause}"

    cursor.execute(query, params)
    events = cursor.fetchall()

    # Fetch attendees for all events
    for event in events:
        # Parse datetime
        for key in ["start_datetime", "end_datetime"]:
            if event.get(key):
                dt = event[key]
                if isinstance(dt, str):
                    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                event[f"{key}_date"] = dt.strftime("%m/%d/%Y")       # Date
                event[f"{key}_time"] = dt.strftime("%I:%M %p").lstrip("0")  # 12-hour time

        # Get attendees
        cursor.execute("""
            SELECT s.first_name, s.last_name 
            FROM Student s
            JOIN Attends a ON s.student_id = a.student_id
            WHERE a.event_id = %s
        """, (event["event_id"],))
        event["attendees"] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("events.html", events=events, search=search, sort=sort_key)


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

