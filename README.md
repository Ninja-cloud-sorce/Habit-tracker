# Habit-tracker

MySQL Code :
DROP DATABASE IF EXISTS habit_tracker;
CREATE DATABASE habit_tracker;
USE habit_tracker;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE habits (
    habit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE completions (
    completion_id INT AUTO_INCREMENT PRIMARY KEY,
    habit_id INT,
    completion_date DATE NOT NULL,
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
);
