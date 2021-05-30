import pandas as pd
import pandas._testing as tm
from numpy import NaN
import numpy as np

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

    def test_array_returns(self):
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        prices_1 = np.array([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1, drop_first=False)
        np.testing.assert_array_almost_equal(
            rs_1, np.array([NaN, 0.02413793, -0.02244669, -0.03214696, 0.03558719])
        )

        prices_2 = np.array([10.66, 11.08, 10.71, 11.59, 12.11])
        rs_2 = returns.returns(prices_2, drop_first=False)
        np.testing.assert_array_almost_equal(
            rs_2, np.array([NaN, 0.0393996, -0.0333935, 0.0821661, 0.0448662])
        )

    def test_array_returns_with_drop(self):
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        prices_1 = np.array([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1)
        np.testing.assert_array_almost_equal(
            rs_1,
            np.array([0.0241379, -0.0224466, -0.032147, 0.035587]),
        )

        prices_2 = np.array([10.66, 11.08, 10.71, 11.59, 12.11])
        rs_2 = returns.returns(prices_2)
        np.testing.assert_array_almost_equal(
            rs_2,
            np.array([0.0393996, -0.0333935, 0.0821661, 0.0448662]),
        )


class TestCumReturns:
    def test_series_total_return(self):
        prices_1 = pd.Series([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1)

        hpr = (prices_1.iloc[-1] - prices_1.iloc[0]) / prices_1.iloc[0]

        print(rs_1)
        print(hpr)

        tm.assert_almost_equal(returns.total_return(rs_1), hpr)

    def test_frame_total_return(self):
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

        tm.assert_almost_equal(returns.total_return(rs), expected, rtol=1e-4)

    def test_array_total_return(self):
        prices_1 = np.array([8.7, 8.91, 8.71, 8.43, 8.73])
        rs_1 = returns.returns(prices_1)

        hpr = (prices_1[-1] - prices_1[0]) / prices_1[0]

        tm.assert_almost_equal(returns.total_return(rs_1), hpr)


class TestEffect:
    def test_series_effect(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        tm.assert_almost_equal(
            returns.effect(pd.Series([0.03, 0.015, 0.04]), periods.Period.QUARTERLY),
            pd.Series([0.1255, 0.06136, 0.169859]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(pd.Series([0.03]), periods.Period.SEMIANNUAL),
            pd.Series([0.0609]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(pd.Series([0.005, 0.01]), periods.Period.MONTHLY),
            pd.Series([0.06168, 0.126825]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(pd.Series([0.0001]), periods.Period.DAILY),
            pd.Series([0.025519]),
            rtol=1e-4,
        )

    def test_array_effect(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        np.testing.assert_array_almost_equal(
            returns.effect(np.array([0.03, 0.015, 0.04]), periods.Period.QUARTERLY),
            np.array([0.125509, 0.061364, 0.169859]),
        )

        np.testing.assert_array_almost_equal(
            returns.effect(np.array([0.03]), periods.Period.SEMIANNUAL),
            np.array([0.0609]),
        )

        np.testing.assert_array_almost_equal(
            returns.effect(np.array([0.005, 0.01]), periods.Period.MONTHLY),
            np.array([0.061678, 0.126825]),
        )

        np.testing.assert_array_almost_equal(
            returns.effect(np.array([0.0001]), periods.Period.DAILY),
            np.array([0.025519]),
        )

    def test_float_effect(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        tm.assert_almost_equal(
            returns.effect(0.03, periods.Period.QUARTERLY),
            0.1255,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(0.03, periods.Period.SEMIANNUAL),
            0.0609,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(0.015, periods.Period.QUARTERLY),
            0.06136,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(0.04, periods.Period.QUARTERLY),
            0.169859,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(0.005, periods.Period.MONTHLY),
            0.06168,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(0.01, periods.Period.MONTHLY),
            0.126825,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect(0.0001, periods.Period.DAILY),
            0.025519,
            rtol=1e-4,
        )


class TestEffectVol:
    def test_series_effect_vol(self):
        # From Wikipedia - https://en.wikipedia.org/wiki/Volatility_(finance)
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        tm.assert_almost_equal(
            returns.effect_vol(pd.Series([0.01]), periods.Period.DAILY),
            pd.Series([0.15874]),
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect_vol(pd.Series([0.02397, 0.079601]), periods.Period.MONTHLY),
            pd.Series([0.0830345, 0.275747]),
            rtol=1e-4,
        )

    def test_array_effect_vol(self):
        # From Wikipedia - https://en.wikipedia.org/wiki/Volatility_(finance)
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        np.testing.assert_array_almost_equal(
            returns.effect_vol(np.array([0.01]), periods.Period.DAILY),
            np.array([0.158745]),
        )

        tm.assert_almost_equal(
            returns.effect_vol(np.array([0.02397, 0.079601]), periods.Period.MONTHLY),
            np.array([0.0830345, 0.275747]),
            rtol=1e-4,
        )

    def test_float_effect_vol(self):
        # From Wikipedia - https://en.wikipedia.org/wiki/Volatility_(finance)
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk
        tm.assert_almost_equal(
            returns.effect_vol(0.01, periods.Period.DAILY),
            0.15874,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect_vol(0.02397, periods.Period.MONTHLY),
            0.0830345,
            rtol=1e-4,
        )

        tm.assert_almost_equal(
            returns.effect_vol(0.079601, periods.Period.MONTHLY),
            0.275747,
            rtol=1e-4,
        )
