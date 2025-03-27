CREATE TABLE IF NOT EXISTS accounts.card(
    id          UUID                                    PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT               CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT               CURRENT_TIMESTAMP,
    qr          UUID                                       NOT NULL,
    bonuses     INTEGER                                    NOT NULL,
    type        VARCHAR(60)                                NOT NULL,
    state       VARCHAR(60)                                NOT NULL,
    user_id     UUID     REFERENCES accounts.user(id)      NOT NULL
);
