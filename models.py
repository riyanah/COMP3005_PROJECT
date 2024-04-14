from db import get_db
import psycopg2

class Member:
    def __init__(self, name, email, date_of_birth, fitness_goals):
        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.fitness_goals = fitness_goals
    
    def save(self):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO members (name, email, date_of_birth, fitness_goals)
                VALUES (%s, %s, %s, %s) RETURNING id
                """, (self.name, self.email, self.date_of_birth, self.fitness_goals))
            member_id = cursor.fetchone()[0]
            db.commit()
            print(f"Member ID {member_id} added successfully.")
        except psycopg2.errors.UniqueViolation:
            db.rollback()  # If the email already exists, rollback the transaction
            print("Error: This email is already registered.")
        except Exception as e:
            db.rollback() 
            print(f"An error occurred: {e}")
class Trainer:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.trainer_id = None  # This will be set when the trainer is saved to the database

    def save(self):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO trainers (name, specialization)
                VALUES (%s, %s) RETURNING id
                """, (self.name, self.specialization))
            self.trainer_id = cursor.fetchone()[0]
            db.commit()
            print(f"Trainer ID {self.trainer_id} added successfully.")
        except Exception as e:
            db.rollback()
            print(f"An error occurred: {e}")

    def set_trainer_availability():
        print("Set Trainer Availability")
        trainer_id = input("Select Trainer ID: ")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name, specialization FROM trainers WHERE id = %s", (trainer_id,))
        trainer_data = cursor.fetchone()

        if trainer_data:
            trainer = Trainer(name=trainer_data[0], specialization=trainer_data[1])
            date = input("Date (YYYY-MM-DD): ")
            start_time = input("Start Time (HH:MM): ")
            end_time = input("End Time (HH:MM): ")

            trainer.trainer_id = trainer_id  # Assigning ID to the instance
            trainer.set_availability(date, start_time, end_time)
        else:
            print("Trainer not found.")



class AdministrativeStaff:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def save(self):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO administrative_staff (name, position)
                VALUES (%s, %s) RETURNING id
                """, (self.name, self.position))
            self.staff_id = cursor.fetchone()[0]
            db.commit()
            print(f"Administrative Staff ID {self.staff_id} added successfully.")
        except Exception as e:
            db.rollback()
            print(f"An error occurred: {e}")

    def manage_room_booking(self, room_id, date, start_time, end_time):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO room_bookings (room_id, date, start_time, end_time)
                VALUES (%s, %s, %s, %s)
                """, (room_id, date, start_time, end_time))
            db.commit()
            print("Room booked successfully.")
        except psycopg2.Error as e:
            db.rollback()
            print(f"Failed to book the room: {e}")

    def update_class_schedule(self, class_id, new_schedule):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE fitness_classes SET schedule = %s WHERE id = %s", (new_schedule, class_id))
            db.commit()
            print("Class schedule updated successfully.")
        except Exception as e:
            db.rollback()
            print(f"Failed to update class schedule: {e}")