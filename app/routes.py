from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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

    query = "SELECT event_id, title, description, type, start_datetime, end_datetime, location FROM `Event`"
    params = ()

    if search:
        query += " WHERE title LIKE %s OR description LIKE %s OR type LIKE %s OR location LIKE %s"
        params = (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%")

    query += f" {order_clause}"

    cursor.execute(query, params)
    events = cursor.fetchall()
    cursor.close()
    conn.close()

    # Separate date and time for template
    for event in events:
        for key in ["start_datetime", "end_datetime"]:
            if event.get(key):
                dt = event[key]
                if isinstance(dt, str):
                    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                event[f"{key}_date"] = dt.strftime("%m/%d/%Y")       # Date
                event[f"{key}_time"] = dt.strftime("%I:%M %p").lstrip("0")  # 12-hour time without leading zero

    return render_template("events.html", events=events, search=search, sort=sort_key)



@bp.route("/users")
def users():
    sort = request.args.get("sort", "alpha")
    search = request.args.get("q", "").strip()
    selected_skill = request.args.get("skill", "")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            s.student_id,
            s.first_name,
            s.last_name,
            s.email,
            s.grad_year,
            s.profile_pic,
            GROUP_CONCAT(DISTINCT sk.name ORDER BY sk.name SEPARATOR ', ') AS skills
        FROM Student s
        LEFT JOIN StudentSkill ss ON s.student_id = ss.student_id
        LEFT JOIN Skill sk ON ss.skill_id = sk.skill_id
        WHERE 1=1
    """

    params = []

    if selected_skill:
        query += """
            AND s.student_id IN (
                SELECT student_id
                FROM StudentSkill
                WHERE skill_id = %s
            )
        """
        params.append(selected_skill)

    if search:
        query += """ AND (
            s.first_name LIKE %s OR
            s.last_name  LIKE %s OR
            s.email      LIKE %s
        )"""
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])


    query += """
        GROUP BY
            s.student_id,
            s.first_name,
            s.last_name,
            s.email,
            s.grad_year,
            s.profile_pic
    """

    if sort == "year":
        query += " ORDER BY s.grad_year ASC, s.last_name ASC, s.first_name ASC"
    else:
        query += " ORDER BY s.last_name ASC, s.first_name ASC"

    cursor.execute(query, params)
    users = cursor.fetchall()


    cursor.execute("SELECT skill_id, name FROM Skill ORDER BY name")
    all_skills = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "users.html",
        users=users,
        all_skills=all_skills,
        selected_skill=selected_skill if selected_skill else "",
        search=search,
        sort=sort,
    )



@bp.route("/demo")
def demo():
    return render_template("demo.html")
