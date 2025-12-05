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
    if not g.user:
        return redirect(url_for("auth.login"))
    return render_template("profile.html", user=g.user)


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
        WHERE id=%s
    """, (first, last, email, grad_year, g.user['id']))

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
        filename = secure_filename(f"user_{g.user['id']}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Save file
        file.save(filepath)

        # Update database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student
            SET profile_pic=%s
            WHERE id=%s
        """, (filename, g.user['id']))
        conn.commit()
        cursor.close()
        close_db()

        flash("Profile picture updated!", "success")
        return redirect(url_for("profile.view_profile"))

    flash("Invalid file type.", "danger")
    return redirect(url_for("profile.view_profile"))
