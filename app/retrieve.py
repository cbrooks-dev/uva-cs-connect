# app/retrieve.py
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from werkzeug.security import generate_password_hash  # included to mirror add.py imports
from .db import execute

bp = Blueprint("retrieve", __name__)

def _limit():
    try:
        n = int(request.args.get("limit", 100))
        return max(1, min(500, n))
    except ValueError:
        return 100

# --------- Students ----------
@bp.get("/students")
def get_students():
    rows = execute("""
        SELECT student_id, first_name, last_name, email, grad_year
        FROM Student
        ORDER BY last_name, first_name
        LIMIT %s
    """, (_limit(),), fetchall=True)
    return jsonify(rows)

@bp.get("/students/<int:student_id>")
def get_student(student_id: int):
    row = execute("""
        SELECT student_id, first_name, last_name, email, grad_year
        FROM Student
        WHERE student_id = %s
    """, (student_id,), fetchone=True)
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row)

# --------- Courses ----------
@bp.get("/courses")
def get_courses():
    rows = execute("""
        SELECT course_id, title, year, section
        FROM Course
        ORDER BY title
        LIMIT %s
    """, (_limit(),), fetchall=True)
    return jsonify(rows)

# --------- Events ----------
@bp.get("/events")
def get_events():
    rows = execute("""
        SELECT event_id, title, description, type, start_datetime, end_datetime, location
        FROM `Event`
        ORDER BY start_datetime DESC
        LIMIT %s
    """, (_limit(),), fetchall=True)
    return jsonify(rows)

@bp.get("/events/<int:event_id>")
def get_event(event_id: int):
    row = execute("""
        SELECT event_id, title, description, type, start_datetime, end_datetime, location
        FROM `Event`
        WHERE event_id = %s
    """, (event_id,), fetchone=True)
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(row)

# --------- Experiences (by student) ----------
@bp.get("/students/<int:student_id>/experiences")
def get_student_experiences(student_id: int):
    rows = execute("""
        SELECT experience_id, job_title, organization, start_date, end_date, description
        FROM Experience
        WHERE student_id = %s
        ORDER BY start_date DESC
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)

# --------- Skills / Interests ----------
@bp.get("/skills")
def get_skills():
    rows = execute("""
        SELECT skill_id, name
        FROM Skill
        ORDER BY name
        LIMIT %s
    """, (_limit(),), fetchall=True)
    return jsonify(rows)

@bp.get("/interests")
def get_interests():
    rows = execute("""
        SELECT interest_id, name
        FROM Interest
        ORDER BY name
        LIMIT %s
    """, (_limit(),), fetchall=True)
    return jsonify(rows)

# --------- Availability (by student) ----------
@bp.get("/students/<int:student_id>/availability")
def get_student_availability(student_id: int):
    rows = execute("""
        SELECT slot_id, day_of_week, start_time, end_time
        FROM AvailabilitySlot
        WHERE student_id = %s
        ORDER BY day_of_week, start_time
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)

# --------- Matches ----------
@bp.get("/matches")
def get_matches():
    rows = execute("""
        SELECT match_id, status, match_score, capacity
        FROM `Match`
        ORDER BY match_id
        LIMIT %s
    """, (_limit(),), fetchall=True)
    return jsonify(rows)

# --------- Enrollment / Attends / Organizes (by student) ----------
@bp.get("/students/<int:student_id>/enrollments")
def get_student_enrollments(student_id: int):
    rows = execute("""
        SELECT c.course_id, c.title, c.year, c.section
        FROM Enrollment e
        JOIN Course c ON c.course_id = e.course_id
        WHERE e.student_id = %s
        ORDER BY c.title
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)

@bp.get("/students/<int:student_id>/attends")
def get_student_attends(student_id: int):
    rows = execute("""
        SELECT ev.event_id, ev.title, ev.start_datetime, ev.end_datetime, ev.location
        FROM Attends a
        JOIN `Event` ev ON ev.event_id = a.event_id
        WHERE a.student_id = %s
        ORDER BY ev.start_datetime DESC
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)

@bp.get("/students/<int:student_id>/organizes")
def get_student_organizes(student_id: int):
    rows = execute("""
        SELECT ev.event_id, ev.title, ev.start_datetime, ev.end_datetime, ev.location
        FROM Organizes o
        JOIN `Event` ev ON ev.event_id = o.event_id
        WHERE o.student_id = %s
        ORDER BY ev.start_datetime DESC
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)

# --------- Student <-> Skills / Interests ----------
@bp.get("/students/<int:student_id>/skills")
def get_student_skills(student_id: int):
    rows = execute("""
        SELECT sk.skill_id, sk.name
        FROM StudentSkill ss
        JOIN Skill sk ON sk.skill_id = ss.skill_id
        WHERE ss.student_id = %s
        ORDER BY sk.name
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)

@bp.get("/students/<int:student_id>/interests")
def get_student_interests(student_id: int):
    rows = execute("""
        SELECT i.interest_id, i.name
        FROM StudentInterest si
        JOIN Interest i ON i.interest_id = si.interest_id
        WHERE si.student_id = %s
        ORDER BY i.name
        LIMIT %s
    """, (student_id, _limit()), fetchall=True)
    return jsonify(rows)
