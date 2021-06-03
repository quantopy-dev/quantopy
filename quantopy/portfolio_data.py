import os
import urllib.request
import zipfile
from collections import namedtuple
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd

Portfolio = namedtuple("Portfolio", ["url", "skip_rows", "start_date", "slice"])


ff_base_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"

NUMBER_OF_ROWS = 1138


class FF_Portfolios(Enum):
    Formed_on_ME_VW = Portfolio(
        url="Portfolios_Formed_on_ME",
        skip_rows=12,
        start_date=datetime(1926, 7, 1),
        slice=0,
    )
    Formed_on_ME_EW = Portfolio(
        url="Portfolios_Formed_on_ME",
        skip_rows=12,
        start_date=datetime(1926, 7, 1),
        slice=1,
    )


def get_portfolio(portfolio_id: FF_Portfolios) -> pd.DataFrame:
    # Create the download url
    portfolio_url = f"{ff_base_url}{portfolio_id.value.url}_CSV.zip"

    # Download the file and save it
    # We will name it tmp.zip file
    urllib.request.urlretrieve(portfolio_url, "tmp.zip")

    # Use the zipfile package to load the contents, here we are
    # Reading the file
    zip_file = zipfile.ZipFile("tmp.zip", "r")
    # Next we extact the file data
    # We will call it ff_factors.csv
    zip_file.extractall("downloads")
    # Make sure you close the file after extraction
    zip_file.close()

    os.remove("tmp.zip")

    from datetime import datetime

    dateparse = lambda x: datetime.strptime(x, "%Y%m")

    end_date = datetime.now()
    start_date = portfolio_id.value.start_date
    months_diff = (end_date.year - start_date.year) * 12 + (
        end_date.month - start_date.month
    )

    ff_factors = pd.read_csv(
        f"downloads/{portfolio_id.value.url}.csv",
        skiprows=portfolio_id.value.skip_rows
        + months_diff * portfolio_id.value.slice
        + 3 * portfolio_id.value.slice,
        header=0,
        nrows=months_diff - 1,
        index_col=0,
        na_values=[-99.99],
        skipinitialspace=True,
        date_parser=dateparse,
    )

    return ff_factors.astype(float) / 100
