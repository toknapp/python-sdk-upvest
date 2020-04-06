Upvest Python SDK
=================

[![CircleCI](https://circleci.com/gh/upvestco/upvest-python.svg?style=svg)](https://circleci.com/gh/upvestco/upvest-python)
[![PyPI version](https://img.shields.io/pypi/v/upvest.svg)](https://pypi.org/project/upvest/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/upvest.svg)](https://pypi.org/project/upvest/)

Installation
------
The Upvest SDK is available on [PYPI](https://pypi.org/project/upvest/). Install with pip:
```python
pip install upvest
```

The default SDK is lightweight, and user recovery kits are returned as an SVG in string format. If you wish to process the recovery kit in binary format, then additional requirements are necessary:

```python
pip install upvest[recovery]
```

Note that this may require additional system level dependencies to support [PyNaCl](https://pypi.org/project/PyNaCl/).

Documentation
------

Documentation is available at upvest.readthedocs.io.
