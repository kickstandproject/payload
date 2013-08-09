# vim: tabstop=4 shiftwidth=4 softtabstop=4

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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Drop QueueCallers table

Revision ID: 4da98432c4cd
Revises: caa0c1b6be2
Create Date: 2013-08-08 21:53:16.346831

"""

from alembic import op
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

revision = '4da98432c4cd'
down_revision = 'caa0c1b6be2'

queue_caller = (
    'queue_caller',
    Column('id', Integer, primary_key=True, index=True),
    Column('created_at', DateTime),
    Column('called_id', String(255)),
    Column('caller_id', String(255)),
    Column('caller_name', String(255)),
    Column('queue_id', Integer),
    Column('updated_at', DateTime),
)

tables = [queue_caller]


def upgrade():
    for table in sorted(tables):
        op.drop_table(table[0])


def downgrade():
    for table in sorted(tables):
        op.create_table(*table)
