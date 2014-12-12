#!/usr/bin/env python

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
import sys


sys.path.insert(0, os.path.abspath('../..'))

extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.httpdomain']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'payload'
copyright = u'2013, Paul Belanger'
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'payloadedoc'

latex_elements = {
}

latex_documents = [
    ('index', 'payload.tex', u'payload Documentation',
     u'Paul Belanger', 'manual'),
]

man_pages = [
    ('man/payload-api', 'payload-api', u'payload Documentation',
     [u'Paul Belanger'], 1),
    ('man/payload-manage', 'payload-manage', u'payload Documentation',
     [u'Paul Belanger'], 1),
]

texinfo_documents = [
    ('index', 'payload', u'payload Documentation',
     u'Paul Belanger', 'payload', 'One line description of project.',
     'Miscellaneous'),
]
