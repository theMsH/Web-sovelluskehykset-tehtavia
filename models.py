

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
