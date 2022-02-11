DROP TABLE IF EXISTS cats;

CREATE TABLE cats (
    id TEXT PRIMARY KEY,
    catName TEXT NOT NULL,
    catColor TEXT NOT NULL,
    catBreed TEXT NOT NULL
);