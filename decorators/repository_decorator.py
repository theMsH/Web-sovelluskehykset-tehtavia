import os
from repositories.repository_factory import users_repository_factory, products_repository_factory


# Tunnilla käyty: decoraattorille välitetään parametrejä
def init_repository(name):
    def decorator(route_handler_func):
        # jotta tämä toimii, täytyy ennen tätä decoraattoria kutsua get_db_conn dekoraattoria, josta saadaan con.
        # Parametrin avulla määritellään mitä repositoriota halutaan käyttää
        def wrapper(con, *args, **kwargs):
            _db = os.getenv('DB')
            repo = None
            if name == 'users':
                repo = users_repository_factory(con)

            # Lisätään tänne productsille määrittely
            if name == 'products':
                repo = products_repository_factory(con)

            # Aina pitää muistaa palauttaa potentiaaliset *args ja **kwargs, jottei decoraattori hajoa.
            return route_handler_func(repo, *args, **kwargs)
        return wrapper
    return decorator
