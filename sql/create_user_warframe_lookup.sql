CREATE TABLE IF NOT EXISTS warframes_users_lookup (
    user_id integer,
    warframe_id integer,
    PRIMARY KEY (user_id, warframe_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (warframe_id) REFERENCES warframes(warframe_id)
)