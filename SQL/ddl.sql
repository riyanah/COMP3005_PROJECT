-- Members table
CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    fitness_goals TEXT
);

-- Trainers table
CREATE TABLE IF NOT EXISTS trainers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialization TEXT
);

-- Administrative Staff table
CREATE TABLE IF NOT EXISTS administrative_staff (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);


-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    capacity INTEGER NOT NULL
);

-- Room Bookings table
CREATE TABLE IF NOT EXISTS room_bookings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

-- Fitness Classes table
CREATE TABLE IF NOT EXISTS fitness_classes (
    id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    schedule TIMESTAMP NOT NULL
);

-- Class Registrations table
CREATE TABLE IF NOT EXISTS class_registrations (
    id SERIAL PRIMARY KEY,
    class_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    FOREIGN KEY (class_id) REFERENCES fitness_classes(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Trainer Availability table
CREATE TABLE IF NOT EXISTS trainer_availability (
    trainer_id INTEGER NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    PRIMARY KEY (trainer_id, date),
    FOREIGN KEY (trainer_id) REFERENCES trainers(id)
);

CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    last_maintenance DATE NOT NULL,
    maintenance_interval INTEGER NOT NULL
);

CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    amount_due DECIMAL(10, 2) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Unpaid',  
    FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    bill_id INTEGER NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (bill_id) REFERENCES bills(id)
);
