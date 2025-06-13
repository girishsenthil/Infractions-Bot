SELECT target_user_id, target_username, COUNT(*) as count
FROM infractions
WHERE guild_id = :guild_id AND status = "approved"
GROUP BY target_user_id, target_username
ORDER BY count DESC
LIMIT :limit;

