from flask import request, jsonify
import models
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository

'''
Kokeilen hieman toista toteutustapaa tässä, kuin users controllerissa:

app.py kutsutaan tätä view_funcissa. Tämä functio puolestaan määrittää minkä metodin routehandleria kutsutaan.
Luodaan ensin tietokantayhteys ja sitten määritellään products repositorio dekoraattorien avulla
Nyt meidän ei tarvitse käyttää näitä dekoraattoreita joka ikisessä routehandlerissa, koska se välittyy tämän
funtion kautta

Idea on oma aikaisempia tehtäviä soveltaen
'''
@get_db_conn
@init_repository('products')
def request_products(con):
    if request.method == "GET":
        return _get_all_products(con)

    elif request.method == "POST":
        return _create_product(con)

'''
Merkkaan nämä alaviivalla vaikka nää periaatteessa ei oo minkään luokan "privaatti" metodeita. 
En ole tässä vaiheessavarma voisko nämäkin joskus sitten johonkin luokkaan tms. 
Ajatuksena kuitenkin, että tässä controllerissa on yksi funktio, 
jota clientti kutsuu jollain metodilla, 
ja se clientin kutsuma funktio itse määrittelee mitä näistä muista funktioista se käyttää.
'''

def _create_product(con):
    try:
        data = request.get_json()
        product = models.Product(0, data['name'], data['description'])
        con.save(product)

        return jsonify(models.Product.to_json(product)), 201

    except Exception as e:
        return jsonify({'err': str(e)})


def _get_all_products(con):
    products = con.get_all()
    return jsonify(models.Product.list_to_json(products)), 200
