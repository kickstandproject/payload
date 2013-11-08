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

"""Initial database

Revision ID: caa0c1b6be2
Revises: None
Create Date: 2013-08-03 17:41:42.991217

"""

from alembic import op
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

revision = 'caa0c1b6be2'
down_revision = None

agent = (
    'agent',
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('user_id', String(length=255)),
    Column('uuid', String(length=255), unique=True),
)

queue_member = (
    'queue_member',
    Column('id', Integer, primary_key=True, index=True),
    Column('created_at', DateTime),
    Column('agent_id', Integer, unique=True),
    Column('queue_id', Integer),
    Column('updated_at', DateTime),
)

queue = (
    'queue',
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('created_at', DateTime),
    Column('description', Text),
    Column('disabled', Boolean),
    Column('name', String(length=80)),
    Column('updated_at', DateTime),
    Column('user_id', String(length=255)),
    Column('uuid', String(length=255), unique=True),
)

tables = [agent, queue_member, queue]


def upgrade():
    for table in sorted(tables):
        op.create_table(*table)


def downgrade():
    for table in sorted(tables):
        op.drop_table(table[0])
