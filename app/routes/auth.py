import re

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.auth import load_logged_in_user
from app.db import get_db

bp = Blueprint("auth", __name__)


@bp.before_app_request
def load_user():
    load_logged_in_user()


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user is not None:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        error = None

        if not identifier or not password:
            error = "Enter your campus username or email and password."
        elif len(identifier) > 254 or len(password) > 128:
            error = "The username, email, or password is too long."

        user = None
        if error is None:
            user = get_db().execute(
                "SELECT * FROM users WHERE username = ? OR email = ? OR student_number = ?",
                (identifier, identifier, identifier),
            ).fetchone()
            if user is None or not check_password_hash(user["password_hash"], password):
                error = "Invalid login details. Please try again."

        if error is not None:
            flash(error, "danger")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")


@bp.route("/logout", methods=("POST",))
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
