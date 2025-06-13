UPDATE infractions
SET approve_votes = :approve_votes, 
    reject_votes = :reject_votes
WHERE id = :infraction_id;