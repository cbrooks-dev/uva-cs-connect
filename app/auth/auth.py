import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector.errors import IntegrityError
from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        grad_year = request.form.get("grad_year")
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        # Validation
        if not first_name or not last_name:
            error = "Full name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if grad_year:
            try:
                grad_year = int(grad_year)
                if grad_year < 2025 or grad_year > 2035:
                    error = "Graduation year must be between 2025 and 2035."
            except ValueError:
                error = "Graduation year must be a number."

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO Student (first_name, last_name, email, grad_year, password) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (
                        first_name,
                        last_name,
                        email,
                        grad_year,
                        generate_password_hash(password),
                    ),
                )
                db.commit()
            except IntegrityError:
                db.rollback()
                error = f"User {email} is already registered."
            else:
                cursor.close()
                return redirect(url_for("auth.login"))

        flash(error)
        cursor.close()

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        cursor.execute("SELECT * FROM Student WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            error = "Incorrect email."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["student_id"]
            cursor.close()
            return redirect(url_for("main.index"))

        flash(error)
        cursor.close()

    return render_template("login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None  # Initialize g.user as None
    
    if user_id:
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Student WHERE student_id = %s", (user_id,))
            g.user = cursor.fetchone()  # Set the user data in g.user
            cursor.close()
        except Exception as e:
            # Log the error (optional) or handle it
            print(f"Error loading user: {e}")
            g.user = None  # If there's an error, ensure g.user remains None


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
