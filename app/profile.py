from flask import Blueprint, render_template, request, redirect, url_for, flash, g
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
    """Show profile page with current user info + their skills."""
    if not g.user:
        return redirect(url_for("auth.login"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)


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


    cursor.execute("SELECT skill_id, name FROM Skill ORDER BY name")
    all_skills = cursor.fetchall()

    cursor.close()
    close_db()

    return render_template(
        "profile.html",
        user=g.user,
        skills=skills,        
        all_skills=all_skills 
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

    cursor.execute("""
        UPDATE Student
        SET first_name=%s, last_name=%s, email=%s, grad_year=%s
        WHERE student_id=%s
    """, (first, last, email, grad_year, g.user['student_id']))

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
        filename = secure_filename(f"user_{g.user['student_id']}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Save file
        file.save(filepath)

        # Update database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student
            SET profile_pic=%s
            WHERE student_id=%s
        """, (filename, g.user['student_id']))
        conn.commit()
        cursor.close()
        close_db()

        flash("Profile picture updated!", "success")
        return redirect(url_for("profile.view_profile"))

    flash("Invalid file type.", "danger")
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
    """Change how a skill appears on the user's profile.

    Implementation: create/use a skill with the new name and
    point this user's StudentSkill row at that skill.
    """
    if not g.user:
        return redirect(url_for("auth.login"))

    old_skill_id = request.form.get("skill_id")
    new_name = (request.form.get("new_name") or "").strip()

    if not old_skill_id or not new_name:
        flash("Please choose a skill and enter a new name.", "danger")
        return redirect(url_for("profile.view_profile"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT skill_id FROM Skill WHERE name = %s", (new_name,))
    row = cursor.fetchone()
    if row:
        new_skill_id = row["skill_id"]
    else:
        cursor.execute("INSERT INTO Skill (name) VALUES (%s)", (new_name,))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID() AS skill_id")
        new_skill_id = cursor.fetchone()["skill_id"]


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


