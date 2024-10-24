import models


class ProductsRepository:
    def __init__(self, con):
        self.con = con


    def _create(self, product):
        try:
            with self.con.cursor() as cur:
                query = "INSERT INTO products(name, description) VALUES(%s, %s)"
                params = (product.name, product.description)
                cur.execute(query, params)

                # Tässä ei tarvitse fetchaa mitään, koska meille välitettiin instanssi
                product.id = cur.lastrowid

        except Exception as e:
            raise e


    def save(self, product):
        if product:
            self._create(product)
        else:
            pass


    def get_all(self):
        with self.con.cursor() as cur:
            query = "SELECT * FROM products"
            cur.execute(query)
            result = cur.fetchall()

            products_list = []
            for product in result:
                products_list.append(models.Product(product[0], product[1], product[2]))

            return products_list

