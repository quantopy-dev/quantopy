import pandas.testing as tm
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
