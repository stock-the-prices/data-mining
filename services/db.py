from pymongo import MongoClient
import logging
import pprint
from abc import ABC, ABCMeta, abstractmethod


class DBConnection(ABC):
    """
    An abstract DBConnection. Decouples interface from implementation.
    Allows clients to interface with their database dependency in an abstract way so that
    it is not implementation specific (decoupled from implementation). Standarized interface of different DBs.
    """
    __metaclass__ = ABCMeta

    # Creates DBConnection
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        super().__init__()

    @abstractmethod
    def connect(self):
        # connect to db
        pass

    @abstractmethod
    def update_record(self, stock: str):
        # update record on DB
        pass

# class DBConnectionFactory(ABC):
#     """ Abstract factory to create DBConnection. Decoupled from the instantiation of DBConnection. """
#     __metaclass__ = ABCMeta

#     # Creates DBConnectionFactory by setting up common fields
#     def __init__(self, host: str, port: int):
#         self.host = host
#         self.port = port
#         super().__init__()

#     @abstractmethod
#     def create(self) -> DBConnection:
#         # create db client
#         pass

class MongoDBConnection(DBConnection):
    """
    Facade for MongoDB client.
    Wraps the client and introduce business-logic specific methods.
    """
    
    # Creates DBConnection
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    connection = None

    def connect(self):
        logging.info("Establishing connection to MongoDB")
        if not self.connection:
            self.connection = MongoClient(self.host, self.port)        

    def update_record(self, stock: str):
        # update record on DB
        print("DB test")
        db = self.connection.test_database
        result = db.test_database.insert_one({
            "name": "David"
        })

# class MongoDBConnectionFactory(DBConnectionFactory):
#     @abstractmethod
#     def create(self) -> MongoDBConnection:
#         # create mongo db connection
#         return MongoDBConnection(self.host, self.port)

