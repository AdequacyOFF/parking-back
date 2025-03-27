CREATE TABLE IF NOT EXISTS accounts.services(
    id          UUID                      PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    title       VARCHAR(255)                 NOT NULL
);


CREATE TABLE IF NOT EXISTS accounts.station(
    id          UUID                      PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    name        VARCHAR(255)                 NOT NULL,
    address     VARCHAR(255)                 NOT NULL,
    coordinates GEOGRAPHY(Point)             NOT NULL
);


CREATE TABLE IF NOT EXISTS accounts.services_relation_table(
    service_id   UUID      REFERENCES accounts.services(id)   NULL,
    station_id   UUID      REFERENCES accounts.station(id)   NULL
);

CREATE TABLE IF NOT EXISTS accounts.oils(
    id          UUID                             PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT         CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ DEFAULT         CURRENT_TIMESTAMP,
    title       VARCHAR(255)                         NOT NULL,
    price       INTEGER                              NOT NULL,
    station_id  UUID REFERENCES accounts.station(id) NOT NULL
);