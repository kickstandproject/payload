# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2012-2014 Julien Danjou
# Copyright (C) 2013-2014 PolyBeacon, Inc.
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

"""
Payload Service API
"""

import sys

from payload.api import app
from payload import config
from payload.openstack.common import log as logging


def main():
    config.prepare_args(sys.argv)
    logging.setup('payload')
    srv = app.build_server()
    srv.serve_forever()
