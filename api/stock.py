from flask_injector import inject
from services.db import DBConnection
from services.news import News
from services.sentiment import Sentiment
from services.price import Price
from services.prediction import Prediction
from services.rating import Rating

import logging
import pprint

@inject
def put(db_connection: DBConnection,
        news: News,
        sentiment: Sentiment,
        pricing: Price,
        prediction: Prediction,
        rating: Rating,
        stock_id: str, mining_info: dict) -> list:
    # parameter to handler "injected", easier to test, and seperation of concerns
    logging.info("Stock id: %s", stock_id)
    logging.info("Mining info:\n%s", pprint.pformat(mining_info, 4))

    # get keywords
    query = stock_id + " stock"

    articles = news.get_articles(query, mining_info['numArticlesToMine'],
                                 mining_info['startDate'] if 'startDate' in mining_info.keys() else None,
                                 mining_info['endDate'] if 'endDate' in mining_info.keys() else None)
    logging.info("Got article information for %s", stock_id)

    for article in articles:
        # TODO introduce domain object to create layer of abtraction to response
        text = article['title']
        if article['description'] is not None:
            text += ": " + article['description']
        article['sentiment'] = sentiment.analyze(text)    # TODO introduce domain object for sentiment

    logging.info("Finished article sentiment analysis for %s", stock_id)

    historical_pricing = pricing.get_historical_daily_prices(stock_id, True) # TODO true for prod
    # logging.info("Got pricing information for %s", stock_id)

    # price prediction
    prediction.seed(historical_pricing)
    price_next_day = prediction.predict(Prediction.Time.DAY.value)
    price_next_week = prediction.predict(Prediction.Time.WEEK.value)

    logging.info("Finished price prediction for %s", stock_id)


    # conenct to DB
    db_connection.connect()
    db_connection.update_articles(stock_id, articles)
    db_connection.update_pricing(stock_id, historical_pricing,
                                           price_next_day,
                                           price_next_week)

    # get rating
    rating = rating.get_rating(stock_id)
    logging.info("Calculated rating for %s", stock_id)

    db_connection.update_rating(stock_id, rating)

    stock_record = db_connection.get_record(stock_id)
    db_connection.close()

    return {'stock': stock_record['_id'], 'updated': str(stock_record['date_updated'])}
