import numpy as np
from numpy.testing import assert_allclose
import pytest

import quantopy as qp


@pytest.fixture(autouse=True)
def random():
    np.random.seed(0)


class TestSimpleReturnsFromPrice:
    def test_return_series(self) -> None:
        # From Introduction to Computational Finance and Financial Econometrics with R, Eric Zivot
        expected = [0.0625, 0.058824]

        assert_allclose(
            qp.stats.get_simple_returns_from_price(qp.ReturnSeries([80, 85, 90])),
            expected,
            rtol=1e-1,
        )

        assert_allclose(
            qp.stats.get_simple_returns_from_price(qp.ReturnSeries([80])),
            [],
            rtol=1e-1,
        )

        assert_allclose(
            qp.stats.get_simple_returns_from_price(
                qp.ReturnSeries([], dtype="float64")
            ),
            [],
            rtol=1e-1,
        )

    def test_return_data_frame(self) -> None:
        assert_allclose(
            qp.stats.get_simple_returns_from_price(
                qp.ReturnDataFrame({"stock_1": [80, 85, 90], "stock_2": [10, 20, 30]})
            ),
            [[0.0625, 1.0], [0.058824, 0.5]],
            rtol=1e-1,
        )

        assert qp.stats.get_simple_returns_from_price(qp.ReturnDataFrame([80])).empty

        assert qp.stats.get_simple_returns_from_price(qp.ReturnDataFrame([])).empty


class TestCumulated:
    def test_return_series(self) -> None:
        # From Introduction to Computational Finance and Financial Econometrics with R, Eric Zivot
        assert_allclose(
            qp.stats.cumulated(qp.ReturnSeries([0.062500, 0.058824])),
            [1.0625, 1.1250],
            rtol=1e-1,
        )

        assert_allclose(
            qp.stats.cumulated(qp.ReturnSeries([0.500000, 0.333333])),
            [1.5, 2.0],
            rtol=1e-1,
        )

        assert_allclose(
            qp.stats.cumulated(qp.ReturnSeries([0.5])),
            [1.5],
            rtol=1e-1,
        )

        assert_allclose(
            qp.stats.cumulated(qp.ReturnSeries([], dtype="float64")),
            [],
            rtol=1e-1,
        )

    def test_return_data_frame(self) -> None:
        assert_allclose(
            qp.stats.cumulated(
                qp.ReturnDataFrame(
                    {"stock_1": [0.062500, 0.058824], "stock_2": [0.500000, 0.333333]}
                )
            ),
            [[1.0625, 1.5], [1.125001, 2.0]],
            rtol=1e-1,
        )

        assert_allclose(
            qp.stats.cumulated(qp.ReturnDataFrame([0.5])),
            [[1.5]],
            rtol=1e-1,
        )

        assert qp.stats.cumulated(qp.ReturnDataFrame([], dtype="float64")).empty


class TestRatio:
    def test_sharpe_ratio_return_series(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        # First Example
        mu = (1 + 0.25) ** (1 / 12) - 1  # monthly
        sigma = (1 + 0.1) ** (1 / 12) - 1  # monthly
        riskfree_rate = 0.1  # yearly
        rs = qp.random.generator.returns(mu, sigma, 4000)
        periodicity = qp.stats.period.MONTHLY
        rs_sharpe_ratio = qp.stats.sharpe(rs, riskfree_rate, periodicity)

        expected = (rs.annualized(periodicity) - riskfree_rate) / rs.effect_vol(
            periodicity
        )
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

        # Second Example
        mu = (1 + 0.12) ** (1 / 12) - 1  # monthly
        sigma = (1 + 0.1) ** (1 / 12) - 1  # monthly
        riskfree_rate = 0.05  # yearly
        rs = qp.random.generator.returns(mu, sigma, 4000)
        rs_sharpe_ratio = qp.stats.sharpe(rs, riskfree_rate)

        expected = (rs.annualized(periodicity) - riskfree_rate) / rs.effect_vol(
            periodicity
        )
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

    def test_sharpe_ratio_return_dataframe(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        mu = [(1 + 0.25) ** (1 / 12) - 1, (1 + 0.12) ** (1 / 12) - 1]  # monthly
        sigma = [(1 + 0.1) ** (1 / 12) - 1, (1 + 0.1) ** (1 / 12) - 1]  # monthly
        riskfree_rate = 0.1  # yearly
        periodicity = qp.stats.period.MONTHLY
        rdf = qp.random.generator.returns(mu, sigma, 10000)
        rs_sharpe_ratio = qp.stats.sharpe(rdf, riskfree_rate, periodicity)

        expected = (rdf.annualized(periodicity) - riskfree_rate) / rdf.effect_vol(
            periodicity
        )
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-1)
        assert type(rs_sharpe_ratio) is qp.ReturnSeries


class TestDrawdown:
    def test_return_series(self) -> None:
        rs = qp.random.generator.returns(0.01, 0.1, 100)
        rs_drawdown = qp.stats.drawdown(rs)
        assert type(rs_drawdown) is qp.ReturnSeries

        # Compute expected value
        wealth_index = (rs + 1).cumprod()  # type: ignore
        previous_peaks = wealth_index.cummax()
        expected = (wealth_index - previous_peaks) / previous_peaks

        assert_allclose(rs_drawdown, expected, rtol=1e-2)

    def test_return_data_frame(self) -> None:
        rs = qp.random.generator.returns([0.01, 0.02], [0.1, 0.05], 100)
        rs_drawdown = qp.stats.drawdown(rs)
        assert type(rs_drawdown) is qp.ReturnDataFrame

        # Compute expected value
        wealth_index = (rs + 1).cumprod()  # type: ignore
        previous_peaks = wealth_index.cummax()
        expected = (wealth_index - previous_peaks) / previous_peaks

        assert_allclose(rs_drawdown, expected, rtol=1e-2)
