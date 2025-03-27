CREATE TABLE IF NOT EXISTS accounts.device (
    id UUID PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_id UUID REFERENCES accounts.user(id) NOT NULL,
    device_id VARCHAR(256) NOT NULL,
    fcm_token VARCHAR(256) NOT NULL,
    type VARCHAR(50) NOT NULL,
    os_version VARCHAR(50) NOT NULL,
    app_version VARCHAR(50) NOT NULL,
    locale VARCHAR(50) NOT NULL,
    screen_resolution VARCHAR(50) NOT NULL
);
ALTER TABLE accounts.session ADD COLUMN device_id UUID REFERENCES accounts.device(id) NULL;
