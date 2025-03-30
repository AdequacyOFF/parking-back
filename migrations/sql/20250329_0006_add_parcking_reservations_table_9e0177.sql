CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE TABLE parking.reservations (
    id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL,
    reserved_from TIMESTAMP NOT NULL,
    reserved_to TIMESTAMP NOT NULL,
    reserved_by UUID NOT NULL,
    CONSTRAINT fk_reservation_place FOREIGN KEY (place_id)
        REFERENCES parking.places(id) ON DELETE CASCADE,
    CONSTRAINT valid_reservation_period CHECK (reserved_to > reserved_from),
    EXCLUDE USING gist (
        place_id WITH =,
        tsrange(reserved_from, reserved_to) WITH &&
    )
);
CREATE INDEX idx_reservations_place_id ON parking.reservations(place_id);
CREATE INDEX idx_reservations_reserved_by ON parking.reservations(reserved_by);