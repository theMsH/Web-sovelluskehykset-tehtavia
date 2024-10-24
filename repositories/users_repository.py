from werkzeug.exceptions import NotFound
import models

'''
Muistiinpanoja itselleni:

Respository pattern. Tämä tiedosto toimii controllerin ja modelin välissä. 
Eli controllerista data ei mene suoraan modeliin, vaan se välittyy repositoryn kautta modeliin, ja repositoryn kautta
takaisin controllerille.

Eli tänne tulee nyt ne tietokantayhteydet ja kyselyt, jotka meni ennen modeliin
Luokan metodit palauttavat vain User luokan instansseja tai tietyissä virhetapauksissa raise e yms.

Mysql ja postgres repot periytyvät tästä, ja täällä on niille molemmille toimivaa koodia. Repofactory päättää
mitä childiä käytetään. Toimimattomat functiot ylikirjoitetaan siellä lapsirepossa, mikä vaatii erilaisen kyselyn.
'''


class UsersRepository:

    # Yhteys tietokantaan injektoidaan sieltä child reposta, jota tätä käytetään
    def __init__(self, con):
        self.con = con

    # Tällä metodilla vähennän koodissa toistuvaa palauttelua
    @staticmethod
    def instantiate_user(user):
        return models.User(user[0], user[1], user[2], user[3])

    def _create(self, user):
        try:
            with self.con.cursor() as cur:
                query = 'INSERT INTO users(username, firstname, lastname) VALUES(%s, %s, %s)'
                params = (user.username, user.firstname, user.lastname)
                cur.execute(query, params)
                user.id = cur.lastrowid

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM users')
            result = cur.fetchall()
            users = []
            for user in result:
                users.append(self.instantiate_user(user))

            return users

    # Haetaan user id:n perusteella
    def get_by_id(self, user_id):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cur.fetchone()

            if user is None:
                raise NotFound('user not found')

            return self.instantiate_user(user)

    def _update(self, user):
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

    # Palautevideolta opittua abstractiota
    # Jos id:tä ei ole annettu, eli se on 0 (false), niin päivitetään käyttäjä.
    def save(self, user):
        if not user.id:
            self._create(user)
        else:
            self._update(user)

    def delete_by_id(self, user_id):
        try:
            with self.con.cursor() as cur:
                cur.execute('DELETE FROM users WHERE id = %s', (user_id,))

                '''
                Jos ei poistettu mitään, nostetaan NotFound. Teen tämän tänne siksi, 
                koska requesti tullaan aina tekemään tietokantaan, 
                tässä tapauksessa delete suoritetaan aina, vaikka ID:llä ei löydy käyttäjää.
                Jos tekisin get_user_by_id requestin, tekisin joissain tapauksissa 2 requestia.
                Ja ajattelin, että ihan sama tehdä se delete aina, jolloin tulis aina se 1 requesti joka tapauksessa.
                '''

                if not cur.rowcount:
                    raise NotFound('user not found')

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e
