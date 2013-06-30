# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
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
Routines for configuring Stripe
"""

from oslo.config import cfg
from stripe.version import VERSION_INFO as version

common_opts = [
]

CONF = cfg.CONF
CONF.register_opts(common_opts)


def parse_args(args=None, usage=None, default_config_files=None):
    CONF(
        args=args,
        project='stripe',
        version=version,
        usage=usage,
        default_config_files=default_config_files
    )
