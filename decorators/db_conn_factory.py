import contextlib
import os
import mysql.connector
import psycopg2


# Tunneilla käytyä:
# koska return ei säilytä connectionia, tarvitaan conxtexmanager decoraattori.
# sen sijaan käytetään yield, jotta yhteys säilyy. Suorituksen jälkeen ohjelma palaa tänne ja sulkee yhteyden.
# Eli kun with blockin ulkopuolelle mennään, se palaa finally blockkiin
@contextlib.contextmanager
def init_db_conn():
    con = None
    try:
        _db = os.getenv('DB')

        if _db == 'mysql':
            con = mysql.connector.connect(user='root', database='sovelluskehykset_bad1')

        elif _db == 'postgres':
            con = psycopg2.connect(
                user='postgres', host='localhost', password='salasana', dbname='sovelluskehykset_bad1')

        yield con

    finally:
        if con is not None:
            con.close()
