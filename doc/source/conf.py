#!/usr/bin/env python

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

import os
import sys

from stripe.version import STRIPE_VERSION as stripe_version


extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Stripe'
copyright = u'2013, Paul Belanger'
release = stripe_version.version_string_with_vcs()
version = stripe_version.canonical_version_string()
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'stripeedoc'

latex_elements = {
}

latex_documents = [
  ('index', 'Stripe.tex', u'Stripe Documentation',
   u'Paul Belanger', 'manual'),
]

man_pages = [
    ('index', 'Stripe', u'Stripe Documentation',
     [u'Paul Belanger'], 1)
]

texinfo_documents = [
  ('index', 'Stripe', u'Stripe Documentation',
   u'Paul Belanger', 'Stripe', 'One line description of project.',
   'Miscellaneous'),
]
