CREATE TABLE users
(
   id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    username VARCHAR(15) NOT NULL UNIQUE,
    password VARCHAR(20) NOT NULL
);

INSERT INTO users
    (name, email, username, password)
VALUES
    ('Abby', 'prican1011@gmail.com', 'Asanti1011', 'Pickles1011!'),
    ('Britt', 'britt121@gmail.com', 'BrittBratt', 'LoveWins'),
    ('John Doe', 'made_up@yahoo.com', 'MadeUp', 'merp123456');

    