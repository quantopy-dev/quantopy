# Quantopy
[![Android-master Actions Status](https://github.com/quantopy-dev/quantopy/workflows/CI/badge.svg)](https://github.com/quantopy-dev/quantopy/actions)
[![Coverage](https://codecov.io/github/quantopy-dev/quantopy/coverage.svg?branch=main)](https://codecov.io/gh/quantopy-dev/quantopy)
[![License](https://img.shields.io/pypi/l/quantopy.svg)](https://github.com/quantopy-dev/quantopy/blob/master/LICENSE)

The Quantopy Project is a community effort to develop a single core package for Finance in Python and foster interoperability between Python finance packages. This repository contains the core package which is intended to contain much of the core functionality and some common tools needed for performing quantitative finance with Python.

Releases are [registered on PyPI!](https://pypi.org/project/quantopy/), and development is occurring at the [project's GitHub page!](https://github.com/quantopy-dev/quantopy).

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
