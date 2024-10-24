import os
from repositories.users_mysql_repository import UsersMysqlRepository
from repositories.users_postgres_repository import UsersPostgresRepository

# Factory pattern: määritellään enviin merkattu repositorio täällä.


# con tulee get_db_conn dekoraattorista
def users_repository_factory(con):
    _db = os.getenv("DB")

    if _db == 'mysql':
        repo = UsersMysqlRepository(con)
    elif _db == 'postgres':
        repo = UsersPostgresRepository(con)
    else:
        repo = UsersMysqlRepository(con)

    return repo
