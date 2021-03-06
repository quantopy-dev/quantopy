from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import scipy.stats

from quantopy.stats import (
    financial,
    stats,
)

if TYPE_CHECKING:
    from quantopy.core.return_series import ReturnSeries


class ReturnDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return ReturnDataFrame

    @property
    def _constructor_sliced(self):
        """
        Used when a ReturnDataFrame (sub-)class manipulation result should be a ReturnSeries
        (sub-)class.
        """
        from quantopy.core.return_series import ReturnSeries

        return ReturnSeries

    @classmethod
    def from_price(cls, price) -> "ReturnDataFrame":
        """
        Generate a new ReturnDataFrame with simple returns from given prices.

        Parameters
        ----------
        price : ndarray (structured or homogeneous), Iterable, dict, or DataFrame
            Dict can contain Series, arrays, constants, dataclass or list-like objects.

        Returns
        -------
        ReturnDataFrame
            A new ReturnDataFrame object with simple returns for the given price series.

        See Also
        --------
        ReturnSeries.from_price: Analogous function for ReturnSeries.

        Examples
        --------
        >>> qp.ReturnDataFrame.from_price([10, 15, 20])
                  0
        1  0.500000
        2  0.333333

        >>> qp.ReturnDataFrame.from_price(
                {
                    "stock_1": [10, 15, 20],
                    "stock_2": [30, 20, 35]
                }
            )
            stock_1   stock_2
        1  0.500000 -0.333333
        2  0.333333  0.750000

        >>> qp.ReturnDataFrame.from_price(
                pd.DataFrame(
                    {
                        "stock_1": [10, 15, 20],
                        "stock_2": [30, 20, 35]
                    }
                )
            )
            stock_1   stock_2
        1  0.500000 -0.333333
        2  0.333333  0.750000
        """
        return financial.get_simple_returns_from_price(
            ReturnDataFrame(price, dtype="float64")
        )

    def cumulated(self) -> "ReturnDataFrame":
        """
        Computes cumulated indexed values from simple returns.

        Returns
        -------
        ReturnDataFrame
            A ReturnDataFrame object with cumulated indexed values.

        Examples
        --------
        >>> rdf = qp.ReturnDataFrame(
                    {
                        "stock_1": [0.5, 0.333333],
                        "stock_2": [-0.333333, 0.75]
                    }
            )
        >>> rdf.cumulated()
            stock_1   stock_2
        0       1.5  0.666667
        1       2.0  1.166667
        """
        return financial.cumulated(self)

    def mean(self) -> "ReturnSeries":
        """
        Compute the arithmetic mean of pasts returns.

        Returns
        -------
        ReturnSeries
            The arithmetic mean of past returns.

        Examples
        --------
        >>> rdf = qp.ReturnDataFrame(
                    {
                        "stock_1": [0.5, 0.333333],
                        "stock_2": [-0.333333, 0.75]
                    }
            )
        >>> rdf.mean()
        stock_1    0.416666
        stock_2    0.208334
        dtype: float64
        """
        return super().mean()

    def gmean(self) -> "ReturnSeries":
        """
        Compute the geometric mean of series of simple returns. Commonly used to determine the
        performance results of an investment or portfolio.

        Return the geometric average of the simple returns.
        That is:  n-th root of (1+R1) * (1+R2) * ... * (1+Rn)

        Returns
        -------
        ReturnSeries
            The geometric mean of past simple returns

        References
        ----------
        .. [1] "Weighted Geometric Mean", *Wikipedia*,
                    https://en.wikipedia.org/wiki/Weighted_geometric_mean.

        Examples
        --------
        >>> rdf = qp.ReturnDataFrame(
                    {
                        "stock_1": [0.5, 0.333333],
                        "stock_2": [-0.333333, 0.75]
                    }
            )
        >>> rdf.gmean()
        stock_1    0.414213
        stock_2    0.080124
        dtype: float64
        """
        return stats.gmean(self)

    def annualized(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> "ReturnSeries":
        """
        Determines the annualized rate of return. Commonly used for comparison
        of investment that have different time lenghts.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' for purposes of
            annualizing.

        Returns
        -------
        ReturnSeries
            The annualized rate of return

        Examples
        --------
        >>> rdf = qp.ReturnDataFrame(
                        {
                            "stock_1": [0.01, 0.02],
                            "stock_2": [-0.333333, 0.75]
                        }
                    )
        >>> rdf.gmean()
        stock_1    0.014988
        stock_2    0.080124
        dtype: float64
        >>> rdf.annualized(period=qp.stats.period.DAILY)
        stock_1    4.147318e+01
        stock_2    2.724726e+08
        dtype: float64
        >>> rdf.annualized(period=qp.stats.period.WEEKLY)
        stock_1     1.167505
        stock_2    54.032872
        dtype: float64
        >>> rdf.annualized(period=qp.stats.period.MONTHLY)
        stock_1    0.195444
        stock_2    1.521634
        dtype: float64
        >>> rdf.annualized(period=qp.stats.period.YEARLY)
        stock_1    0.014988
        stock_2    0.080124
        dtype: float64
        """
        return stats.annualized(self, period)

    def sharpe_ratio(
        self, riskfree_rate: float, period: stats.period = stats.period.MONTHLY
    ) -> "ReturnSeries":
        """Compute the sharpe ratio. Commonly used to measure the performance of an investment compared
        to a risk-free asset, after adjusting for its risk.

        Return the difference between the returns of the investment and the risk-free return,
        divided by the standard deviation of the investment.

        Parameters
        ----------

        riskfree_rate: float
            Risk free rate, with the same periodicity as simple retuns (e.g. daily, monthly, ...).

        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        sharpe_ratio : ReturnSeries

        References
        ----------
        .. [1] "Sharpe Ratio", *Wikipedia*, https://en.wikipedia.org/wiki/Sharpe_ratio.
        """
        return financial.sharpe(self, riskfree_rate, period)

    def drawdown(self) -> "ReturnDataFrame":
        """Compute the maximum drawdown in series of simple returns. Commonly used to measure the risk
        of a portfolio.

        Returns
        -------
        out : qp.ReturnDataFrame

        References
        ----------
        .. [1] "Drawdown", *Wikipedia*, https://en.wikipedia.org/wiki/Drawdown_(economics).
        """
        return financial.drawdown(self)

    def effect_vol(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> "ReturnSeries":
        """
        Determines the annual effective annual volatility.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        effective_annual_volatility : qp.ReturnSeries
        """
        return stats.effect_vol(self, period)

    def total_return(self) -> "ReturnSeries":
        """
        Compute total returns.

        Returns
        -------
        total_returns : np.float64
        """
        return stats.total_return(self)

    def log(self):
        return (self + 1).apply(np.log)  # type: ignore

    def skew(self):
        return self.aggregate(scipy.stats.skew)

    def kurtosis(self):
        return self.aggregate(scipy.stats.kurtosis) + 3

    def is_normal(self, pvalue=0.01):
        return self.aggregate(scipy.stats.jarque_bera).iloc[1] > pvalue
