-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- create table players
DROP TABLE IF EXISTS Players;
CREATE TABLE players (
  id serial PRIMARY KEY,
  name varchar(50) NOT NULL
);

-- create table Matches
DROP TABLE IF EXISTs Matches;
CREATE TABLE Matches (
  id serial PRIMARY KEY,
  winner integer REFERENCES Players (id),
  loser integer REFERENCES Players (id)
);

-- create table standings view
CREATE OR REPLACE VIEW Standings AS
  SELECT tmp.id, tmp.name, count(matches.winner) as wins, tmp.matches
  FROM (
      SELECT players.id AS id, players.name AS name, count(matches.*) AS matches
      FROM players LEFT JOIN matches
      ON players.id IN (matches.winner, matches.loser)
      GROUP BY players.id
  ) as tmp
  LEFT JOIN matches
  ON tmp.id = matches.winner
  GROUP by tmp.id, tmp.name, tmp.matches
  ORDER by wins DESC;
--);
