CREATE TABLE IF NOT EXISTS accounts.order_requests (
    id              UUID                                 PRIMARY KEY,
    fuel_type       VARCHAR(50)                             NOT NULL,
    volume          BIGINT                                  NOT NULL,
    user_id         UUID REFERENCES accounts.user(id)       NOT NULL,
    comment         TEXT                                        NULL,
    feedback_score  INTEGER                                     NULL,
    feedback_text   TEXT                                        NULL,
    created_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP   NOT NULL,
    updated_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP   NOT NULL
);

ALTER TABLE accounts.admin ADD COLUMN IF NOT EXISTS min_fuel_volume INTEGER NULL;
