# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 IBM Corp.
# Copyright (C) 2013-2014 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket

from oslo.config import cfg

from payload.api import app
from payload.openstack.common.fixture import config
from payload import test


class TestCase(test.TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.CONF = self.useFixture(config.Config()).conf

    def test_WSGI_address_family(self):
        self.CONF.set_override('host', '::', group='api')
        server_cls = app.get_server_cls(cfg.CONF.api.host)
        self.assertEqual(server_cls.address_family, socket.AF_INET6)

        self.CONF.set_override('host', '127.0.0.1', group='api')
        server_cls = app.get_server_cls(cfg.CONF.api.host)
        self.assertEqual(server_cls.address_family, socket.AF_INET)

        self.CONF.set_override('host', 'ddddd', group='api')
        server_cls = app.get_server_cls(cfg.CONF.api.host)
        self.assertEqual(server_cls.address_family, socket.AF_INET)
