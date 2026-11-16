from flask import Blueprint, render_template

from app.auth import admin_required
from app.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@admin_required
def dashboard():
    database = get_db()
    student_count = database.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'student'"
    ).fetchone()[0]
    attendance_count = database.execute(
        "SELECT COUNT(*) FROM attendance"
    ).fetchone()[0]
    assignment_count = database.execute(
        "SELECT COUNT(*) FROM assignments"
    ).fetchone()[0]
    students = database.execute(
        """
        SELECT student_number, name, email, department, year
        FROM users WHERE role = 'student' ORDER BY name
        """
    ).fetchall()
    return render_template(
        "admin/dashboard.html",
        student_count=student_count,
        attendance_count=attendance_count,
        assignment_count=assignment_count,
        students=students,
    )
