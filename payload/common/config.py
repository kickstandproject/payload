# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
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
Routines for configuring payload
"""

from oslo.config import cfg

from payload.common import paths
from payload.openstack.common.db.sqlalchemy import session as db_session
from payload import version

CONF = cfg.CONF
_DEFAULT_SQL_CONNECTION = 'sqlite:///' + paths.state_path_def('$sqlite_db')


def parse_args(args=None, usage=None, default_config_files=None):
    db_session.set_defaults(
        sql_connection=_DEFAULT_SQL_CONNECTION, sqlite_db='payload.sqlite'
    )
    CONF(
        args=args,
        project='payload',
        version=version.VERSION_INFO,
        usage=usage,
        default_config_files=default_config_files
    )
