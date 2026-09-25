UPDATE warframes_users_lookup
SET (user_id, warframe_id) = (
    (SELECT u.user_id
    FROM users u
    WHERE u.user_name LIKE :user_name),
    (SELECT w.warframe_id
    FROM warframes w
    WHERE w.warframe_name LIKE :new_warframe_name)
)
WHERE warframes_users_lookup.user_id = (
    SELECT u.user_id
    FROM users u
    WHERE u.user_name LIKE :user_name
)
AND warframes_users_lookup.warframe_id = (
    SELECT w.warframe_id
    FROM warframes w
    WHERE w.warframe_name LIKE :old_warframe_name
)