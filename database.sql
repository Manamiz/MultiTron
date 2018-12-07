CREATE DATABASE IF NOT EXISTS multitron;

USE multitron;

CREATE TABLE player 
(
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    login VARCHAR(255),
    password VARCHAR(255),
    score FLOAT,
    isAdmin BOOLEAN
);
