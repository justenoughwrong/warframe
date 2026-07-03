CREATE TABLE IF NOT EXISTS warframes (
    warframe_id integer PRIMARY KEY,
    warframe_name varchar(20) NOT NULL UNIQUE
)