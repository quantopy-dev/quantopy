# Quantopy
[![YourActionName Actions Status](https://github.com/quantopy-dev/quantopy/workflows/ci.yml/badge.svg)](https://github.com/quantopy-dev/quantopy/actions)

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
