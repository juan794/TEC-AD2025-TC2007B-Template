CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin' NOT NULL,
    doctor_id INT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    specialty VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    user_id INT DEFAULT NULL
);

INSERT INTO users(name, email, password, role)
VALUES
    ('Dr. Alice Johnson', 'alice.johnson@example.com', 'doctor', 'doctor'),
    ('Dr. Bob Williams', 'bob.williams@example.com', 'doctor', 'doctor'),
    ('Dr. Carol Davis', 'carol.davis@example.com', 'doctor', 'doctor');

INSERT INTO doctors(user_id, specialty)
SELECT id, 'General Professional' FROM users WHERE role = 'doctor';

INSERT INTO appointments(doctor_id, appointment_date, appointment_time)
SELECT d.id, CURRENT_DATE + (i || ' days')::interval AS appointment_date, 
    (i % 8 + 9 || ':00:00')::time AS appointment_time
FROM doctors d, generate_series(1, 10) AS i;

INSERT INTO users(name, email, password, role)
VALUES ('Administrator', 'admin@example.com', 'admin', 'admin');