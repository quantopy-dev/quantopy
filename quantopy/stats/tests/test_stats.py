import numpy as np
import pandas as pd
import pandas._testing as tm
import quantopy as qp
from numpy.testing import assert_allclose


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


class TestEffect:
    def test_return_dataframe(self):
        # From CFA 2019 Schweser - Level 1. LOS 6.c
        # From Introduction to Portfolio Construction and Analysis with Python. EDHEC-Risk

        # 1. Test with monthly period
        mu_list = [0.03, 0.015, 0.04, 0.005, 0.01]  # mean
        sigma_list = [0.01, 0.01, 0.01, 0.01, 0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 12 - 1  # type: ignore

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

        expected = (qp.ReturnSeries(mu_list) + 1) ** 2 - 1  # type: ignore

        tm.assert_almost_equal(
            qp.stats.effect(rdf, qp.stats.period.SEMIANNUAL),
            expected,
            rtol=1e-1,
        )

        # 3. Test with daily period
        mu_list = [0.0001]  # mean
        sigma_list = [0.00001]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 200)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 252 - 1  # type: ignore

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

        tm.assert_almost_equal(
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

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )
