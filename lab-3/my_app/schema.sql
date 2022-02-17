DROP TABLE IF EXISTS samples;

CREATE TABLE samples (
    key varchar(500) PRIMARY KEY,
    value varchar(500) NOT NULL,
    message varchar(500) NOT NULL
);