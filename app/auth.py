from functools import wraps

from flask import g, redirect, request, session, url_for

from app.db import get_db


def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = (
        get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user_id is not None
        else None
    )


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(**kwargs):
        if g.user["role"] != "admin":
            from flask import abort

            abort(403)
        return view(**kwargs)

    return wrapped_view
