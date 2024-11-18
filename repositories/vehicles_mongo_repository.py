from bson import ObjectId
from pymongo import MongoClient
from models import Vehicle
from repositories.vehicles_repository import VehiclesRepository


class VehiclesMongoRepository(VehiclesRepository):

    def __init__(self, con: MongoClient):
        self.db = con.sovelluskehykset_bad1
        super(VehiclesMongoRepository, self).__init__(con)


    def _create(self, vehicle):
        with self.con.start_session() as session:
            session.start_transaction()

            try:
                result = self.db.vehicles.insert_one(Vehicle.to_json(vehicle))
                vehicle.id = str(result.inserted_id)
                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e


    def get_all(self):
        result = self.db.vehicles.find()

        vehicles = []
        for vehicle in result:
            vehicles.append(Vehicle(str(vehicle['_id']), vehicle['make'], vehicle['model']))

        return vehicles


    def get_by_id(self, vehicle_oid):
        result = self.db.vehicles.find( {"_id": ObjectId(vehicle_oid)} ).to_list()

        if not result:
            return None

        vehicle = result[0]
        return Vehicle(str(vehicle['_id']), vehicle['make'], vehicle['model'])


    def _update_by_id(self, vehicle):
        with self.con.start_session() as session:
            session.start_transaction()
            try:
                self.db.vehicles.update_one(
                    { "_id": ObjectId(vehicle.id) },
                    { "$set":
                          { "make": vehicle.make, "model": vehicle.model }
                    }
                )
                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e


    def delete_by_id(self, vehicle_oid):
        with self.con.start_session() as session:
            session.start_transaction()
            try:
                result = self.db.vehicles.delete_one( { "_id": ObjectId(vehicle_oid) })

                if result.deleted_count == 0:
                    return False

                session.commit_transaction()
                return True

            except Exception as e:
                session.abort_transaction()
                raise e
