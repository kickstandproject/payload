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
      "uuid": "5f91c19d-84f0-4122-bc7f-dcdda6704953",
      "created_at": "2011-04-22T13:33:48Z",
      "user_id": "02d99a62af974b26b510c3564ba84644",
      "updated_at": "2011-04-22T13:33:48Z",
    }
  ]

Get a single agent
------------------

.. code-block:: html

  GET /v1/agents/:uuid

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "uuid": "5f91c19d-84f0-4122-bc7f-dcdda6704953",
    "created_at": "2011-04-22T13:33:48Z",
    "user_id": "02d99a62af974b26b510c3564ba84644",
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

  PUT /v1/agents/:uuid

Parameters
''''''''''

Input
'''''

Response
''''''''

Delete an agent
---------------

.. code-block:: html

  DELETE /v1/agents/:uuid

Parameters
''''''''''

Response
''''''''
