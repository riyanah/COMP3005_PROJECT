from prettytable import PrettyTable
from datetime import datetime
from db import create_tables, get_db
from models import Member, Trainer, AdministrativeStaff
import psycopg2

# helpers

def is_valid_date(date_string):
    """Check if the date_string is in the YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def insert_default_rooms():
    db = get_db()
    cursor = db.cursor()
    # Check if the rooms table is empty and insert default rooms if it is
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:  # No rooms present
        rooms = [
            ('Yoga Studio', 20),
            ('Weight Room', 15),
            ('Cardio Room', 10),
        ]
        cursor.executemany("INSERT INTO rooms (name, capacity) VALUES (%s, %s)", rooms)
        db.commit()
        print("Default rooms inserted.")
    else:
        print("Default rooms already present.")

# administrative staff 
def manage_room_booking():
    db = get_db()
    cursor = db.cursor()
    
    # Optional
    insert_default_rooms()

    # Fetch and display all rooms
    print("Fetching available rooms...")
    cursor.execute("SELECT id, name, capacity FROM rooms ORDER BY id ASC")
    rooms = cursor.fetchall()
    
    if rooms:
        print("\nAvailable Rooms:")
        room_table = PrettyTable()
        room_table.field_names = ["Room ID", "Name", "Capacity"]
        for room in rooms:
            room_table.add_row([room[0], room[1], room[2]])
        print(room_table)
    else:
        print("No available rooms to book.")
        return

    # Prompt the user to enter a Room ID from the list
    room_id = input("Enter the Room ID from the list above to book: ")
    date = input("Date (YYYY-MM-DD): ")
    start_time = input("Start Time (HH:MM): ")
    end_time = input("End Time (HH:MM): ")
    
    try:
        cursor.execute("""
        INSERT INTO room_bookings (room_id, date, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        """, (room_id, date, start_time, end_time))
        db.commit()
        print("Room booked successfully.")
    except psycopg2.Error as e:
        db.rollback()  # Roll back in case of any error
        print(f"Failed to book the room: {e}")
    
def display_member_dashboard(member_id):
    db = get_db()
    cursor = db.cursor()
    
    # Fetch member's personal training sessions
    cursor.execute("""
    SELECT session_date, start_time, duration_minutes, (SELECT name FROM trainers WHERE id = trainer_id)
    FROM personal_training_sessions
    WHERE member_id = %s
    ORDER BY session_date ASC, start_time ASC
    """, (member_id,))
    sessions = cursor.fetchall()
    
    session_table = PrettyTable()
    session_table.field_names = ["Session Date", "Start Time", "Duration (Minutes)", "Trainer"]
    for session in sessions:
        session_table.add_row([session[0], session[1].strftime("%H:%M"), session[2], session[3]])
    
    print(f"Personal Training Sessions for Member ID {member_id}:")
    print(session_table)

def generate_bill(member_id, session_cost):
    db = get_db()
    cursor = db.cursor()
    # Generate a new bill
    cursor.execute("""
        INSERT INTO bills (member_id, amount_due, due_date)
        VALUES (%s, %s, CURRENT_DATE + INTERVAL '30 days')
        RETURNING id;
    """, (member_id, session_cost))
    bill_id = cursor.fetchone()[0]
    db.commit()
    print(f"Bill generated successfully with Bill ID: {bill_id} and Amount Due: ${session_cost}")
    return bill_id


def schedule_training_session(member_id):
    db = get_db()
    cursor = db.cursor()
    
    # Display available trainers
    cursor.execute("SELECT id, name, specialization FROM trainers")
    trainers = cursor.fetchall()
    if trainers:
        print("\nAvailable Trainers:")
        trainer_table = PrettyTable()
        trainer_table.field_names = ["Trainer ID", "Name", "Specialization"]
        for trainer in trainers:
            trainer_table.add_row([trainer[0], trainer[1], trainer[2]])
        print(trainer_table)
    else:
        print("No trainers available.")
        return

    # Select a trainer
    trainer_id = input("Enter the Trainer ID you wish to schedule with: ")
    date = input("Enter date for session (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")
    duration_minutes = int(input("Enter the duration of the session in minutes: "))

    # Calculate the time interval for duration
    end_time = f"{start_time} + interval '{duration_minutes} minutes'"

    cursor.execute("""
        SELECT * FROM trainer_availability
        WHERE trainer_id = %s AND date = %s AND start_time <= %s::time AND end_time >= %s::time + interval '%s minutes'
    """, (trainer_id, date, start_time, start_time, duration_minutes))
    if cursor.fetchone():
        # Trainer is available, schedule the session
        cursor.execute("""
            INSERT INTO personal_training_sessions (member_id, trainer_id, session_date, start_time, duration_minutes)
            VALUES (%s, %s, %s, %s, %s)
        """, (member_id, trainer_id, date, start_time, duration_minutes))
        db.commit()
        print("Training session scheduled successfully.")

        session_cost = 50  
        bill_id = generate_bill(member_id, session_cost)
        payment_amount = float(input("Enter the amount to pay now: "))
        process_payment(member_id, bill_id, payment_amount)
        confirm_transaction(bill_id)

    else:
        print("Trainer is not available at this time. Please try a different time or trainer.")




def add_member():
    print("Add a new member")
    name = input("Name: ")
    email = input("Email: ")
    
    date_of_birth = ""
    while True:
        date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
        if is_valid_date(date_of_birth):
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    # Ask for weight change goal and time frame
    weight_change = input("Goal Weight Change (in lbs, use + or - sign): ")  # Example: -10 or +5
    time_frame = input("Time Frame (in days): ")  # Example: 90 days
    
    # Formulate fitness goals in a structured string
    fitness_goals = f"{weight_change} lbs in {time_frame} days"
    
    member = Member(name, email, date_of_birth, fitness_goals)
    
    try:
        member.save()
    except Exception as e:
        print(f"An error occurred: {e}")

def add_trainer():
    print("Add a new trainer")
    name = input("Trainer Name: ")
    specialization = input("Specialization: ")
    
    trainer = Trainer(name=name, specialization=specialization)
    
    try:
        trainer.save()
        print("Trainer added successfully.")
    except Exception as e:
        print(f"An error occurred while adding the trainer: {e}")


def add_admin_staff():
    print("Add a new administrative staff member")
    name = input("Staff Name: ")
    position = input("Position: ")
    
    admin_staff = AdministrativeStaff(name=name, position=position)
    
    try:
        admin_staff.save()
        print("Administrative staff added successfully.")
    except Exception as e:
        print(f"An error occurred while adding the administrative staff: {e}")


def update_member_profile():
    print("Update Member Profile")
    member_id = input("Member ID: ")
    new_email = input("New Email (leave blank to keep current): ")
    
    # Update fitness goals in structured format
    new_weight_change = input("New Goal Weight Change (in lbs, use + or - sign, leave blank to keep current): ")
    new_time_frame = input("New Time Frame (in days, leave blank to keep current): ")
    
    if new_weight_change and new_time_frame:
        new_fitness_goals = f"{new_weight_change} lbs in {new_time_frame} days"
    else:
        new_fitness_goals = ""
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE members SET email = COALESCE(NULLIF(%s, ''), email), fitness_goals = COALESCE(NULLIF(%s, ''), fitness_goals) WHERE id = %s",
                   (new_email, new_fitness_goals, member_id))
    db.commit()
    print("Profile updated successfully.")


def view_member_profile():
    print("View Member Profile")
    member_name = input("Enter Member Name: ")
    # Retrieve and display member profile from the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, date_of_birth, fitness_goals FROM members WHERE name = %s", (member_name,))
    member = cursor.fetchone()
    if member:
        print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Date of Birth: {member[3]}, Fitness Goals: {member[4]}")
    else:
        print("Member not found.")

def list_members():
    db = get_db()
    cursor = db.cursor()
    
    print("Fetching list of members...")
    cursor.execute("SELECT id, name, email, date_of_birth, fitness_goals FROM members ORDER BY id ASC")
    members = cursor.fetchall()
    
    if members:
        print("\nList of Members:")
        member_table = PrettyTable()
        member_table.field_names = ["Member ID", "Name", "Email", "Date of Birth", "Fitness Goals"]
        for member in members:
            member_table.add_row([member[0], member[1], member[2], member[3], member[4]])
        print(member_table)
    else:
        print("No members found.")


def list_trainers():
    db = get_db()
    cursor = db.cursor()
    
    print("Fetching list of trainers...")
    cursor.execute("SELECT id, name, specialization FROM trainers ORDER BY id ASC")
    trainers = cursor.fetchall()
    
    if trainers:
        print("\nList of Trainers:")
        trainer_table = PrettyTable()
        trainer_table.field_names = ["Trainer ID", "Name", "Specialization"]
        for trainer in trainers:
            trainer_table.add_row([trainer[0], trainer[1], trainer[2]])
        print(trainer_table)
    else:
        print("No trainers found.")

def list_administrative_staff():
    db = get_db()
    cursor = db.cursor()
    
    
    print("Fetching list of all administrative staff...")
    cursor.execute("SELECT id, name, position, email FROM administrative_staff ORDER BY id ASC")
    staff = cursor.fetchall()
    
    if staff:
        print("\nList of Administrative Staff:")
        staff_table = PrettyTable()
        staff_table.field_names = ["Staff ID", "Name", "Position", "Email"]
        for person in staff:
            staff_table.add_row([person[0], person[1], person[2], person[3]])
        print(staff_table)
    else:
        print("No administrative staff found.")

def process_payment(member_id, bill_id, payment_amount):
    db = get_db()
    cursor = db.cursor()
    # Record payment
    cursor.execute("""
        INSERT INTO payments (bill_id, member_id, amount, payment_date)
        VALUES (%s, %s, %s, CURRENT_DATE)
    """, (bill_id, member_id, payment_amount))
    db.commit()
    print("Payment processed successfully.")


def confirm_transaction(bill_id):
    db = get_db()
    cursor = db.cursor()
    # Update the bill status to paid
    cursor.execute("""
        UPDATE bills SET status = 'Paid'
        WHERE id = %s;
    """, (bill_id,))
    db.commit()
    print(f"Transaction confirmed for Bill ID: {bill_id}.")



def main():
    create_tables()  
    while True:
        print("\nFitness Club Management System")
        print("1. Add Member (User Registration)")
        print("2. Add Trainer")
        print("3. Add Administrative Staff")
        print("4. Manage Room Booking")
        print("5. Display Member Dashboard")
        print("6. Set Trainer Availability")
        print("7. Update Member Profile (Profile Management)")
        print("8. View Member Profile (Search by Member's Name)")
        print("9. Schedule Training Session")
        print("10. Process Payment")
        print("11. Confirm Transaction")
        print("12. List all Members")
        print("13. List all Trainers")
        print("14. List all Administrative Staff")
        print("15. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            add_member()
        elif choice == '2':
            add_trainer()
        elif choice == '3':
            add_admin_staff()
        elif choice == '4':
            manage_room_booking()
        elif choice == '5':
            member_id = input("Enter Member ID: ")
            display_member_dashboard(member_id)
        elif choice == '6':
            trainer_id = input("Enter Trainer ID: ")
            set_trainer_availability(trainer_id)
        elif choice == '7':
            update_member_profile()
        elif choice == '8':
            view_member_profile()
        elif choice == '9':
            member_id = input("Enter Member ID to schedule a session: ")
            schedule_training_session(member_id)
        elif choice == '10':
            member_id = input("Enter Member ID for payment: ")
            amount = float(input("Enter the amount to be paid: "))
            process_payment(member_id, amount)
        elif choice == '11':
            member_id = input("Enter Member ID to confirm transaction: ")
            confirm_transaction(member_id)
        elif choice == '12':
            list_members()
        elif choice == '13':
            list_trainers()
        elif choice == '14':
            list_administrative_staff()
        elif choice == '15':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
