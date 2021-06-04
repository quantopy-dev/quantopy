import numpy as np
import pandas.testing as tm
from numpy.testing import assert_allclose

import quantopy as qp


class TestReturnDataFrame:
    def test_manipulations(self):
        rdf = qp.ReturnDataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
        assert type(rdf) is qp.ReturnDataFrame

        sliced1 = rdf[["A", "B"]]
        assert type(sliced1) is qp.ReturnDataFrame

        to_series = rdf["A"]
        assert type(to_series) is qp.ReturnSeries

    def test_gmean(self):
        rs = qp.ReturnDataFrame(
            {"x": [0.9, 0.1, 0.2, 0.3, -0.9], "y": [0.05, 0.1, 0.2, -0.5, 0.2]}
        )
        expected = qp.ReturnSeries([-0.200802, -0.036209], index=["x", "y"])
        tm.assert_series_equal(rs.gmean(), expected, rtol=1e-5)
        assert type(rs.gmean()) is qp.ReturnSeries

    def test_sharpe_ratio_return_dataframe(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        mu = [0.25, 0.12]
        sigma = [0.1, 0.1]  # mean and standard deviation
        riskfree_rate = 0.1
        rdf = qp.random.generator.returns(mu, sigma, 10000)
        rs_sharpe_ratio = rdf.sharpe_ratio(riskfree_rate)

        expected = (np.array(mu) - riskfree_rate) / sigma
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-1)
        assert type(rs_sharpe_ratio) is qp.ReturnSeries
