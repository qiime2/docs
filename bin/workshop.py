# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
from urllib.parse import quote_plus as qp

import lxml
import lxml.html

import qiime2


workshop_slug = os.environ['WORKSHOP_SLUG']
workshop_title = os.environ['WORKSHOP_TITLE']
tutorial_name = os.environ['TUTORIAL_NAME']

tutorial_data_url = ('https://docs.qiime2.org/%s/data/tutorials/%s' %
                     (qiime2.__release__,  tutorial_name))
tutorials_url = ('https://docs.qiime2.org/%s/tutorials/' %
                 (qiime2.__release__,))
tutorial_url = ''.join([tutorials_url, tutorial_name])
s3_url = ('https://s3-us-west-2.amazonaws.com/qiime2-data/workshops/%s/data/' %
          (workshop_slug, ))

base_fp = os.path.join('.', 'build', 'preview', 'tutorials', tutorial_name,
                       'index.html')
tutorial_fp = os.path.join('.', 'build', workshop_slug)

shutil.rmtree(tutorial_fp, ignore_errors=True)
os.mkdir(tutorial_fp)

tree = lxml.html.parse(base_fp)

for node in tree.xpath('//title'):
    node.text = workshop_title

for node in tree.xpath('//link'):
    if node.attrib['rel'] in ['author', 'top', 'up', 'next', 'prev']:
        node.getparent().remove(node)

for misc in ['DOCUMENTATION_OPTIONS', 'UA-86671044-2']:
    for node in tree.xpath('//script'):
        if node.text is not None and misc in node.text:
            node.getparent().remove(node)

# Drop sidebar, as well as some other misc nodes
for id_ in ['sidebar', 'header', 'github-banner']:
    for node in tree.xpath("//*[@id='%s']" % id_):
        node.getparent().remove(node)
for node in tree.xpath("//*[@class='footer']"):
    node.getparent().remove(node)

# Clean up assets
for href in ['style.css', 'pygments.css', 'basic.css', 'favicon.ico']:
    for node in tree.xpath("//*[@href='../../_static/%s']" % href):
        node.attrib['href'] = href
    href_fp = os.path.join('.', 'build', 'preview', '_static', href)
    shutil.copy(href_fp, tutorial_fp)
for href in ['bootstrap.min.css', 'normalize.css']:
    for node in tree.xpath("//*[@href='../../_static/css/%s']" % href):
        node.attrib['href'] = href
    href_fp = os.path.join('.', 'build', 'preview', '_static', 'css', href)
    shutil.copy(href_fp, tutorial_fp)
for src in ['jquery.js', 'underscore.js', 'doctools.js', 'external-links.js',
            'bootstrap-dropdown.js', 'bootstrap.min.js', 'clipboard.min.js',
            'clipboard-driver.js', 'documentation_options.js',
            'language_data.js']:
    for node in tree.xpath("//*[@src='../../_static/%s']" % src):
        node.attrib['src'] = src
    src_fp = os.path.join('.', 'build', 'preview', '_static', src)
    shutil.copy(src_fp, tutorial_fp)

css_fp = os.path.join(tutorial_fp, 'bootstrap.min.css')
with open(css_fp, 'r') as fh:
    css = fh.read()
css = css.replace('../fonts/', './fonts/')
with open(css_fp, 'w') as fh:
    fh.write(css)

# Clean up q2view links
for node in tree.xpath('//a'):
    if qp(tutorial_data_url) in node.attrib['href']:
        node.attrib['href'] = node.attrib['href'].replace(
            qp(tutorial_data_url), qp(s3_url))
        node.attrib['target'] = '_blank'

# Clean up download links
for node in tree.xpath('//a'):
    if tutorial_data_url in node.attrib['href']:
        node.attrib['href'] = node.attrib['href'].replace(
            tutorial_data_url, s3_url)

# Clean up xrefs
for node in tree.xpath('//a'):
    if node.attrib['href'].startswith('../'):
        node.attrib['href'] = node.attrib['href'].replace('../',
                                                          tutorials_url, 1)

built_data_fp = os.path.join('.', 'build', 'html', 'data', 'tutorials',
                             tutorial_name)
shutil.copytree(built_data_fp, os.path.join(tutorial_fp, 'data'))
fonts_fp = os.path.join('.', 'build', 'preview', '_static', 'fonts')
shutil.copytree(fonts_fp, os.path.join(tutorial_fp, 'fonts'))
tree.write(os.path.join(tutorial_fp, 'index.html'), method='html')
