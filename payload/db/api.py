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

from sqlalchemy.orm import exc

from payload.common import exception
from payload.db import models
from payload.openstack.common.db import api
from payload.openstack.common.db.sqlalchemy import session as db_session
from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)

get_session = db_session.get_session


def get_instance():
    """Return a DB API instance."""
    backend_mapping = {'sqlalchemy': 'payload.db.api'}

    return api.DBAPI(backend_mapping=backend_mapping)


def get_backend():
    """The backend is this module itself."""
    return Connection()


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


class Connection(object):
    """SqlAlchemy connection."""

    def __init__(self):
        pass

    def create_agent(self, values):
        """Create a new agent."""
        res = self._create_model(model=models.Agent(), values=values)

        return res

    def create_queue(self, values):
        """Create a new queue."""
        res = self._create_model(model=models.Queue(), values=values)

        return res

    def create_queue_member(self, agent_id, queue_id):
        """Create a new queue member."""
        values = {
            'agent_id': agent_id,
            'queue_id': queue_id,
        }
        res = self._create_model(model=models.QueueMember(), values=values)

        return res

    def delete_agent(self, agent_id):
        """Delete an agent."""
        res = self._delete_model(model=models.Agent, id=agent_id)

        if res != 1:
            raise exception.AgentNotFound(agent_id=agent_id)

    def delete_queue(self, queue_id):
        """Delete a queue."""
        res = self._delete_model(model=models.Queue, id=queue_id)

        if res != 1:
            raise exception.QueueNotFound(queue_id=queue_id)

    def delete_queue_member(self, agent_id, queue_id):
        """Delete a queue member."""
        res = self._delete_model(
            model=models.QueueMember, agent_id=agent_id, queue_id=queue_id
        )

        if res != 1:
            raise exception.QueueMemberNotFound(
                agent_id=agent_id
            )

    def get_agent(self, agent_id):
        """Retrieve information about the given agent."""
        try:
            res = self._get_model(model=models.Agent, id=agent_id)
        except exc.NoResultFound:
            raise exception.AgentNotFound(agent_id=agent_id)

        return res

    def get_queue(self, queue_id):
        """Retrieve information about the given queue."""
        try:
            res = self._get_model(model=models.Queue, id=queue_id)
        except exc.NoResultFound:
            raise exception.QueueNotFound(queue_id=queue_id)

        return res

    def get_queue_member(self, agent_id, queue_id):
        """Retrieve information about the given queue member."""
        try:
            res = self._get_model(
                model=models.QueueMember, agent_id=agent_id, queue_id=queue_id
            )
        except exc.NoResultFound:
            raise exception.QueueMemberNotFound(
                agent_id=agent_id
            )

        return res

    def get_user(self, user_id):
        """Retrieve information about the given user."""
        try:
            res = self._get_model(model=models.User, id=user_id)
        except exc.NoResultFound:
            raise exception.UserNotFound(user_id=user_id)

        return res

    def list_agents(self):
        """Retrieve a list of agents."""
        res = self._list_model(model=models.Agent)

        return res

    def list_queues(self):
        """Retrieve a list of queues."""
        res = self._list_model(model=models.Queue)

        return res

    def list_queue_members(self):
        """Retrieve a list of queue members."""
        res = self._list_model(model=models.QueueMember)

        return res

    def list_users(self):
        """Retrieve a list of users."""
        res = self._list_model(model=models.User)

        return res

    def _create_model(self, model, values):
        """Create a new model."""
        model.update(values)
        model.save()

        return model

    def _delete_model(self, model, **kwargs):
        session = get_session()
        with session.begin():
            query = model_query(
                model, session=session
            ).filter_by(**kwargs)

            count = query.delete()

            return count

    def _get_model(self, model, **kwargs):
        """Retrieve information about the given model."""
        query = model_query(model).filter_by(**kwargs)
        res = query.one()

        return res

    def _list_model(self, model):
        """Retrieve a list of the given model."""
        query = model_query(model)

        return [m for m in query.all()]
