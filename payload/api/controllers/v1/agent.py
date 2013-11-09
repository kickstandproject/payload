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

import pecan
import wsme

from pecan import rest
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from payload.api.controllers.v1 import base
from payload.common import exception
from payload.db import models
from payload.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class Agent(base.APIBase):
    """API representation of an agent."""

    id = int
    project_id = wtypes.text
    user_id = wtypes.text
    uuid = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.Agent)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class AgentsController(rest.RestController):
    """REST Controller for Agents."""

    _custom_actions = {
        'login': ['POST'],
    }

    @wsme_pecan.wsexpose(None, wtypes.text, status_code=204)
    def delete(self, uuid):
        """Delete an agent."""
        pecan.request.db_api.delete_agent(uuid=uuid)

    @wsme_pecan.wsexpose([Agent])
    def get_all(self):
        """Retrieve a list of agents."""
        res = pecan.request.db_api.list_agents()

        return res

    @wsme_pecan.wsexpose(Agent, unicode)
    def get_one(self, uuid):
        """Retrieve information about the given agent."""
        try:
            result = pecan.request.db_api.get_agent(uuid)
        except exception.AgentNotFound:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError('Not found')

        return result

    @wsme_pecan.wsexpose(None, unicode)
    def login(self, uuid):
        pass

    @wsme.validate(Agent)
    @wsme_pecan.wsexpose(Agent, body=Agent)
    def post(self, body):
        """Create a new agent."""
        user_id = pecan.request.headers.get('X-User-Id')
        project_id = pecan.request.headers.get('X-Tenant-Id')

        try:
            d = body.as_dict()

            if not d.get('uuid'):
                raise wsme.exc.ClientSideError('Invalid data')

            d['user_id'] = user_id
            d['project_id'] = project_id
            new_agent = pecan.request.db_api.create_agent(d)
        except Exception:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError('Invalid data')
        return new_agent

    @wsme.validate(Agent)
    @wsme_pecan.wsexpose(Agent, wtypes.text, body=Agent)
    def put(self, uuid, body):
        """Update an existing agent."""
        agent = pecan.request.db_api.get_agent(uuid=uuid)
        items = body.as_dict().items()
        for k, v in [(k, v) for (k, v) in items if v]:
            agent[k] = v

        agent.save()
        return agent
