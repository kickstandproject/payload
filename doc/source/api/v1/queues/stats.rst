:title: Queue Stats

Queue Stats API
=================

List Stats from queue
---------------------

.. code-block:: html

  GET /v1/queues/:queue_id/stats

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "callers": "32",
      "queue_id": 1,
      "updated_at": "2011-04-22T13:33:48Z"
    }
  ]
