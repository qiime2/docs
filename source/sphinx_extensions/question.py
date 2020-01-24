# ----------------------------------------------------------------------------
# Copyright (c) 2016-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class QuestionAdmonition(nodes.Admonition, nodes.Element):
    pass


class QuestionDirective(SphinxDirective):
    has_content = True

    def run(self):
        target_id = 'question-%d' % self.env.new_serialno('question')
        target_node = nodes.target('', '', ids=[target_id])

        question_node = QuestionAdmonition(self.content)
        question_node += nodes.title(text='Question')
        question_node['classes'] += ['question']
        self.state.nested_parse(self.content, self.content_offset,
                                question_node)

        return [target_node, question_node]


def setup(app):
    app.add_node(QuestionAdmonition,
                 html=(lambda s, n: s.visit_admonition(n),
                       lambda s, n: s.depart_admonition(n)))
    app.add_directive('question', QuestionDirective)

    return {'version': '0.0.2'}
