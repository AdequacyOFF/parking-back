CREATE TABLE IF NOT EXISTS accounts.user (
    id UUID PRIMARY KEY,
    phone_number VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NULL,
    last_name VARCHAR(50) NULL
);
CREATE INDEX IF NOT EXISTS phone_number_idx ON accounts.user USING btree(phone_number);


CREATE TABLE IF NOT EXISTS accounts.session (
    id UUID PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_id UUID REFERENCES accounts.user(id) NOT NULL,
    status VARCHAR(30) NOT NULL,
    token TEXT NOT NULL,
    expired_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS status_expired_dt_idx ON accounts.session USING btree(status, expired_at);
