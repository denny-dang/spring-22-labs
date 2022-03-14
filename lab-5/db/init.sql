CREATE DATABASE catsdb;
use catsdb;

CREATE TABLE IF NOT EXISTS cats (
    `id` varchar(500) PRIMARY KEY,
    `catName` varchar(500) NOT NULL,
    `catColor` varchar(500) NOT NULL,
    `catBreed` varchar(500) NOT NULL
);
INSERT INTO cats VALUES
    ('cat1','Test Cat','Test Cat','Test Cat'),
    ('cat2','Test Cat','Test Cat','Test Cat');
