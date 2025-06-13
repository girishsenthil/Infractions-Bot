SELECT id, reason, reporter_username, reporter_id, timestamp
FROM infractions
WHERE guild_id = :guild_id 
AND target_user_id = :user_id 
AND status = "approved"
ORDER BY timestamp DESC;