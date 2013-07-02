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

from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)
ENGINE = 'InnoDB'
CHARSET = 'uft8'


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

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

    tables = [queues]

    for table in tables:
        try:
            table.create()
        except Exception:
            LOG.info(repr(table))
            LOG.Exception('Exception while creating table.')
            raise


def downgrade(migrate_engine):
    raise NotImplementedError(
        'Downgrading from initial database is not supported.'
    )
