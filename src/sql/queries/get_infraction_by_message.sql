SELECT *
FROM infractions
WHERE
message_id = :message_id AND status = "pending";