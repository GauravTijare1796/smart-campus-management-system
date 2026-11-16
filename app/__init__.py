import os
from pathlib import Path

from flask import Flask

from app.db import init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SCMS_SECRET_KEY", "change-this-secret-key"),
        DATABASE=os.environ.get(
            "SCMS_DATABASE",
            str(Path(app.instance_path) / "scms.sqlite3"),
        ),
    )

    if test_config is not None:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    init_db(app)

    from app.routes import admin, auth, main

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    return app
