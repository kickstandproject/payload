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
      "called_id": "5195558812",
      "caller_id": "6135551234",
      "caller_name": "John Doe",
      "created_at": "2011-04-22T13:33:48Z",
      "position": 0,
      "status": "1",
      "updated_at": "2011-04-22T13:33:48Z",
      "uuid": "360a5b5a-c901-49db-a0f3-f9d4e5abffbc",
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
    "called_id": "5195558812",
    "caller_id": "6135551234",
    "caller_name": "John Doe",
    "created_at": "2011-04-22T13:33:48Z",
    "position": 0,
    "status": "1",
    "updated_at": "2011-04-22T13:33:48Z",
    "uuid": "360a5b5a-c901-49db-a0f3-f9d4e5abffbc",
  }

Add caller to queue
-------------------

.. code-block:: html

  POST /v1/queues/:queue_id/callers

Input
'''''

Response
''''''''

Remove caller from queue
------------------------

.. code-block:: html

  DELETE /v1/queues/:queue_id/callers/:uuid

Parameters
''''''''''

Response
''''''''
