SELECT * FROM infractions
WHERE guild_id = :guild_id AND status = "pending"
ORDER BY timestamp DESC;