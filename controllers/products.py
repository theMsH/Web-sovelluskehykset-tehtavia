from flask import request, jsonify
from werkzeug.exceptions import NotFound
import models
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository

'''
Kokeilen hieman toista toteutustapaa tässä, kuin users controllerissa:

app.py kutsutaan tätä view_funcissa. Tämä functio puolestaan määrittää minkä metodin routehandleria kutsutaan.
Luodaan ensin tietokantayhteys ja sitten määritellään products repositorio dekoraattorien avulla
Nyt meidän ei tarvitse käyttää näitä dekoraattoreita joka ikisessä routehandlerissa, koska se välittyy tämän
funtion kautta

Lisäksi voidaan siirtää jokaisessa routehändlerissä toistuva virheenkäsittely tähän functioon.

Ideat on peräisin omista havainnoista ja aikaisempia tehtäviä soveltaen
Havaintoni usersiin verraten: koodia tulee lopulta lähes saman verran (ilman kommentteja), 
mutta tästä toistuva koodi on karsiutunut pois.
'''

@get_db_conn
@init_repository('products')
def request_products(con):
    try:
        if request.method == "GET":
            return _get_all_products(con)

        if request.method == "POST":
            return _create_product(con)

    except NotFound:
        return jsonify({'err': 'products not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500
'''
Merkkaan nämä alaviivalla vaikka nää periaatteessa ei oo minkään luokan "privaatti" metodeita. 
En ole tässä vaiheessavarma tulisko nämäkin joskus sitten johonkin luokkaan tms. 
Ajatuksena kuitenkin, että tässä controllerissa on yksi funktio "route_handlerien handler" 
eli varsinainen route_handler, jota clientti kutsuu jollain metodilla, 
ja se clientin kutsuma funktio itse määrittelee mitä näistä muista _funktioista se käyttää.
Olisin voinut tietty lyödä nämä tuonne function sisälle kuten tehtävässä 1 tein, mutta näin on jotenkin
selkeämpää koodia.
'''

def _get_all_products(con):
    products = con.get_all()

    # Jos tietokannasta ei löydy yhtään tuotteita, nostetaan poikkeus
    if not products:
        raise NotFound('products not found')

    return jsonify(models.Product.list_to_json(products)), 200


def _create_product(con):
    data = request.get_json()
    product = models.Product(0, data['name'], data['description'])
    con.save(product)

    return jsonify(models.Product.to_json(product)), 201


@get_db_conn
@init_repository('products')
def request_products_by_id(con, product_id):
    try:
        if request.method == "GET":
            return _get_product_by_id(con, product_id)

        if request.method == "PUT":
            return _update_product_by_id(con, product_id)

        if request.method == "DELETE":
            return _delete_product_by_id(con, product_id)

    except NotFound:
        return jsonify({'err': 'product not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def _get_product_by_id(con, product_id):
    product = con.get_by_id(product_id)
    return jsonify(models.Product.to_json(product)), 200


def _update_product_by_id(con, product_id):
    data = request.get_json()

    product = con.get_by_id(product_id)
    product.name = data["name"]
    product.description = data["description"]
    con.save(product)

    return jsonify(models.Product.to_json(product)), 200


def _delete_product_by_id(con, product_id):
    con.delete_by_id(product_id)
    return jsonify(), 204
