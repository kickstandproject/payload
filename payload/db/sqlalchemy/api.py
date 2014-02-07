# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
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

"""SQLAlchemy storage backend."""

import sys

from sqlalchemy.orm import exc

from payload.common import exception
from payload.db.sqlalchemy import models
from payload.openstack.common.db.sqlalchemy import session as db_session
from payload.openstack.common import log as logging
from payload.openstack.common import uuidutils

LOG = logging.getLogger(__name__)

get_session = db_session.get_session


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def _model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


def create_agent(user_id, project_id):
    """Create a new agent."""
    values = {
        'project_id': project_id,
        'user_id': user_id,
    }

    values['uuid'] = uuidutils.generate_uuid()
    res = _create_model(model=models.Agent(), values=values)

    return res


def create_queue(name, user_id, project_id, description='', disabled=False):
    """Create a new queue."""
    values = {
        'description': description,
        'disabled': disabled,
        'name': name,
        'project_id': project_id,
        'user_id': user_id,
    }

    values['uuid'] = uuidutils.generate_uuid()
    res = _create_model(model=models.Queue(), values=values)

    return res


def create_queue_member(agent_uuid, queue_uuid):
    """Create a new queue member."""
    values = {
        'agent_uuid': agent_uuid,
        'queue_uuid': queue_uuid,
    }
    res = _create_model(model=models.QueueMember(), values=values)

    return res


def delete_agent(uuid):
    """Delete an agent."""
    res = _delete_model(model=models.Agent, uuid=uuid)

    if res != 1:
        raise exception.AgentNotFound(uuid=uuid)


def delete_queue(uuid):
    """Delete a queue."""
    res = _delete_model(model=models.Queue, uuid=uuid)

    if res != 1:
        raise exception.QueueNotFound(uuid=uuid)


def delete_queue_member(agent_uuid, queue_uuid):
    """Delete a queue member."""
    res = _delete_model(
        model=models.QueueMember, agent_uuid=agent_uuid,
        queue_uuid=queue_uuid)

    if res != 1:
        raise exception.QueueMemberNotFound(uuid=agent_uuid)


def get_agent(uuid):
    """Retrieve information about the given agent."""
    try:
        res = _get_model(model=models.Agent, uuid=uuid)
    except exc.NoResultFound:
        raise exception.AgentNotFound(uuid=uuid)

    return res


def get_queue(uuid):
    """Retrieve information about the given queue."""
    try:
        res = _get_model(model=models.Queue, uuid=uuid)
    except exc.NoResultFound:
        raise exception.QueueNotFound(uuid=uuid)

    return res


def get_queue_member(agent_uuid, queue_uuid):
    """Retrieve information about the given queue member."""
    try:
        res = _get_model(
            model=models.QueueMember, agent_uuid=agent_uuid,
            queue_uuid=queue_uuid)
    except exc.NoResultFound:
        raise exception.QueueMemberNotFound(uuid=agent_uuid)

    return res


def list_agents():
    """Retrieve a list of agents."""
    res = _list_model(model=models.Agent)

    return res


def list_queues():
    """Retrieve a list of queues."""
    res = _list_model(model=models.Queue)

    return res


def list_queue_members(uuid):
    """Retrieve a list of queue members."""
    res = _list_model(model=models.QueueMember, queue_uuid=uuid)

    return res


def _create_model(model, values):
    """Create a new model."""
    model.update(values)
    model.save()

    return model


def _delete_model(model, **kwargs):
    session = get_session()
    with session.begin():
        query = _model_query(
            model, session=session
        ).filter_by(**kwargs)

        count = query.delete()

        return count


def _get_model(model, **kwargs):
    """Retrieve information about the given model."""
    query = _model_query(model).filter_by(**kwargs)
    res = query.one()

    return res


def _list_model(model, **kwargs):
    """Retrieve a list of the given model."""
    query = _model_query(model).filter_by(**kwargs)

    return query.all()
