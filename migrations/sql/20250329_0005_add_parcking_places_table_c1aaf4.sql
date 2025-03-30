CREATE TABLE IF NOT EXISTS parking.places (
    id SERIAL PRIMARY KEY,
    car_number VARCHAR(20) NULL,
    owner UUID NULL,
    is_busy BOOLEAN NOT NULL,
    CONSTRAINT fk_places_owner FOREIGN KEY (owner)
    REFERENCES accounts.user(id)
    ON DELETE SET NULL
);