# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# Copyright (C) 2013 PolyBeacon, Inc.
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

"""Base class for API tests."""

import pecan
import pecan.testing
import warlock

from stripe.openstack.common import log as logging
from stripe.tests.api.v1 import utils
from stripe.tests import base


LOG = logging.getLogger(__name__)


class FunctionalTest(base.TestCase):

    PATH_PREFIX = '/v1'

    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.app = self._make_app()

    def tearDown(self):
        super(FunctionalTest, self).tearDown()
        pecan.set_config({}, overwrite=True)

    def _make_app(self):
        root_dir = self.path_get()

        config = {
            'app': {
                'root': 'stripe.api.controllers.root.RootController',
                'modules': ['stripe.api'],
                'static_root': '%s/public' % root_dir,
                'template_path': '%s/api/templates' % root_dir,
                'enable_acl': False,
            },
        }

        return pecan.testing.load_test_app(config)

    def delete(self, path, expect_errors=False, headers=None,
               extra_environ=None, status=None):
        full_path = self.PATH_PREFIX + path
        LOG.debug('DELETE: %s' % (full_path))
        response = self.app.delete(str(full_path),
                                   headers=headers,
                                   status=status,
                                   extra_environ=extra_environ,
                                   expect_errors=expect_errors)
        LOG.debug('GOT: %s' % response)
        return response

    def get_json(self, path, expect_errors=False, headers=None,
                 extra_environ=None, q=[], **params):
        full_path = self.PATH_PREFIX + path
        query_params = {'q.field': [],
                        'q.value': [],
                        'q.op': [],
                        }
        for query in q:
            for name in ['field', 'op', 'value']:
                query_params['q.%s' % name].append(query.get(name, ''))
        all_params = {}
        all_params.update(params)
        if q:
            all_params.update(query_params)
        LOG.debug('GET: %s %r' % (full_path, all_params))
        response = self.app.get(full_path,
                                params=all_params,
                                headers=headers,
                                extra_environ=extra_environ,
                                expect_errors=expect_errors)
        if not expect_errors:
            response = response.json
        LOG.debug('GOT: %s' % response)
        return response

    def post_json(self, path, params={}, expect_errors=False, headers=None,
                  method="post", extra_environ=None, status=None):
        full_path = self.PATH_PREFIX + path
        LOG.debug('%s: %s %s' % (method.upper(), full_path, params))
        response = getattr(self.app, "%s_json" % method)(
            str(full_path),
            params=params,
            headers=headers,
            status=status,
            extra_environ=extra_environ,
            expect_errors=expect_errors
        )
        LOG.debug('GOT: %s' % response)
        return response

    def put_json(self, path, params={}, expect_errors=False, headers=None,
                 extra_environ=None, status=None):
        return self.post_json(path=path, params=params,
                              expect_errors=expect_errors,
                              headers=headers, extra_environ=extra_environ,
                              status=status, method="put")

    def _assertEqualSchemas(self, schema, obj1):
        s = self.get_json('/schemas/%s' % schema)
        model = warlock.model_factory(s)
        obj2 = model(obj1)
        self.assertEqual(obj1, obj2)

    def _create_test_agent(self, **kwargs):
        json = utils.get_api_agent(**kwargs)
        res = self.post_json(
            '/agents', params=json, status=200
        )
        self._assertEqualSchemas('agent', res.json)

        return res.json

    def _create_test_queue(self, **kwargs):
        json = utils.get_api_queue(**kwargs)
        res = self.post_json(
            '/queues', params=json, status=200
        )
        self._assertEqualSchemas('queue', res.json)

        return res.json

    def _create_test_queue_caller(self, queue_id, **kwargs):
        json = utils.get_api_queue_caller(**kwargs)
        res = self.post_json(
            '/queues/%s/callers' % queue_id, params=json, status=200
        )
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')

        return res.json

    def _create_test_user(self, **kwargs):
        json = utils.get_api_user(**kwargs)
        res = self.post_json(
            '/users', params=json, status=200
        )
        self._assertEqualSchemas('user', res.json)

        return res.json
