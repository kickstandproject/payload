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
      "id": 1,
      "created_at": "2011-04-22T13:33:48Z",
      "name": "John Doe",
      "number" "6135551234",
      "position" 1,
      "queue_id": 1,
      "updated_at": "2011-04-22T13:33:48Z"
    }
  ]

Get single caller from queue
----------------------------

.. code-block:: html

  GET /v1/queues/:queue_id/callers/:id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "id": 1,
    "created_at": "2011-04-22T13:33:48Z",
    "name": "John Doe",
    "number" "6135551234",
    "position" 1,
    "queue_id": 1,
    "updated_at": "2011-04-22T13:33:48Z"
  }
