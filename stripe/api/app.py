# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright © 2012 New Dream Network, LLC (DreamHost)
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

from oslo.config import cfg
import pecan

CONF = cfg.CONF


def setup_app():
    app = pecan.make_app(
        'stripe.api.root.RootController',
        static_root=None,
        debug=CONF.debug,
        force_canonical=True,
    )
    return app


class VersionSelectorApplication(object):
    def __init__(self):
        self.v1 = setup_app()

    def __call__(self, environ, start_response):
        return self.v1(environ, start_response)
