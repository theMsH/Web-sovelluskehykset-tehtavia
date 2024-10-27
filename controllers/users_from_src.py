from flask import request, jsonify
from werkzeug.exceptions import NotFound
import models
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository


'''
Eli haetaan data jostain, josta voidaan luoda User instansseja ja user controlleri palauttaa sen clientille jsonina.
Tietokantayhteyttä ei varsinaisesti tarvita, mutta koodasin sen valmiiksi, jos sen tarvii joskus

Tavoitteena oli koodata tämä siten, että tänne voisi helposti lisätä muita datalähteitä
'''

# Tässä kohtaa käsitellään, onko endpointissa parametrina annettu lähteen nimi tuettu
# Vähentää koodin toistoa ja helpottaa uusien urlien tuen lisäystä
def _check_for_url(src):
    if src == 'jsonplaceholder':
        return 'https://jsonplaceholder.typicode.com/users'
    else:
        return None


@get_db_conn
@init_repository('external sources')
def request_users_from_src(con, src):
    try:
        if request.method == "GET":
            # Käsitellään onko url tuettu.
            url = _check_for_url(src)
            if url:
                return _get_users_from_url(con, url)

            # tähän vois tulla elif jossei olekkaan url, vaan joku muu tyyppi,
            # johon reagoidaan jollain muulla kuin get_from_url() metodilla

            return jsonify({'err': 'source not found'}), 404

    except NotFound:
        return jsonify({'err': 'users not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def _get_users_from_url(con, url):
    users = con.get_all_from_url(url)
    return jsonify(models.User.list_to_json(users)), 200


# Ei ollut tehtävänantona, mutta huvikseni testaan hakea yksittäisen userin, samalla tuli huomattua, miten voin
# vähentää koodin toistoa sourcen määrittelyssä
@get_db_conn
@init_repository('external sources')
def request_user_from_src(con, src, user_id):
    try:
        if request.method == "GET":
            url = _check_for_url(src)
            if url:
                return _get_user_from_url(con, url, user_id)

            return jsonify({'err': 'source not found'}), 404

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def _get_user_from_url(con, url, user_id):
    user = con.get_user_from_url(url, user_id)
    return jsonify(models.User.to_json(user)), 200
