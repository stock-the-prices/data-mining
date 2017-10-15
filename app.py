import connexion

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver

from services.db import DbConnection, DbConnectionFactory

import logging
import json
import os


SERVER_HOST = os.environ['DATA_MINER_HOST']
SERVER_PORT = os.environ['DATA_MINER_PORT']

MONGODB_HOST = os.environ['MONGODB_HOST']
MONGODB_PORT = int(os.environ['MONGODB_PORT'])

CONFIG_PATH = 'config/config.json'
SWAGGER_PATH = 'swagger/'

def load_config() -> dict:
    with open(CONFIG_PATH) as config_json:
        return json.load(config_json)

def configure_logger():
    # server logging
    logging.getLogger().setLevel(logging.INFO)

    # app level logging
    logging.getLogger('app').setLevel(logging.INFO)


def configure(binder: Binder) -> Binder:
    # dependency injection
    binder.bind(                # bind(interface, implementation)
        DbConnection,
        DbConnection(
            DbConnectionFactory(
                MONGODB_HOST,
                MONGODB_PORT
            )
        )
    )

def main():
    configure_logger()
    config = load_config()

    app = connexion.FlaskApp(__name__, port=SERVER_PORT, specification_dir=SWAGGER_PATH)
    app.add_api('data_mine.yaml', resolver=RestyResolver('api')) # ('api_spec_file', 'api_defn_folder')

    FlaskInjector(app=app.app, modules=[configure])
    app.run()

if __name__ == '__main__':
    main()
