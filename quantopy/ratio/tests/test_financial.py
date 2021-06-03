import numpy as np
import pandas.testing as tm
import pytest
from numpy.testing import assert_allclose

import quantopy as qp


@pytest.fixture(autouse=True)
def random():
    np.random.seed(0)


class TestRatio:
    def test_sharpe_ratio(self) -> None:
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

    # def test_return_dataframe(self) -> None:
    #     rs = qp.ReturnDataFrame(
    #         {"x": [0.9, 0.1, 0.2, 0.3, -0.9], "y": [0.05, 0.1, 0.2, -0.5, 0.2]}
    #     )
    #     rs_gmean = qp.stats.gmean(rs)
    #     expected = qp.ReturnSeries([-0.200802, -0.036209], index=["x", "y"])
    #     tm.assert_series_equal(rs_gmean, expected, rtol=1e-5)  # type: ignore
    #     assert type(rs_gmean) is qp.ReturnSeries

    #     sliced1 = rs["x"]
    #     rs_gmean = qp.stats.gmean(sliced1)  # type: ignore
    #     assert_allclose(rs_gmean, -0.200802, rtol=1e-5)
    #     assert type(rs_gmean) is np.float64
