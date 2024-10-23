from flask import jsonify, request
from werkzeug.exceptions import NotFound
import models
from repositories.repository_factory import users_repository_factory

# Luodaan repository repository_factoryn avulla, niin voidaan helposti vaihtaa .envistä tietokantayhteys.


# Jokaista controlleria vastaa yksi tiedosto. Tiedostot sisältävät kaikki funktiot, jotka pitävät
# huolen requestin vastaanottamisesta ja responsen lähettämisestä.
def get_all_users():
    repo = users_repository_factory()
    users = repo.get_all()

    # Hyödynnetään palautuksessa userin list_to_json funktiota, niin saadaan parempaa koodia.
    return jsonify(models.User.list_to_json(users)), 200


def get_user_by_id(user_id):
    # Tässä tietokantakysely voi todennäköisesti palauttaa tyhjää, joten lyödään virheenkäsittely tähän NotFoundin varalta
    # Lähde toteutustapaan: Tehtävän 1 palautevideo
    try:
        repo = users_repository_factory()
        user = repo.get_by_id(user_id)
        return jsonify(models.User.to_json(user)), 200

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    # Napataan kiinni kaikki muu odottamaton virhe tässä, niin voidaan muotoilla virheet yhtenäiseksi json dataksi.
    # Flask palauttaa defaultisti html:lää näissä tapauksissa.
    except Exception as e:
        return jsonify({'err': str(e)}), 500


def update_user_by_id(user_id):
    try:
        repo = users_repository_factory()
        user = repo.get_by_id(user_id)
        data = request.get_json()
        '''
        Käytin tässä aikaisemmin data.get('username'), joka piti määritellä uudestaan user.username :ksi,
        jos sitä ei löytynyt reqbodystä, koska se muuten päivitti puuttuvan tiedon Noneksi.
        Tän takia koodi välitti aina status 200, vaikkei se periaatteessa tehnyt mitään. Siellä saattoi olla random dataa
        tai sitten typo. Mutta se tapa mahdollisti yksittäisen tiedon päivittämisen.
        Data['username'] käytössä tälläiset typot tai niiden puuttuminen nostaa virheen. 
        
        Lähde: edellisen tehtävän palautevideo + omat testailut ja havainnot
        '''

        user.username = data["username"]
        user.firstname = data["firstname"]
        user.lastname = data["lastname"]

        repo.save(user)

        return jsonify(models.User.to_json(user)), 200

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def create_user():
    try:
        repo = users_repository_factory()
        data = request.get_json()
        # Palautevideolta opittu abstraktio: annetaan id:ksi nolla, koska siitä voidaan myöhemmin päätellä,
        # että onko käyttäjä uusi vai olemassa oleva.
        user = models.User(0, data["username"], data["firstname"], data["lastname"])
        repo.save(user)

        return jsonify(models.User.to_json(user)), 201

    except Exception as e:
        return jsonify({'err': str(e)}), 500


def delete_user_by_id(user_id):
    try:
        repo = users_repository_factory()
        repo.delete_by_id(user_id)
        return jsonify(), 204

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500
