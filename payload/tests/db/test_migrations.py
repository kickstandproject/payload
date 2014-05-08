# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010-2011 OpenStack Foundation
# Copyright 2012-2013 IBM Corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Tests for database migrations. This test case reads the configuration
file test_migrations.conf for database connection settings
to use in the tests. For each connection found in the config file,
the test case runs a series of test cases to ensure that migrations work
properly both upgrading and downgrading, and that no data loss occurs
if possible.

There are also "opportunistic" tests for mysql and postgresql in here, which
allows testing against all 3 databases (sqlite in memory, mysql and postgresql)
in a properly configured unit test environment.

For the opportunistic testing you need to set up a db named 'kickstand_citest'
with user 'kickstand_citest' and password 'kickstand_citest' on localhost.
The test will then use that db and u/p combo to run the tests.
"""

import os
import shutil
import tempfile
import urlparse

from migrate.versioning import repository
from oslo.config import cfg
import sqlalchemy
from sqlalchemy import exc

from payload.db import migration
from payload.db.sqlalchemy import migrate_repo
from payload.db.sqlalchemy import utils as db_utils
from payload.openstack.common.db.sqlalchemy import test_migrations
from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class TestPayloadMigrations(test_migrations.BaseMigrationTestCase,
                            test_migrations.WalkVersionsMixin):
    """Test sqlalchemy-migrate migrations."""

    USER = "kickstand_citest"
    PASSWD = "kickstand_citest"
    DATABASE = "kickstand_citest"

    def __init__(self, *args, **kwargs):
        super(TestPayloadMigrations, self).__init__(*args, **kwargs)

        self.DEFAULT_CONFIG_FILE = os.path.join(
            os.path.dirname(__file__), 'test_migrations.conf')
        # Test machines can set the PAYLOAD_TEST_MIGRATIONS_CONF variable
        # to override the location of the config file for migration testing
        self.CONFIG_FILE_PATH = os.environ.get(
            'PAYLOAD_TEST_MIGRATIONS_CONF', self.DEFAULT_CONFIG_FILE)
        self.MIGRATE_FILE = migrate_repo.__file__
        self.REPOSITORY = repository.Repository(
            os.path.abspath(os.path.dirname(self.MIGRATE_FILE)))

    def setUp(self):
        lock_path = tempfile.mkdtemp()
        CONF.set_override('lock_path', lock_path)

        super(TestPayloadMigrations, self).setUp()

        def clean_lock_path():
            shutil.rmtree(lock_path, ignore_errors=True)

        self.addCleanup(clean_lock_path)
        self.snake_walk = True
        self.downgrade = True
        self.INIT_VERSION = migration.INIT_VERSION

        if self.migration_api is None:
            temp = __import__(
                'payload.openstack.common.db.sqlalchemy.migration',
                globals(), locals(), ['versioning_api'], -1)
            self.migration_api = temp.versioning_api

    def _test_mysql_opportunistically(self):
        # Test that table creation on mysql only builds InnoDB tables
        if not test_migrations._have_mysql(
                self.USER, self.PASSWD, self.DATABASE):
            self.skipTest("mysql not available")
        # add this to the global lists to make reset work with it, it's removed
        # automatically in tearDown so no need to clean it up here.
        connect_string = test_migrations._get_connect_string(
            "mysql", self.USER, self.PASSWD, self.DATABASE)
        (user, password, database, host) = \
            test_migrations.get_db_connection_info(urlparse.urlparse(
                connect_string))
        engine = sqlalchemy.create_engine(connect_string)
        self.engines[database] = engine
        self.test_databases[database] = connect_string

        # build a fully populated mysql database with all the tables
        self._reset_databases()
        self._walk_versions(engine, self.snake_walk)

        connection = engine.connect()
        # sanity check
        total = connection.execute("SELECT count(*) "
                                   "from information_schema.TABLES "
                                   "where TABLE_SCHEMA='%(database)s'" %
                                   {'database': database})
        self.assertTrue(total.scalar() > 0, "No tables found. Wrong schema?")

        noninnodb = connection.execute("SELECT count(*) "
                                       "from information_schema.TABLES "
                                       "where TABLE_SCHEMA='%(database)s' "
                                       "and ENGINE!='InnoDB' "
                                       "and TABLE_NAME!='migrate_version'" %
                                       {'database': database})
        count = noninnodb.scalar()
        self.assertEqual(count, 0, "%d non InnoDB tables created" % count)
        connection.close()

    def _test_postgresql_opportunistically(self):
        # Test postgresql database migration walk
        if not test_migrations._have_postgresql(
                self.USER, self.PASSWD, self.DATABASE):
            self.skipTest("postgresql not available")
        # add this to the global lists to make reset work with it, it's removed
        # automatically in tearDown so no need to clean it up here.
        connect_string = test_migrations._get_connect_string(
            "postgres", self.USER, self.PASSWD, self.DATABASE)
        engine = sqlalchemy.create_engine(connect_string)
        (user, password, database, host) = \
            test_migrations.get_db_connection_info(urlparse.urlparse(
                connect_string))
        self.engines[database] = engine
        self.test_databases[database] = connect_string

        # build a fully populated postgresql database with all the tables
        self._reset_databases()
        self._walk_versions(engine, self.snake_walk)

    def assertColumnExists(self, engine, table, column):
        t = db_utils.get_table(engine, table)
        self.assertIn(column, t.c)

    def assertColumnNotExists(self, engine, table, column):
        t = db_utils.get_table(engine, table)
        self.assertNotIn(column, t.c)

    def test_mysql_opportunistically(self):
        self._test_mysql_opportunistically()

    def test_mysql_connect_fail(self):
        """Check mysql doesn't exists.

        Test that we can trigger a mysql connection failure and we fail
        gracefully to ensure we don't break people without mysql
        """
        if test_migrations._is_backend_avail(
                'mysql', 'kickstand_cifail', self.PASSWD, self.DATABASE):
            self.fail("Shouldn't have connected")

    def test_postgresql_opportunistically(self):
        self._test_postgresql_opportunistically()

    def test_postgresql_connect_fail(self):
        """Check postgres doesn't exists.

        Test that we can trigger a postgres connection failure and we fail
        gracefully to ensure we don't break people without postgres
        """
        if test_migrations._is_backend_avail(
                'postgres', 'kickstand_cifail', self.PASSWD, self.DATABASE):
            self.fail("Shouldn't have connected")

    def test_walk_versions(self):
        for key, engine in self.engines.items():
            self._walk_versions(engine, self.snake_walk, self.downgrade)

    def _check_001(self, engine, data):
        cols = [
            'id', 'created_at', 'project_id', 'updated_at', 'user_id', 'uuid']

        for c in cols:
            self.assertColumnExists(engine, 'agents', c)

        cols = [
            'id', 'created_at', 'description', 'disabled', 'name',
            'project_id', 'updated_at', 'user_id', 'uuid']

        for c in cols:
            self.assertColumnExists(engine, 'queues', c)

        cols = [
            'id', 'created_at', 'agent_uuid', 'queue_uuid', 'updated_at']

        for c in cols:
            self.assertColumnExists(engine, 'queue_members', c)

    def _post_downgrade_001(self, engine):
        self.assertRaises(
            exc.NoSuchTableError, db_utils.get_table, engine, 'agents')
        self.assertRaises(
            exc.NoSuchTableError, db_utils.get_table, engine, 'queues')
        self.assertRaises(
            exc.NoSuchTableError, db_utils.get_table, engine, 'queue_memebers')
