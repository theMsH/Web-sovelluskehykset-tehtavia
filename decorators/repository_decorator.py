from repositories.repository_factory import repository_factory


# Tunnilla käyty: decoraattorille välitetään parametrejä
def init_repository(name):
    def decorator(route_handler_func):
        # Jotta tämä toimii, täytyy ennen tätä decoraattoria kutsua get_db_conn dekoraattoria, josta saadaan con.
        # Name parametrin avulla määritellään mitä repositoriota halutaan käyttää
        def wrapper(con, *args, **kwargs):
            """
            Vanha koodi. Toteutin tämän määrittelyn suoraan repository_factoryssä
            Koska se mielestäni on loogista olla siellä.

            _db = os.getenv('DB')
            repo = None
            if name == 'users':
                repo = users_repository_factory(con)

            if name == 'products':
                repo = products_repository_factory(con)
            """

            # Tai sitten ihan vaan:
            repo = repository_factory(con, name)

            # Tehtävän 2 palautevideolta saatu vinkki: Nostetaan virhe, jos repo ei pystytty asettamaan.
            if repo is None:
                raise Exception(f"Repo is not initialized. Repository name used: {name}")

            # Aina pitää muistaa palauttaa potentiaaliset *args ja **kwargs, jottei decoraattori hajoa.
            return route_handler_func(repo, *args, **kwargs)
        return wrapper
    return decorator
