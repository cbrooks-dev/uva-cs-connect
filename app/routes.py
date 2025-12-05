from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db import execute, get_db, close_db

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
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY date ASC")
    events = cursor.fetchall()
    cursor.close()
    close_db()
    return render_template("events.html", events=events)


@bp.route("/users")
def users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users ORDER BY name ASC")
    users = cursor.fetchall()
    cursor.close()
    close_db()
    return render_template("profiles.html", users=users)


@bp.route("/demo")
def demo():
    return render_template("demo.html")
