# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

"""Base class for API tests."""

import pecan
import pecan.testing

from stripe import test


class FunctionalTest(test.TestCase):

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
                'root': 'stripe.api.root.RootController',
                'modules': ['stripe.api'],
                'static_root': '%s/public' % root_dir,
                'template_path': '%s/api/templates' % root_dir,
            },
        }

        return pecan.testing.load_test_app(config)

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
        response = self.app.get(full_path,
                                params=all_params,
                                headers=headers,
                                extra_environ=extra_environ,
                                expect_errors=expect_errors)
        if not expect_errors:
            response = response.json
        return response
