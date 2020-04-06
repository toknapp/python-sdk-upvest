.. _api:

Developer Interface
===================

.. module:: upvest

This part of the documentation covers all the interfaces of Upvest Python SDK.


Authentication
----------------

.. autoclass:: upvest.authentication.KeyAuth
.. autoclass:: upvest.authentication.OAuth

API resources
----------------

.. autoclass:: upvest.model.Users
   :members:

.. autoclass:: upvest.model.Assets
   :members:

.. autoclass:: upvest.model.Wallets
   :members:

.. autoclass:: upvest.model.Transactions
   :members:

.. autoclass:: upvest.model.ECDSASignature
   :members:

.. autoclass:: upvest.model.Webhooks
   :members:

.. autoclass:: upvest.model.HistoricalData
   :members:

Exceptions
----------

.. autoexception:: upvest.exceptions.InvalidRequest
.. autoexception:: upvest.exceptions.RecoveryFailedError
.. autoexception:: upvest.exceptions.AuthenticationError
