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
    selected_skill = request.args.get("skill", "")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Base query: students + skills + profile_pic
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

    # Skill filter — filter by student_id, not by joined skill rows
    if selected_skill:
        query += """
            AND s.student_id IN (
                SELECT student_id
                FROM StudentSkill
                WHERE skill_id = %s
            )
        """
        params.append(selected_skill)

    # Search filter
    if search:
        query += """ AND (
            s.first_name LIKE %s OR
            s.last_name  LIKE %s OR
            s.email      LIKE %s
        )"""
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    # Group by student
    query += """
        GROUP BY
            s.student_id, s.first_name, s.last_name, s.email,
            s.grad_year, s.profile_pic
    """

    # Sorting
    if sort == "year":
        query += " ORDER BY s.grad_year ASC, s.last_name ASC, s.first_name ASC"
    else:
        query += " ORDER BY s.last_name ASC, s.first_name ASC"

    cursor.execute(query, params)
    users = cursor.fetchall()

    # ---------- Pull experiences, courses, and availability for all these users ----------
    student_ids = [u["student_id"] for u in users]

    experiences_by_student = {}
    courses_by_student = {}
    availability_by_student = {}

    # helper: convert time to minutes since midnight
    def to_minutes(t):
        # strings like "13:30:00"
        from datetime import datetime, time, timedelta
        if isinstance(t, str):
            h, m, *_ = t.split(":")
            return int(h) * 60 + int(m)
        if hasattr(t, "hour"):
            return t.hour * 60 + t.minute
        if hasattr(t, "seconds"):
            s = t.seconds
            return (s // 3600) * 60 + (s // 60) % 60
        return 0

    def slots_overlap(slot, my_slot):
        if slot["day_of_week"] != my_slot["day_of_week"]:
            return False
        s1 = to_minutes(slot["start_time"])
        e1 = to_minutes(slot["end_time"])
        s2 = to_minutes(my_slot["start_time"])
        e2 = to_minutes(my_slot["end_time"])
        return s1 < e2 and s2 < e1  # standard interval overlap

    # current user's slots (for overlap computation)
    my_slots = []
    if getattr(g, "user", None):
        cursor.execute(
            """
            SELECT day_of_week, start_time, end_time
            FROM AvailabilitySlot
            WHERE student_id = %s
            """,
            (g.user["student_id"],),
        )
        my_slots = cursor.fetchall()

    if student_ids:
        placeholders = ",".join(["%s"] * len(student_ids))

        # Experiences
        cursor.execute(
            f"""
            SELECT
                experience_id,
                student_id,
                job_title,
                organization,
                start_date,
                end_date,
                description
            FROM Experience
            WHERE student_id IN ({placeholders})
            ORDER BY start_date DESC
            """,
            student_ids,
        )
        for row in cursor.fetchall():
            experiences_by_student.setdefault(row["student_id"], []).append(row)

        # Courses
        cursor.execute(
            f"""
            SELECT
                e.student_id,
                c.course_id,
                c.title,
                c.year,
                c.section
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            WHERE e.student_id IN ({placeholders})
            ORDER BY c.year DESC, c.title
            """,
            student_ids,
        )
        for row in cursor.fetchall():
            courses_by_student.setdefault(row["student_id"], []).append(row)

        # Availability slots for all displayed users
        cursor.execute(
            f"""
            SELECT
                slot_id,
                student_id,
                day_of_week,
                start_time,
                end_time
            FROM AvailabilitySlot
            WHERE student_id IN ({placeholders})
            ORDER BY FIELD(day_of_week,'Mon','Tue','Wed','Thu','Fri','Sat','Sun'),
                     start_time
            """,
            student_ids,
        )
        for row in cursor.fetchall():
            # compute overlap with current user (if any)
            overlaps = any(slots_overlap(row, ms) for ms in my_slots) if my_slots else False
            row["overlaps"] = overlaps
            availability_by_student.setdefault(row["student_id"], []).append(row)

    # Attach experiences, courses, availability to each user dict
    for u in users:
        sid = u["student_id"]
        u["experiences"] = experiences_by_student.get(sid, [])
        u["courses"] = courses_by_student.get(sid, [])
        u["availability"] = availability_by_student.get(sid, [])

    # Skills for dropdown
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
        logged_in=bool(getattr(g, "user", None)), 
    )



@bp.route("/demo")
def demo():
    return render_template("demo.html")
