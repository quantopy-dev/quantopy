import numpy as np
import pandas.testing as tm
import pytest
from numpy.testing import assert_allclose, assert_almost_equal

import quantopy as qp


@pytest.fixture(autouse=True)
def random():
    np.random.seed(0)


class TestGenerator:
    def test_returns_basic(self) -> None:
        # Test single mu and sigma
        mu, sigma = 0, 0.1  # mean and standard deviation
        rs = qp.random.generator.returns(mu, sigma, 10000)
        assert type(rs) is qp.ReturnSeries

        assert_almost_equal(rs.mean(), mu, decimal=2)
        assert_almost_equal(rs.std(), sigma, decimal=2)

        assert rs.shape == (10000,)

        # Test list of mu and sigma
        mu_list = [1, 2]  # mean
        sigma_list = [0.1, 0.2]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 10000)
        assert type(rdf) is qp.ReturnDataFrame

        assert rdf.shape == (10000, 2)

        assert_almost_equal(rdf.iloc[:, 0].mean(), mu_list[0], decimal=2)
        assert_almost_equal(rdf.iloc[:, 0].std(), sigma_list[0], decimal=2)
        assert_almost_equal(rdf.iloc[:, 1].mean(), mu_list[1], decimal=2)
        assert_almost_equal(rdf.iloc[:, 1].std(), sigma_list[1], decimal=2)

    def test_returns_gbm(self) -> None:
        # Test single mu and sigma
        mu, sigma = 0, 0.1  # mean and standard deviation
        rs = qp.random.generator.returns(mu, sigma, 10000, 'gbm')
        assert type(rs) is qp.ReturnSeries

        expected_sigma = np.sqrt(sigma**2 + 1**2)

        assert_almost_equal(rs.mean(), mu, decimal=1)
        #assert_almost_equal(rs.std(), expected_sigma, decimal=2)

        assert rs.shape == (10000,)

        # Test list of mu and sigma
        mu_list = [1, 2]  # mean
        sigma_list = [0.1, 0.2]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 50000, 'gbm')
        assert type(rdf) is qp.ReturnDataFrame

        assert rdf.shape == (50000, 2)

        assert_almost_equal(rdf.iloc[:, 0].mean(), mu_list[0], decimal=2)
        #assert_almost_equal(rdf.iloc[:, 0].std(), sigma_list[0], decimal=2)
        assert_almost_equal(rdf.iloc[:, 1].mean(), mu_list[1], decimal=2)
        #assert_almost_equal(rdf.iloc[:, 1].std(), sigma_list[1], decimal=2)