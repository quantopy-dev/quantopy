import numpy as np
import pandas as pd


def stock_price(mu: float, sigma: float, size: int, initial_price: float = 1.0):
    simulated_returns = np.random.normal(mu, sigma, size - 1) + 1
    simulated_price = simulated_returns.cumprod() * initial_price
    simulated_price = np.insert(simulated_price, 0, initial_price, axis=0)

    return pd.Series(simulated_price)
