import re

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth import login_required
from app.db import get_db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if g.user is not None:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@bp.route("/dashboard")
@login_required
def dashboard():
    database = get_db()
    attendance = database.execute(
        "SELECT status FROM attendance WHERE user_id = ?", (g.user["id"],)
    ).fetchall()
    total_attendance = len(attendance)
    present_count = sum(row["status"] == "Present" for row in attendance)
    attendance_rate = round(present_count / total_attendance * 100) if total_attendance else 0
    assignment_count = database.execute("SELECT COUNT(*) FROM assignments").fetchone()[0]
    return render_template(
        "main/dashboard.html",
        attendance_rate=attendance_rate,
        attendance_count=total_attendance,
        assignment_count=assignment_count,
    )


@bp.route("/profile", methods=("GET", "POST"))
@login_required
def profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        errors = []

        if not name or len(name) > 80:
            errors.append("Name is required and must be 80 characters or fewer.")
        if len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            errors.append("Enter a valid email address (maximum 254 characters).")
        if phone and not re.fullmatch(r"[0-9+() .-]{7,20}", phone):
            errors.append("Enter a valid phone number using 7 to 20 common phone characters.")

        existing = get_db().execute(
            "SELECT id FROM users WHERE email = ? AND id != ?", (email, g.user["id"])
        ).fetchone()
        if existing is not None:
            errors.append("That email address is already in use.")

        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            database = get_db()
            database.execute(
                "UPDATE users SET name = ?, email = ?, phone = ? WHERE id = ?",
                (name, email, phone, g.user["id"]),
            )
            database.commit()
            flash("Your profile has been updated.", "success")
            return redirect(url_for("main.profile"))

    refreshed_user = get_db().execute(
        "SELECT * FROM users WHERE id = ?", (g.user["id"],)
    ).fetchone()
    return render_template("main/profile.html", profile_user=refreshed_user)


@bp.route("/attendance")
@login_required
def attendance():
    records = get_db().execute(
        """
        SELECT course, attendance_date, status FROM attendance
        WHERE user_id = ? ORDER BY attendance_date DESC, id DESC
        """,
        (g.user["id"],),
    ).fetchall()
    return render_template("main/attendance.html", records=records)


@bp.route("/assignments")
@login_required
def assignments():
    records = get_db().execute(
        "SELECT * FROM assignments ORDER BY due_date, title"
    ).fetchall()
    return render_template("main/assignments.html", records=records)
