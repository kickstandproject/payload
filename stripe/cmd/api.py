# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

"""
Stripe API Server
"""

from pecan import make_app
from stripe.common import config
from stripe.common import log
from wsgiref import simple_server


def setup_app():
    app = make_app(
        'stripe.api.root.RootController',
        static_root='%(confdir)s/public',
        template_path='%(confdir)s/stripe/api/templates',
        debug=False,
        force_canonical=True,
    )
    return app


class Application(object):
    def __init__(self):
        self.v1 = setup_app()

    def __call__(self, environ, start_response):
        return self.v1(environ, start_response)


def main():
    config.parse_args()
    log.setup('stripe')
    application = Application()
    server = simple_server.make_server('0.0.0.0', 8080, application)
    server.serve_forever()
