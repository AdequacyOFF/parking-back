CREATE TABLE IF NOT EXISTS accounts.promotions(
    id             UUID               PRIMARY KEY,
    created_at     TIMESTAMP          DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP          DEFAULT CURRENT_TIMESTAMP,
    title          VARCHAR(255)       NOT NULL,
    description    VARCHAR(255)       NOT NULL,
    photo          UUID               NOT NULL,
    url            VARCHAR(255)       NULL
);