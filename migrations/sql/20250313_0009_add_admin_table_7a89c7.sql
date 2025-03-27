CREATE TABLE IF NOT EXISTS accounts.admin(
    id            UUID                                PRIMARY KEY,
    name          VARCHAR(255)                        NOT NULL,
    username      VARCHAR(50)                         NOT NULL,
    password_hash VARCHAR(255)                        NOT NULL,
    status        VARCHAR(255)                        NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

ALTER TABLE accounts.session ADD COLUMN IF NOT EXISTS admin_id UUID REFERENCES accounts.admin(id) NULL;
ALTER TABLE accounts.promotions ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL;
ALTER TABLE accounts.session ALTER COLUMN user_id DROP NOT NULL, ALTER COLUMN user_id TYPE UUID, ALTER COLUMN user_id SET DEFAULT NULL;