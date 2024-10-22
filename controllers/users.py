from flask import jsonify
from repositories.users_mysql_repository import UsersMysqlRepository
from repositories.users_postgres_repository import UsersPostgresRepository


# Nyt jokaista controlleria vastaa yksi tiedosto. Tiedostot sisältävät kaikki funktiot,jotka pitävät
# huolen requestin vastaanottamisesta ja responsen lähettämisestä.
def get_all_users():
    # Luodaan mysql reposta instanssi ja käytetään sitä.
    #repo = UsersMysqlRepository()
    repo = UsersPostgresRepository()
    users = repo.get_all()
    users_json = []
    for user in users:
        users_json.append({
            'id': user.id,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
        })
    return jsonify(users_json)