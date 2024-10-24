from dotenv import load_dotenv
from flask import Flask
from controllers import users


app = Flask(__name__)

'''
Jos tekoäly ehdottaa tässä lambdaa yhteyden välittämiseen routehandlerille view_funcissa, ei saa käyttää
t. Juhani
'''

# Tulee AssertionError, jos tulee päälekkäisyyksiä urlien endpointeissa.
# add_url_rule documentaation mukaan voidaan asettaa oma nimitys endpointeille
# Tämän voi kiertää laittamalla metodit samaan url ruleen, mutta ne pitää sitten käsitellä kontrollerissa
# erikseen, mikä lisää sitten koodia controllerin puolelle.

app.add_url_rule('/api/users', "get_users", users.get_all_users, methods=["GET"])
app.add_url_rule('/api/users', "post_users", users.create_user, methods=["POST"])
app.add_url_rule('/api/users/<user_id>', "get_user_by_id", users.get_user_by_id, methods=["GET"])
app.add_url_rule('/api/users/<user_id>', "put_user_by_id", users.update_user_by_id, methods=["PUT"])
app.add_url_rule('/api/users/<user_id>', "delete_user_by_id", users.delete_user_by_id, methods=["DELETE"])


if __name__ == '__main__':
    load_dotenv()
    app.run()
