import sqlite3
from pathlib import Path

from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db(app):
    with app.app_context():
        database = get_db()
        schema_path = Path(__file__).with_name("schema.sql")
        database.executescript(schema_path.read_text(encoding="utf-8"))

        if database.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            database.executemany(
                """
                INSERT INTO users
                    (student_number, username, name, email, password_hash,
                     role, department, year, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        "STU1001",
                        "maya",
                        "Maya Sharma",
                        "maya.sharma@campus.edu",
                        generate_password_hash("Student123!"),
                        "student",
                        "Computer Science",
                        3,
                        "9876543210",
                    ),
                    (
                        "STU1002",
                        "arjun",
                        "Arjun Patel",
                        "arjun.patel@campus.edu",
                        generate_password_hash("Student123!"),
                        "student",
                        "Information Technology",
                        2,
                        "9876501234",
                    ),
                    (
                        "ADMIN01",
                        "admin",
                        "Campus Administrator",
                        "admin@scms.local",
                        generate_password_hash("Admin123!"),
                        "admin",
                        "Administration",
                        None,
                        "",
                    ),
                ],
            )
            database.executemany(
                """
                INSERT INTO attendance (user_id, course, attendance_date, status)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (1, "Agile Software Engineering", "2026-11-02", "Present"),
                    (1, "Database Management Systems", "2026-11-03", "Present"),
                    (1, "Computer Networks", "2026-11-04", "Absent"),
                    (1, "Agile Software Engineering", "2026-11-09", "Present"),
                    (1, "Database Management Systems", "2026-11-10", "Present"),
                    (2, "Data Structures", "2026-11-02", "Present"),
                    (2, "Operating Systems", "2026-11-03", "Absent"),
                ],
            )
            database.executemany(
                """
                INSERT INTO assignments
                    (title, course, description, due_date, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        "Campus Service Blueprint",
                        "Agile Software Engineering",
                        "Submit a service blueprint for a campus process.",
                        "2026-11-24",
                        "In progress",
                    ),
                    (
                        "Relational Schema Design",
                        "Database Management Systems",
                        "Design and normalize a schema for a library system.",
                        "2026-11-28",
                        "Not started",
                    ),
                    (
                        "Routing Protocol Analysis",
                        "Computer Networks",
                        "Compare routing approaches using a short report.",
                        "2026-12-03",
                        "Submitted",
                    ),
                ],
            )
            database.commit()

        app.teardown_appcontext(close_db)
