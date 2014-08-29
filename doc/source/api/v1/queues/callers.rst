:title: Queue Callers

Queue Callers API
=================

List callers from queue
-----------------------

.. code-block:: html

  GET /v1/queues/:queue_id/callers

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "created_at": "2011-04-22T13:33:48Z",
      "name": "Bob Smith",
      "number": "6135551234",
      "position": 0,
      "queue_id": "cc096e0b-0c96-4b8b-b812-ef456f361ee3",
      "uuid": "360a5b5ac90149dba0f3f9d4e5abffbc",
    }
  ]

Get single caller from queue
----------------------------

.. code-block:: html

  GET /v1/queues/:queue_id/callers/:uuid

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "created_at": "2011-04-22T13:33:48Z",
    "name": "Bob Smith",
    "number": "6135551234",
    "position": 0,
    "queue_id": "cc096e0b-0c96-4b8b-b812-ef456f361ee3",
    "uuid": "360a5b5ac90149dba0f3f9d4e5abffbc",
  }
