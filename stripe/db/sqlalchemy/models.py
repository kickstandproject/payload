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

import json

from sqlalchemy import Column
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, VARCHAR

from stripe.openstack.common.db.sqlalchemy import models


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class StripeBase(models.TimestampMixin, models.ModelBase):

    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d


Base = declarative_base(cls=StripeBase)


class QueueCaller_(Base):
    __tablename__ = 'queue_caller'
    id = Column(Integer, primary_key=True)
    called_id = Column(String(255))
    caller_id = Column(String(255))
    caller_name = Column(String(255))
    queue_id = Column(Integer, ForeignKey('queue.id'))


class QueueMember(Base):
    __tablename__ = 'queue_member'
    id = Column(Integer, primary_key=True)
    disabled = Column(Boolean, default=False)
    disabled_reason = Column(String(255))
    extension = Column(String(255))
    member_id = Column(Integer, ForeignKey('member.id'), unique=True)
    queue_id = Column(Integer, ForeignKey('queue.id'))


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    password = Column(String(255))


class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    description = Column(JSONEncodedDict)
    disabled = Column(Boolean, default=False)
    name = Column(String(80))
