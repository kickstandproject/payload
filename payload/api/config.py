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

# Server Specific Configurations
server = {
    'port': '9859',
    'host': '0.0.0.0',
}

# Pecan Application Configurations
app = {
    'root': 'payload.api.controllers.root.RootController',
    'modules': ['payload.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/payload/api/templates',
}
