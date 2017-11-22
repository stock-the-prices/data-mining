from flask_injector import inject
from services.db import DBConnection
from services.news import News
from services.sentiment import Sentiment
 
import logging
import pprint

@inject
def put(db_connection: DBConnection, news: News, sentiment: Sentiment, stock_id: str, mining_info: dict) -> list:
    # parameter to handler "injected", easier to test, and seperation of concerns
    logging.info("Stock id: %s", stock_id)
    logging.info("Mining info:\n%s", pprint.pformat(mining_info, 4))

    # get keywords
    query = stock_id

    articles = news.get_articles(query, mining_info['numArticlesToMine'],
                                 mining_info['startDate'] if 'startDate' in mining_info.keys() else None,
                                 mining_info['endDate'] if 'endDate' in mining_info.keys() else None
                                )

    for article in articles:
        # TODO introduce domain object to create layer of abtraction to response
        text = article['title'] if article['description'] is None else article['description']
        article['sentiment'] = sentiment.analyze(text)    # TODO introduce domain object for sentiment

    logging.info("articles:\n%s", pprint.pformat(articles, 4))

    # conenct to DB
    db_connection.connect()
    stock_record = db_connection.update_record(stock_id, articles)
    return {'stock': stock_record['_id'], 'updated': str(stock_record['date_updated'])}
