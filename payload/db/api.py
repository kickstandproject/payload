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

from oslo.config import cfg

from payload.openstack.common.db import api as db_api
from payload.openstack.common import log as logging

CONF = cfg.CONF

_BACKEND_MAPPING = {'sqlalchemy': 'payload.db.sqlalchemy.api'}

IMPL = db_api.DBAPI(backend_mapping=_BACKEND_MAPPING)
LOG = logging.getLogger(__name__)


def create_agent(user_id, project_id):
    """Create a new agent."""

    return IMPL.create_agent(user_id=user_id, project_id=project_id)


def create_queue(name, user_id, project_id, description='', disabled=False):
    """Create a new queue."""

    return IMPL.create_queue(
        name=name, user_id=user_id, project_id=project_id,
        description=description, disabled=disabled)


def create_queue_member(agent_uuid, queue_uuid):
    """Create a new queue member."""

    return IMPL.create_queue_member(
        agent_uuid=agent_uuid, queue_uuid=queue_uuid)


def delete_agent(uuid):
    """Delete an agent."""

    IMPL.delete_agent(uuid=uuid)


def delete_queue(uuid):
    """Delete a queue."""

    IMPL.delete_queue(uuid=uuid)


def delete_queue_member(agent_uuid, queue_uuid):
    """Delete a queue member."""

    IMPL.delete_queue_member(agent_uuid=agent_uuid, queue_uuid=queue_uuid)


def get_agent(uuid):
    """Retrieve information about the given agent."""

    return IMPL.get_agent(uuid=uuid)


def get_queue(uuid):
    """Retrieve information about the given queue."""

    return IMPL.get_queue(uuid=uuid)


def get_queue_member(agent_uuid, queue_uuid):
    """Retrieve information about the given queue member."""

    return IMPL.get_queue_member(
        agent_uuid=agent_uuid, queue_uuid=queue_uuid)


def list_agents():
    """Retrieve a list of agents."""

    return IMPL.list_agents()


def list_queues():
    """Retrieve a list of queues."""

    return IMPL.list_queues()


def list_queue_members(uuid):
    """Retrieve a list of queue members."""

    return IMPL.list_queue_members(uuid=uuid)
