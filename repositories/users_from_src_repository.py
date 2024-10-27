import json
import urllib.request
from werkzeug.exceptions import NotFound

import models


# Tämä repo käsittelee json datan, joka löytyy jostain toisesta API:sta

class UsersFromSrcRepository:

    def __init__(self, con):
        self.con = con

    '''
    Koodi json datan haku urlista poimittu stackoverflow kyselyn vastauksista:
    https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
    
    Tämä tulee repositioon vaikkei olekkaan tietokantakysely, koska clientti heittää requestin controllerille,
    controller kutsuu repositiota, repositio tekee siitä instanssin ja palauttaa controllerille, controller palauttaa
    responsena käyttäjän
    
    Tälle olisi kuitenki mahdollista tehdä tietokantayhteys ja tallentaa tuolta saadut tiedot sinne. Tällä hetkellä
    se on staticmethod, koska yhteyttä siinä ei tarvita ja python ehottelee tuota
    '''
    @staticmethod
    def get_all_from_url(url):
        # Example data from api:
        # { "id": int, "name": "Firstname Lastname", "username": "string", ... }
        with urllib.request.urlopen(url) as data:
            # Ajattelen, että tämä on vähänniinkuin tekisi selectin tietokantaan, ja siksi tämä on täällä.
            json_data = json.loads(data.read())

            user_list = []
            for user in json_data:
                # Splitataan name fullname muuttujaan, jotta voidaan antaa instanssille etu ja sukunimi erikseen.
                fullname = user['name'].split(" ")
                user_list.append(models.User(user['id'], user['username'], fullname[0], fullname[1]))

            return user_list


    # Ei ollut tehtävänannossa, mutta huvikseni testailen hakea yksittäisen käyttäjän ulkoisesta datasta
    # kahden parametrin avulla
    @staticmethod
    def get_user_from_url(url, user_id):
        with urllib.request.urlopen(url) as data:
            json_data = json.loads(data.read())

            for user in json_data:
                # Palautetaan User instanssi heti, jos se löytyy.
                # Vähentää virhetilanteita, kun tarkastellaan user['id'] string muodossa vertailua tehdessä
                # Esim. users/a getti users controlleriin aiheuttaa ongelmia, koska a ei ole integer ja tietokanta
                # vaatii integerin. Tietysti aina nyt sitä integeriä käytetään, mutta tässä ainaki on varaa
                # monimutkaistaa, jos tulevaisuudessa laittaisikin vaikka usernamen perusteella tehdä requestin.
                # Lähde: oma päättely
                if str(user['id']) == user_id:
                    fullname = user['name'].split(" ")

                    return models.User(user['id'], user['username'], fullname[0], fullname[1])

            # Jos sitä ei löydy, koodi pääsee tähän.
            raise NotFound('user not found')
