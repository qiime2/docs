# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import pathlib
import uuid

from sphinx.util import logging

import os.path
import shutil
import subprocess
import textwrap

import jinja2
import qiime2.sdk


logger = logging.getLogger(__name__)
root = pathlib.Path(__file__).parent.absolute()
rst_dir = root / 'plugins' / 'available'
plugin_directory_rst_dir = rst_dir


def generate_plugin_rst():
    logger.info(
        "Generating QIIME 2 plugin directory... (this may take a while)")

    # Refresh the CLI cache just in case it is out of date with what's
    # installed (this should only affect packages while they are installed in
    # development mode). The CLI is used below to generate some of the help
    # text.
    subprocess.run(['qiime', 'dev', 'refresh-cache'], check=True)

    plugins = qiime2.sdk.PluginManager().plugins
    loader = jinja2.PackageLoader('utils', '_templates')
    env = jinja2.Environment(loader=loader)

    cleanup_plugin_rst()
    os.mkdir(rst_dir)

    index_path = os.path.join(rst_dir, 'index.rst')
    with open(index_path, 'w') as fh:
        template = env.get_template('available.rst')
        rendered = template.render(plugins=plugins)
        fh.write(rendered)

    for plugin in plugins.values():
        plugin_cli_name = plugin.name.replace('_', '-')
        plugin_dir = os.path.join(rst_dir, plugin_cli_name)
        os.mkdir(plugin_dir)

        index_path = os.path.join(plugin_dir, 'index.rst')
        with open(index_path, 'w') as fh:
            template = env.get_template('plugin.rst')
            rendered = template.render(title=plugin_cli_name, plugin=plugin)
            fh.write(rendered)

        if plugin.citations:
            index_bib = os.path.join(plugin_dir, 'citations.bib')
            write_bibtex(plugin.citations, index_bib)

        for action in plugin.actions.values():
            import_path, action_api_name = action.get_import_path().rsplit(
                '.', 1)
            action_cli_name = action.id.replace('_', '-')
            action_path = os.path.join(plugin_dir, '%s.rst' % action_cli_name)

            bib_id = ':'.join([plugin_cli_name, action_cli_name])
            if action.citations:
                action_bib = os.path.join(plugin_dir,
                                          '%s.bib' % bib_id)
                write_bibtex(action.citations, action_bib)

            with open(action_path, 'w') as fh:
                title = '%s: %s' % (action_cli_name, action.name)
                directive_indent = ' ' * 3

                logger.info("Generating help text for `%s %s`..." %
                            (plugin_cli_name, action_cli_name))
                command = ['qiime', plugin_cli_name, action_cli_name, '--help']
                proc = subprocess.run(command, check=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
                cli_help = textwrap.indent(proc.stdout.decode('utf-8'),
                                           directive_indent).strip()
                api_help = textwrap.indent(action.__call__.__doc__,
                                           directive_indent).strip()

                template = env.get_template('action.rst')
                rendered = template.render(title=title, cli_help=cli_help,
                                           api_help=api_help, bib_id=bib_id,
                                           has_citations=bool(
                                            action.citations),
                                           import_path=import_path,
                                           action_api_name=action_api_name)
                fh.write(rendered)


def cleanup_plugin_rst(*_):
    if plugin_directory_rst_dir.exists():
        shutil.rmtree(plugin_directory_rst_dir)


def write_bibtex(records, path):
    citations = qiime2.sdk.Citations()
    for record in records:
        citations['key%s' % str(uuid.uuid4())] = record
    citations.save(path)
