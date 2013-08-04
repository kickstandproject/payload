# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
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

"""SQLAlchemy storage backend."""

from sqlalchemy.orm import exc

from stripe.common import exception
from stripe.db import models
from stripe.openstack.common.db import api
from stripe.openstack.common.db.sqlalchemy import session as db_session
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)

get_session = db_session.get_session


def get_instance():
    """Return a DB API instance."""
    backend_mapping = {'sqlalchemy': 'stripe.db.api'}

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
        agent = models.Agent()
        agent.update(values)
        agent.save()

        return agent

    def create_queue(self, values):
        """Create a new queue."""
        queue = models.Queue()
        queue.update(values)
        queue.save()

        return queue

    def delete_agent(self, agent):
        """Delete an agent."""
        session = get_session()
        with session.begin():
            query = model_query(
                models.Agent, session=session
            ).filter_by(id=agent)

            count = query.delete()
            if count != 1:
                raise exception.AgentNotFound(agent=agent)

            query.delete()

    def delete_queue(self, queue):
        """Delete a queue."""
        session = get_session()
        with session.begin():
            query = model_query(
                models.Queue, session=session
            ).filter_by(id=queue)

            count = query.delete()
            if count != 1:
                raise exception.QueueNotFound(queue=queue)

            query.delete()

    def get_agent(self, agent):
        """Retrieve information about the given agent."""
        query = model_query(models.Agent).filter_by(id=agent)
        try:
            result = query.one()
        except exc.NoResultFound:
            raise exception.AgentNotFound(agent=agent)

        return result

    def get_queue(self, queue):
        """Retrieve information about the given queue."""
        query = model_query(models.Queue).filter_by(id=queue)
        try:
            result = query.one()
        except exc.NoResultFound:
            raise exception.QueueNotFound(queue=queue)

        return result

    def get_agent_list(self):
        """Retrieve a list of agents."""
        query = model_query(models.Agent)

        return [a for a in query.all()]

    def get_queue_list(self):
        """Retrieve a list of queues."""
        query = model_query(models.Queue)

        return [q for q in query.all()]
