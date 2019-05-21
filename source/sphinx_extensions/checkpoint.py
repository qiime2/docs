# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class CheckpointAdmonition(nodes.Admonition, nodes.Element):
    pass


class CheckpointDirective(SphinxDirective):
    has_content = True

    def run(self):
        target_id = 'checkpoint-%d' % self.env.new_serialno('checkpoint')
        target_node = nodes.target('', '', ids=[target_id])

        checkpoint_node = CheckpointAdmonition(self.content)
        checkpoint_node += nodes.title(text='Checkpoint')
        checkpoint_node['checkpoint'] += ['checkpoint']
        self.state.nested_parse(self.content, self.content_offset,
                                question_node)

        return [target_node, checkpoint_node]


def setup(app):
    app.add_node(CheckpointAdmonition,
                 html=(lambda s, n: s.visit_admonition(n),
                       lambda s, n: s.depart_admonition(n)))
    app.add_directive('checkpoint', CheckpointDirective)

    return {'version': '0.0.2'}
