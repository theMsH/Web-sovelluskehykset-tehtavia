import psycopg2
from repositories.user_repository import UserRepository


class UsersPostgresRepository(UserRepository):

    def __init__(self):
        self.con = psycopg2.connect(
            user='postgres', host='localhost', password='salasana', dbname='sovelluskehykset_bad1')

    def __del__(self):
        if self.con is not None and not self.con.closed:
            self.con.close()

    '''
    Ylikirjoitetaan _create, koska postgre vaatii "RETURNING id" kyselyyn, jotta sieltä palautuisi luodessa oikea id.
    Defaultisti insert ei siis palauta mitään. RETURNING vaatii yhteensopivan yhteyden, kuten psycopg2 tai asyncpg.
    Vaikuttaa siltä, että cur.lastrowid tuetaan laajemmin, joten jätin sen parenttiin ns. defaultiksi
    
    Lähde: Chatgpt: "cursor.lastrowid returns 0 in postgre insert operation. Why?"
    '''
    def _create(self, user):
        try:
            with self.con.cursor() as cur:
                query = 'INSERT INTO users(username, firstname, lastname) VALUES(%s, %s, %s) RETURNING id'
                params = (user.username, user.firstname, user.lastname)
                cur.execute(query, params)

                # cur.lastrowid ei toimi postgresissä, asetetaan tällätavoin oikea id,
                # joka voidaan palauttaa viewiin aikanaan
                user.id = cur.fetchone()[0]

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e
