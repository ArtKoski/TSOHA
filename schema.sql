CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE exercises(
    id SERIAL PRIMARY KEY,
    exercise TEXT UNIQUE NOT NULL,
    popularity INTEGER
);

CREATE TABLE trackedExercises(
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises NOT NULL,
    user_id INTEGER REFERENCES users NOT NULL,
    UNIQUE (exercise_id, user_id),
    visible INTEGER
);

CREATE TABLE exerciseVariables(
    id SERIAL PRIMARY KEY,
    trackedExercise_id INTEGER REFERENCES trackedExercises NOT NULL,
    setsTotal INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight NUMERIC NOT NULL,
    info TEXT,
    time DATE DEFAULT CURRENT_DATE
);

