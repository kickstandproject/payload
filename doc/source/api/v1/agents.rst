:title: Agents

Agents API
==========

.. toctree::
   :maxdepth: 2
   :glob:

List agents
-----------

.. code-block:: html

  GET /v1/agents

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "id": 1,
      "created_at": "2011-04-22T13:33:48Z",
      "user_id": '1',
      "updated_at": "2011-04-22T13:33:48Z",
    }
  ]

Get a single agent
------------------

.. code-block:: html

  GET /v1/agents/:id

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "id": 1,
    "created_at": "2011-04-22T13:33:48Z",
    "user_id": '1',
    "updated_at": "2011-04-22T13:33:48Z",
  }

Create an agent
---------------

.. code-block:: html

  POST /v1/agents

Input
'''''

Response
''''''''

Edit an agent
-------------

.. code-block:: html

  PUT /v1/agents/:id

Parameters
''''''''''

Input
'''''

Response
''''''''

Delete an agent
---------------

.. code-block:: html

  DELETE /v1/agents/:id

Parameters
''''''''''

Response
''''''''
