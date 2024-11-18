

class User:
    def __init__(self, _id, username, firstname, lastname):
        self.id = _id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    # Opittu ensimmäisen tehtävän videopalautteesta.
    # Nämä funtiot vähentää toistuvaa json-konversio koodia
    def to_json(self):
        return {'id': self.id, 'username': self.username, 'firstname': self.firstname, 'lastname': self.lastname}

    @staticmethod
    def list_to_json(users):
        res = []
        for user in users:
            res.append(user.to_json())
        return res


class Product:
    def __init__(self, _id, name, description):
        self.id = _id
        self.name = name
        self.description = description

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

    @staticmethod
    def list_to_json(products):
        res = []
        for product in products:
            res.append(product.to_json())
        return res


class Vehicle:
    def __init__(self, _id, make, model):
        self.id = _id
        self.make = make
        self.model = model

    def to_json(self):
        return {'id': self.id, 'make': self.make, 'model': self.model}

    # Tämän staticmethodin varmaan saisi jotenkin yhdistettyä noiden muiden kanssa, kunhan vain saisi välittettyä
    # tiedon, minkä classin to_json() halutaan käyttää.
    @staticmethod
    def list_to_json(vehicles):
        res = []
        for vehicle in vehicles:
            res.append(vehicle.to_json())
        return res

