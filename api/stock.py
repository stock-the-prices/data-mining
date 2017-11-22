from flask_injector import inject
from services.db import DBConnection
from services.news import News
from services.sentiment import Sentiment
 
import logging
import pprint
import json

@inject
def put(db_connection: DBConnection, news: News, sentiment: Sentiment, stock_id: str, mining_info: dict) -> list:
    # parameter to handler "injected", easier to test, and seperation of concerns
    logging.info("stock_id: %s", stock_id)
    logging.info("mining_info:\n%s", pprint.pformat(mining_info, 4))

    # get keywords
    query = stock_id

    articles = news.get_articles(query, mining_info['numArticlesToMine'],
                                 mining_info['startDate'] if 'startDate' in mining_info.keys() else None,
                                 mining_info['endDate'] if 'endDate' in mining_info.keys() else None
                                )

    for article in articles:
        # TODO introduce domain object to create layer of abtraction to response
        article['sentiment'] = sentiment.analyze(article['description'])    # TODO introduce domain object for sentiment

    logging.info("articles:\n%s", pprint.pformat(articles, 4))

    # conenct to DB
    # db_connection.connect()
    # db_connection.update_record(stock_id)

    return json.dumps(articles, sort_keys=True, indent=4, separators=(',', ': '))
