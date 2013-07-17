:title: Members

Members API
===========

.. toctree::
   :maxdepth: 2
   :glob:

List members
------------

.. code-block:: html

  GET /v1/members

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "id": 1,
      "created_at": "2011-04-22T13:33:48Z",
      "name": "John Smith",
      "password": "3a528267660d23d7cbf35388c6e21e6b",
      "updated_at": "2011-04-22T13:33:48Z",
    }
  ]

Get a single member
-------------------

.. code-block:: html

  GET /v1/members/:id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "id": 1,
    "created_at": "2011-04-22T13:33:48Z",
    "name": "John Smith",
    "password": "3a528267660d23d7cbf35388c6e21e6b",
    "updated_at": "2011-04-22T13:33:48Z",
  }

Create a member
---------------

.. code-block:: html

  POST /v1/members

Input
'''''

Response
''''''''

Edit a member
-------------

.. code-block:: html

  PUT /v1/members/:id

Parameters
''''''''''

Input
'''''

Response
''''''''

Delete a member
---------------

.. code-block:: html

  DELETE /v1/members/:id

Parameters
''''''''''

Response
''''''''
