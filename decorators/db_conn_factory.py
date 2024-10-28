import contextlib
import os
import mysql.connector
import psycopg2
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


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

        elif _db == 'mongo':
            # Koodit yhteyden luontiin löytyi mongo db:n sivuilta, kun loi uuden clusterin ja haki siihen esimerkkikoodin
            # pythonille ja opetusmateriaaleista. Latasin paikallisen mongodb softan ja nyt client käyttää localhost
            con = MongoClient(host='mongodb://localhost:27017/', server_api=ServerApi('1'))

        yield con

    finally:
        if con is not None:
            con.close()
