-- ========================================================
-- SignSpeak PostgreSQL Relational Database Schema DDL
-- ========================================================

CREATE TABLE IF NOT EXISTS vocabulary_signs (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(32) NOT NULL UNIQUE,
    label VARCHAR(64) NOT NULL,
    category VARCHAR(32) NOT NULL,
    description TEXT,
    tips TEXT,
    image_url VARCHAR(256),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc') NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_vocabulary_signs_symbol ON vocabulary_signs(symbol);
CREATE INDEX IF NOT EXISTS idx_vocabulary_signs_category ON vocabulary_signs(category);

CREATE TABLE IF NOT EXISTS recognition_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(64),
    predicted_sign VARCHAR(32) NOT NULL,
    confidence REAL NOT NULL,
    latency_ms REAL NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc') NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_recognition_logs_session_id ON recognition_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_recognition_logs_predicted_sign ON recognition_logs(predicted_sign);

CREATE TABLE IF NOT EXISTS translation_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    translated_text TEXT NOT NULL,
    total_gestures INTEGER DEFAULT 0 NOT NULL,
    avg_confidence REAL DEFAULT 0.0 NOT NULL,
    duration_seconds REAL DEFAULT 0.0 NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc') NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_translation_sessions_session_id ON translation_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_translation_sessions_created_at ON translation_sessions(created_at DESC);
