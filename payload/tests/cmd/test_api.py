# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2012 eNovance <licensing@enovance.com>
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

import os
import random
import socket
import subprocess
import time

import httplib2

from payload import test
from payload.tests import utils


class TestCase(test.TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        # create api_paste.ini file without authentication
        content = \
            "[pipeline:main]\n"\
            "pipeline = api-server\n"\
            "[app:api-server]\n"\
            "paste.app_factory = payload.api.app:app_factory\n"
        self.paste = utils.write_to_tempfile(
            content=content, prefix='api_paste', suffix='.ini')

        # create payload.conf file
        self.api_port = random.randint(10000, 11000)
        self.http = httplib2.Http()
        content = "[DEFAULT]\n"\
                  "debug=true\n"\
                  "api_paste_config={0}\n"\
                  "[api]\n"\
                  "port={1}\n"\
                  "[database]\n"\
                  "connection=log://localhost\n".format(self.paste,
                                                        self.api_port)

        self.tempfile = utils.write_to_tempfile(
            content=content, prefix='payload', suffix='.conf')
        self.subp = subprocess.Popen([
            'payload-api', "--config-file=%s" % self.tempfile])

    def tearDown(self):
        super(TestCase, self).tearDown()
        self.subp.kill()
        self.subp.wait()
        os.remove(self.tempfile)

    def _get_response(self, path):
        url = 'http://%s:%d/%s' % ('127.0.0.1', self.api_port, path)

        for x in range(10):
            try:
                r, c = self.http.request(url, 'GET')
            except socket.error:
                time.sleep(.5)
                self.assertIsNone(self.subp.poll())
            else:
                return r, c
        return (None, None)

    def test_v1(self):
        response, content = self._get_response('v1')
        self.assertEqual(404, response.status)
