-- Create a user at the server 'localhost' and set the password as Auth123
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

-- Create a db 'auth'
CREATE DATABASE auth;

-- Give all permissions for all tables in auth database to the user: auth_user at the server: localhost
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- Switch the the auth db
USE auth;

-- Create a table: user
CREATE TABLE user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Insert a new user with email and password
INSERT INTO user (email, password) VALUES ('hayoun@email.com', 'Admin123')