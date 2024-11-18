from dotenv import load_dotenv
from flask import Flask
from controllers import users, products, users_from_src, vehicles

app = Flask(__name__)

'''
Jos tekoäly ehdottaa tässä lambdaa yhteyden välittämiseen routehandlerille view_funcissa, ei saa käyttää
t. Juhani
'''

# Tulee AssertionError, jos tulee päälekkäisyyksiä urlien endpointeissa.
# add_url_rule documentaation mukaan voidaan asettaa oma nimitys endpointeille
app.add_url_rule('/api/users', "get_users", users.get_all_users, methods=["GET"])
app.add_url_rule('/api/users', "post_users", users.create_user, methods=["POST"])
app.add_url_rule('/api/users/<user_id>', "get_user_by_id", users.get_user_by_id, methods=["GET"])
app.add_url_rule('/api/users/<user_id>', "put_user_by_id", users.update_user_by_id, methods=["PUT"])
app.add_url_rule('/api/users/<user_id>', "delete_user_by_id", users.delete_user_by_id, methods=["DELETE"])

# Teen eri tyylillä productsille. Tämä tyyli on peräisin tehtävä 1, mutta vähän paremmin toteutettuna.
app.add_url_rule(rule = '/api/products', endpoint = "products",
                 view_func = products.request_products, methods = ["GET", "POST"])

app.add_url_rule(rule = '/api/products/<product_id>', endpoint = "products/id",
                 view_func = products.request_products_by_id, methods = ["GET", "PUT", "DELETE"])

'''
Tehtävän 3 koodia

Tavoitteena oli luoda route, jossa ulkoisen lähteen käsittelyyn on oma controller, ja että routeen olisi helppo
jatkossa lisätä myös muita ulkoisia lähteitä, joista saa luotua User instansseja.
'''
app.add_url_rule('/api/users-from-source/<src>','users-from-source/src',
                 view_func = users_from_src.request_users_from_src, methods = ['GET'])

# Ei ollut tehtävänannossa, mutta huvikseni testailen kahden parametrin requestia
app.add_url_rule('/api/users-from-source/<src>/<user_id>','users-from-source/src/id',
                 view_func = users_from_src.request_user_from_src, methods = ['GET'])

# Tehtävä 5
app.add_url_rule('/api/vehicles','vehicles',
                 view_func = vehicles.request_vehicles, methods = ["GET", "POST"])
app.add_url_rule('/api/vehicles/<vehicle_id>','vehicles/id',
                 view_func = vehicles.request_vehicle_by_id, methods = ["GET", "PUT", "DELETE"])


if __name__ == '__main__':
    load_dotenv()
    app.run()
