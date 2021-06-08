import numpy as np
from numpy.testing import assert_allclose
import pytest

import quantopy as qp


@pytest.fixture(autouse=True)
def random():
    np.random.seed(0)


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

        expected = (rs.effect(periodicity) - riskfree_rate) / rs.effect_vol(periodicity)
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

        # Second Example
        mu = (1 + 0.12) ** (1 / 12) - 1  # monthly
        sigma = (1 + 0.1) ** (1 / 12) - 1  # monthly
        riskfree_rate = 0.05  # yearly
        rs = qp.random.generator.returns(mu, sigma, 4000)
        rs_sharpe_ratio = qp.stats.sharpe(rs, riskfree_rate)

        expected = (rs.effect(periodicity) - riskfree_rate) / rs.effect_vol(periodicity)
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

        expected = (rdf.effect(periodicity) - riskfree_rate) / rdf.effect_vol(
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
