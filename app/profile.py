from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from werkzeug.utils import secure_filename
import os
from app.db import get_db, close_db

bp = Blueprint("profile", __name__, url_prefix="/profile")

UPLOAD_FOLDER = "static/uploads/profile_pics"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def view_profile():
    """Show profile page with current user info + their skills, courses, experience, availability."""
    if not g.user:
        return redirect(url_for("auth.login"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # ---------- SKILLS for this student ----------
    cursor.execute(
        """
        SELECT s.skill_id, s.name
        FROM Skill s
        JOIN StudentSkill ss ON s.skill_id = ss.skill_id
        WHERE ss.student_id = %s
        ORDER BY s.name
        """,
        (g.user["student_id"],),
    )
    skills = cursor.fetchall()

    # All possible skills for dropdown
    cursor.execute("SELECT skill_id, name FROM Skill ORDER BY name")
    all_skills = cursor.fetchall()

    # ---------- ENROLLMENTS for this student ----------
    cursor.execute(
        """
        SELECT c.course_id, c.title, c.year, c.section
        FROM Enrollment e
        JOIN Course c ON e.course_id = c.course_id
        WHERE e.student_id = %s
        ORDER BY c.year DESC, c.title
        """,
        (g.user["student_id"],),
    )
    enrollments = cursor.fetchall()

    # All available courses (pre-defined)
    cursor.execute(
        """
        SELECT course_id, title, year, section
        FROM Course
        ORDER BY year DESC, title
        """
    )
    all_courses = cursor.fetchall()

    # ---------- EXPERIENCE for this student ----------
    cursor.execute(
        """
        SELECT experience_id, job_title, organization, start_date, end_date, description
        FROM Experience
        WHERE student_id = %s
        ORDER BY start_date DESC
        """,
        (g.user["student_id"],),
    )
    experiences = cursor.fetchall()

    # ---------- AVAILABILITY for this student ----------
    cursor.execute(
        """
        SELECT
            slot_id,
            day_of_week,
            TIME_FORMAT(start_time, '%H:%i') AS start_time,
            TIME_FORMAT(end_time,   '%H:%i') AS end_time
        FROM AvailabilitySlot
        WHERE student_id = %s
        ORDER BY day_of_week, start_time
        """,
        (g.user["student_id"],),
    )
    availability_slots = cursor.fetchall()

    cursor.close()
    close_db()

    # 30-minute time choices (tweak hours if you want)
    time_choices = []
    for hour in range(8, 22):      # 08:00–21:30
        for minute in (0, 30):
            time_choices.append(f"{hour:02d}:{minute:02d}")

    days_of_week = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    return render_template(
        "profile.html",
        user=g.user,
        skills=skills,
        all_skills=all_skills,
        enrollments=enrollments,
        all_courses=all_courses,
        experiences=experiences,
        availability_slots=availability_slots,
        time_choices=time_choices,
        days_of_week=days_of_week,
    )



@bp.route("/update", methods=["POST"])
def update_profile():
    if not g.user:
        return redirect(url_for("auth.login"))

    first = request.form.get("first_name")
    last = request.form.get("last_name")
    email = request.form.get("email")
    grad_year = request.form.get("grad_year")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Student
        SET first_name=%s, last_name=%s, email=%s, grad_year=%s
        WHERE student_id=%s
        """,
        (first, last, email, grad_year, g.user["student_id"]),
    )

    conn.commit()
    cursor.close()
    close_db()

    flash("Profile updated successfully!", "success")
    return redirect(url_for("profile.view_profile"))


@bp.route("/upload_photo", methods=["POST"])
def upload_photo():
    if not g.user:
        return redirect(url_for("auth.login"))

    if "photo" not in request.files:
        flash("No file uploaded.", "danger")
        return redirect(url_for("profile.view_profile"))

    file = request.files["photo"]

    if file.filename == "":
        flash("No selected file.", "danger")
        return redirect(url_for("profile.view_profile"))

    if file and allowed_file(file.filename):
        # Make a safe filename like user_3_originalname.png
        filename = secure_filename(f"user_{g.user['student_id']}_{file.filename}")

        # Build an absolute path to static/uploads/profile_pics
        upload_dir = os.path.join(
            current_app.root_path, "static", "uploads", "profile_pics"
        )
        os.makedirs(upload_dir, exist_ok=True)

        filepath = os.path.join(upload_dir, filename)

        # Save file to disk
        file.save(filepath)

        # Update database with just the filename
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Student
            SET profile_pic=%s
            WHERE student_id=%s
            """,
            (filename, g.user["student_id"]),
        )
        conn.commit()
        cursor.close()
        close_db()

        flash("Profile picture updated!", "success")
        return redirect(url_for("profile.view_profile"))

    flash("Invalid file type. Please upload a PNG, JPG, or GIF.", "danger")
    return redirect(url_for("profile.view_profile"))


@bp.route("/add_skill", methods=["POST"])
def add_skill():
    """Add a skill to the current user's profile."""
    if not g.user:
        return redirect(url_for("auth.login"))

    existing_skill_id = request.form.get("skill_id")
    skill_name = (request.form.get("skill_name") or "").strip()

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if existing_skill_id:
        skill_id = int(existing_skill_id)
    elif skill_name:
        cursor.execute("SELECT skill_id FROM Skill WHERE name = %s", (skill_name,))
        row = cursor.fetchone()
        if row:
            skill_id = row["skill_id"]
        else:
            cursor.execute("INSERT INTO Skill (name) VALUES (%s)", (skill_name,))
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID() AS skill_id")
            skill_id = cursor.fetchone()["skill_id"]
    else:
        cursor.close()
        close_db()
        flash("Please choose a skill or type a new one.", "danger")
        return redirect(url_for("profile.view_profile"))

    cursor.execute(
        """
        SELECT 1 FROM StudentSkill
        WHERE student_id = %s AND skill_id = %s
        """,
        (g.user["student_id"], skill_id),
    )
    if cursor.fetchone():
        flash("You already have that skill.", "info")
    else:
        cursor.execute(
            """
            INSERT INTO StudentSkill (student_id, skill_id)
            VALUES (%s, %s)
            """,
            (g.user["student_id"], skill_id),
        )
        conn.commit()
        flash("Skill added to your profile!", "success")

    cursor.close()
    close_db()
    return redirect(url_for("profile.view_profile"))


@bp.route("/delete_skill", methods=["POST"])
def delete_skill():
    """Remove a skill from the current user's profile (does NOT delete global skill)."""
    if not g.user:
        return redirect(url_for("auth.login"))

    skill_id = request.form.get("skill_id")
    if not skill_id:
        flash("No skill selected.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM StudentSkill
        WHERE student_id = %s AND skill_id = %s
        """,
        (g.user["student_id"], skill_id),
    )
    conn.commit()
    cursor.close()
    close_db()

    flash("Skill removed from your profile.", "success")
    return redirect(url_for("profile.view_profile"))


@bp.route("/edit_skill", methods=["POST"])
def edit_skill():
    """Change how a skill appears on the user's profile."""
    if not g.user:
        return redirect(url_for("auth.login"))

    old_skill_id = request.form.get("skill_id")
    new_name = (request.form.get("new_name") or "").strip()

    if not old_skill_id or not new_name:
        flash("Please choose a skill and enter a new name.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Find or create skill with the new name
    cursor.execute("SELECT skill_id FROM Skill WHERE name = %s", (new_name,))
    row = cursor.fetchone()
    if row:
        new_skill_id = row["skill_id"]
    else:
        cursor.execute("INSERT INTO Skill (name) VALUES (%s)", (new_name,))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID() AS skill_id")
        new_skill_id = cursor.fetchone()["skill_id"]

    # If user already has the new skill, just remove the old one
    cursor.execute(
        """
        SELECT 1 FROM StudentSkill
        WHERE student_id = %s AND skill_id = %s
        """,
        (g.user["student_id"], new_skill_id),
    )
    if cursor.fetchone():
        cursor.execute(
            """
            DELETE FROM StudentSkill
            WHERE student_id = %s AND skill_id = %s
            """,
            (g.user["student_id"], old_skill_id),
        )
    else:
        cursor.execute(
            """
            UPDATE StudentSkill
            SET skill_id = %s
            WHERE student_id = %s AND skill_id = %s
            """,
            (new_skill_id, g.user["student_id"], old_skill_id),
        )

    conn.commit()
    cursor.close()
    close_db()

    flash("Skill updated.", "success")
    return redirect(url_for("profile.view_profile"))

@bp.route("/add_enrollment", methods=["POST"])
def add_enrollment():
    """Add a course to the student's enrollments.

    Either:
      - choose an existing course_id, OR
      - create a new Course row from title/year/section, then enroll.
    """
    if not g.user:
        return redirect(url_for("auth.login"))

    existing_course_id = request.form.get("course_id")
    new_title = (request.form.get("new_course_title") or "").strip()
    new_year = (request.form.get("new_course_year") or "").strip()
    new_section = (request.form.get("new_course_section") or "").strip()

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Decide which course to use / create
    if existing_course_id:
        course_id = int(existing_course_id)

    elif new_title:
        # Require year + section when creating a new course
        if not new_year or not new_section:
            cursor.close()
            close_db()
            flash("Please provide year and section for the new course.", "danger")
            return redirect(url_for("profile.view_profile"))

        # See if a course with same title/year/section already exists
        cursor.execute(
            """
            SELECT course_id
            FROM Course
            WHERE title = %s AND year = %s AND section = %s
            """,
            (new_title, new_year, new_section),
        )
        row = cursor.fetchone()

        if row:
            course_id = row["course_id"]
        else:
            # Create new course
            cursor.execute(
                """
                INSERT INTO Course (title, year, section)
                VALUES (%s, %s, %s)
                """,
                (new_title, new_year, new_section),
            )
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID() AS course_id")
            course_id = cursor.fetchone()["course_id"]

    else:
        cursor.close()
        close_db()
        flash("Please select a course or enter a new one.", "danger")
        return redirect(url_for("profile.view_profile"))

    # Avoid duplicate enrollment
    cursor.execute(
        """
        SELECT 1 FROM Enrollment
        WHERE student_id = %s AND course_id = %s
        """,
        (g.user["student_id"], course_id),
    )
    if cursor.fetchone():
        flash("You are already enrolled in that course.", "info")
    else:
        cursor.execute(
            """
            INSERT INTO Enrollment (student_id, course_id)
            VALUES (%s, %s)
            """,
            (g.user["student_id"], course_id),
        )
        conn.commit()
        flash("Course added to your enrollments!", "success")

    cursor.close()
    close_db()
    return redirect(url_for("profile.view_profile"))



@bp.route("/delete_enrollment", methods=["POST"])
def delete_enrollment():
    """Remove a course from the student's enrollments."""
    if not g.user:
        return redirect(url_for("auth.login"))

    course_id = request.form.get("course_id")
    if not course_id:
        flash("No course selected.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM Enrollment
        WHERE student_id = %s AND course_id = %s
        """,
        (g.user["student_id"], course_id),
    )
    conn.commit()
    cursor.close()
    close_db()

    flash("Course removed from your enrollments.", "success")
    return redirect(url_for("profile.view_profile"))

@bp.route("/add_experience", methods=["POST"])
def add_experience():
    """Add an experience row for this student."""
    if not g.user:
        return redirect(url_for("auth.login"))

    job_title = (request.form.get("job_title") or "").strip()
    organization = (request.form.get("organization") or "").strip()
    start_date = request.form.get("start_date") or None  # yyyy-mm-dd
    end_date = request.form.get("end_date") or None
    description = (request.form.get("description") or "").strip()

    if not job_title or not organization:
        flash("Please provide at least a job title and organization.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Experience (student_id, job_title, organization, start_date, end_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (g.user["student_id"], job_title, organization, start_date, end_date, description),
    )
    conn.commit()
    cursor.close()
    close_db()

    flash("Experience added!", "success")
    return redirect(url_for("profile.view_profile"))


@bp.route("/delete_experience", methods=["POST"])
def delete_experience():
    """Delete one experience row for this student."""
    if not g.user:
        return redirect(url_for("auth.login"))

    experience_id = request.form.get("experience_id")
    if not experience_id:
        flash("No experience selected.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM Experience
        WHERE experience_id = %s AND student_id = %s
        """,
        (experience_id, g.user["student_id"]),
    )
    conn.commit()
    cursor.close()
    close_db()

    flash("Experience removed.", "success")
    return redirect(url_for("profile.view_profile"))


@bp.route("/availability/add", methods=["POST"])
def add_availability():
    """Add a weekly availability slot for the current user."""
    if not g.user:
        return redirect(url_for("auth.login"))

    day = request.form.get("day_of_week")
    start = request.form.get("start_time")
    end = request.form.get("end_time")

    if not day or not start or not end:
        flash("Please pick a day and a start/end time.", "danger")
        return redirect(url_for("profile.view_profile"))

    # simple validation: end must be after start
    if end <= start:
        flash("End time must be after start time.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO AvailabilitySlot (student_id, day_of_week, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        """,
        (g.user["student_id"], day, start, end),
    )
    conn.commit()
    cursor.close()
    close_db()

    flash("Availability slot added.", "success")
    return redirect(url_for("profile.view_profile"))


@bp.route("/availability/delete", methods=["POST"])
def delete_availability():
    """Remove one availability slot for the current user."""
    if not g.user:
        return redirect(url_for("auth.login"))

    slot_id = request.form.get("slot_id")
    if not slot_id:
        flash("No slot selected.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM AvailabilitySlot
        WHERE slot_id = %s AND student_id = %s
        """,
        (slot_id, g.user["student_id"]),
    )
    conn.commit()
    cursor.close()
    close_db()

    flash("Availability slot removed.", "success")
    return redirect(url_for("profile.view_profile"))



