DELETE FROM warframes_users_lookup
WHERE warframes_users_lookup.user_id = (
    SELECT u.user_id
    FROM users u
    WHERE u.user_name LIKE :user_name
)