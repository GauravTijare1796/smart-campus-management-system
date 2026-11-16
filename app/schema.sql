CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin')),
    department TEXT NOT NULL,
    year INTEGER,
    phone TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    course TEXT NOT NULL,
    attendance_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Present', 'Absent'))
);

CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    course TEXT NOT NULL,
    description TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Not started', 'In progress', 'Submitted'))
);
