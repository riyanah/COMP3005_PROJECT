import psycopg2
import psycopg2.extras

DATABASE_NAME = "FitnessClubManagementSystem"
USER = "user2"
PASSWORD = "postgres"
HOST = "localhost"

def get_db():
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST)
    return conn

def create_tables():
    members_table = """
    CREATE TABLE IF NOT EXISTS members (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        date_of_birth DATE NOT NULL,
        fitness_goals TEXT
    )"""

    trainers_table = """
    CREATE TABLE IF NOT EXISTS trainers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        specialization TEXT
    )"""

    administrative_staff_table = """
    CREATE TABLE IF NOT EXISTS administrative_staff (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        position VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    )"""

    rooms_table = """
    CREATE TABLE IF NOT EXISTS rooms (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        capacity INTEGER NOT NULL
    )"""

    room_bookings_table = """
    CREATE TABLE IF NOT EXISTS room_bookings (
        id SERIAL PRIMARY KEY,
        room_id INTEGER NOT NULL,
        date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms(id)
    )"""

    fitness_classes_table = """
    CREATE TABLE IF NOT EXISTS fitness_classes (
        id SERIAL PRIMARY KEY,
        class_name VARCHAR(255) NOT NULL,
        schedule TIMESTAMP NOT NULL
    )"""

    class_registrations_table = """
    CREATE TABLE IF NOT EXISTS class_registrations (
        id SERIAL PRIMARY KEY,
        class_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        FOREIGN KEY (class_id) REFERENCES fitness_classes(id),
        FOREIGN KEY (member_id) REFERENCES members(id)
    )"""

    personal_training_sessions_table = """
    CREATE TABLE IF NOT EXISTS personal_training_sessions (
        id SERIAL PRIMARY KEY,
        member_id INTEGER NOT NULL,
        trainer_id INTEGER NOT NULL,
        session_date DATE NOT NULL,
        start_time TIME NOT NULL, 
        duration_minutes INTEGER NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (trainer_id) REFERENCES trainers(id)
    )"""

    equipment_table = """
    CREATE TABLE IF NOT EXISTS equipment (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        last_maintenance DATE NOT NULL,
        maintenance_interval INTEGER NOT NULL
    )"""

    tables = [members_table, trainers_table, administrative_staff_table, rooms_table, room_bookings_table, fitness_classes_table, class_registrations_table, personal_training_sessions_table, equipment_table]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    db.commit()

if __name__ == "__main__":
    create_tables()