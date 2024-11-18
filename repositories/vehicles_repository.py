from werkzeug.exceptions import NotFound
from models import Vehicle


class VehiclesRepository:
    def __init__(self, con):
        self.con = con

    def _create(self, vehicle: Vehicle):
        try:
            with self.con.cursor() as cur:
                query = 'INSERT INTO vehicles(make, model) VALUES(%s, %s)'
                params = (vehicle.make, vehicle.model)
                cur.execute(query, params)
                vehicle.id = cur.lastrowid

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM vehicles')
            result = cur.fetchall()
            vehicles = []
            for vehicle in result:
                vehicles.append(Vehicle(vehicle[0], vehicle[1], vehicle[2]))

            return vehicles

    def get_by_id(self, vehicle_id):
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM vehicles WHERE id = %s', (vehicle_id,))
            vehicle = cur.fetchone()

            # Muissa repoissa tässä palautu raise NotFound, mutta se kuuluikin controllerin tehtäväksi
            # ja teen sen tässä oikeaoppisemmin.
            if vehicle is None:
                return None

            return Vehicle(vehicle[0], vehicle[1], vehicle[2])

    def _update_by_id(self, vehicle: Vehicle):
        try:
            with self.con.cursor() as cur:
                query = 'UPDATE vehicles SET make = %s, model = %s WHERE id = %s'
                params = (vehicle.make, vehicle.model, vehicle.id)
                cur.execute(query, params)
                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e

    def save(self, vehicle):
        if not vehicle.id:
            self._create(vehicle)
        else:
            self._update_by_id(vehicle)

    def delete_by_id(self, vehicle_id):
        try:
            with self.con.cursor() as cur:
                cur.execute('DELETE FROM vehicles WHERE id = %s', (vehicle_id,))
                # Laitoin tämän palauttamaan booleanin määrittämään onnistuiko poisto vai ei.
                # Jos se ei onnistu, se tarkoittaa että ajoneuvoa ei löytynyt.
                # Näin saan siirretty tämänkin controllerin huoleksi täysin
                if not cur.rowcount:
                    return False
                    #raise NotFound

                self.con.commit()
                return True

        except Exception as e:
            self.con.rollback()
            raise e
