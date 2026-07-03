CREATE TABLE IF NOT EXISTS users (
    user_id integer PRIMARY KEY,
    user_name varchar(24) NOT NULL UNIQUE
)