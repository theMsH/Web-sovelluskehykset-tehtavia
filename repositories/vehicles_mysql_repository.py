from repositories.vehicles_repository import VehiclesRepository


class VehiclesMysqlRepository(VehiclesRepository):
    def __init__(self, con):
        super(VehiclesMysqlRepository, self).__init__(con)
