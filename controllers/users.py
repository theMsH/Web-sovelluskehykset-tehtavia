from flask import jsonify, request
from werkzeug.exceptions import NotFound
import models
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository

# Jokaista controlleria vastaa yksi tiedosto. Tiedostot sisältävät kaikki funktiot, jotka pitävät
# huolen requestin vastaanottamisesta ja responsen lähettämisestä.

'''
Decoraattori: dekoraattorin alapuolella olevasta functiosta tulee dekoraattorin route_handler_func,
jolle dekoraattorin wrapper antaa parametriksi connectionin, *args ja **kwargs
Decoraattoreita voi olla useita, ja dekoraattorille voi antaa parametrin. 

Ensin luodaan tietokantayhteys @get_db_conn dekoraattorilla,
sen jälkeen voidaan alustaa haluttu repositorio käyttämällä @init_repository()
ja antamalla sille parametrinä haluttu repositorio.

Nämä dekoraattorit pitää antaa kaikille routehändlereile

Aiemmin täällä määriteltiin myös repo, mutta se repo määriytyy nykyään dekoraattorien avulla, ja palautuvassa 
con muuttujassa on meillä toimiva yhteys haluttuun tietokantaan, joka käyttää haluttua repoa. Tämä con muuttuja
välitetään route händlerille, joka tässä kyseisessä tiedostossa käyttää parent UserRepoa envissä määritellyn 
tietokantayhteyden mukaan nimettyä child UserRepoa eli esim UsersMysqlRepository
'''


@get_db_conn
@init_repository('users')
def get_all_users(con):
    users = con.get_all()

    # Hyödynnetään palautuksessa userin list_to_json funktiota, niin saadaan parempaa koodia.
    return jsonify(models.User.list_to_json(users)), 200


@get_db_conn
@init_repository('users')
def get_user_by_id(con, user_id):
    # Tässä tietokantakysely voi todennäköisesti palauttaa tyhjää,
    # joten lyödään virheenkäsittely tähän NotFoundin varalta
    # Lähde toteutustapaan: Tehtävän 1 palautevideo
    try:
        user = con.get_by_id(user_id)
        return jsonify(models.User.to_json(user)), 200

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    # Napataan kiinni kaikki muu odottamaton virhe tässä, niin voidaan muotoilla virheet yhtenäiseksi json dataksi.
    # Flask palauttaa defaultisti html:lää näissä tapauksissa.
    except Exception as e:
        return jsonify({'err': str(e)}), 500


@get_db_conn
@init_repository('users')
def update_user_by_id(con, user_id):
    try:
        user = con.get_by_id(user_id)
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

        con.save(user)

        return jsonify(models.User.to_json(user)), 200

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500


@get_db_conn
@init_repository('users')
def create_user(con):
    try:
        data = request.get_json()
        # Palautevideolta opittu abstraktio: annetaan id:ksi nolla, koska siitä voidaan myöhemmin päätellä,
        # että onko käyttäjä uusi vai olemassa oleva.
        user = models.User(0, data["username"], data["firstname"], data["lastname"])
        con.save(user)

        return jsonify(models.User.to_json(user)), 201

    except Exception as e:
        return jsonify({'err': str(e)}), 500


@get_db_conn
@init_repository('users')
def delete_user_by_id(con, user_id):
    try:
        con.delete_by_id(user_id)
        return jsonify(), 204

    except NotFound:
        return jsonify({'err': 'user not found'}), 404

    except Exception as e:
        return jsonify({'err': str(e)}), 500
