from pandas.core.generic import NDFrame


def returns(prices: NDFrame, drop_first: bool = True) -> NDFrame:
    """
    Compute simple returns from a timeseries of prices.

    Parameters
    ----------
    prices : pd.Series or pd.DataFrame
        Prices of assets in wide-format, with assets as columns,
        and indexed by datetimes.

    drop_first: bool, default True
        How to handle the initial obvservation.

    Returns
    -------
        returns : Series or DataFrame
            The same type as the calling object.

    """
    out = prices.pct_change()

    if drop_first:
        out = out.iloc[1:]

    return out
