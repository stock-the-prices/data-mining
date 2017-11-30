import logging
import pprint
import requests

from enum import Enum

class Price(object):
    # enums
    class Function(Enum):
        # the function for ext api to do
        TSERIES='TIME_SERIES_DAILY'

    class ResultSize(Enum):
        # amount of data to return
        FULL ='full'
        CMPT ='compact'     # last 30 entries

    TIME_SERIES_DAILY_FIELD = 'Time Series (Daily)'
    TIME_SERIES_PRICE_FIELD = '4. close'

    MAX_TRIES = 20

    def __init__(self, api_key: str, host: str):
        self.api_key = api_key
        self.host = host

    def create_payload(self, stock_id: str, function, result_size):
        payload = {'apikey': self.api_key,
                   'function': function,
                   'symbol': stock_id,
                   'outputsize': result_size}
        return payload


    def get_historical_daily_prices(self, stock_id: str, is_complete: bool):
        # returns list of objs {'date': date, 'price': price}
        payload = self.create_payload(stock_id, self.Function.TSERIES.value,
                                      self.ResultSize.FULL.value if is_complete else self.ResultSize.CMPT.value)
        prices = []

        num_tries = 0
        while num_tries != self.MAX_TRIES:
            num_tries += 1
            try:
                logging.info("Getting pricing information for stock %s", stock_id)
                res = requests.get(self.host, params=payload)
                if res.status_code != 200:
                    continue
                break
            except:
                logging.info("Getting pricing information for stock %s failed. Trying again.", stock_id)

        res = res.json()[self.TIME_SERIES_DAILY_FIELD]
        for day in res.keys():
            prices.append({
                'date': day,
                'price': float(res[day][self.TIME_SERIES_PRICE_FIELD])
                })

        prices = sorted(prices, key=lambda entry: entry['date'])

        logging.info("Got pricing information for %d days for stock %s", len(prices), stock_id)

        return prices
