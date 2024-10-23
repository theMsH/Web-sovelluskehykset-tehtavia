import mysql.connector
from werkzeug.exceptions import NotFound
import models

'''
Muistiinpanoja itselleni:

Respository pattern. Tämä tiedosto toimii controllerin ja modelin välissä. 
Eli controllerista data ei mene suoraan modeliin, vaan se välittyy repositoryn kautta modeliin, ja repositoryn kautta
takaisin controllerille.

Eli tänne tulee nyt ne tietokantayhteydet ja kyselyt, jotka meni ennen modeliin
Luokan metodit palauttavat vain User luokan instansseja tai tietyissä virhetapauksissa None/raise e yms.
'''

class UsersMysqlRepository:
    def __init__(self):
        self.con = mysql.connector.connect(user='root', database='sovelluskehykset_bad1')

    # Destructor: siivotaan jäljet sulkemalla yhteys, jos se on vielä olemassa. Muuten se täyttää muistin
    def __del__(self):
        if self.con is not None and self.con.connected():
            self.con.close()

    # Tällä metodilla vähennän koodissa toistuvaa palauttelua
    @staticmethod
    def instantiate_user(user):
        return models.User(user[0], user[1], user[2], user[3])

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM users')
            result = cur.fetchall()
            users = []
            for user in result:
                users.append(self.instantiate_user(user))

            return users

    # Haetaan user id:n perusteella
    def get_by_id(self, _id):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (_id,))
            user = cur.fetchone()

            if user is None:
                raise NotFound('user not found')

            return self.instantiate_user(user)

    def update(self, user):
        # Koska kyseessä on muokkaava kysely, käytetään virheenhallintaa täällä
        try:
            with self.con.cursor() as cur:
                query = 'UPDATE users SET username = %s, firstname = %s, lastname = %s WHERE id = %s'
                params = (user.username, user.firstname, user.lastname, user.id)
                cur.execute(query, params)
                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e







