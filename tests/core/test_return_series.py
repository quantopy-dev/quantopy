import numpy as np
import quantopy as qp
from numpy.testing import assert_allclose


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
