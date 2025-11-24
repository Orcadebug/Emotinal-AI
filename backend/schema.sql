CREATE TABLE IF NOT EXISTS biological_state (
    id SERIAL PRIMARY KEY,
    adenosine FLOAT DEFAULT 0.0,
    circadian_rhythm FLOAT DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS relationships (
    user_id VARCHAR(255) PRIMARY KEY,
    affinity FLOAT DEFAULT 0.0,
    interaction_count INT DEFAULT 0,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    message TEXT,
    response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    emotional_valence FLOAT DEFAULT 0.0
);
