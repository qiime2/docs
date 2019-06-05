# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import collections
import os
import os.path
import shutil
import subprocess
import tempfile
import urllib.parse
import functools

import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.directives
import docutils.statemachine
import jinja2
import sphinx
from sphinx.util import logging

import qiime2


loader = jinja2.PackageLoader('sphinx_extensions.command_block', 'templates')
jinja_env = jinja2.Environment(loader=loader)
logger = logging.getLogger(__name__)


class download_node(docutils.nodes.Element):
    def __init__(self, id_, url, saveas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id_
        self.url = url
        self.saveas = saveas


def visit_download_node(self, node):
    pass


def depart_download_node(self, node):
    template = jinja_env.get_template('download.html')
    rendered = template.render(node=node)
    self.body.append(rendered)


def setup_working_dir(app):
    app.command_block_working_dir = tempfile.TemporaryDirectory(
        prefix='qiime2-docs-command-block-')


def teardown_working_dir(app, exception):
    app.command_block_working_dir.cleanup()


OutputPath = collections.namedtuple('OutputPath', ['file', 'url'])


class CommandBlockDirective(docutils.parsers.rst.Directive):
    has_content = True

    option_spec = {
        'no-exec': docutils.parsers.rst.directives.flag,
        'url': docutils.parsers.rst.directives.unchanged_required,
        'saveas': docutils.parsers.rst.directives.unchanged_required,
        'stdout': docutils.parsers.rst.directives.flag,
        'stderr': docutils.parsers.rst.directives.flag,
    }

    def run(self):
        command_mode = True if self.name == 'command-block' else False
        opts = self.options
        download_opts = [k in opts for k in ['url', 'saveas']]

        if command_mode:
            self.assert_has_content()
            if any(download_opts):
                raise sphinx.errors.ExtensionError('command-block does not '
                                                   'support the following '
                                                   'options: `url`, `saveas`.')
            commands = functools.reduce(self._parse_multiline_commands,
                                        self.content, [])
            nodes = [self._get_literal_block_node(self.content)]
        else:
            if self.content:
                raise sphinx.errors.ExtensionError('Content block not '
                                                   'supported for the '
                                                   'download directive.')
            if not all(download_opts):
                raise sphinx.errors.ExtensionError('Missing options for the '
                                                   'download directive. '
                                                   'Please specify `url` and '
                                                   '`saveas`.')
            commands = ['wget -O "%s" "%s"' % (opts['saveas'], opts['url'])]
            id_ = self.state.document.settings.env.new_serialno('download')
            nodes = [download_node(id_, opts['url'], opts['saveas'])]

        env = self._get_env()
        if not ((env.config.command_block_no_exec
                 and env.config.debug_page != env.docname) or
                'no-exec' in opts):
            working_dir = os.path.join(env.app.command_block_working_dir.name,
                                       env.docname)
            os.makedirs(working_dir, exist_ok=True)

            completed_processes = self._execute_commands(commands, working_dir)

            if command_mode:
                for stream_type in ['stdout', 'stderr']:
                    if stream_type in opts:
                        node = self._get_stream_node(completed_processes,
                                                     stream_type)
                        if node is not None:
                            nodes.extend(node)

                artifacts, visualizations = self._get_output_paths(working_dir)
                if artifacts or visualizations:
                    nodes.append(
                        self._get_output_links_node(artifacts, visualizations))

        return nodes

    def _get_env(self):
        return self.state.document.settings.env

    def _get_literal_block_node(self, commands):
        content = '\n'.join(commands)
        node = docutils.nodes.literal_block(content, content)
        node['language'] = 'shell'
        return node

    def _execute_commands(self, commands, working_dir):
        for command in commands:
            command = command.strip()
            if not command:
                continue

            try:
                logger.info("Running command: %s" % command)
                comp_proc = subprocess.run(command,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           cwd=working_dir,
                                           shell=True,
                                           encoding='utf-8',
                                           universal_newlines=True)
            except OSError as e:
                raise sphinx.errors.ExtensionError("Unable to execute "
                                                   "command %r: %s" %
                                                   (command, e))

            if comp_proc.returncode != 0:
                msg = (
                    "Command %r exited with non-zero return code %d.\n\n"
                    "stdout:\n\n%s\n\n"
                    "stderr:\n\n%s" %
                    (command, comp_proc.returncode, comp_proc.stdout,
                     comp_proc.stderr)
                )
                raise sphinx.errors.ExtensionError(msg)

            return comp_proc

    def _get_output_paths(self, working_dir):
        env = self._get_env()
        # TODO don't harcode build dir. Not sure how to get this value from
        # Sphinx programmatically.
        root_build_dir = 'build/html'
        doc_data_dir = os.path.join(root_build_dir, 'data', env.docname)

        artifacts = []
        visualizations = []
        for dirpath, _, filenames in os.walk(working_dir):
            for filename in filenames:
                if filename.endswith('.qza') or filename.endswith('.qzv'):
                    src_filepath = os.path.join(dirpath, filename)
                    file_relpath = os.path.relpath(src_filepath,
                                                   start=working_dir)

                    dest_dir = os.path.join(doc_data_dir,
                                            os.path.dirname(file_relpath))
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_filepath = os.path.join(dest_dir, filename)

                    if os.path.exists(dest_filepath):
                        if (os.path.getmtime(dest_filepath) <
                                os.path.getmtime(src_filepath)):
                            msg = (
                                "Command overwrote path %r that was created "
                                "by a previous command in this file. Output "
                                "overwriting is not supported by the `%s` "
                                "directive." % (file_relpath, self.name)
                            )
                            raise sphinx.errors.ExtensionError(msg)
                    else:
                        shutil.copyfile(src_filepath, dest_filepath)

                        url_relpath = os.path.relpath(dest_filepath,
                                                      root_build_dir)

                        output_path = OutputPath(file=file_relpath,
                                                 url=url_relpath)
                        if filename.endswith('.qza'):
                            artifacts.append(output_path)
                        elif filename.endswith('.qzv'):
                            visualizations.append(output_path)

        return artifacts, visualizations

    def _get_output_links_node(self, artifacts, visualizations):
        # TODO it may be worth making the output data links admonition its
        # own type of admonition (e.g. similar to `qiime1-users` or
        # `question` custom admonitions). Or maybe keeping it a general
        # admonition and adding a custom `class` option is sufficient if
        # we're mainly going for CSS styling. For now, a general admonition
        # works.
        node = docutils.nodes.admonition()

        content = []
        content.extend(self._get_output_links(artifacts, 'artifacts'))
        content.extend(self._get_output_links(visualizations,
                                              'visualizations'))

        env = self._get_env()
        content = docutils.statemachine.ViewList(content, env.docname)
        self.state.nested_parse(content, 0, node)

        return node

    def _get_stream_node(self, comp_proc, stream_type):
        content = getattr(comp_proc, stream_type)
        if content:
            subtitle = '%s:' % (stream_type,)
            subtitle_node = docutils.nodes.subtitle(subtitle, subtitle)
            pre_node = docutils.nodes.literal_block(content, content)
            return [subtitle_node, pre_node]

    def _get_output_links(self, output_paths, name):
        content = []
        if output_paths:
            # TODO it would be nice to not hardcode this.
            url_prefix = 'https://docs.qiime2.org/%s/' % qiime2.__release__

            # TODO it would be cool to format the artifacts/visualizations
            # as tables instead of unordered lists, but will take a little
            # work to format the RST tables correctly.
            content.append('**Output %s:**' % name)
            content.append('')
            content.append('')

            for output_path in output_paths:
                download_url = url_prefix + output_path.url
                content.append(
                    '* :file:`%s`: '
                    '`view <https://view.qiime2.org?src=%s>`__ | '
                    '`download <%s>`__' %
                    (output_path.file, urllib.parse.quote_plus(download_url),
                     download_url))
                content.append('')
        return content

    def _parse_multiline_commands(self, previous, next):
        result = previous.copy()
        if result and result[-1].endswith('\\'):
            result[-1] = result[-1][:-1]
            result[-1] += next.strip()
        else:
            result.append(next.strip())
        return result


def setup(app):
    app.connect('builder-inited', setup_working_dir)
    app.connect('build-finished', teardown_working_dir)
    app.add_directive('command-block', CommandBlockDirective)
    app.add_directive('download', CommandBlockDirective)
    app.add_config_value('command_block_no_exec', False, 'html')
    app.add_config_value('debug_page', '', 'html')
    app.add_node(download_node, html=(visit_download_node,
                                      depart_download_node))

    return {'version': '0.0.1'}
