import mysql.connector
from repositories.user_repository import UserRepository

# Tämä perii userRepositoryn, ja syöttää sinne tietokantayhteyden.
# Tämä myös huolehtii yhteyden sulkemisesta, koska se on eri kuin postgrellä


class UsersMysqlRepository(UserRepository):
    '''
    Tälläinenkin tapa on periaatteessa oikein, mutta tunneilla käytyjen esimerkkien perusteella voidaan tehdä
    koodi vieläkin modulaarisemmin

    def __init__(self):
        self.con = mysql.connector.connect(user='root', database='sovelluskehykset_bad1')

    # Destructor: siivotaan jäljet sulkemalla yhteys, jos se on vielä olemassa. Muuten se täyttää muistin
    def __del__(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()
    '''

    # Täällä ei enää tarvitse sulkea yhteyttä, koska se missä se luodaan, siellä se myös suljetaan eli db_conn
    # factoryssä.
    def __init__(self, con):
        super(UsersMysqlRepository, self).__init__(con)
