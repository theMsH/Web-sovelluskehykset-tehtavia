from bson import ObjectId
from pymongo import MongoClient
from werkzeug.exceptions import NotFound
import models
from repositories.products_repository import ProductsRepository


class ProductsMongoRepository(ProductsRepository):

    def __init__(self, con: MongoClient):
        self.db = con.sovelluskehykset_bad1
        super(ProductsMongoRepository, self).__init__(con)


    def _create(self, product):
        with self.con.start_session() as session:
            session.start_transaction()

            try:
                result = self.db.products.insert_one(models.Product.to_json(product))
                product.id = str(result.inserted_id)

                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e


    def get_all(self):
        result = self.db.products.find()

        products = []
        for product in result:
            products.append(models.Product(str(product['_id']), product['name'], product['description']))

        return products


    def get_by_id(self, product_oid):
        result = self.db.products.find( {"_id": ObjectId(product_oid)} ).to_list()

        if not result:
            raise NotFound('product not found')

        product = result[0]
        return models.Product(str(product['_id']), product['name'], product['description'])


    def _update_by_id(self, product):
        with self.con.start_session() as session:
            session.start_transaction()

            try:
                print("kävin täällä ##############################################################################################")
                self.db.products.update_one(
                    { "_id": ObjectId(product.id) },
                    { "$set":
                          { "name": product.name, "description": product.description }
                    }
                )
                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e


    def delete_by_id(self, product_oid):
        with self.con.start_session() as session:
            session.start_transaction()
            try:
                result = self.db.products.delete_one( { "_id": ObjectId(product_oid) })

                if result.deleted_count == 0:
                    raise NotFound('product not found')

                session.commit_transaction()

            except Exception as e:
                session.abort_transaction()
                raise e
