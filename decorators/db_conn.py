from decorators.db_conn_factory import init_db_conn


# Juhanin koodia webistä ja tunneilta ja lisätty omaa kommentointia:

# route_handler_func on funktio,
# jonka yläpuolella dekoraattoria kutsutaan
# python huolehtii siitä, että dekoraattori saa
# sen alapuolella olevan funktio itselleen autom. parametrina
def get_db_conn(route_handler_func):
    # dekoraattori on siitä erikoinen,
    # että sen sisälle luodaan toinen funktio
    # tämä wrapper ottaa parametrikseen *args ja **kwargs

    # *args sisältää kaikki positional argumentit jotka functio voi ottaa vastaan, ja **kwargs puolestaan
    # ottaa keywordargumentit
    def wrapper(*args, **kwargs):
        # kun tietokantayhteys avataan
        # ennen alkuperäisen funktion palauttamista, voimme
        # normaalisti laittaa con-muuttujan (tietokantayhteys)
        # routehandlerille parametrinä

        # Eli nyt yhteys luodaan controllerin ulkopuolella,
        # ja tässä controllerin routehändleriä käytetään db factoryn kanssa (josta se yhteys tulee).
        with init_db_conn() as con:
            return route_handler_func(con, *args, **kwargs)

        # Tämän avulla saadaan yhteydenmuodostus pois controllerista, ja controlleriin jää vain ne mitkä sille kuuluu

    # huom dekoraattorin pitää palauttaa sen sisäpuolella luotu funktio
    # mutta palautukseen ei tule sulkuja perään
    return wrapper
