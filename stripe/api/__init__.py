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

from oslo.config import cfg

API_SERVICE_OPTS = [
    cfg.StrOpt(
        'bind_host', default='0.0.0.0', help='The host IP to bind to'
    ),
    cfg.IntOpt('bind_port', default=9859, help='The port to bind to'),
]

CONF = cfg.CONF
CONF.register_opts(API_SERVICE_OPTS)
