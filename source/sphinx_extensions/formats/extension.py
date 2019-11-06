# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import shutil

import jinja2
import qiime2.sdk
import qiime2.core

from sphinx.util import logging
logger = logging.getLogger(__name__)


def generate_rst(app):
    pm = qiime2.sdk.PluginManager()

    loader = jinja2.PackageLoader('sphinx_extensions.formats', 'templates')
    env = jinja2.Environment(loader=loader)

    rst_dir = os.path.join(app.env.srcdir, 'formats-list')
    app.formats_rst_dir = rst_dir
    cleanup_rst(app, None)
    os.mkdir(rst_dir)

    index_path = os.path.join(rst_dir, 'formats-list.rst')

    importable_formats = [
        repr(importable_format) for importable_format in pm._importable]
    importable_formats.sort()

    exportable_formats = [
        repr(exportable_format) for exportable_format in pm._exportable]
    exportable_formats.sort()

    all_formats_set = {*importable_formats, *exportable_formats,
                       *[repr(format) for format in pm._canonical_formats]}
    all_formats = [repr(format) for format in all_formats_set]
    all_formats.sort()

    template = env.get_template('formats-list.rst')
    with open(index_path, 'w') as fh:
        rendered = template.render(format_list=all_formats,
                                   importable_formats=importable_formats,
                                   exportable_formats=exportable_formats)
        fh.write(rendered)


def cleanup_rst(app, exception):
    if hasattr(app, 'formats_rst_dir') and \
            os.path.exists(app.formats_rst_dir):
        shutil.rmtree(app.formats_rst_dir)


def setup(app):
    app.connect('builder-inited', generate_rst)
    return {'version': '0.0.1'}
