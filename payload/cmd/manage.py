# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

"""
  CLI interface for payload management.
"""

import logging

from oslo.config import cfg

from payload.db import migration as db_migration
from payload.openstack.common import log
from payload import service

CONF = cfg.CONF
LOG = log.getLogger(__name__)


def do_db_version():
    """Print database's current migration level."""
    print(db_migration.db_version())


def do_db_sync():
    """Place a database under migration control and upgrade,
    creating first if necessary.
    """
    db_migration.db_sync(CONF.command.version)


def add_command_parsers(subparsers):
    parser = subparsers.add_parser('db-version')
    parser.set_defaults(func=do_db_version)

    parser = subparsers.add_parser('db-sync')
    parser.set_defaults(func=do_db_sync)
    parser.add_argument('version', nargs='?')
    parser.add_argument('current_version', nargs='?')

    parser.add_argument(
        '-g', '--granularity', default='days',
        choices=['days', 'hours', 'minutes', 'seconds'],
        help='Granularity to use for age argument, defaults to days.')

command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Available commands',
                                handler=add_command_parsers)


def main():
    CONF.register_cli_opt(command_opt)
    service.prepare_service()
    CONF.log_opt_values(LOG, logging.INFO)

    try:
        CONF.command.func()
    except Exception as e:
        LOG.exception(e)
