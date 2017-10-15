from pymongo import MongoClient
import logging

class DbConnectionFactory(object):
    # decouple implementation from interface.
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create(self) -> MongoClient:
        # create mongo  client
        return MongoClient(self.host, self.port)
    

class DbConnection(object):
    def __init__(
            self, 
            db_factory: DbConnectionFactory
    ):
        self.db_factory = db_factory
        self.connection = None

    def connect(self):
        logging.getLogger('app').info("Establishing connection")
        if not self.connection:
            self.connection = self.db_factory.create()
        return self.connection

    def update_news(self, payload: dict) -> bool:
        print("Updated news")
        db = self.connection.test_database

        result = db.test_database.insert_one({
            "name": "David"
        })

        print(result)
        # TODO self.connection()
