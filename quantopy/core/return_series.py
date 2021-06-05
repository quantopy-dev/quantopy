from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from quantopy.ratio.financial import sharpe
from quantopy.stats import stats

if TYPE_CHECKING:
    from quantopy.core.return_frame import ReturnDataFrame


class ReturnSeries(pd.Series):
    @property
    def _constructor(self) -> type["ReturnSeries"]:
        return ReturnSeries

    @property
    def _constructor_expanddim(self) -> type["ReturnDataFrame"]:
        from quantopy.core.return_frame import ReturnDataFrame

        return ReturnDataFrame

    @classmethod
    def from_price(cls, prices: pd.Series) -> "ReturnSeries":
        """Generate simple return series from prices.

        Returns
        -------
        Simple return series
        """
        return ReturnSeries(prices.pct_change()[1:])

    def gmean(self) -> np.float64:
        """Compute the geometric mean of series of returns. Commonly used to determine the
        performance results of an investment or portfolio.

        Return the geometric average of the simple returns.
        That is:  n-th root of (1+R1) * (1+R2) * ... * (1+Rn)

        Returns
        -------
        gmean

        References
        ----------
        .. [1] "Weighted Geometric Mean", *Wikipedia*, https://en.wikipedia.org/wiki/Weighted_geometric_mean.
        """
        return stats.gmean(self)

    def sharpe_ratio(self, riskfree_rate: float) -> np.float64:
        """Compute the sharpe ratio. Commonly used to measure the performance of an investment compared
        to a risk-free asset, after adjusting for its risk.

        Return the difference between the returns of the investment and the risk-free return,
        divided by the standard deviation of the investment.

        Parameters
        ----------

        riskfree_rate: float
            Risk free rate, with the same periodicity as simple retuns (e.g. daily, monthly, ...).

        Returns
        -------
        sharpe_ratio : np.float64

        References
        ----------
        .. [1] "Sharpe Ratio", *Wikipedia*, https://en.wikipedia.org/wiki/Sharpe_ratio.
        """
        return sharpe(self, riskfree_rate)

    def effect(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> np.float64:
        """
        Determines the annual effective annual return.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        effective_annual_rate : qp.ReturnSeries or qp.ReturnDataFrame
        """
        return stats.effect(self, period)

    def effect_vol(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> np.float64:
        """
        Determines the annual effective annual volatility.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        effective_annual_volatility : qp.ReturnSeries or qp.ReturnDataFrame
        """
        return stats.effect_vol(self, period)
