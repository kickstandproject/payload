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
      "user_id": "02d99a62af974b26b510c3564ba84644",
      "updated_at": "2011-04-22T13:33:48Z",
      "uuid": "51419ce0411511e3aa6e0800200c9a66",
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
    "user_id": "02d99a62af974b26b510c3564ba84644",
    "updated_at": "2011-04-22T13:33:48Z",
    "uuid": "51419ce0411511e3aa6e0800200c9a66",
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
