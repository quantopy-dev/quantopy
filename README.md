# Quantopy: powerful Python quantitative finance analysis toolkit
[![Android-master Actions Status](https://github.com/quantopy-dev/quantopy/workflows/CI/badge.svg)](https://github.com/quantopy-dev/quantopy/actions)
[![Coverage](https://codecov.io/github/quantopy-dev/quantopy/coverage.svg?branch=main)](https://codecov.io/gh/quantopy-dev/quantopy)
[![Docs](https://readthedocs.org/projects/quantopy/badge/)](https://quantopy.readthedocs.io)
[![License](https://img.shields.io/pypi/l/quantopy.svg)](https://github.com/quantopy-dev/quantopy/blob/master/LICENSE)

## What is it?

**quantopy** is a community effort to develop a single core package for Finance in Python and foster interoperability between Python finance packages. This repository contains the core package which is intended to contain much of the core functionality and some common tools needed for performing Quantitative Finance with Python. Additionally, it has the broader goal of becoming **the most powerful and flexible open source finance analysis / manipulation tool available in any language**. It is already well on its way towards this goal.

Releases are [registered on PyPI!](https://pypi.org/project/quantopy/), and development is occurring at the [project's GitHub page!](https://github.com/quantopy-dev/quantopy).

## Main Features
Here are just a few of the things that quantopy does well:
  - Easy download of portfolio data from the most common sources (e.g. Fama and French)
  - Generation of simulated stock data following different return distributions (e.g. Random Walk, Geometric Random Walk)
  - Perform Returns Analysis
  - Perform risk analysis of portfolios

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/quantopy-dev/quantopy

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/quantopy/).


```sh
# PyPI
pip install quantopy
```

## Dependencies
- [NumPy - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays](https://www.numpy.org)
- [Pandas - Adds support for relational or labeled data](https://pandas.pydata.org)
- [Scipy - Adds support for statistics calculations](https://www.scipy.org)

## Installation from sources


```python
# Create and activate the build environment
conda env create -f environment.yml
conda activate quantopy-dev

# Make sure you have the latest versions of PyPA’s build installed:
python -m pip install --upgrade build

# Build and install tutorial-python
python -m build
python -m pip install -e .
```

## License
[MIT](LICENSE)

## Contributing to quantopy

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

If you are simply looking to start working with the quantopy codebase, navigate to the [GitHub "issues" tab](https://github.com/quantopy-dev/quantopy/issues) and start looking through interesting issues. There are a number of issues listed under [good first issue](https://github.com/quantopy-dev/quantopy/issues?labels=good+first+issue&sort=updated&state=open) where you could start out.

Or maybe through using quantopy you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!
