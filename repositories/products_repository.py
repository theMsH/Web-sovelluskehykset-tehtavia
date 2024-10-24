from werkzeug.exceptions import NotFound
import models


class ProductsRepository:

    def __init__(self, con):
        self.con = con


    def save(self, product):
        if not product.id:
            self._create(product)
        else:
            self._update_by_id(product)


    def _create(self, product):
        try:
            with self.con.cursor() as cur:
                query = "INSERT INTO products(name, description) VALUES(%s, %s)"
                params = (product.name, product.description)
                cur.execute(query, params)

                # Tässä ei tarvitse fetchaa mitään, koska meille välitettiin instanssi
                product.id = cur.lastrowid

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e


    def get_all(self):
        with self.con.cursor() as cur:
            query = "SELECT * FROM products"
            cur.execute(query)
            result = cur.fetchall()

            products_list = []
            for product in result:
                products_list.append(models.Product(product[0], product[1], product[2]))

            return products_list


    def get_by_id(self, product_id):
        with self.con.cursor() as cur:
            query = "SELECT * FROM products WHERE id = %s"
            params = (product_id,)
            cur.execute(query, params)
            result = cur.fetchone()

            if result is None:
                raise NotFound('product not found')

            return models.Product(result[0], result[1], result[2])


    def _update_by_id(self, product):
        try:
            with self.con.cursor() as cur:
                query = "UPDATE products SET name = %s, description = %s WHERE id = %s"
                params = (product.name, product.description, product.id)
                cur.execute(query, params)
                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e


    def delete_by_id(self, product_id):
        try:
            with self.con.cursor() as cur:
                query = "DELETE FROM products WHERE id = %s"
                params = (product_id,)
                cur.execute(query, params)

                if not cur.rowcount:
                    raise NotFound('product not found')

                self.con.commit()

        except Exception as e:
            self.con.rollback()
            raise e



