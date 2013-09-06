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

import threading
import time

from stripe.asterisk import models
from stripe.middleware import api
from stripe.openstack.common import log as logging


class Trigger(threading.Thread):

    log = logging.getLogger('asterisk.Trigger')

    def __init__(self, app):
        super(Trigger, self).__init__()
        self.app = app
        self.session = api.get_instance()
        self._stopped = False
        self.count = 0

    def create_queue_caller(self, queue_id, values):
        self.queue_id = queue_id
        caller = self.session.create_queue_caller(
            queue_id=self.queue_id, values=values
        )
        self.uuid = caller['uuid']

    def hangup_queue_caller(self):
        self.session.delete_queue_caller(
            queue_id=self.queue_id, uuid=self.uuid
        )

    def stop(self):
        self.log.debug('Preparing to stop')
        self._stopped = True
        self.log.debug('Waiting for stop')

    def run(self):
        while True:
            self.log.debug('Run handler awake')
            if self._stopped:
                self.log.debug('Stopping')
                return
            try:
                self._handle_event()
            except Exception:
                self.log.exception('Exception moving event:')

            self.log.debug('Run handler sleeping')
            time.sleep(5)

    def _handle_event(self):
        self.count += 1
        if self._stopped:
            return
        event = models.TriggerEvent()
        if self.count > 6:
            self.count = 0
            event.type = 'position'
            caller = self.session.get_queue_caller(
                queue_id=self.queue_id, uuid=self.uuid
            )
            self.log.debug('Caller = %s' % caller)
            event.data = caller['position']

        self.app.add_event(event)
