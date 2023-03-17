DROP DATABASE IF EXISTS gym_buddy;

CREATE DATABASE gym_buddy;

\c gym_buddy

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users
    (name, email, username, password)
VALUES
    ('Abby', 'prican1011@gmail.com', 'Asanti1011', 'Pickles1011!'),
    ('Britt', 'britt121@gmail.com', 'BrittBratt', 'LoveWins'),
    ('John Doe', 'made_up@yahoo.com', 'MadeUp', 'merp123456');

    