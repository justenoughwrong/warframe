SELECT u.user_name
FROM users u
WHERE u.user_id IN (
    SELECT wul.user_id
    FROM warframes_users_lookup wul
    JOIN warframes w ON
        wul.warframe_id = w.warframe_id
    WHERE w.warframe_name LIKE :warframe_name
)
ORDER BY u.user_name