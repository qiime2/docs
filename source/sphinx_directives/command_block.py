import collections
import os
import os.path
import shutil
import subprocess
import tempfile
import urllib.parse

import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.directives
import docutils.statemachine
import sphinx.errors

import qiime


def setup_working_dir(app):
    app.command_block_working_dir = tempfile.TemporaryDirectory(
        prefix='qiime2-docs-command-block-')


def teardown_working_dir(app, exception):
    app.command_block_working_dir.cleanup()


OutputPath = collections.namedtuple('OutputPath', ['file', 'url'])


class CommandBlockDirective(docutils.parsers.rst.Directive):
    has_content = True

    option_spec = {
        'no-exec': docutils.parsers.rst.directives.flag
    }

    def run(self):
        self.assert_has_content()
        commands = self.content

        nodes = [
            self._get_literal_block_node(commands)
        ]

        env = self._get_env()
        if not (env.config.command_block_no_exec or 'no-exec' in self.options):
            working_dir = os.path.join(env.app.command_block_working_dir.name,
                                       env.docname)
            os.makedirs(working_dir, exist_ok=True)

            self._execute_commands(commands, working_dir)

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
        app = self._get_env().app
        for command in commands:
            command = command.strip()
            if not command:
                continue

            try:
                app.info("Running command: %s" % command)
                comp_proc = subprocess.run(command,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           cwd=working_dir,
                                           shell=True,
                                           universal_newlines=True)
            except OSError as e:
                raise sphinx.errors.ExtensionError(
                    "Unable to execute command %r: %s" % (command, e))

            if comp_proc.returncode != 0:
                msg = (
                    "Command %r exited with non-zero return code %d.\n\n"
                    "stdout:\n\n%s\n\n"
                    "stderr:\n\n%s" %
                    (command, comp_proc.returncode, comp_proc.stdout,
                     comp_proc.stderr)
                )
                raise sphinx.errors.ExtensionError(msg)

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

    def _get_output_links(self, output_paths, name):
        content = []
        if output_paths:
            # TODO it would be nice to not hardcode this.
            url_prefix = 'https://docs.qiime2.org/%s/' % qiime.__version__

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


def setup(app):
    app.connect('builder-inited', setup_working_dir)
    app.connect('build-finished', teardown_working_dir)
    app.add_directive('command-block', CommandBlockDirective)
    app.add_config_value('command_block_no_exec', False, 'html')

    return {'version': '0.0.1'}
