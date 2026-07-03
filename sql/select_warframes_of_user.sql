SELECT w.warframe_name
FROM warframes w
WHERE w.warframe_id IN (
    SELECT wul.warframe_id
    FROM warframes_users_lookup wul
    JOIN users u ON
        wul.user_id = u.user_id
    WHERE u.user_name LIKE :user_name
)
ORDER BY w.warframe_name