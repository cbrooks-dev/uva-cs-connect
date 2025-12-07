from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from .db import get_db
from .db import execute

bp = Blueprint("add", __name__)

# TODO: ensure uniqueness of query parameters, as well as other security checks


@bp.route("/student", methods=["POST"])
def add_student():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        grad_year = request.form.get("grad_year")
        password = request.form.get("password")
        error = None

        if not student_id:
            error = "Student ID is required."
        if not first_name:
            error = "First Name is required."
        elif not last_name:
            error = "Last Name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Student (student_id, first_name, last_name, email, grad_year, password)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    student_id,
                    first_name,
                    last_name,
                    email,
                    grad_year if grad_year else None,
                    generate_password_hash(password),
                ),
                commit=True,
            )
            flash("Student added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/course", methods=["POST"])
def add_course():
    if request.method == "POST":
        course_id = request.form.get("course_id")
        title = request.form.get("title")
        year = request.form.get("year")
        section = request.form.get("section")
        error = None

        if not course_id:
            error = "Course ID is required."
        elif not title:
            error = "Title is required."
        elif not year:
            error = "Year is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Course (course_id, title, year, section)
                VALUES (%s, %s, %s, %s)
                """,
                (course_id, title, year, section if section else None),
                commit=True,
            )
            flash("Course added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/event", methods=["POST"])
def add_event():
    if request.method == "POST":
        event_id = request.form.get("event_id")
        title = request.form.get("title")
        description = request.form.get("description")
        event_type = request.form.get("event_type")
        start_datetime = request.form.get("start_datetime")
        end_datetime = request.form.get("end_datetime")
        location = request.form.get("location")
        error = None

        if not event_id:
            error = "Event ID is required."
        elif not title:
            error = "Title is required."
        elif not start_datetime:
            error = "Start Date and Time is required."
        elif not end_datetime:
            error = "End Date and Time is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Event (event_id, title, description, type, start_datetime, end_datetime, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    event_id,
                    title,
                    description if description else None,
                    event_type if event_type else None,
                    start_datetime,
                    end_datetime,
                    location if location else None,
                ),
                commit=True,
            )
            flash("Event added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/experience", methods=["POST"])
def add_experience():
    if request.method == "POST":
        experience_id = request.form.get("experience_id")
        student_id = request.form.get("student_id")
        job_title = request.form.get("job_title")
        organization = request.form.get("organization")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        description = request.form.get("description")
        error = None

        if not experience_id:
            error = "Experience ID is required."
        elif not student_id:
            error = "Student ID is required."
        elif not job_title:
            error = "Job Title is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Experience (experience_id, student_id, job_title, organization, start_date, end_date, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    experience_id,
                    student_id,
                    job_title,
                    organization if organization else None,
                    start_date if start_date else None,
                    end_date if end_date else None,
                    description if description else None,
                ),
                commit=True,
            )
            flash("Experience added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/skill", methods=["POST"])
def add_skill():
    if request.method == "POST":
        skill_id = request.form.get("skill_id")
        name = request.form.get("name")
        error = None

        if not skill_id:
            error = "Skill ID is required."
        elif not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Skill (skill_id, name)
                VALUES (%s, %s)
                """,
                (skill_id, name),
                commit=True,
            )
            flash("Skill added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/interest", methods=["POST"])
