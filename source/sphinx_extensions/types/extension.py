# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import jinja2
import qiime2.sdk
import qiime2.core

from sphinx.util import logging
logger = logging.getLogger(__name__)


def generate_rst(app):
    pm = qiime2.sdk.PluginManager()

    loader = jinja2.PackageLoader('sphinx_extensions.types',
                                  'templates')
    env = jinja2.Environment(loader=loader)

    type_list = []

    for type in pm.get_semantic_types():
        type_list.append(repr(type))

    type_list.sort()
    template = env.get_template('types-list.rst')
    with open('types_list.rst', 'w') as fh:
        rendered = template.render(type_list=type_list)
        fh.write(rendered)


def setup(app):
    app.connect('builder-inited', generate_rst)
    return {'version': '0.0.1'}
