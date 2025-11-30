from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db import execute

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
    return render_template("events.html")


@bp.route("/demo")
def demo():
    return render_template("demo.html")
