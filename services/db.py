from pymongo import MongoClient
import logging
import pprint
import datetime
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
    def get_record(self, stock_id: str):
        # get stock record
        pass

    @abstractmethod
    def insert_new_stock(self, stock_id: str):
        # insert new stock
        pass

    @abstractmethod
    def update_pricing(self, stock_id, historical_prices,
                       price_next_day,
                       price_next_week):
        # update record on DB
        pass

    @abstractmethod
    def update_articles(self, stock_id, articles):
        # update record on DB
        pass

    @abstractmethod
    def update_rating(self, stock_id, rating: float):
        # update record on DB
        pass

    @abstractmethod
    def close(self):
        # close connection
        pass

    @abstractmethod
    def get_stock_articles(self, stock_id: str):
        pass

    @abstractmethod
    def get_last_price_and_date(self, stock_id: str):
        pass

    @abstractmethod
    def get_price_next_day(self, stock_id: str):
        pass

    @abstractmethod
    def get_price_next_week(self, stock_id: str):
        pass



class MongoDBConnection(DBConnection):
    """
    Facade for MongoDB client.
    Wraps the client and introduce business-logic specific methods.
    """

    # Creates DBConnection
    def __init__(self, host: str, port: int, dbName: str, user: str, passwd: str):
        self.dbName = dbName
        self.user = user
        self.passwd = passwd

        super().__init__(host, port)

    client = None
    db = None

    def connect(self):
        if not self.client:
            logging.info("Establishing connection to MongoDB")

            if self.user == "":
                uri = "mongodb://%s:%s" % (self.host, self.port)
            else:
                uri = "mongodb://%s:%s@%s:%s/%s" % (self.user, self.passwd, self.host, self.port, self.dbName)

            self.client = MongoClient(uri)

            # might fail if user but no pass
            self.db = self.client[self.dbName]

    def close(self):
        # close connection
        if not self.client: return
        self.client.close()
        self.client = None
        self.db = None

    def get_stock_articles(self, stock_id: str):
        if not self.client: return None
        articles = []
        stock_query = {'_id': stock_id}
        a_ids = self.db.stock.find_one(stock_query, {'articles': 1})
        if a_ids is None: return None
        a_ids = a_ids['articles']
        for a_id in a_ids:
            articles.append(self.db.article.find_one({'_id': a_id}))
        return articles

    def get_last_price_and_date(self, stock_id: str):
        if not self.client: return None
        stock_query = {'_id': stock_id}
        last_price_and_date = self.db.stock.find_one(stock_query, {"prices": {"$slice": -1}})
        if last_price_and_date is None: return None
        last_price_and_date = last_price_and_date['prices'][0]
        return last_price_and_date

    def get_price_next_day(self, stock_id: str):
        if not self.client: return None
        stock_query = {'_id': stock_id}
        price_next_day = self.db.stock.find_one(stock_query, {'price_next_day': 1})
        if price_next_day is None: return None
        price_next_day = price_next_day['price_next_day']
        return price_next_day

    def get_price_next_week(self, stock_id: str):
        if not self.client: return None
        stock_query = {'_id': stock_id}
        price_next_week = self.db.stock.find_one(stock_query, {'price_next_week': 1})
        if price_next_week is None: return None
        price_next_week = price_next_week['price_next_week']
        return price_next_week

    def insert_new_stock(self, stock_id: str):
        # schema
        if not self.client: return
        new_stock = {
            "_id": stock_id,
	        "date_updated": datetime.datetime.utcnow(),
	        "articles": [],
            "prices": [],
            "price_next_day": None,
            "price_next_week": None,
            "rating": None
        }
        logging.warning("Inserted new stock record for %s", stock_id)

        return self.db.stock.insert_one(new_stock).inserted_id

    def get_record(self, stock_id):
        if not self.client: return
        stock_query = {"_id": stock_id}
        record = self.db.stock.find_one(stock_query)
        return record

    def update_pricing(self, stock_id, historical_prices=None,
                       price_next_day=None,
                       price_next_week=None):
        if not self.client: return

        stocks = self.db.stock
        stock_query = {"_id": stock_id}

        if self.get_record(stock_id) is None:
            self.insert_new_stock(stock_id)

        # update pricing
        if historical_prices is not None:
            stocks.update_one(stock_query, {'$set': {'prices': historical_prices}})
            logging.info("Updated stock %s record with historical pricing information", stock_id)

        if price_next_day is not None:
            stocks.update_one(stock_query, {'$set': {'price_next_day': price_next_day}})
            logging.info("Updated stock %s record with tomorrow's price", stock_id)

        if price_next_week is not None:
            stocks.update_one(stock_query, {'$set': {'price_next_week': price_next_week}})
            logging.info("Updated stock %s record with next week's price", stock_id)

        # update stock updated time
        stocks.update_one(stock_query, {'$set': {"date_updated": datetime.datetime.utcnow()}})
        logging.info("Updated pricing of stock: %s", stock_id)

    def update_articles(self, stock_id: str, new_articles):
        # update record on DB with articles
        # article DNE: create article document -> insert into stock document
        # OR article exists: if article linked to stock -> do nothing ELSE link to stock

        if not self.client: return

        stocks = self.db.stock
        articles = self.db.article
        stock_query = {"_id": stock_id}

        record = self.get_record(stock_id)
        if record is None:
            # insert stock if necessary
            self.insert_new_stock(stock_id)
            record = self.get_record(stock_id)

        # update articles
        for art in new_articles:
            logging.info("Processing article: %s", art['title'])
            article_record = articles.find_one({"title": art['title']})
            if article_record is None:
                # new article
                a_id = articles.insert_one(art).inserted_id
                logging.info("Inserted new article: %s", art['title'])
            else:
                # old article
                a_id = article_record['_id']

                record = self.get_record(stock_id)

                if a_id in record['articles']:
                    # article already in stock record
                    continue

            stocks.update_one(stock_query, {'$push': {'articles': a_id}})
            logging.info("Updated stock %s record with article: %s", stock_id, art['title'])

        # update stock updated time
        stocks.update_one(stock_query, {'$set': {"date_updated": datetime.datetime.utcnow()}})
        logging.info("Updated articles of stock: %s", stock_id)

    def update_rating(self, stock_id: str, rating: float):
        if not self.client: return

        stock_query = {"_id": stock_id}

        record = self.get_record(stock_id)
        if record is None:
            # insert stock if necessary
            self.insert_new_stock(stock_id)

        self.db.stock.update_one(stock_query, {'$set': {'rating': rating}})
        logging.info("Updated rating of stock %s to %f", stock_id, rating)
