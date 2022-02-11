DROP TABLE IF EXISTS cats;

CREATE TABLE cats (
    id varchar(500) PRIMARY KEY,
    catName varchar(500) NOT NULL,
    catColor varchar(500) NOT NULL,
    catBreed varchar(500) NOT NULL
);