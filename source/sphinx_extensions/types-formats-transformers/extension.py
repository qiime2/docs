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

    loader = jinja2.PackageLoader(
        'sphinx_extensions.types-formats-transformers', 'templates')
    env = jinja2.Environment(loader=loader)

    rst_dir = os.path.join(app.env.srcdir, 'types-formats-transformers-list')
    app.types_rst_dir = rst_dir
    cleanup_rst(app, None)
    os.mkdir(rst_dir)

    index_path = os.path.join(rst_dir, 'types-formats-transformers-list.rst')

    type_list = []
    for type in pm.get_semantic_types():
        type_list.append(repr(type))

    importable_formats = [
        repr(importable_format) for importable_format
        in pm.get_formats(importable=True)]
    importable_formats.sort()

    exportable_formats = [
        repr(exportable_format) for exportable_format
        in pm.get_formats(exportable=True)]
    exportable_formats.sort()

    all_formats_set = {*importable_formats, *exportable_formats,
                       *[repr(format) for format
                         in pm.get_formats(include_all=True)]}
    all_formats = [repr(format) for format in all_formats_set]
    all_formats.sort()

    transformers_list = []
    for from_type in pm.transformers:
        for to_type in pm.transformers[from_type]:
            from_type = qiime2.core.util.get_view_name(from_type)
            to_type = qiime2.core.util.get_view_name(to_type)
            transformers_list.append((from_type, to_type))

    # .upper() because Python sorts all capitalized elements above all
    # lowercase ones, and I figured we didn't want 'dict' sorting under
    # 'TaxonomicClassifierDirFmt'
    transformers_list.sort(
        key=lambda element: (element[0].upper(), element[1].upper()))

    reverse_transformers_list = []
    for to_type in pm._reverse_transformers:
        for from_type in pm.transformers[to_type]:
            from_type = qiime2.core.util.get_view_name(to_type)
            to_type = qiime2.core.util.get_view_name(from_type)
            reverse_transformers_list.append((from_type, to_type))

    # .upper() because Python sorts all capitalized elements above all
    # lowercase ones, and I figured we didn't want 'dict' sorting under
    # 'TaxonomicClassifierDirFmt'
    reverse_transformers_list.sort(
        key=lambda element: (element[0].upper(), element[1].upper()))

    type_list.sort()
    template = env.get_template('types-formats-transformers-list.rst')
    with open(index_path, 'w') as fh:
        rendered = template.render(
            type_list=type_list, format_list=all_formats,
            importable_formats=importable_formats,
            exportable_formats=exportable_formats,
            transformers_list=transformers_list,
            reverse_transformers_list=reverse_transformers_list)
        fh.write(rendered)


def cleanup_rst(app, exception):
    if hasattr(app, 'types_rst_dir') and \
            os.path.exists(app.types_rst_dir):
        shutil.rmtree(app.types_rst_dir)


def setup(app):
    app.connect('builder-inited', generate_rst)
    app.connect('build-finished', cleanup_rst)
    return {'version': '0.0.1'}
