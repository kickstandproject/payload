:title: Users

Users API
=========

.. toctree::
   :maxdepth: 2
   :glob:

List users
-----------

.. code-block:: html

  GET /v1/users

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "id": 1,
      "created_at": "2011-04-22T13:33:48Z",
      "email": "alice@example.org",
      "name": "Alice Smith",
      "password": "secret",
      "updated_at": "2011-04-22T13:33:48Z",
    }
  ]

Get a single user
-----------------

.. code-block:: html

  GET /v1/users/:id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "id": 1,
    "created_at": "2011-04-22T13:33:48Z",
    "email": "alice@example.org",
    "name": "Alice Smith",
    "password": "secret",
    "updated_at": "2011-04-22T13:33:48Z",
  }

Create an user
--------------

.. code-block:: html

  POST /v1/users

Input
'''''

Response
''''''''

Edit an user
------------

.. code-block:: html

  PUT /v1/users/:id

Parameters
''''''''''

Input
'''''

Response
''''''''

Delete an user
--------------

.. code-block:: html

  DELETE /v1/users/:id

Parameters
''''''''''

Response
''''''''
