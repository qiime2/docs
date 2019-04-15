# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class QIIME1UsersAdmonition(nodes.Admonition, nodes.Element):
    pass


class QIIME1UsersDirective(SphinxDirective):
    has_content = True

    def run(self):
        target_id = 'qiime1users-%d' % self.env.new_serialno('qiime1users')
        target_node = nodes.target('', '', ids=[target_id])

        qiime1user_node = QIIME1UsersAdmonition(self.content)
        qiime1user_node += nodes.title(text='QIIME 1 Users')
        qiime1user_node['classes'] += ['qiime1']
        self.state.nested_parse(self.content, self.content_offset,
                                qiime1user_node)

        return [target_node, qiime1user_node]


def setup(app):
    app.add_node(QIIME1UsersAdmonition,
                 html=(lambda s, n: s.visit_admonition(n),
                       lambda s, n: s.depart_admonition(n)))
    app.add_directive('qiime1-users', QIIME1UsersDirective)

    return {'version': '0.0.2'}
