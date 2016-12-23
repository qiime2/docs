# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.compat import make_admonition


class qiime1users(nodes.Admonition, nodes.Element):
    pass


def visit_qiime1users_node(self, node):
    self.visit_admonition(node)


def depart_qiime1users_node(self, node):
    self.depart_admonition(node)


class QIIME1UsersDirective(Directive):
    has_content = True

    def run(self):
        env = self.state.document.settings.env

        targetid = 'qiime1users-%d' % env.new_serialno('qiime1users')
        targetnode = nodes.target('', '', ids=[targetid])

        self.options['class'] = ['qiime1']
        ad = make_admonition(qiime1users, self.name, ['QIIME 1 Users'],
                             self.options, self.content, self.lineno,
                             self.content_offset, self.block_text, self.state,
                             self.state_machine)
        return [targetnode] + ad


def setup(app):
    app.add_node(qiime1users,
                 html=(visit_qiime1users_node, depart_qiime1users_node))
    app.add_directive('qiime1-users', QIIME1UsersDirective)

    return {'version': '0.0.1'}
