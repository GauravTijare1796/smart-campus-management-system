import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, identifier="maya", password="Student123!"):
    return client.post(
        "/login",
        data={"identifier": identifier, "password": password},
        follow_redirects=True,
    )
