from models import Vehicle
from repositories.vehicles_repository import VehiclesRepository


class VehiclesPostgresRepository(VehiclesRepository):
    def __init__(self, con):
        super(VehiclesPostgresRepository, self).__init__(con)

    def _create(self, vehicle: Vehicle):
        try:
            with self.con.cursor() as cur:
                query = 'INSERT INTO vehicles(make, model) VALUES(%s, %s) RETURNING id'
                params = (vehicle.make, vehicle.model)
                cur.execute(query, params)
                vehicle.id = cur.fetchone()[0]
                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e