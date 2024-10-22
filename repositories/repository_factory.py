import os
from repositories.users_mysql_repository import UsersMysqlRepository
from repositories.users_postgres_repository import UsersPostgresRepository

# Factory pattern: määritellään repositorio


def users_repository_factory():
    _db = os.getenv("DB")
    repo = None

    if _db == 'mysql':
        repo = UsersMysqlRepository()
    elif _db == 'postgres':
        repo = UsersPostgresRepository()
    else:
        repo = UsersMysqlRepository()

    return repo
