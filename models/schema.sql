-- -- Admins Table
-- CREATE TABLE IF NOT EXISTS admins (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL
-- );

-- -- Students Table
-- -- Students Table
-- CREATE TABLE IF NOT EXISTS students (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     student_id TEXT UNIQUE NOT NULL,
--     name TEXT NOT NULL,
--     face_encoding BLOB  -- removed NOT NULL, face added later during enrollment
-- );

-- -- Sessions Table
-- CREATE TABLE IF NOT EXISTS sessions (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     session_name TEXT NOT NULL,
--     start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
--     end_time DATETIME,
--     is_active BOOLEAN DEFAULT 1
-- );

-- -- Attendance Table
-- CREATE TABLE IF NOT EXISTS attendance (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     session_id INTEGER NOT NULL,
--     student_id TEXT NOT NULL,
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (session_id) REFERENCES sessions(id),
--     FOREIGN KEY (student_id) REFERENCES students(student_id)
-- );



-- Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    face_encoding BLOB  -- removed NOT NULL, face added later during enrollment
);

-- Sessions Table
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    student_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);