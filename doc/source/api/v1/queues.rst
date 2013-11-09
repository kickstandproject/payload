:title: Queues

Queues API
==========

.. toctree::
   :maxdepth: 2
   :glob:

   queues/*

List queues
-----------

.. code-block:: html

  GET /v1/queues

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  [
    {
      "uuid": "8090f8b0-4115-11e3-aa6e-0800200c9a66",
      "created_at": "2011-04-22T13:33:48Z",
      "description": "24/7 Technical support",
      "disabled": False,
      "name": "support",
      "project_id": "793491dd5fa8477eb2d6a820193a183b",
      "user_id": "02d99a62af974b26b510c3564ba84644",
      "updated_at": "2011-04-22T13:33:48Z",
    }
  ]

Get a single queue
------------------

.. code-block:: html

  GET /v1/queues/:uuid

Parameters
''''''''''

Response
''''''''

.. code-block:: html

  {
    "uuid": "8090f8b0-4115-11e3-aa6e-0800200c9a66",
    "created_at": "2011-04-22T13:33:48Z",
    "description": "24/7 Technical support",
    "disabled": False,
    "name": "support",
    "project_id": "793491dd5fa8477eb2d6a820193a183b",
    "user_id": "02d99a62af974b26b510c3564ba84644",
    "updated_at": "2011-04-22T13:33:48Z",
  }

Create a queue
--------------

.. code-block:: html

  POST /v1/queues

Input
'''''

Response
''''''''

Edit a queue
------------

.. code-block:: html

  PUT /v1/queues/:uuid

Parameters
''''''''''

Input
'''''

Response
''''''''

Delete a queue
--------------

.. code-block:: html

  DELETE /v1/queues/:uuid

Parameters
''''''''''

Response
''''''''
