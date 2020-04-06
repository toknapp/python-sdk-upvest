Upvest Python SDK
=================

.. image:: https://img.shields.io/pypi/pyversions/upvest.svg
    :target: https://pypi.org/project/upvest/

.. image:: https://img.shields.io/pypi/v/upvest.svg
    :target: https://pypi.org/project/upvest/

.. image:: https://circleci.com/gh/upvestco/upvest-python.svg?style=svg
   :target: https://circleci.com/gh/upvestco/upvest-python


Installation
------------

The Upvest SDK is available on `PYPI <https://pypi.org/project/upvest/>`_.

Install with pip: ``pip install upvest``

The default SDK is lightweight, and user recovery kits are returned as an SVG in string format. If you wish to process the recovery kit in binary format, then additional requirements are necessary:

``pip install upvest[recovery]``

Note that this may require additional system level dependencies to support `PyNaCl <https://pypi.org/project/PyNaCl/>`_.

Credentials
-----------

In order to retrieve your API credentials for using this Python client, you'll need to `sign up with Upvest <https://login.upvest.co/sign-up>`_.


The User Guide
--------------

This part of the documentation takes you through scenario of
integrating this library into a servicce/platform you are building.

.. toctree::
   :maxdepth: 2

   usage

The API Documentation / Guide
-----------------------------

Read this section for information on a specific function, class, or method.

.. toctree::
   :maxdepth: 2

   api
