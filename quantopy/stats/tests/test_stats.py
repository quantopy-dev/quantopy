import numpy as np
import pandas.testing as tm
from numpy.testing import assert_allclose

import quantopy as qp


class TestGeoMean:
    def test_return_series(self) -> None:
        rs = qp.ReturnSeries([0.9, 0.1, 0.2, 0.3, -0.9])
        rs_gmean = qp.stats.gmean(rs)
        assert_allclose(rs_gmean, -0.200802, rtol=1e-5)
        assert type(rs_gmean) is np.float64

        rs = qp.ReturnSeries([0.05, 0.1, 0.2, -0.5, 0.2])
        rs_gmean = qp.stats.gmean(rs)
        assert_allclose(rs_gmean, -0.03621, rtol=1e-4)
        assert type(rs_gmean) is np.float64

        rs = qp.ReturnSeries([0.2, 0.06, 0.01, 0.1])
        sliced1 = rs[:3]
        rs_gmean = qp.stats.gmean(sliced1)  # type: ignore
        assert_allclose(rs_gmean, 0.0871, rtol=1e-3)
        assert type(rs_gmean) is np.float64

    def test_return_dataframe(self) -> None:
        rs = qp.ReturnDataFrame(
            {"x": [0.9, 0.1, 0.2, 0.3, -0.9], "y": [0.05, 0.1, 0.2, -0.5, 0.2]}
        )
        rs_gmean = qp.stats.gmean(rs)
        expected = qp.ReturnSeries([-0.200802, -0.036209], index=["x", "y"])
        tm.assert_series_equal(rs_gmean, expected, rtol=1e-5)  # type: ignore
        assert type(rs_gmean) is qp.ReturnSeries

        sliced1 = rs["x"]
        rs_gmean = qp.stats.gmean(sliced1)  # type: ignore
        assert_allclose(rs_gmean, -0.200802, rtol=1e-5)
        assert type(rs_gmean) is np.float64
