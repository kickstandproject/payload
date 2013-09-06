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

import os
import Queue
import threading

from stripe.openstack.common import log as logging


class App(threading.Thread):

    log = logging.getLogger('asterisk.App')

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = None
        self.event_queue = Queue.Queue()
        self.trigger = None
        self._hangup = False

    def hangup(self):
        self.log.debug('Preparing to hangup')
        self._hangup = True
        self.add_event(None)
        self.log.debug('Waiting for hangup')

    def run(self):
        while True:
            self.log.debug('Run handler awake')

            if self._hangup:
                self._do_hangup()

            self.process_event_queue()

    def add_event(self, event):
        self.log.debug('Adding event: %s' % event)
        self.event_queue.put(event)
        self.log.debug('Done adding event: %s' % event)

    def process_event_queue(self):
        self.log.debug('Fetching event')
        event = self.event_queue.get()
        if event is not None:
            self.log.debug('Processing event %s' % event)
            if event.name == 'Client':
                self._process_client_event(event)
            elif event.name == 'Trigger':
                self._process_trigger_event(event)

        self.event_queue.task_done()

    def set_client(self, client):
        self.client = client

    def set_trigger(self, trigger):
        self.trigger = trigger

    def _do_hangup(self):
        self.log.debug('Hangup')
        if self.trigger:
            self.trigger.hangup_queue_caller()
            self.trigger.stop()
        os._exit(0)

    def _process_client_event(self, event):
        if event.type == 'answer':
            self.trigger.create_queue_caller(
                queue_id=event.queue, values=event.data
            )
            self.trigger.start()

    def _process_trigger_event(self, event):
        if event.type == 'position':
            self.client.handle_position(event.data)
