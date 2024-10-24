from repositories.products_repository import ProductsRepository


class ProductsPostgresRepository(ProductsRepository):

    def __init__(self, con):
        super(ProductsPostgresRepository, self).__init__(con)


    def _create(self, product):
        try:
            with self.con.cursor() as cur:
                query = "INSERT INTO products(name, description) VALUES(%s, %s) RETURNING id"
                params = (product.name, product.description)
                cur.execute(query, params)

                # Tässä ei tarvitse fetchaa mitään, koska meille välitettiin instanssi
                product.id = cur.fetch

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e
