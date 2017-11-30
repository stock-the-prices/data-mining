import logging
import pprint
import math
import numpy as np

from enum import Enum

class Prediction(object):
    # enums
    lookback_factor = 7
    sorted_prices = None

    class Time(Enum):
        DAY = 1
        WEEK = 7
        MONTH = 30
        YEAR = 356
        DECADE = 3560

    def __init__(self):
        pass

    def setup(self, prices: dict):
        # create a regression based on the prices
        self.sorted_prices = sorted([(day, prices[day]) for day in prices.keys()], key=lambda d: d[0])

    def create_regression(self, num_points):
        # create regression based on # points
        if self.sorted_prices is None:
            return None

        x = [i for i in range(num_points)]
        y = [self.sorted_prices[-i][1] for i in range(num_points, 0, -1)]

        x = np.array(x)
        y = np.array(y)

        order = math.log(num_points)
        poly_fit = np.polyfit(x, y, order)
        return np.poly1d(poly_fit)


    def predict(self, time: int):
        # predicts the price for sometime in the future
        if self.sorted_prices is None: return None

        num_points = time * self.lookback_factor
        if num_points > len(self.sorted_prices):
            return None

        regression = self.create_regression(num_points)
        logging.info("Created regression")

        return regression(num_points - 1 + time)
