from repositories.products_repository import ProductsRepository


class ProductsMysqlRepository(ProductsRepository):
    def __init__(self, con):
        super(ProductsMysqlRepository, self).__init__(con)
