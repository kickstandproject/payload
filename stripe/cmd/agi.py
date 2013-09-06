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

import signal

from oslo.config import cfg

from stripe.openstack.common import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class Client(object):

    def hangup_handler(self, signum, frame):
        signal.signal(signal.SIGUSR1, signal.SIG_IGN)
        self.app.hangup()

    def main(self):
        from stripe.asterisk import app
        from stripe.asterisk import client
        from stripe.asterisk import trigger

        self.app = app.App()
        _client = client.Client(self.app)
        _trigger = trigger.Trigger(self.app)
        self.app.set_client(_client)
        self.app.set_trigger(_trigger)
        self.app.start()

        signal.signal(signal.SIGHUP, self.hangup_handler)
        while True:
            try:
                signal.pause()
            except KeyboardInterrupt:
                self.hangup_handler(signal.SIGINT, None)


def main():
    CONF(
        project='stripe-agi',
    )
    logging.setup('stripe-agi')
    client = Client()
    client.main()
