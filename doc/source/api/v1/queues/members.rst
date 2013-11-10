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
      "agent_id": 1,
      "updated_at": "2011-04-22T13:33:48Z"
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

Add queue member
----------------

.. code-block:: html

  POST /v1/queues/:queue_id/members/:agent_id

Input
'''''

Response
''''''''

Remove queue member
-------------------

.. code-block:: html

  DELETE /v1/queues/:queue_id/members/:agent_id

Parameters
''''''''''

Response
''''''''
