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

import socket

from oslo.config import cfg
from oslo import messaging

from payload.openstack.common import context

OPTS = [
    cfg.StrOpt(
        'host', default=socket.gethostname(),
        help='Name of this node.  This can be an opaque identifier. It is '
        'not necessarily a host name, FQDN, or IP address.'),
]
CONF = cfg.CONF
CONF.register_opts(OPTS)

TRANSPORT = None
NOTIFIER = None


def cleanup():
    """Cleanup the oslo.messaging layer."""
    global TRANSPORT, NOTIFIER
    assert TRANSPORT is not None
    assert NOTIFIER is not None
    TRANSPORT.cleanup()
    TRANSPORT = NOTIFIER = None


def get_notifier(service=None, host=None, publisher_id=None):
    """Return a configured oslo.messaging notifier."""
    assert NOTIFIER is not None
    if not publisher_id:
        publisher_id = "%s.%s" % (service, host or CONF.host)
    return NOTIFIER.prepare(publisher_id=publisher_id)


def init(conf):
    """Initialise the oslo.messaging layer."""
    global TRANSPORT, NOTIFIER
    messaging.set_transport_defaults('payload')
    TRANSPORT = messaging.get_transport(conf)
    serializer = RequestContextSerializer(None)
    NOTIFIER = messaging.Notifier(TRANSPORT, serializer=serializer)


class RequestContextSerializer(messaging.Serializer):
    def __init__(self, base):
        self._base = base

    def serialize_entity(self, ctxt, entity):
        if not self._base:
            return entity
        return self._base.serialize_entity(ctxt, entity)

    def deserialize_entity(self, ctxt, entity):
        if not self._base:
            return entity
        return self._base.deserialize_entity(ctxt, entity)

    def serialize_context(self, ctxt):
        return ctxt.to_dict()

    def deserialize_context(self, ctxt):
        return context.RequestContext(ctxt)
