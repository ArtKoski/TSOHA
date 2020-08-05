CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE exercises(
    id SERIAL PRIMARY KEY,
    exercise TEXT UNIQUE,
    popularity INTEGER
);

CREATE TABLE trackedExercises(
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    user_id INTEGER REFERENCES users,
    visible INTEGER
);

CREATE TABLE exerciseVariables(
    id SERIAL PRIMARY KEY,
    trackedExercise_id INTEGER REFERENCES trackedExercises NOT NULL,
    setsTotal INTEGER,
    reps INTEGER,
    weight INTEGER,
    info TEXT,
    time TIMESTAMP
);

