INSERT INTO infractions (
    id, guild_id, target_user_id, target_username, reporter_id,
    reporter_username, reason, channel_id, message_id, timestamp,
    status, end_time)
    VALUES 
    (:id, :guild_id, :target_user_id, :target_username, :reporter_id,
    :reporter_username, :reason, :channel_id, :message_id, :timestamp, :status, 
    :end_time);