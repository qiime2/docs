# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os

import jinja2
import qiime2.sdk
import qiime2.core

from sphinx.util import logging
logger = logging.getLogger(__name__)


def generate_rst(app):
    pm = qiime2.sdk.PluginManager()

    loader = jinja2.PackageLoader(
        'sphinx_extensions.transformers', 'templates')
    env = jinja2.Environment(loader=loader)

    template = env.get_template('transformers.rst')
    with open(os.path.join(app.env.srcdir, 'transformers.rst'), 'w') as fh:
        rendered = template.render(plugin_manager=pm)
        fh.write(rendered)


def setup(app):
    app.connect('builder-inited', generate_rst)
    return {'version': '0.0.1'}
