UPDATE infractions
SET status = :status, approve_votes = :approve_votes, reject_votes = :reject_votes
WHERE id = :id;