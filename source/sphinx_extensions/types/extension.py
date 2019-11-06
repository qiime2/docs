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
import os
import shutil

from sphinx.util import logging
logger = logging.getLogger(__name__)


def generate_rst(app):
    pm = qiime2.sdk.PluginManager()

    loader = jinja2.PackageLoader('sphinx_extensions.types', 'templates')
    env = jinja2.Environment(loader=loader)

    rst_dir = os.path.join(app.env.srcdir, 'types-list')
    app.types_rst_dir = rst_dir
    cleanup_rst(app, None)
    os.mkdir(rst_dir)

    index_path = os.path.join(rst_dir, 'types-list.rst')

    type_list = []
    for type in pm.get_semantic_types():
        type_list.append(repr(type))

    type_list.sort()
    template = env.get_template('types-list.rst')
    with open(index_path, 'w') as fh:
        rendered = template.render(type_list=type_list)
        fh.write(rendered)


def cleanup_rst(app, exception):
    if hasattr(app, 'types_rst_dir') and \
            os.path.exists(app.types_rst_dir):
        shutil.rmtree(app.types_rst_dir)


def setup(app):
    app.connect('builder-inited', generate_rst)
    return {'version': '0.0.1'}
