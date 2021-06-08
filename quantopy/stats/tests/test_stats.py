import numpy as np
from numpy.testing import assert_allclose
import pandas as pd
import pandas._testing as tm

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
        rs_gmean = qp.stats.gmean(sliced1)
        assert_allclose(rs_gmean, 0.0871, rtol=1e-3)
        assert type(rs_gmean) is np.float64

    def test_return_dataframe(self) -> None:
        rs = qp.ReturnDataFrame(
            {"x": [0.9, 0.1, 0.2, 0.3, -0.9], "y": [0.05, 0.1, 0.2, -0.5, 0.2]}
        )
        rs_gmean = qp.stats.gmean(rs)
        expected = qp.ReturnSeries([-0.200802, -0.036209], index=["x", "y"])
        tm.assert_series_equal(rs_gmean, expected, rtol=1e-5)
        assert type(rs_gmean) is qp.ReturnSeries

        sliced1 = rs["x"]
        rs_gmean = qp.stats.gmean(sliced1)
        assert_allclose(rs_gmean, -0.200802, rtol=1e-5)
        assert type(rs_gmean) is np.float64


class TestEffect:
    def test_return_dataframe(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk

        # 1. Test with monthly period
        mu_list = [0.03, 0.015, 0.04, 0.005, 0.01]  # mean
        sigma_list = [0.01, 0.01, 0.01, 0.01, 0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 12 - 1

        effect = qp.stats.effect(rdf, qp.stats.period.MONTHLY)
        assert type(effect) is qp.ReturnSeries

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )

        # 2. Test with semiannual period
        mu_list = [0.03]  # mean
        sigma_list = [0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 200)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 2 - 1

        tm.assert_almost_equal(
            qp.stats.effect(rdf, qp.stats.period.SEMIANNUAL),
            expected,
            rtol=1e-1,
        )

        # 3. Test with daily period
        mu_list = [0.0001]  # mean
        sigma_list = [0.00001]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 200)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 252 - 1

        tm.assert_almost_equal(
            qp.stats.effect(rdf, qp.stats.period.DAILY),
            expected,
            rtol=1e-1,
        )

    def test_return_series(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk

        # 1. Test with monthly period
        mu = 0.03  # mean
        sigma = 0.01  # standard deviation
        rs = qp.random.generator.returns(mu, sigma, 1000)

        expected = (mu + 1) ** 12 - 1

        effect = qp.stats.effect(rs, qp.stats.period.MONTHLY)
        assert type(effect) is np.float64

        assert_allclose(
            effect,
            expected,
            rtol=1e-1,
        )

        # 2. Test with semiannual period
        mu = 0.03  # mean
        sigma = 0.01  # standard deviation
        rs = qp.random.generator.returns(mu, sigma, 200)

        expected = (mu + 1) ** 2 - 1

        assert_allclose(
            qp.stats.effect(rs, qp.stats.period.SEMIANNUAL),
            expected,
            rtol=1e-1,
        )

        # 3. Test with daily period
        mu = 0.0001  # mean
        sigma = 0.00001  # standard deviation
        rdf = qp.random.generator.returns(mu, sigma, 200)

        expected = (mu + 1) ** 252 - 1

        assert_allclose(
            qp.stats.effect(rdf, qp.stats.period.DAILY),
            expected,
            rtol=1e-1,
        )


class TestEffectVol:
    def test_return_dataframe(self):
        # From Wikipedia - https://en.wikipedia.org/wiki/Volatility_(finance)
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk

        # 1. Test with daily period
        mu_list = [0.01]  # mean
        sigma_list = [0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = qp.ReturnSeries(sigma_list) * np.sqrt(252)

        effect = qp.stats.effect_vol(rdf, qp.stats.period.DAILY)
        assert type(effect) is qp.ReturnSeries

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )

        # 2. Test with monthly period
        mu_list = [0.01, 0.01]  # mean
        sigma_list = [0.02397, 0.079601]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = qp.ReturnSeries(sigma_list) * np.sqrt(12)

        effect = qp.stats.effect_vol(rdf, qp.stats.period.MONTHLY)
        assert type(effect) is qp.ReturnSeries

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )

    def test_return_series(self):
        # From Wikipedia - https://en.wikipedia.org/wiki/Volatility_(finance)
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk

        # 1. Test with daily period
        mu = 0.01  # mean
        sigma = 0.01  # standard deviation
        rs = qp.random.generator.returns(mu, sigma, 1000)

        expected = sigma * np.sqrt(252)

        effect = qp.stats.effect_vol(rs, qp.stats.period.DAILY)
        assert type(effect) is np.float64

        assert_allclose(
            effect,
            expected,
            rtol=1e-1,
        )

        # 2. Test with monthly period
        mu = 0.01  # mean
        sigma = 0.02397  # standard deviation
        rdf = qp.random.generator.returns(mu, sigma, 1000)

        expected = sigma * np.sqrt(12)

        effect = qp.stats.effect_vol(rdf, qp.stats.period.MONTHLY)
        assert type(effect) is np.float64

        assert_allclose(
            effect,
            expected,
            rtol=1e-1,
        )


class TestTotalReturn:
    def test_return_series(self):
        ps = pd.Series([8.7, 8.91, 8.71, 8.43, 8.73])
        rs = qp.ReturnSeries.from_price(ps)

        rs_total_return = qp.stats.total_return(rs)
        assert type(rs_total_return) is np.float64

        hpr = (ps.iloc[-1] - ps.iloc[0]) / ps.iloc[0]

        assert_allclose(
            rs_total_return,
            hpr,
            rtol=1e-1,
        )

    def test_return_frame(self):
        pdf = pd.DataFrame(
            {
                "stock_1": [8.7, 8.91, 8.71, 8.43, 8.73],
                "stock_2": [10.66, 11.08, 10.71, 11.59, 12.11],
            }
        )
        rdf = qp.ReturnDataFrame.from_price(pdf)

        rdf_total_return = qp.stats.total_return(rdf)
        assert type(rdf_total_return) is qp.ReturnSeries

        hpr_1 = (pdf["stock_1"].iloc[-1] - pdf["stock_1"].iloc[0]) / pdf[
            "stock_1"
        ].iloc[0]
        hpr_2 = (pdf["stock_2"].iloc[-1] - pdf["stock_2"].iloc[0]) / pdf[
            "stock_2"
        ].iloc[0]

        expected = qp.ReturnSeries([hpr_1, hpr_2], index=["stock_1", "stock_2"])

        tm.assert_almost_equal(rdf_total_return, expected, rtol=1e-4)
