

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
