import numpy as np
import pandas.testing as tm
import pytest
from numpy.testing import assert_allclose

import quantopy as qp


@pytest.fixture(autouse=True)
def random():
    np.random.seed(0)


class TestRatio:
    def test_sharpe_ratio_return_series(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        # First Example
        mu, sigma = 0.25, 0.1  # mean and standard deviation
        riskfree_rate = 0.1
        rs = qp.random.generator.returns(mu, sigma, 4000)
        rs_sharpe_ratio = qp.ratio.sharpe(rs, riskfree_rate)

        expected = (mu - riskfree_rate) / sigma
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

        # Second Example
        mu, sigma = 0.12, 0.1  # mean and standard deviation
        riskfree_rate = 0.05
        rs = qp.random.generator.returns(mu, sigma, 4000)
        rs_sharpe_ratio = qp.ratio.sharpe(rs, riskfree_rate)

        expected = (mu - riskfree_rate) / sigma
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-2)
        assert type(rs_sharpe_ratio) is np.float64

    def test_sharpe_ratio_return_dataframe(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        mu = [0.25, 0.12]
        sigma = [0.1, 0.1]  # mean and standard deviation
        riskfree_rate = 0.1
        rdf = qp.random.generator.returns(mu, sigma, 10000)
        rs_sharpe_ratio = qp.ratio.sharpe(rdf, riskfree_rate)

        expected = (np.array(mu) - riskfree_rate) / sigma
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-1)
        assert type(rs_sharpe_ratio) is qp.ReturnSeries
