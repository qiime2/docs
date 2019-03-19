# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.compat import make_admonition


class question(nodes.Admonition, nodes.Element):
    pass


def visit_question_node(self, node):
    self.visit_admonition(node)


def depart_question_node(self, node):
    self.depart_admonition(node)


class QuestionDirective(Directive):
    has_content = True

    def run(self):
        env = self.state.document.settings.env

        targetid = 'question-%d' % env.new_serialno('question')
        targetnode = nodes.target('', '', ids=[targetid])

        self.options['class'] = ['question']
        ad = make_admonition(question, self.name, ['Question'], self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)
        return [targetnode] + ad


def setup(app):
    app.add_node(question, html=(visit_question_node, depart_question_node))
    app.add_directive('question', QuestionDirective)

    return {'version': '0.0.1'}
