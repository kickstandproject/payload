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

import os

from payload.common import utils

IMPL = utils.LazyPluggable(
    'backend', config_group='database',
    sqlalchemy='payload.openstack.common.db.sqlalchemy.migration')

INIT_VERSION = 0

MIGRATE_REPO_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'sqlalchemy',
    'migrate_repo')


def db_sync(version=None):
    """Migrate the database to `version` or the most recent version."""
    return IMPL.db_sync(abs_path=MIGRATE_REPO_PATH, version=version)


def db_version():
    """Display the current database version."""
    return IMPL.db_version(
        abs_path=MIGRATE_REPO_PATH, init_version=INIT_VERSION)
