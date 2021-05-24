import numpy as np
import pandas._testing as tm

from quantopy import returns, simulate


class TestSimulate:
    def test_simulate_stock_price(self):
        prices_1 = simulate.stock_price(0.1, 0.05, 1000)

        returns_1 = returns.returns(prices_1)

        tm.assert_almost_equal(np.mean(returns_1), 0.1, rtol=1e-01)
        tm.assert_almost_equal(np.std(returns_1), 0.05, rtol=1e-01)
        assert len(prices_1) == 1000