def add_interest():
    if request.method == "POST":
        interest_id = request.form.get("interest_id")
        name = request.form.get("name")
        error = None

        if not interest_id:
            error = "Interest ID is required."
        elif not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Interest (interest_id, name)
                VALUES (%s, %s)
                """,
                (interest_id, name),
                commit=True,
            )
            flash("Interest added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/availability", methods=["POST"])
def add_availability():
    if request.method == "POST":
        slot_id = request.form.get("slot_id")
        student_id = request.form.get("student_id")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        day_of_week = request.form.get("day_of_week")
        error = None

        if not slot_id:
            error = "Slot ID is required."
        elif not student_id:
            error = "Student ID is required."
        elif not start_time:
            error = "Start Time is required."
        elif not end_time:
            error = "End Time is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO AvailabilitySlot (slot_id, student_id, start_time, end_time, day_of_week)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    slot_id,
                    student_id,
                    start_time,
                    end_time,
                    day_of_week if day_of_week else None,
                ),
                commit=True,
            )
            flash("Availability slot added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/match", methods=["POST"])
def add_match():
    if request.method == "POST":
        match_id = request.form.get("match_id")
        status = request.form.get("status")
        match_score = request.form.get("match_score")
        capacity = request.form.get("capacity")
        error = None

        if not match_id:
            error = "Match ID is required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO `Match` (match_id, status, match_score, capacity)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    match_id,
                    status if status else None,
                    match_score if match_score else None,
                    capacity if capacity else None,
                ),
                commit=True,
            )
            flash("Match added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/enrollment", methods=["POST"])
def add_enrollment():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        course_id = request.form.get("course_id")
        error = None

        if not student_id or not course_id:
            error = "Both Student ID and Course ID are required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Enrollment (student_id, course_id)
                VALUES (%s, %s)
                """,
                (student_id, course_id),
                commit=True,
            )
            flash("Enrollment added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/attends", methods=["POST"])
def add_attends():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        event_id = request.form.get("event_id")
        error = None

        if not student_id or not event_id:
            error = "Both Student ID and Event ID are required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Attends (student_id, event_id)
                VALUES (%s, %s)
                """,
                (student_id, event_id),
                commit=True,
            )
            flash("Attendance added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/organizes", methods=["POST"])
def add_organizes():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        event_id = request.form.get("event_id")
        error = None

        if not student_id or not event_id:
            error = "Both Student ID and Event ID are required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO Organizes (student_id, event_id)
                VALUES (%s, %s)
                """,
                (student_id, event_id),
                commit=True,
            )
            flash("Organizer link added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/student-skill", methods=["POST"])
def add_student_skill():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        skill_id = request.form.get("skill_id")
        error = None

        if not student_id or not skill_id:
            error = "Both Student ID and Skill ID are required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO StudentSkill (student_id, skill_id)
                VALUES (%s, %s)
                """,
                (student_id, skill_id),
                commit=True,
            )
            flash("Student skill added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/student-interest", methods=["POST"])
def add_student_interest():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        interest_id = request.form.get("interest_id")
        error = None

        if not student_id or not interest_id:
            error = "Both Student ID and Interest ID are required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO StudentInterest (student_id, interest_id)
                VALUES (%s, %s)
                """,
                (student_id, interest_id),
                commit=True,
            )
            flash("Student interest added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")


@bp.route("/match-participation", methods=["POST"])
def add_match_participation():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        match_id = request.form.get("match_id")
        error = None

        if not student_id or not match_id:
            error = "Both Student ID and Match ID are required."

        if error is not None:
            flash(error)
        else:
            execute(
                """
                INSERT INTO MatchParticipation (student_id, match_id)
                VALUES (%s, %s)
                """,
                (student_id, match_id),
                commit=True,
            )
            flash("Match participation added successfully!")
            return redirect(url_for("main.demo"))

    return render_template("something.html")

@bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    if not g.user:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        start_datetime = request.form["start_datetime"]
        end_datetime = request.form["end_datetime"]
        location = request.form["location"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Event (title, description, start_datetime, end_datetime, location, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, description, start_datetime, end_datetime, location, g.user["student_id"]))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("main.events"))

    return render_template("create_event.html")

@bp.route('/attend_event/<int:event_id>', methods=['POST'])
def attend_event(event_id):
    if not g.user:
        flash("You need to be logged in to attend events.", "warning")
        return redirect(url_for("main.events"))

    student_id = g.user['student_id']  # adjust based on your g.user

    db = get_db()
    cursor = db.cursor(dictionary=True)  # dictionary=True makes fetchone return a dict

    # Check if already attending
    cursor.execute(
        "SELECT * FROM Attends WHERE student_id = %s AND event_id = %s",
        (student_id, event_id)
    )
    existing = cursor.fetchone()

    if existing:
        flash("You are already attending this event!", "warning")
    else:
        cursor.execute(
            "INSERT INTO Attends (student_id, event_id) VALUES (%s, %s)",
            (student_id, event_id)
        )
        db.commit()
        flash("You are now attending this event!", "success")

    cursor.close()
    return redirect(url_for('main.events'))
