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

Unit Tests
==========

.. note::

  This document originates from the OpenStack Nova project. Since we also use
  the same toolset for testing, we can also use some of their documentaion. We
  have obviously made changes that only affect our project but we credit the
  OpenStack project for the original [#f1]_.

Payload contains a suite of unit tests, in the payload/tests directory.

Any proposed code change will be automatically rejected by the Kickstand
Project Jenkins server if the change causes unit test failures.

Running the tests
-----------------
Run the unit tests by doing::

    tox

This script is a wrapper around the `nose`_ testrunner and the `pep8`_ checker.

.. _nose: http://code.google.com/p/python-nose/
.. _pep8: https://github.com/jcrocholl/pep8

.. rubric:: Footnotes

.. [#f1] See http://docs.openstack.org/developer/nova/devref/unit_tests.html
