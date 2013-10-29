# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- encoding: utf-8 -*-

# Copyright © 2012 New Dream Network, LLC (DreamHost)
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

import pecan

from oslo.config import cfg

from stripe.api import acl
from stripe.api import config
from stripe.api import hooks
from stripe.api import middleware

auth_opts = [
    cfg.StrOpt(
        'auth_strategy', default='keystone',
        help='The strategy to use for auth: noauth or keystone.'),
]

CONF = cfg.CONF
CONF.register_opts(auth_opts)


def get_pecan_config():
    # Set up the pecan configuration
    filename = config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(pecan_config=None):
    app_hooks = [
        hooks.DBHook(),
        hooks.MiddlewareHook(),
    ]

    if not pecan_config:
        pecan_config = get_pecan_config()

    pecan.configuration.set_config(dict(pecan_config, overwrite=True))

    static_root = None
    if CONF.debug:
        static_root = pecan_config.app.static_root,

    app = pecan.make_app(
        pecan_config.app.root,
        static_root=static_root,
        template_path=pecan_config.app.template_path,
        debug=CONF.debug,
        force_canonical=getattr(pecan_config.app, 'force_canonical', True),
        hooks=app_hooks,
        wrap_app=middleware.ParsableErrorMiddleware,
    )

    if pecan_config.app.enable_acl:
        return acl.install(app, cfg.CONF)

    return app


class VersionSelectorApplication(object):
    def __init__(self):
        self.v1 = setup_app()

    def __call__(self, environ, start_response):
        return self.v1(environ, start_response)
