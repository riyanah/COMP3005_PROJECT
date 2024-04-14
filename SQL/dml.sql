-- Insert sample members
INSERT INTO members (name, email, date_of_birth, fitness_goals) VALUES
('Apple John', 'apple.john@example.com', '1980-04-01', 'Increase strength'),
('Bob Smith', 'bob.smith@example.com', '1990-08-15', 'Improve cardiovascular health');

-- Insert sample trainers
INSERT INTO trainers (name, specialization) VALUES
('Alex Johnson', 'Strength training'),
('Samantha Lee', 'Cardiovascular fitness');

-- Insert sample administrative staff
INSERT INTO administrative_staff (name, position, email) VALUES
('Michael Brown', 'Club Manager', 'michael.brown@example.com'),
('Sarah Connor', 'Reception Manager', 'sarah.connor@example.com');

-- Insert sample rooms
INSERT INTO rooms (name, capacity) VALUES
('Yoga Studio', 20),
('Weight Room', 15),
('Cardio Room', 10);

-- Insert sample fitness classes
INSERT INTO fitness_classes (class_name, schedule) VALUES
('Morning Yoga', '2024-01-01 08:00:00'),
('Evening Weights', '2024-01-01 18:00:00');

-- Insert sample equipment
INSERT INTO equipment (name, last_maintenance, maintenance_interval) VALUES
('Treadmill', '2023-12-01', 90),
('Elliptical Machine', '2023-12-15', 60);

-- Insert sample room bookings
INSERT INTO room_bookings (room_id, date, start_time, end_time) VALUES
(1, '2024-01-01', '09:00:00', '10:00:00'),
(2, '2024-01-01', '10:00:00', '11:00:00');

-- Insert sample class registrations
INSERT INTO class_registrations (class_id, member_id) VALUES
(1, 1),
(2, 2);

-- Insert sample trainer availability
INSERT INTO trainer_availability (trainer_id, date, start_time, end_time) VALUES
(1, '2024-01-02', '08:00:00', '12:00:00'),
(2, '2024-01-02', '14:00:00', '18:00:00');
