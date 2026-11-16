from tests.conftest import login


def test_student_can_login_with_username_or_student_number(client):
    response = login(client)
    assert response.status_code == 200
    assert b"Good to see you, Maya." in response.data

    client.post("/logout")
    response = login(client, identifier="STU1001")
    assert response.status_code == 200
    assert b"Good to see you, Maya." in response.data


def test_invalid_login_does_not_create_authenticated_session(client):
    response = client.post(
        "/login",
        data={"identifier": "maya", "password": "incorrect"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid login details" in response.data
    assert b"Sign in with your campus account" in response.data


def test_login_requires_both_fields(client):
    response = client.post(
        "/login", data={"identifier": "", "password": ""}, follow_redirects=True
    )
    assert b"Enter your campus username or email and password." in response.data


def test_logout_clears_session(client):
    login(client)
    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out." in response.data
    assert b"Sign in with your campus account" in response.data
