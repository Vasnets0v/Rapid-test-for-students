CREATE TABLE IF NOT EXISTS admins (
    id integer PRIMARY KEY AUTOINCREMENT,
    email varchar(64) NOT NULL UNIQUE,
    name varchar(64) NOT NULL,
    surname varchar(64) NOT NULL,
    password varchar(512) NOT NULL,
    created integer NOT NULL
);