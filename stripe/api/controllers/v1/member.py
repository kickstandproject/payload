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

import pecan
import wsme

from pecan import rest
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from stripe.api.controllers.v1 import base
from stripe.common import exception
from stripe.db.sqlalchemy import models
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class Member(base.APIBase):
    """API representation of a member."""

    id = int
    name = wtypes.text
    password = wtypes.text

    def __init__(self, **kwargs):
        self.fields = vars(models.Member)
        for k in self.fields:
                setattr(self, k, kwargs.get(k))


class MembersController(rest.RestController):
    """REST Controller for Members."""

    @wsme_pecan.wsexpose(None, wtypes.text, status_code=204)
    def delete(self, id):
        """Delete a member."""
        pecan.request.db_api.delete_member(id)

    @wsme_pecan.wsexpose([Member])
    def get_all(self):
        """Retrieve a list of member."""
        return pecan.request.db_api.get_member_list()

    @wsme_pecan.wsexpose(Member, unicode)
    def get_one(self, id):
        """Retrieve information about the given member."""
        try:
            result = pecan.request.db_api.get_member(id)
        except exception.MemberNotFound:
            pecan.abort(404)

        return result

    @wsme.validate(Member)
    @wsme_pecan.wsexpose(Member, body=Member)
    def post(self, body):
        """Create a new member."""
        try:
            d = body.as_dict()
            new_member = pecan.request.db_api.create_member(d)
        except Exception as e:
            LOG.exception(e)
            raise wsme.exc.ClientSideError('Invalid data')
        return new_member

    @wsme.validate(Member)
    @wsme_pecan.wsexpose(Member, wtypes.text, body=Member)
    def put(self, id, body):
        member = pecan.request.db_api.get_member(id)
        items = body.as_dict().items()
        for k, v in [(k, v) for (k, v) in items if v]:
            member[k] = v

        member.save()
        return member
