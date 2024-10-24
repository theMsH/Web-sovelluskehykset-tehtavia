import os
from repositories.products_postgres_repository import ProductsPostgresRepository
from repositories.products_mysql_repository import ProductsMysqlRepository
from repositories.users_mysql_repository import UsersMysqlRepository
from repositories.users_postgres_repository import UsersPostgresRepository


"""
Factory pattern: määritellään enviin merkattu repositorio täällä.

con tulee get_db_conn dekoraattorilta ja name init_repository dekoraattorilta

Haluan palauttaa potentiaalisesti Nonen, jotta se aiheuttaa virheen, jos repoa ei tässä kohtaa pysty määrittään.
Lähtökohtaisesti uskon, että tietokantaa halutaan käyttää tiedostaen, 
eikä asettamalla random tietokanta defaultiksi.
"""

def repository_factory(con, name):
    repo = None
    _db = os.getenv("DB")

    if _db == 'mysql':
        if name == 'users':
            repo = UsersMysqlRepository(con)
        elif name == 'products':
            repo = ProductsMysqlRepository(con)

    elif _db == 'postgres':
        if name == 'users':
            repo = UsersPostgresRepository(con)
        elif name == 'products':
            repo = ProductsPostgresRepository(con)

    return repo


"""
Vanha koodi

def users_repository_factory(con):
    _db = os.getenv("DB")

    if _db == 'mysql':
        repo = UsersMysqlRepository(con)
    elif _db == 'postgres':
        repo = UsersPostgresRepository(con)
    else:
        repo = UsersMysqlRepository(con)

    return repo


# Products repolle oma tehdas
def products_repository_factory(con):
    _db = os.getenv("DB")

    if _db == 'mysql':
        repo = ProductsMysqlRepository(con)
    elif _db == 'postgres':
        repo = ProductsPostgresRepository(con)
    else:
        repo = ProductsMysqlRepository(con)

    return repo
"""