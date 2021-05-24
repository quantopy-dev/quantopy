import pandas as pd
import pandas._testing as tm
from numpy import NaN

from quantopy import returns, periods


class TestReturns:
    def test_series_returns(self):
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        prices_1 = pd.Series([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1, drop_first=False)
        tm.assert_series_equal(
            rs_1, pd.Series([NaN, 0.0241379, -0.0224466, -0.032147, 0.035587])
        )

        prices_2 = pd.Series([10.66, 11.08, 10.71, 11.59, 12.11])
        rs_2 = returns.returns(prices_2, drop_first=False)
        tm.assert_series_equal(
            rs_2, pd.Series([NaN, 0.0393996, -0.0333935, 0.0821661, 0.0448662])
        )

        # Coherence check
        tm.assert_series_equal(rs_1, prices_1 / prices_1.shift(1) - 1)
        tm.assert_series_equal(rs_2, prices_2 / prices_2.shift(1) - 1)

    def test_series_returns_with_drop(self):
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        prices_1 = pd.Series([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1)
        tm.assert_series_equal(
            rs_1.reset_index(drop=True),
            pd.Series([0.0241379, -0.0224466, -0.032147, 0.035587]),
        )

        prices_2 = pd.Series([10.66, 11.08, 10.71, 11.59, 12.11])
        rs_2 = returns.returns(prices_2)
        tm.assert_series_equal(
            rs_2.reset_index(drop=True),
            pd.Series([0.0393996, -0.0333935, 0.0821661, 0.0448662]),
        )

    def test_frame_returns(self):
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        prices = pd.DataFrame(
            {
                "stock_1": [8.7, 8.91, 8.71, 8.43, 8.73],
                "stock_2": [10.66, 11.08, 10.71, 11.59, 12.11],
            }
        )
        rs = returns.returns(prices, drop_first=False)

        expected = pd.DataFrame(
            {
                "stock_1": [NaN, 0.0241379, -0.0224466, -0.032147, 0.035587],
                "stock_2": [NaN, 0.0393996, -0.0333935, 0.0821661, 0.0448662],
            }
        )

        tm.assert_frame_equal(rs, expected)

        # Coherence check
        tm.assert_frame_equal(rs, prices / prices.shift(1) - 1)

    def test_frame_returns_with_drop(self):
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        prices = pd.DataFrame(
            {
                "stock_1": [8.7, 8.91, 8.71, 8.43, 8.73],
                "stock_2": [10.66, 11.08, 10.71, 11.59, 12.11],
            }
        )
        rs = returns.returns(prices)

        expected = pd.DataFrame(
            {
                "stock_1": [0.0241379, -0.0224466, -0.032147, 0.035587],
                "stock_2": [0.0393996, -0.0333935, 0.0821661, 0.0448662],
            }
        )

        tm.assert_series_equal(
            rs["stock_1"].reset_index(drop=True), expected["stock_1"]
        )
        tm.assert_series_equal(
            rs["stock_2"].reset_index(drop=True), expected["stock_2"]
        )


class TestCumReturns:
    def test_series_cum_returns_final(self):
        prices_1 = pd.Series([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1)

        hpr = (prices_1.iloc[-1] - prices_1.iloc[0]) / prices_1.iloc[0]

        tm.assert_almost_equal(returns.cum_returns_final(rs_1), hpr)

    def test_frame_cum_returns_final(self):
        prices = pd.DataFrame(
            {
                "stock_1": [8.7, 8.91, 8.71, 8.43, 8.73],
                "stock_2": [10.66, 11.08, 10.71, 11.59, 12.11],
            }
        )
        rs = returns.returns(prices)

        hpr_1 = (prices["stock_1"].iloc[-1] - prices["stock_1"].iloc[0]) / prices[
            "stock_1"
        ].iloc[0]
        hpr_2 = (prices["stock_2"].iloc[-1] - prices["stock_2"].iloc[0]) / prices[
            "stock_2"
        ].iloc[0]

        expected = pd.Series([hpr_1, hpr_2], index=["stock_1", "stock_2"])

        tm.assert_almost_equal(returns.cum_returns_final(rs), expected, rtol=1e-4)


class TestEar:
    def test_series_ear(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        tm.assert_almost_equal(
            returns.ear(pd.Series([0.03]), periods.QUARTERLY),
            pd.Series([0.1255]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(pd.Series([0.03]), periods.SEMIANNUAL),
            pd.Series([0.0609]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(pd.Series([0.015]), periods.QUARTERLY),
            pd.Series([0.06136]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(pd.Series([0.04]), periods.QUARTERLY),
            pd.Series([0.169859]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(pd.Series([0.005]), periods.MONTHLY),
            pd.Series([0.06168]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(pd.Series([0.01]), periods.MONTHLY),
            pd.Series([0.126825]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(pd.Series([0.0001]), periods.DAILY),
            pd.Series([0.025519]),
            rtol=1e-4,
        )


    def test_float_ear(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        tm.assert_almost_equal(
            returns.ear(0.03, periods.QUARTERLY),
            0.1255,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(0.03, periods.SEMIANNUAL),
            0.0609,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(0.015, periods.QUARTERLY),
            0.06136,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(0.04, periods.QUARTERLY),
            0.169859,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(0.005, periods.MONTHLY),
            0.06168,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(0.01, periods.MONTHLY),
            0.126825,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.ear(0.0001, periods.DAILY),
            0.025519,
            rtol=1e-4,
        )