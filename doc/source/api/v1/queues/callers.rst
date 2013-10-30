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
      "position": 0,
      "status": "1",
      "updated_at": "2011-04-22T13:33:48Z",
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
    "position": 0,
    "status": "1",
    "updated_at": "2011-04-22T13:33:48Z",
    "uuid": "360a5b5ac90149dba0f3f9d4e5abffbc",
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
