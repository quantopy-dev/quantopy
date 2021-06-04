import pandas as pd
import quantopy as qp


class ReturnDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return ReturnDataFrame

    @property
    def _constructor_sliced(self):
        return qp.ReturnSeries

    @classmethod
    def from_price(cls, prices: pd.DataFrame):
        """Generate simple return series from prices.

        Returns
        -------
        Simple return series
        """
        return ReturnDataFrame(prices.pct_change()[1:])

    def gmean(self):  # -> qp.ReturnSeries:
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
        return qp.stats.gmean(self)

    def sharpe_ratio(self, riskfree_rate: float):  # -> qp.ReturnSeries:
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
        return qp.ratio.sharpe(self, riskfree_rate)
