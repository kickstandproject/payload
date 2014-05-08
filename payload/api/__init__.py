# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from oslo.config import cfg

# Register options for the service
API_SERVICE_OPTS = [
    cfg.IntOpt('port',
               default=9859,
               deprecated_name='bind_port',
               deprecated_group='DEFAULT',
               help='The port for the payload API server.',
               ),
    cfg.StrOpt('host',
               default='0.0.0.0',
               deprecated_name='bind_host',
               deprecated_group='DEFAULT',
               help='The listen IP for the payload API server.',
               ),
    cfg.BoolOpt('enable_reverse_dns_lookup',
                default=False,
                help=('Set it to False if your environment does not need '
                      'or have dns server, otherwise it will delay the '
                      'response from api.')
                ),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='api',
                         title='Options for the payload-api service')
CONF.register_group(opt_group)
CONF.register_opts(API_SERVICE_OPTS, opt_group)
