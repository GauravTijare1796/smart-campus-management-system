from tests.conftest import login


def test_student_can_view_dashboard_attendance_and_assignments(client):
    login(client)

    dashboard = client.get("/dashboard")
    attendance = client.get("/attendance")
    assignments = client.get("/assignments")

    assert b"80<span>%</span>" in dashboard.data
    assert b"Agile Software Engineering" in attendance.data
    assert b"Campus Service Blueprint" in assignments.data


def test_profile_can_be_updated(client):
    login(client)
    response = client.post(
        "/profile",
        data={
            "name": "Maya S.",
            "email": "maya.updated@campus.edu",
            "phone": "+91 98765 43210",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Your profile has been updated." in response.data
    assert b"maya.updated@campus.edu" in response.data


def test_profile_rejects_invalid_email_and_phone(client):
    login(client)
    response = client.post(
        "/profile",
        data={"name": "Maya Sharma", "email": "not-an-email", "phone": "abc"},
    )

    assert response.status_code == 200
    assert b"Enter a valid email address" in response.data
    assert b"Enter a valid phone number" in response.data


def test_profile_rejects_email_used_by_another_user(client):
    login(client)
    response = client.post(
        "/profile",
        data={
            "name": "Maya Sharma",
            "email": "arjun.patel@campus.edu",
            "phone": "9876543210",
        },
    )

    assert b"That email address is already in use." in response.data


def test_admin_dashboard_requires_admin_role(client):
    login(client)
    response = client.get("/admin/")
    assert response.status_code == 403

    client.post("/logout")
    login(client, identifier="admin", password="Admin123!")
    response = client.get("/admin/")
    assert b"Administration" in response.data
    assert b"Student accounts" in response.data


def test_private_pages_redirect_unauthenticated_visitors(client):
    response = client.get("/attendance")
    assert response.status_code == 302
    assert "/login?next=/attendance" in response.headers["Location"]
