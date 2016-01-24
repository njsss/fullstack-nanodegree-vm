#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import contextlib

@contextlib.contextmanager
def get_cursor():
    """
    manage database connection.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        yield cur
    except:
        raise
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as cur:
        cur.execute("DELETE FROM Matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cur:
        cur.execute("DELETE FROM Players;")


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as cur:
        cur.execute("SELECT count(*) FROM Players")
        count = cur.fetchall()[0][0]

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as cur:
        cur.execute("INSERT INTO Players (name) VALUES (%s) RETURNING id", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with get_cursor() as cur:
        cur.execute("SELECT id, name, wins, matches FROM Standings")
        player_standings = cur.fetchall()

    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as cur:
        cur.execute("INSERT INTO Matches (winner,loser) VALUES (%s, %s)", (winner, loser))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    # retrive player standings
    standings = playerStandings()
    for i in range(len(standings)/2):
        p1 = standings[i*2]
        p2 = standings[i*2+1]
        # pair up first with second in line
        pairings.append((p1[0], p1[1], p2[0], p2[1]))

    return pairings
