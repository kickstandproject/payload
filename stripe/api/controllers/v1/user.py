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

from stripe.api.controllers.v1 import base
from stripe.common import exception
from stripe.db import models
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class User(base.APIBase):
    """API representation of a user."""

    id = int
    email = wtypes.text
    name = wtypes.text
    password = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.User)
        for k in self.fields:
            setattr(self, k, kwargs.get(k))


class UsersController(rest.RestController):
    """REST Controller for users."""

    @wsme_pecan.wsexpose(None, wtypes.text, status_code=204)
    def delete(self, id):
        """Delete a user."""
        pecan.request.db_api.delete_user(id)

    @wsme_pecan.wsexpose([User])
    def get_all(self):
        """Retrieve a list of users."""
        res = pecan.request.db_api.list_users()

        return res

    @wsme_pecan.wsexpose(User, unicode)
    def get_one(self, id):
        """Retrieve information about the given user."""
        try:
            result = pecan.request.db_api.get_user(id)
        except exception.UserNotFound:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError('Not found')

        return result

    @wsme.validate(User)
    @wsme_pecan.wsexpose(User, body=User)
    def post(self, body):
        """Create a new user."""
        try:
            d = body.as_dict()
            res = pecan.request.db_api.create_user(d)
        except Exception:
            # TODO(pabelanger): See if there is a better way of handling
            # exceptions.
            raise wsme.exc.ClientSideError('Invalid data')
        return res

    @wsme.validate(User)
    @wsme_pecan.wsexpose(User, wtypes.text, body=User)
    def put(self, id, body):
        res = pecan.request.db_api.get_user(id)
        items = body.as_dict().items()
        for k, v in [(k, v) for (k, v) in items if v]:
            res[k] = v

        res.save()
        return res
