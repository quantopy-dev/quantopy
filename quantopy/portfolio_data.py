import urllib.request
import zipfile
from enum import Enum
import pandas as pd
import os

from collections import namedtuple

Portfolio = namedtuple("Portfolio", ["url", "skip_rows"])


ff_base_url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/'

class FF_Portfolios(Enum):
    Formed_on_ME = Portfolio(
        url="Portfolios_Formed_on_ME",
        skip_rows=12,
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

    ff_factors = pd.read_csv(f"downloads/{portfolio_id.value.url}.csv", skiprows=portfolio_id.value.skip_rows)

    return ff_factors
