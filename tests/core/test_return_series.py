import numpy as np
import pandas as pd
import pytest
import quantopy as qp
from numpy.testing import assert_allclose


@pytest.fixture(autouse=True)
def random():
    np.random.seed(0)


class TestReturnSeries:
    def test_manipulations(self):
        rs = qp.ReturnSeries([1, 2, 3])
        assert type(rs) is qp.ReturnSeries

        to_framed = rs.to_frame()
        assert type(to_framed) is qp.ReturnDataFrame

        sliced1 = rs[:2]
        assert type(sliced1) is qp.ReturnSeries

    def test_gmean(self):
        rs = qp.ReturnSeries([0.9, 0.1, 0.2, 0.3, -0.9])
        assert_allclose(rs.gmean(), -0.200802, rtol=1e-5)
        assert type(rs.gmean()) is np.float64

    def test_sharpe_ratio(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        mu, sigma = 0.25, 0.1  # mean and standard deviation
        riskfree_rate = 0.1
        rs = qp.random.generator.returns(mu, sigma, 4000)
        rs_sharpe_ratio = rs.sharpe_ratio(riskfree_rate)

        expected = (mu - riskfree_rate) / sigma
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

    def test_effect(self):
        mu = 0.03  # mean
        sigma = 0.01  # standard deviation
        rs = qp.random.generator.returns(mu, sigma, 1000)

        expected = (mu + 1) ** 12 - 1

        effect = rs.effect(qp.stats.period.MONTHLY)
        assert type(effect) is np.float64

        assert_allclose(
            effect,
            expected,
            rtol=1e-1,
        )

    def test_effect_vol(self):
        mu = 0.01  # mean
        sigma = 0.01  # standard deviation
        rs = qp.random.generator.returns(mu, sigma, 1000)

        expected = sigma * np.sqrt(252)

        effect = rs.effect_vol(qp.stats.period.DAILY)
        assert type(effect) is np.float64

        assert_allclose(
            effect,
            expected,
            rtol=1e-1,
        )

    def test_total_return(self):
        ps = pd.Series([8.7, 8.91, 8.71, 8.43, 8.73])
        rs = qp.ReturnSeries.from_price(ps)

        rs_total_return = rs.total_return()
        assert type(rs_total_return) is np.float64

        hpr = (ps.iloc[-1] - ps.iloc[0]) / ps.iloc[0]

        assert_allclose(
            rs_total_return,
            hpr,
            rtol=1e-1,
        )
