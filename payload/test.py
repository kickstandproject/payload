# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

import fixtures
import os
import redis
import shutil
import testtools
import time

from oslo.config import cfg

from payload.common import paths
from payload.db import migration
from payload.openstack.common.db.sqlalchemy import session
from payload.openstack.common import log as logging
from payload.tests import conf_fixture


TEST_OPTS = [
    cfg.StrOpt(
        'sqlite_clean_db', default='clean.sqlite',
        help='Filename of clean sqlite db',
    ),
]

CONF = cfg.CONF
CONF.register_opts(TEST_OPTS)
CONF.import_opt(
    'connection', 'payload.openstack.common.db.sqlalchemy.session',
    group='database'
)
CONF.import_opt('sqlite_db', 'payload.openstack.common.db.sqlalchemy.session')

logging.setup('payload')

_DB_CACHE = None


class Database(fixtures.Fixture):

    def __init__(self, db_session, db_migrate, sql_connection,
                 sqlite_db, sqlite_clean_db):
        self.sql_connection = sql_connection
        self.sqlite_db = sqlite_db
        self.sqlite_clean_db = sqlite_clean_db

        self.engine = db_session.get_engine()
        self.engine.dispose()
        conn = self.engine.connect()
        if sql_connection == "sqlite://":
            if db_migrate.db_version() > db_migrate.INIT_VERSION:
                return
        else:
            testdb = paths.state_path_rel(sqlite_db)
            if os.path.exists(testdb):
                return
        db_migrate.db_sync()
        if sql_connection == "sqlite://":
            conn = self.engine.connect()
            self._db = "".join(line for line in conn.connection.iterdump())
            self.engine.dispose()
        else:
            cleandb = paths.state_path_rel(sqlite_clean_db)
            shutil.copyfile(testdb, cleandb)

    def setUp(self):
        super(Database, self).setUp()

        if self.sql_connection == "sqlite://":
            conn = self.engine.connect()
            conn.connection.executescript(self._db)
            self.addCleanup(self.engine.dispose)
        else:
            shutil.copyfile(paths.state_path_rel(self.sqlite_clean_db),
                            paths.state_path_rel(self.sqlite_db))


class Redis(fixtures.Fixture):

    def setUp(self):
        super(Redis, self).setUp()

        _session = redis.StrictRedis(
            host=CONF.middleware.host, port=CONF.middleware.port,
            db=CONF.middleware.database, password=CONF.middleware.password,
        )
        _session.flushdb()
        keys = _session.keys()
        count = 0
        # TODO(pabelanger): This whole section needs to be changed.  The way to
        # properly do it is have redis setup a new namespace per unit test,
        # checking if it first exists, and if then removing it.
        while keys != []:
            time.sleep(1)
            if count > 5:
                raise Exception('Redis took too long')
            count += 1
            keys = _session.keys()


class TestCase(testtools.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Run before each method to initialize test environment."""
        super(TestCase, self).setUp()

        self.log_fixture = self.useFixture(fixtures.FakeLogger())
        self.useFixture(conf_fixture.ConfFixture(CONF))

        global _DB_CACHE
        if not _DB_CACHE:
            _DB_CACHE = Database(
                session, migration, sql_connection=CONF.database.connection,
                sqlite_db=CONF.sqlite_db, sqlite_clean_db=CONF.sqlite_clean_db
            )
        self.useFixture(_DB_CACHE)
        _redis = Redis()
        self.useFixture(_redis)

    def path_get(self, project_file=None):
        """Get the absolute path to a file. Used for testing the API.

        :param project_file: File whose path to return. Default: None.
        :returns: path to the specified file, or path to project root.
        """
        root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..')
        )

        if project_file:
            return os.path.join(root, project_file)
        else:
            return root

    def config(self, **kw):
        """Override some configuration values.

        The keyword arguments are the names of configuration options to
        override and their values.

        If a group argument is supplied, the overrides are applied to
        the specified configuration option group.

        All overrides are automatically cleared at the end of the current
        test by the fixtures cleanup process.
        """
        group = kw.pop('group', None)
        for k, v in kw.iteritems():
            CONF.set_override(k, v, group)
