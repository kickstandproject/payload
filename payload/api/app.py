# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2012 New Dream Network, LLC (DreamHost)
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

import logging
import os
import socket
from wsgiref import simple_server

import netaddr
from oslo.config import cfg
from paste import deploy
import pecan

from payload.api import config
from payload.api import hooks
from payload.api import middleware
from payload.openstack.common import log

LOG = log.getLogger(__name__)

auth_opts = [
    cfg.StrOpt('api_paste_config',
               default="api_paste.ini",
               help="Configuration file for WSGI definition of API."),
]

CONF = cfg.CONF
CONF.register_opts(auth_opts)


def app_factory(global_config, **local_conf):
        return VersionSelectorApplication()


def build_server():
    app = load_app()
    # Create the WSGI server and start it
    host, port = cfg.CONF.api.host, cfg.CONF.api.port
    server_cls = get_server_cls(host)

    srv = simple_server.make_server(
        host, port, app, server_cls, get_handler_cls())

    LOG.info('Starting server in PID %s' % os.getpid())
    LOG.info("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.INFO)

    if host == '0.0.0.0':
        LOG.info(
            'serving on 0.0.0.0:%(sport)s, view at http://127.0.0.1:%(vport)s'
            % ({'sport': port, 'vport': port}))
    else:
        LOG.info("serving on http://%(host)s:%(port)s" % (
                 {'host': host, 'port': port}))

    return srv


def get_handler_cls():
    cls = simple_server.WSGIRequestHandler

    # old-style class doesn't support super
    class CeilometerHandler(cls, object):
        def address_string(self):
            if cfg.CONF.api.enable_reverse_dns_lookup:
                return super(CeilometerHandler, self).address_string()
            else:
                # disable reverse dns lookup, directly return ip adress
                return self.client_address[0]

    return CeilometerHandler


def get_pecan_config():
    # Set up the pecan configuration
    filename = config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def get_server_cls(host):
    """Return an appropriate WSGI server class base on provided host

    :param host: The listen host for the ceilometer API server.
    """
    server_cls = simple_server.WSGIServer
    if netaddr.valid_ipv6(host):
        # NOTE(dzyu) make sure use IPv6 sockets if host is in IPv6 pattern
        if getattr(server_cls, 'address_family') == socket.AF_INET:
            class server_cls(server_cls):
                address_family = socket.AF_INET6
    return server_cls


def load_app():
    # Build the WSGI app
    cfg_file = cfg.CONF.api_paste_config
    LOG.info("WSGI config requested: %s" % cfg_file)
    if not os.path.exists(cfg_file):
        # NOTE(pabelanger): This is a temp solution and should be resolved.
        root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', '..', 'etc', 'payload'))
        cfg_file = os.path.join(root, cfg_file)
    if not os.path.exists(cfg_file):
        raise Exception('api_paste_config file not found')
    LOG.info("Full WSGI config used: %s" % cfg_file)
    return deploy.loadapp("config:" + cfg_file)


def setup_app(pecan_config=None):
    app_hooks = [
        hooks.DBHook(),
        hooks.MiddlewareHook(),
    ]

    if not pecan_config:
        pecan_config = get_pecan_config()

    pecan.configuration.set_config(dict(pecan_config, overwrite=True))

    app = pecan.make_app(
        pecan_config.app.root,
        static_root=pecan_config.app.static_root,
        template_path=pecan_config.app.template_path,
        debug=CONF.debug,
        force_canonical=getattr(pecan_config.app, 'force_canonical', True),
        hooks=app_hooks,
        wrap_app=middleware.ParsableErrorMiddleware,
        guess_content_type_from_ext=False)

    return app


class VersionSelectorApplication(object):
    def __init__(self):
        pc = get_pecan_config()
        pc.app.debug = CONF.debug
        self.v1 = setup_app(pecan_config=pc)

    def __call__(self, environ, start_response):
        return self.v1(environ, start_response)
