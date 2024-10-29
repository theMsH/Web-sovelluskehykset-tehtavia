from bson import ObjectId
from pymongo import MongoClient
from werkzeug.exceptions import NotFound
import models
from repositories.users_repository import UsersRepository

'''
Periytän tämän user reposta sittenkin, koska parentilla on save() metodi, joka toimii myös tässä sellaisenaan.
Käytännössä kaikki muu joutuu käytännössä ylikirjoittamaan.

Käytän koodauksessa opetusmateriaalia ja aikaisempaa tiedonhallinta -kurssin tehtävää, jonka olen tehnyt kurssilla
ja mongodb:n docseja sekä chatgpt
https://juhaniguru-tiedonhallinta.onrender.com/nosql/#komentoja
'''
class UsersMongoRepository(UsersRepository):

    def __init__(self, con: MongoClient):
        # db on se tietokanta, johon päästään käsiksi clientissä, nimesin tietokannan mysql ja
        # postgresql tietokantojen kaltaiseksi
        # con = mongo client
        self.db = con.sovelluskehykset_bad1
        super(UsersMongoRepository, self).__init__(con)


    def _create(self, user):
        # Kysäsin chatgpt:ltä mongodb:n tavan toteuttaa MySQL .commit() ja .rollback() toiminnot
        # Vastaukseksi sain esimerkkikoodin, että täytyy luoda istunto, joka suoritetaan with blockin sisällä.
        # Chatgpt: "It there equivalent for MySQL .commit() and .rollback() in MongoDB?"
        with self.con.start_session() as session:
            session.start_transaction()

            try:
                # Koska mongon helper functiot ottaa vastaan dictionaryjä,
                # voidaan helposti hyödyntää modelsin omaa to_json() metodia.
                result = self.db.users.insert_one(models.User.to_json(user))

                # Tässä on taas eri tavalla luodun Id:n haku, joka saadaan käyttämällä .inserted_id ja se palauttaa ObjectId.
                # Chatgpt: "How to get objectid after inserting mongodb data?"
                # Ja koska "err: ObjectId is not json serializable", muutetaan se muotoon str()
                user.id = str(result.inserted_id)

                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e


    def get_all(self):
        # kursori = tietokanta.kokoelma.kysely()
        # Tuloksena on mongon cursor objekti, josta saadaan loopattua yksittäiset dictinonaryt
        result = self.db.users.find()

        # mongo db palauttaa json datan suoraan
        users = []
        for user in result:
            # Id on mongon ObjectId('671fb084ebc89b1017886382'),
            # joka sisältää muitakin merkkejä kuin numeroita, joten se käsitellään str()
            users.append(models.User(str(user['_id']), user['username'], user['firstname'], user['lastname']))

        return users


    def get_by_id(self, user_oid):
        # Tuloksena tulee lista, jossa on yksi user, kun haetaan ObjectId:llä.
        # Tulokset pitää listauttaa .to_list() funktiolla, koska jos käyttäjää ei löydy,
        # tulee "no such item for cursor instance" virhe.
        # Lähde: https://stackoverflow.com/questions/78233990/no-such-item-for-cursor-instance
        result = self.db.users.find( {"_id": ObjectId(user_oid)} ).to_list()

        if not result:
            raise NotFound('user not found')

        user = result[0]
        return models.User(str(user['_id']), user['username'], user['firstname'], user['lastname'])


    def _update(self, user):
        with self.con.start_session() as session:
            session.start_transaction()

            try:
                self.db.users.update_one(
                    { "_id": ObjectId(user.id) },
                    { "$set":
                          { "username": user.username, "firstname": user.firstname, "lastname":user.lastname }
                    }
                )
                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e


    def delete_by_id(self, user_oid):
        with self.con.start_session() as session:
            session.start_transaction()
            try:
                result = self.db.users.delete_one( { "_id": ObjectId(user_oid) })

                # Chatgpt: "Does mongodb delete_one() return any rows affected?"
                if result.deleted_count == 0:
                    raise NotFound('user not found')

                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e
