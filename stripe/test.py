# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

import fixtures
import os
import shutil
import testtools

from oslo.config import cfg

from stripe.common import paths
from stripe.db import migration
from stripe.openstack.common.db.sqlalchemy import session
from stripe.openstack.common import log as logging
from stripe.tests import conf_fixture


test_opts = [
    cfg.StrOpt(
        'sqlite_clean_db', default='clean.sqlite',
        help='Filename of clean sqlite db',
    ),
]

CONF = cfg.CONF
CONF.register_opts(test_opts)
CONF.import_opt(
    'connection', 'stripe.openstack.common.db.sqlalchemy.session',
    group='database'
)
CONF.import_opt('sqlite_db', 'stripe.openstack.common.db.sqlalchemy.session')

logging.setup('stripe')

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
            self._DB = "".join(line for line in conn.connection.iterdump())
            self.engine.dispose()
        else:
            cleandb = paths.state_path_rel(sqlite_clean_db)
            shutil.copyfile(testdb, cleandb)

    def setUp(self):
        super(Database, self).setUp()

        if self.sql_connection == "sqlite://":
            conn = self.engine.connect()
            conn.connection.executescript(self._DB)
            self.addCleanup(self.engine.dispose)
        else:
            shutil.copyfile(paths.state_path_rel(self.sqlite_clean_db),
                            paths.state_path_rel(self.sqlite_db))


class TestCase(testtools.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Run before each method to initialize test environment."""
        super(TestCase, self).setUp()

        self.useFixture(conf_fixture.ConfFixture(CONF))

        global _DB_CACHE
        if not _DB_CACHE:
            _DB_CACHE = Database(
                session, migration, sql_connection=CONF.database.connection,
                sqlite_db=CONF.sqlite_db, sqlite_clean_db=CONF.sqlite_clean_db
            )
        self.useFixture(_DB_CACHE)

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
