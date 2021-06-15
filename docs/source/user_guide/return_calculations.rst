.. _return_calculations:

{{ header }}

====================================
 Fundamentals of Return Calculations
====================================

Here we discuss a lot of the essential functionality for asset return calculations. We first cover simple
return calculations, which are typically reported in practice but are often not convenient for statistical
modeling purposes. We then describe continuously compounded return calculations, which are more convenient
for statistical modeling purposes.

Customarily, we import as follows:

.. ipython:: python

   import quantopy as qp

To begin, let's create some example stock prices like we did in the :ref:`10 minutes to quantopy <10min>` section:

.. ipython:: python

   stock1_price = [10, 12, 15]
   stock2_price = [30, 20, 35]

.. _return_calculations.simple_returns:

Simple Returns
--------------

Consider purchasing an asset (e.g., stock, bond, ETF, option, etc.) at time t-1 for
the price P\ :sub:`t-1`\ , and then selling the asset at time t for the price
P\ :sub:`t`\ . If there are no intermediate cash flows (e.g., dividends) between t-1  and
t, the *simple net return* on an investment in the asset between t−1 and t is defined as:

.. math::

   R_t = \frac{P_{t} − P_{t-1}}{P_{t-1}}

And we can define the *simple gross return* as:

.. math::

   1 + R_t = \frac{P_{t}}{P_{t-1}}

:meth:`ReturnSeries.from_price` gives a :class:`ReturnSeries` with simple returns calculated from
a given price for a single asset, letting quantopy create a default integer index:

.. ipython:: python

   stock1_rs = qp.ReturnSeries.from_price(stock1_price)

   stock1_rs

To generate the simple returns from a list of multiple asset prices, we use :meth:`ReturnDataFrame.from_price`:

.. ipython:: python

   stocks_rdf = qp.ReturnDataFrame.from_price(
      {
         'stock_1': stock1_price,
         'stock_2': stock2_price,
      }
   )

   stocks_rdf

Multi-period returns
~~~~~~~~~~~~~~~~~~~~

The simple two-month return on an investment in an asset between months t−2 and t is defined as:

.. math::

   R_t(2) = (1 + R_t)(1 + R_{t−1}) − 1.

Then the simple two-month gross return becomes:

.. math::

   1 + R_t(2) = (1+R_t)(1+R_{t−1})

In general, the k-month gross return is defined as the product of k one-month gross returns:

.. math::

   1 + R_t(k) = \prod_{j=0}^{k-1}(1+R_{t−j})

The method :meth:`~ReturnDataFrame.cumulated` computes the cumulated indexed values from simple
returns.

.. ipython:: python

   stock1_rs.cumulated()

   stocks_rdf.cumulated()


Average returns
~~~~~~~~~~~~~~~

For investments over a given horizon, it is often of interest to compute a measure of the average
rate of return over the horizon. To illustrate, consider a sequence of monthly investments over *T*
months with monthly returns R\ :sub:`1`\, R\ :sub:`2`\, ... , R\ :sub:`T`\ . The T−month return is

.. math::

   1 + R(T) = (1+R_1)(1+R_2)...(1+R_T) - 1

What is the average monthly return? There are two possibilities. The first is the *arithmetic
average return*

.. math::

   \bar{R}^A = \frac{1}{T}(R_1+R_2+···+R_T)

The second is the *geometric average return*

.. math::

   \bar{R}^G = [(1+R_1)(1+R_2)...(1+R_T)]^\frac{1}{T} - 1

Notice that the geometric average return is the monthly return which compounded monthly
for T months gives the gross T−month return

.. math::

   (1 + \bar{R}^G)^T = 1 + R(T)

.. note::

   The geometric mean is always less than or equal to the arithmetic mean, and the difference
   increases as the dispersion of the observations increases. The only time the arithmetic and
   geometric means are equal is when there is no variability in the observations
   (i.e., all observations are equal).

Since past returns are compounded each period, the geometric mean of past returns is the
appropriate measure of past performance. The arithmetic mean is, however, the statistically best
estimator of the next year’s returns given only the past returns, athough to estimate multi-year
returns (e.g. expected return over the  next five years), the geometric mean is the appropriate
measure.

The method :meth:`~ReturnDataFrame.mean` computes the arithmetic mean of pasts returns.

.. ipython:: python

   stock1_rs.mean()

   stocks_rdf.mean()

As we have seen, for the evaluation of the average investment performance, the geometric average
return is preferred to the arithmetic average return. The method :meth:`~ReturnDataFrame.gmean`
computes the geometric mean of pasts returns.

.. ipython:: python

   stock1_rs.gmean()

   stocks_rdf.gmean()

Annualizing returns
~~~~~~~~~~~~~~~~~~~~

Very often returns over different horizons are annualized, i.e., converted to an annual return, to
facilitate comparisons with other investments. The annualization process depends on the holding
period of the investment and an implicit assumption about compounding.

The method :meth:`~ReturnDataFrame.annualized` calculates the annualized rate of return, given the
compounding period assumption. For monthly returns, we can calculate the annualized return with:

.. ipython:: python

   stock1_rs.annualized(period=qp.stats.period.MONTHLY)

   stocks_rdf.annualized(period=qp.stats.period.MONTHLY)

We can also compute annualized rate for different periods, like daily, weekly and yearly.

.. _return_calculations.references:

References
----------

1. Zivot, E. (2016). Introduction to Computational Finance and Financial Econometrics with R. Springer.
