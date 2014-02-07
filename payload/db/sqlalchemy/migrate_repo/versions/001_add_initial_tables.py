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

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint

from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    agents = Table(
        'agents', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('created_at', DateTime),
        Column('project_id', String(length=255)),
        Column('updated_at', DateTime),
        Column('user_id', String(length=255)),
        Column('uuid', String(length=255), unique=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8',
    )

    queue_members = Table(
        'queue_members', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('created_at', DateTime),
        Column('agent_uuid', String(255)),
        Column('queue_uuid', String(255)),
        Column('updated_at', DateTime),
        ForeignKeyConstraint(['agent_uuid'], ['agents.uuid'],),
        ForeignKeyConstraint(['queue_uuid'], ['queues.uuid'],),
        UniqueConstraint(
            'agent_uuid', 'queue_uuid',
            name='uniq_queue_members0agent_uuid0queue_uuid'),
        mysql_engine='InnoDB',
        mysql_charset='utf8',
    )

    queues = Table(
        'queues', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('created_at', DateTime),
        Column('description', Text),
        Column('disabled', Boolean),
        Column('name', String(length=80)),
        Column('project_id', String(length=255)),
        Column('updated_at', DateTime),
        Column('user_id', String(length=255)),
        Column('uuid', String(length=255), unique=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8',
    )

    tables = [agents, queue_members, queues]

    for table in tables:
        try:
            table.create()
        except Exception:
            LOG.info(repr(table))
            LOG.exception('Exception while creating table.')
            raise


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
