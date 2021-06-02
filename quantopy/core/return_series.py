import numpy as np
import pandas as pd
import quantopy as qp


class ReturnSeries(pd.Series):
    @property
    def _constructor(self):
        return ReturnSeries

    @property
    def _constructor_expanddim(self):
        return qp.ReturnDataFrame

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
        return qp.stats.gmean(self)
