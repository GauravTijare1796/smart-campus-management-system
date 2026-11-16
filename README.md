# Smart Campus Management System

A small Flask and SQLite campus portal demo for an Agile Software Engineering practical. It includes student sign-in, a student dashboard, profile editing, attendance and assignment views, and a role-protected admin overview.

## Features

- Student login and logout with Werkzeug password hashing
- Student dashboard with attendance and coursework summary cards
- Validated profile editing with unique email addresses
- Attendance records scoped to the signed-in student
- Assignment listing
- Basic admin dashboard and student directory
- Parameterized SQLite queries and seeded demo data
- Pytest coverage, Docker image, and Jenkins install/test/build pipeline

## Demo accounts

| Role | Username | Password |
|---|---|---|
| Student | `maya` | `Student123!` |
| Student | `arjun` | `Student123!` |
| Admin | `admin` | `Admin123!` |

These are demo-only credentials. Change them and set a strong `SCMS_SECRET_KEY` before using this application beyond a local practical. This project is not intended as a production identity or campus-record system.

## Run locally

Python 3.10 or later is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m flask --app app run --debug
```

Open <http://127.0.0.1:5000>. The app creates `instance/scms.sqlite3` and inserts the sample records on first start. The `SCMS_DATABASE` environment variable can point to a different SQLite file. The default development secret key must be replaced with `SCMS_SECRET_KEY` for any deployment.

## Run tests

```powershell
python -m pytest -q
```

The tests use an isolated temporary database and do not alter the local demo database.

## Run with Docker

Build and start the container:

```powershell
docker build -t scms-demo .
docker run --rm -p 5000:5000 -e SCMS_SECRET_KEY="replace-with-a-long-random-secret" -v scms-data:/data scms-demo
```

Open <http://127.0.0.1:5000>. The named Docker volume persists the SQLite database under `/data`. Docker must be installed and its daemon running; access to the Docker daemon may require administrator or Docker-group permissions. The image serves the app with Waitress.

## Jenkins pipeline

The `Jenkinsfile` installs `requirements.txt`, runs pytest, then builds a Docker image tagged `scms-demo:${BUILD_NUMBER}`. A Jenkins agent needs Python 3, pip, pytest dependencies, and permission to access a running Docker daemon. This repository does not claim that Jenkins has run the pipeline.
