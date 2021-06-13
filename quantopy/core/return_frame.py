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
        """Generate a new ReturnDataFrame with simple returns from given prices.

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
        return ReturnDataFrame(price, dtype="float64").pct_change()[1:]

    def gmean(self) -> "ReturnSeries":
        """Compute the geometric mean of series of returns. Commonly used to determine the
        performance results of an investment or portfolio.

        Return the geometric average of the simple returns.
        That is:  n-th root of (1+R1) * (1+R2) * ... * (1+Rn)

        Returns
        -------
        gmean : ReturnSeries

        References
        ----------
        .. [1] "Weighted Geometric Mean", *Wikipedia*,
                    https://en.wikipedia.org/wiki/Weighted_geometric_mean.
        """
        return stats.gmean(self)

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

    def effect(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> "ReturnSeries":
        """
        Determines the annual effective annual return.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        effective_annual_rate : qp.ReturnSeries
        """
        return stats.effect(self, period)

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


# rdf = ReturnDataFrame.from_price([10, 15, 20])
rdf = ReturnDataFrame.from_price([80])

print(rdf)
