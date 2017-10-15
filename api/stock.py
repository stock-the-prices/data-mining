from flask_injector import inject
from services.db import DbConnection

@inject
def post(db_connection: DbConnection, stock: dict) -> list:
    # parameter to handler "injected", easier to test, and seperation of concerns
    db_connection.connect()
    db_connection.update_news(stock)
    return stock
