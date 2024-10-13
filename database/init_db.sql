CREATE DATABASE IF NOT EXISTS email_server;
USE email_server;

CREATE TABLE IF NOT EXISTS bal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bal_id INT,
    title VARCHAR(255),
    content TEXT,
    sender_id INT,
    FOREIGN KEY (bal_id) REFERENCES bal(id) ON DELETE CASCADE
);
