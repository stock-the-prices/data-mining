import logging
import pprint
import requests

from services.db import DBConnection

class Rating(object):
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_rating(self, stock_id: str):
        self.db_connection.connect()

        # average sentiment
        articles = self.db_connection.get_stock_articles(stock_id)
        if articles is None or len(articles) == 0:
            # no articles, not enough information
            return None

        total_neg = 0.0
        total_pos = 0.0
        for article in articles:
            total_neg = total_neg - max(1.0, 1.5 * article['sentiment']['probability']['neg'])
            total_pos = total_pos + article['sentiment']['probability']['pos']

        avg_sentiment_rating = (total_neg + total_pos)/len(articles)

        last_price = self.db_connection.get_last_price_and_date(stock_id)['price']
        if last_price is None: return None

        price_next_day = self.db_connection.get_price_next_day(stock_id)
        if price_next_day is None: return None

        price_next_week = self.db_connection.get_price_next_week(stock_id)
        if price_next_week is None: return None


        # average price
        avg_price_rating = 0.0
        if price_next_day >= last_price:
            avg_price_rating += max((price_next_day*1.0-last_price)/last_price, 1.0)
        else:
            avg_price_rating += max((price_next_day*1.0-last_price)/last_price, -1.0)
        if price_next_week >= last_price:
            avg_price_rating += max((price_next_week*1.0-last_price)/last_price, 1.0)
        else:
            avg_price_rating += max((price_next_week*1.0-last_price)/last_price, -1.0)
        avg_price_rating = avg_price_rating/2

        self.db_connection.close()

        return (avg_sentiment_rating*0.8 + avg_price_rating*0.2)/(0.8 + 0.2)
