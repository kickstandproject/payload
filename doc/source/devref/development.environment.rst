..
      Copyright 2010-2011 United States Government as represented by the
      Administrator of the National Aeronautics and Space Administration.
      Copyright (C) 2013 PolyBeacon, Inc.
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Setting Up a Development Environment
====================================

.. note::

  This document originates from the OpenStack Nova project. Since we also use
  the same toolset for testing, we can also use some of their documentaion. We
  have obviously made changes that only affect our project but we credit the
  OpenStack project for the original [#f1]_.

This page describes how to setup a working Python development
environment that can be used in developing stripe on Ubuntu. These
instructions assume you're already familiar with git.

Following these instructions will allow you to run the stripe unit
tests.


Virtual environments
--------------------

Stripe development uses a set of shell scripts from OpenStack's DevStack.
Virtual enviroments with venv are also available with the source code.

Linux Systems
-------------

.. note::

  This section is tested for Stripe on Ubuntu (12.04-64) distribution. Feel
  free to add notes and change according to your experiences or operating
  system.

Install the prerequisite packages.

On Ubuntu Precise (12.04)::

  sudo apt-get install python-dev python-pip git-core redis-server


Getting the code
----------------
Grab the code from GitHub::

  git clone https://github.com/kickstandproject/stripe.git
  cd stripe


Installing and using the virtualenv
--------------------------------------------

To install the virtual environment you simply run the following::

  python tools/install_venv.py

This will install all of the Python packages listed in the
``requirements.txt`` file into your virtualenv. There will also be some
additional packages (pip, distribute, greenlet) that are installed
by the ``tools/install_venv.py`` file into the virutalenv.

If all goes well, you should get a message something like this::

  Stripe development environment setup is complete.

  Stripe development uses virtualenv to track and manage Python dependencies
  while in development and testing.

  To activate the Stripe virtualenv for the extent of your current shell
  session you can run:

  $ source .venv/bin/activate

  Or, if you prefer, you can run commands in the virtualenv on a case by case
  basis by running:

  $ tools/with_venv.sh <your command>

  Also, make test will automatically use the virtualenv.


Running unit tests
------------------
The unit tests will run by default inside tox env in the ``.tox``
directory. Run the unit tests by doing::

    tox

See :doc:`unit.tests` for more details.

.. _virtualenv:

Contributing Your Work
----------------------

Once your work is complete you may wish to contribute it to the project.
Refer to HowToContribute_ for information.
Nova uses the Gerrit code review system. For information on how to submit
your branch to Gerrit, see GerritWorkflow_.

.. _GerritWorkflow: http://wiki.kickstandproject.org/GerritWorkflow
.. _HowToContribute: http://wiki.kickstandproject.org/HowToContribute

.. rubric:: Footnotes

.. [#f1] See http://docs.openstack.org/developer/nova/devref/development.environment.html
