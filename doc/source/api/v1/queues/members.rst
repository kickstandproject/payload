:title: Queue Members

Queue Members API
=================

List members from queue
-----------------------

.. code-block:: html

  GET /v1/queues/:queue_id/members

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "id": 1,
      "created_at": "2011-04-22T13:33:48Z",
      "extension": "1000",
      "agent_id": 1,
      "paused": true,
      "paused_reason": "lunch",
      "queue_id": 1,
      "updated_at": "2011-04-22T13:33:48Z"
    }
  ]

Get single member from queue
----------------------------

.. code-block:: html

  GET /v1/queues/:queue_id/members/:id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "id": 1,
    "created_at": "2011-04-22T13:33:48Z",
    "extension": "1000",
    "agent_id": 1,
    "paused": true,
    "paused_reason": "lunch",
    "queue_id": 1,
    "updated_at": "2011-04-22T13:33:48Z"
  }

Add member to queue
-------------------

.. code-block:: html

  POST /v1/queues/:queue_id/members

Input
'''''

Response
''''''''

Edit queue member
-----------------

.. code-block:: html

  PUT /v1/queues/:queue_id/members/:id

Parameters
''''''''''

Input
'''''

Response
''''''''

Remove member from queue
------------------------

.. code-block:: html

  DELETE /v1/queues/:queue_id/members/:id

Parameters
''''''''''

Response
''''''''
