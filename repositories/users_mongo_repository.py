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
        self.con = con


    def get_all(self):
        # con = mongo client
        with self.con as client:
            # db on se tietokanta, johon päästään käsiksi clientissä, nimesin tietokannan mysql ja
            # postgresql tietokantojen kaltaiseksi
            db = client.sovelluskehykset_bad1
            # kursori = tietokanta.kokoelma.kysely()
            # Tuloksena on mongon cursor objekti, josta saadaan loopattua yksittäiset dictinonaryt
            result = db.users.find()

            # mongo db palauttaa json datan suoraan
            users = []
            for user in result:
                # Id on mongon ObjectId('671fb084ebc89b1017886382'), joka sisältää muitakin merkkejä kuin numeroita, joten se käsitellään str()
                users.append(models.User(str(user['_id']), user['username'], user['firstname'], user['lastname']))

            return users