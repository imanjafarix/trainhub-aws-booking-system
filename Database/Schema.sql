CREATE DATABASE IF NOT EXISTS trainhub;

USE trainhub;

-- Members table
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training sessions
CREATE TABLE training_passes (
    pass_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    trainer VARCHAR(100),
    session_time DATETIME NOT NULL,
    max_slots INT NOT NULL,
    booked_slots INT DEFAULT 0
);

-- Bookings table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    pass_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (pass_id) REFERENCES training_passes(pass_id),

    UNIQUE(member_id, pass_id)
);
