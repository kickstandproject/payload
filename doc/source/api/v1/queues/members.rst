:title: Queue Members

Queue Members API
=================

List queue members
------------------

.. code-block:: html

  GET /v1/queues/:queue_id/members

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "created_at": "2011-04-22T13:33:48Z",
      "number": "1001@example.org",
      "paused_at": None,
      "uuid": "b1775ea3f7fb451a97ef669d1ccf8e64",
    }
  ]

Get queue memeber
-----------------

.. code-block:: html

  GET /v1/queues/:queue_id/members/:agent_id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "created_at": "2011-04-22T13:33:48Z",
    "number": "1001@example.org",
    "paused_at": None,
    "uuid": "b1775ea3f7fb451a97ef669d1ccf8e64",
  }
