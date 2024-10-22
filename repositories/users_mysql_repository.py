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

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM users')
            result = cur.fetchall()
            users = []
            for user in result:
                users.append(models.User(user[0], user[1], user[2], user[3]))

            return users

    # Haetaan user id:n perusteella
    def get_by_id(self, _id):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (_id,))
            result = cur.fetchone()

            if result is None:
                raise NotFound('user not found')

            return models.User(result[0], result[1], result[2], result[3])






