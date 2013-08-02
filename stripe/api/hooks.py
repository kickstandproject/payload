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

from pecan import hooks

from stripe.db import api as db_api
from stripe.middleware import api as middleware_api


class DBHook(hooks.PecanHook):

    def before(self, state):
        state.request.db_api = db_api.get_instance()


class MiddlewareHook(hooks.PecanHook):

    def before(self, state):
        state.request.middleware_api = middleware_api.get_instance()
