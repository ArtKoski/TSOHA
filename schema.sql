CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    exercise TEXT UNIQUE,
    popularity INTEGER
);