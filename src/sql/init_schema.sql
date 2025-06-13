PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS guild (
    guild_id INTEGER PRIMARY KEY,
    vote_duration INTEGER DEFAULT 300,
    required_votes INTEGER DEFAULT 3,
    approval_threshold REAL DEFAULT 0.6,
    moderator_role_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS infractions (
    id TEXT PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    target_user_id INTEGER NOT NULL,
    target_username TEXT NOT NULL,
    reporter_id INTEGER NOT NULL,
    reporter_username TEXT NOT NULL,
    reason TEXT NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER,
    timestamp DATETIME NOT NULL,
    status TEXT NOT NULL,
    approve_votes INTEGER DEFAULT 0,
    reject_votes INTEGER DEFAULT 0,
    end_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES guild(guild_id) ON DELETE CASCADE

);



CREATE INDEX IF NOT EXISTS idx_infractions_guild_user
ON infractions(guild_id, target_user_id);

CREATE INDEX IF NOT EXISTS idx_guild_user_timestamp
ON infractions(guild_id, target_user_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_infractions_status_timestamp
ON infractions(status, timestamp);
