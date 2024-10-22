from flask import jsonify
from werkzeug.exceptions import NotFound
import models
from repositories.repository_factory import users_repository_factory

# Luodaan repository repository_factoryn avulla, niin voidaan helposti vaihtaa .envistä tietokantayhteys.
repo = users_repository_factory()

# Jokaista controlleria vastaa yksi tiedosto. Tiedostot sisältävät kaikki funktiot, jotka pitävät
# huolen requestin vastaanottamisesta ja responsen lähettämisestä.
def get_all_users():
    users = repo.get_all()

    # Hyödynnetään palautuksessa userin list_to_json funktiota, niin saadaan parempaa koodia.
    return jsonify(models.User.list_to_json(users))


def get_user_by_id(user_id):
    # Tässä tietokantakysely voi todennäköisesti palauttaa tyhjää, joten lyödään virheenkäsittely tähän NotFoundin varalta
    # Lähde toteutustapaan: Tehtävän 1 palautevideo
    try:
        user = repo.get_by_id(user_id)
        return jsonify(models.User.to_json(user))

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    # Napataan kiinni kaikki muu odottamaton virhe tässä, niin voidaan muotoilla virheet yhtenäiseksi json dataksi.
    # Flask palauttaa defaultisti html:lää näissä tapauksissa.
    except Exception as e:
        return jsonify({'err': str(e)}), 500
