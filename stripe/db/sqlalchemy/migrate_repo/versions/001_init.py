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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

from sqlalchemy import Table, Column, MetaData
from sqlalchemy import DateTime, Integer, String, Text

from stripe.db.sqlalchemy.migrate_repo import schema
from stripe.openstack.common import log as logging


LOG = logging.getLogger(__name__)
ENGINE = 'InnoDB'
CHARSET = 'uft8'


def define_queues_table(meta):
    queues = Table(
        'queues', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('created_at', DateTime),
        Column('description', Text),
        Column('name', String(length=80)),
        Column('updated_at', DateTime),
        mysql_engine=ENGINE,
        mysql_charset=CHARSET,
    )
    return queues


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    tables = [define_queues_table(meta)]
    schema.create_tables(tables)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    tables = [define_queues_table(meta)]
    schema.drop_tables(tables)
