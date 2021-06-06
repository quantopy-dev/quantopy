import numpy as np
import pandas.testing as tm
import pytest
import quantopy as qp
from numpy.testing import assert_allclose


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
        rs_sharpe_ratio = qp.ratio.sharpe(rs, riskfree_rate, periodicity)

        expected = (rs.effect(periodicity) - riskfree_rate) / rs.effect_vol(periodicity)
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

        # Second Example
        mu = (1 + 0.12) ** (1 / 12) - 1  # monthly
        sigma = (1 + 0.1) ** (1 / 12) - 1  # monthly
        riskfree_rate = 0.05  # yearly
        rs = qp.random.generator.returns(mu, sigma, 4000)
        rs_sharpe_ratio = qp.ratio.sharpe(rs, riskfree_rate)

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
        rs_sharpe_ratio = qp.ratio.sharpe(rdf, riskfree_rate, periodicity)

        expected = (rdf.effect(periodicity) - riskfree_rate) / rdf.effect_vol(
            periodicity
        )
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-1)
        assert type(rs_sharpe_ratio) is qp.ReturnSeries
