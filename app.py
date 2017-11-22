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
from collections import defaultdict

CONFIG = defaultdict()

CONFIG_PATH = 'config/config.json'
SWAGGER_PATH = 'swagger/'

DEPLOY_MODE_ENV_NAME = 'DEPLOY_MODE'
PORT_ENV_NAME = 'PORT'

def load_config():
    with open(CONFIG_PATH) as config_json:
        temp = json.load(config_json)
        CONFIG.update(temp[os.environ[DEPLOY_MODE_ENV_NAME]])

        if PORT_ENV_NAME in os.environ:
            CONFIG['server']['port'] = int(os.environ[PORT_ENV_NAME])
    
    logging.info("config:\n%s", pprint.pformat(CONFIG, 4))


def configure_logger():
    # server logging
    logging.getLogger().setLevel(logging.INFO)

    # app level logging
    # logging.getLogger('app').setLevel(logging.INFO)


def configure(binder: Binder) -> Binder:
    # dependency injection
    binder.bind(                # bind(interface, implementation)
        DBConnection,
        MongoDBConnection(CONFIG['db']['host'],
                          CONFIG['db']['port'],
                          CONFIG['db']['dbName'],
                          CONFIG['db']['user'],
                          CONFIG['db']['passwd']
                          )
    )

    binder.bind(                # bind(interface, implementation)
        News,
        News(CONFIG['external']['news']['apiKey'],
             CONFIG['external']['news']['host'],
             CONFIG['external']['news']['resultsPerPage']
            )
    )

    binder.bind(                # bind(interface, implementation)
        Sentiment,
        Sentiment(CONFIG['external']['sentiment']['host'])
    )

def main():
    configure_logger()
    load_config()
    app = connexion.FlaskApp(__name__,
                             port=CONFIG['server']['port'],
                             specification_dir=SWAGGER_PATH
                            )

    app.add_api('openapi.json', resolver=RestyResolver('api')) # ('api_spec_file','api_defn_folder')

    FlaskInjector(app=app.app, modules=[configure])
    app.run(threaded=True)

if __name__ == '__main__':
    main()
