import numpy as np
import pandas_datareader.data as web
from pandas_datareader import famafrench
from quantopy.core.return_frame import ReturnDataFrame


def get_available_datasets(data_source):
    expected_source = ["famafrench"]

    if data_source not in expected_source:
        msg = "data_source=%r is not implemented" % data_source
        raise NotImplementedError(msg)

    if data_source == "famafrench":
        return famafrench.get_available_datasets()


def get(name, data_source=None, start=None, end=None, retry_count=3, pause=0.1):
    """
    Imports data from a number of online sources.

    Currently only supports Kenneth French's data library.

    Parameters
    ----------
    name : str or list of strs
        the name of the dataset. Some data sources (IEX, fred) will
        accept a list of names.
    data_source: {str, None}
        the data source ("iex", "fred", "ff")
    start : string, int, date, datetime, Timestamp
        left boundary for range (defaults to 1/1/2010)
    end : string, int, date, datetime, Timestamp
        right boundary for range (defaults to today)
    retry_count : {int, 3}
        Number of times to retry query request.
    pause : {numeric, 0.001}
        Time, in seconds, to pause between consecutive queries of chunks. If
        single value given for symbol, represents the pause between retries.

    Examples
    ----------

    # Data from Fama/French
    ff = get("F-F_Research_Data_Factors", "famafrench")
    ff = get("F-F_Research_Data_Factors_weekly", "famafrench")
    ff = get("6_Portfolios_2x3", "famafrench")
    ff = get("F-F_ST_Reversal_Factor", "famafrench")
    """
    expected_source = ["famafrench"]

    if data_source not in expected_source:
        msg = "data_source=%r is not implemented" % data_source
        raise NotImplementedError(msg)

    if data_source == "famafrench" and start is None:
        start = "1926-07"

    ds = web.DataReader(
        name,
        data_source=data_source,
        start=start,
        end=end,
        retry_count=retry_count,
        pause=pause,
    )

    for key, value in ds.items():
        if key != "DESCR":
            value[value <= -99.99] = np.nan

            ds[key] = ReturnDataFrame(value) / 100

    return ds
