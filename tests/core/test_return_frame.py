import numpy as np
from numpy.testing import assert_allclose
import pandas as pd
import pandas._testing as tm

import quantopy as qp


class TestReturnDataFrame:
    def test_from_price(self):
        rdf = qp.ReturnDataFrame.from_price([80, 85, 90])
        assert type(rdf) is qp.ReturnDataFrame

        assert_allclose(
            rdf,
            [[0.0625], [0.058824]],
            rtol=1e-1,
        )

        assert_allclose(
            qp.ReturnDataFrame.from_price(
                {"stock_1": [80, 85, 90], "stock_2": [10, 20, 30]}
            ),
            [[0.0625, 1.0], [0.058824, 0.5]],
            rtol=1e-1,
        )

        assert_allclose(
            qp.ReturnDataFrame.from_price(
                pd.DataFrame({"stock_1": [80, 85, 90], "stock_2": [10, 20, 30]})
            ),
            [[0.0625, 1.0], [0.058824, 0.5]],
            rtol=1e-1,
        )

        assert qp.ReturnDataFrame.from_price([80]).empty

        assert qp.ReturnDataFrame.from_price([]).empty

        assert qp.ReturnDataFrame.from_price(
            pd.DataFrame({"stock_1": [], "stock_2": []})
        ).empty

    def test_cumulated(self) -> None:
        val = qp.ReturnDataFrame(
            {"stock_1": [0.062500, 0.058824], "stock_2": [0.500000, 0.333333]}
        ).cumulated()
        assert type(val) is qp.ReturnDataFrame

        assert_allclose(
            val,
            [[1.0625, 1.5], [1.125001, 2.0]],
            rtol=1e-1,
        )

        assert_allclose(
            qp.ReturnDataFrame([0.5]).cumulated(),
            [[1.5]],
            rtol=1e-1,
        )

        assert qp.ReturnDataFrame([], dtype="float64").cumulated().empty

    def test_mean(self) -> None:
        arithmetic_mean = qp.ReturnDataFrame(
            {"stock_1": [0.062500, 0.058824], "stock_2": [0.500000, 0.333333]}
        ).mean()
        assert type(arithmetic_mean) is qp.ReturnSeries

        assert_allclose(
            arithmetic_mean,
            [0.060662, 0.416666],
            rtol=1e-1,
        )

    def test_gmean(self):
        rs = qp.ReturnDataFrame(
            {"x": [0.9, 0.1, 0.2, 0.3, -0.9], "y": [0.05, 0.1, 0.2, -0.5, 0.2]}
        )
        expected = qp.ReturnSeries([-0.200802, -0.036209], index=["x", "y"])
        tm.assert_series_equal(rs.gmean(), expected, rtol=1e-5)
        assert type(rs.gmean()) is qp.ReturnSeries

    def test_manipulations(self):
        rdf = qp.ReturnDataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
        assert type(rdf) is qp.ReturnDataFrame

        sliced1 = rdf[["A", "B"]]
        assert type(sliced1) is qp.ReturnDataFrame

        to_series = rdf["A"]
        assert type(to_series) is qp.ReturnSeries

    def test_sharpe_ratio(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        mu = [(1 + 0.25) ** (1 / 12) - 1, (1 + 0.12) ** (1 / 12) - 1]  # monthly
        sigma = [(1 + 0.1) ** (1 / 12) - 1, (1 + 0.1) ** (1 / 12) - 1]  # monthly
        riskfree_rate = 0.1  # yearly
        periodicity = qp.stats.period.MONTHLY
        rdf = qp.random.generator.returns(mu, sigma, 10000)
        rs_sharpe_ratio = rdf.sharpe_ratio(riskfree_rate, periodicity)

        expected = (rdf.effect(periodicity) - riskfree_rate) / rdf.effect_vol(
            periodicity
        )
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-1)
        assert type(rs_sharpe_ratio) is qp.ReturnSeries

    def test_return_data_frame(self) -> None:
        rs = qp.random.generator.returns([0.01, 0.02], [0.1, 0.05], 100)
        rs_drawdown = rs.drawdown()
        assert type(rs_drawdown) is qp.ReturnDataFrame

        # Compute expected value
        wealth_index = (rs + 1).cumprod()  # type: ignore
        previous_peaks = wealth_index.cummax()
        expected = (wealth_index - previous_peaks) / previous_peaks

        assert_allclose(rs_drawdown, expected, rtol=1e-2)

    def test_effect(self):
        mu_list = [0.03, 0.015, 0.04, 0.005, 0.01]  # mean
        sigma_list = [0.01, 0.01, 0.01, 0.01, 0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 12 - 1

        effect = rdf.effect(qp.stats.period.MONTHLY)
        assert type(effect) is qp.ReturnSeries

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )

    def test_return_dataframe(self):
        mu_list = [0.01]  # mean
        sigma_list = [0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = qp.ReturnSeries(sigma_list) * np.sqrt(252)

        effect = rdf.effect_vol(qp.stats.period.DAILY)
        assert type(effect) is qp.ReturnSeries

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )

    def test_total_return(self):
        pdf = pd.DataFrame(
            {
                "stock_1": [8.7, 8.91, 8.71, 8.43, 8.73],
                "stock_2": [10.66, 11.08, 10.71, 11.59, 12.11],
            }
        )
        rdf = qp.ReturnDataFrame.from_price(pdf)

        rdf_total_return = rdf.total_return()
        assert type(rdf_total_return) is qp.ReturnSeries

        hpr_1 = (pdf["stock_1"].iloc[-1] - pdf["stock_1"].iloc[0]) / pdf[
            "stock_1"
        ].iloc[0]
        hpr_2 = (pdf["stock_2"].iloc[-1] - pdf["stock_2"].iloc[0]) / pdf[
            "stock_2"
        ].iloc[0]

        expected = qp.ReturnSeries([hpr_1, hpr_2], index=["stock_1", "stock_2"])

        tm.assert_almost_equal(rdf_total_return, expected, rtol=1e-4)
