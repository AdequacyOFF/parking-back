CREATE TYPE sex_type AS ENUM ('MALE', 'FEMALE');

CREATE TABLE IF NOT EXISTS accounts.user (
    id UUID PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    phone_number VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NULL,
    last_name VARCHAR(50) NULL,
    middle_name VARCHAR(50) NULL,
    sex sex_type NULL,
    birth_date DATE NULL,
    user_agreement BOOLEAN NOT NULL DEFAULT FALSE,
    privacy_policy BOOLEAN NOT NULL DEFAULT FALSE,
    company_rules BOOLEAN NOT NULL DEFAULT FALSE
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
