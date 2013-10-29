:title: Queues

Queues API
==========

.. toctree::
   :maxdepth: 2
   :glob:

   queues/*

List queues
-----------

.. code-block:: html

  GET /v1/queues

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "id": 1,
      "created_at": "2011-04-22T13:33:48Z",
      "description": "24/7 Technical support",
      "disabled": False,
      "name": "support",
      "updated_at": "2011-04-22T13:33:48Z",
      "user_id": '1',
    }
  ]

Get a single queue
------------------

.. code-block:: html

  GET /v1/queues/:id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "id": 1,
    "created_at": "2011-04-22T13:33:48Z",
    "description": "24/7 Technical support",
    "disabled": False,
    "name": "support",
    "updated_at": "2011-04-22T13:33:48Z",
    "user_id": '1',
  }

Create a queue
--------------

.. code-block:: html

  POST /v1/queues

Input
'''''

Response
''''''''

Edit a queue
------------

.. code-block:: html

  PUT /v1/queues/:id

Parameters
''''''''''

Input
'''''

Response
''''''''

Delete a queue
--------------

.. code-block:: html

  DELETE /v1/queues/:id

Parameters
''''''''''

Response
''''''''
