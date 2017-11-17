import connexion

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver

from services.db import DBConnection, MongoDBConnection
from services.news import News
from services.sentiment import Sentiment

import pprint
import logging
import json
import os

env = {}
config = {}

CONFIG_PATH = 'config/config.json'
SWAGGER_PATH = 'swagger/'

def load_env():
    env['SERVER_HOST'] = os.environ['DATA_MINER_HOST']
    env['SERVER_PORT'] = os.environ['DATA_MINER_PORT']

    env['MONGODB_HOST'] = os.environ['MONGODB_HOST']
    env['MONGODB_PORT'] = int(os.environ['MONGODB_PORT'])

    env['NEWS_API_KEY'] = os.environ['NEWS_API_KEY']

    logging.info("env:\n%s", pprint.pformat(env, 4))
    


def load_config():
    with open(CONFIG_PATH) as config_json:
        config.update(json.load(config_json))
    
    logging.info("config:\n%s", pprint.pformat(config, 4))


def configure_logger():
    # server logging
    logging.getLogger().setLevel(logging.INFO)

    # app level logging
    # logging.getLogger('app').setLevel(logging.INFO)


def configure(binder: Binder) -> Binder:
    # dependency injection
    binder.bind(                # bind(interface, implementation)
        DBConnection,
        MongoDBConnection(env['MONGODB_HOST'], env['MONGODB_PORT'])
    )

    binder.bind(                # bind(interface, implementation)
        News,
        News(env['NEWS_API_KEY'], config['news']['url'], config['news']['resultsPerPage'])
    )

    binder.bind(                # bind(interface, implementation)
        Sentiment,
        Sentiment(config['sentiment']['url'])
    )

def main():
    configure_logger()
    load_env()
    load_config()
    app = connexion.FlaskApp(__name__, port=env['SERVER_PORT'], specification_dir=SWAGGER_PATH)
    app.add_api('openapi.json', resolver=RestyResolver('api')) # ('api_spec_file', 'api_defn_folder')

    FlaskInjector(app=app.app, modules=[configure])
    app.run()

if __name__ == '__main__':
    main()
