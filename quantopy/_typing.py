from typing import Union

from pandas.core.frame import DataFrame
from pandas.core.series import Series

# scalars

PythonScalar = Union[str, int, float, bool]

# FrameOrSeriesUnion  means either a DataFrame or a Series. E.g.
# `def func(a: FrameOrSeriesUnion) -> FrameOrSeriesUnion: ...` means that if a Series
# is passed in, either a Series or DataFrame is returned, and if a DataFrame is passed
# in, either a DataFrame or a Series is returned.
FrameOrSeries = Union["DataFrame", "Series"]
