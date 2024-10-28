from bson import ObjectId
from werkzeug.exceptions import NotFound
import models
from repositories.users_repository import UsersRepository

'''
Tämä luokka ei peri usersrepoa, koska niiden funktiot ei vaan toimi ja en halua ainakaan tällä hetkellä, 
että koodarin olisi mahdollsta kutsua parentin ei-ylikirjoitettuja metodeita.

Käytän koodauksessa opetusmateriaalia ja aikaisempaa tiedonhallinta -kurssin tehtävää, jonka olen tehnyt kurssilla
https://juhaniguru-tiedonhallinta.onrender.com/nosql/#komentoja
'''
class UsersMongoRepository:

    def __init__(self, con):
        # db on se tietokanta, johon päästään käsiksi clientissä, nimesin tietokannan mysql ja
        # postgresql tietokantojen kaltaiseksi
        # con = mongo client
        self.db = con.sovelluskehykset_bad1


    def get_all(self):
        # kursori = tietokanta.kokoelma.kysely()
        # Tuloksena on mongon cursor objekti, josta saadaan loopattua yksittäiset dictinonaryt
        result = self.db.users.find()

        # mongo db palauttaa json datan suoraan
        users = []
        for user in result:
            # Id on mongon ObjectId('671fb084ebc89b1017886382'), joka sisältää muitakin merkkejä kuin numeroita, joten se käsitellään str()
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


