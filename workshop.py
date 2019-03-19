import fileinput
import os
import shutil
from urllib.parse import quote_plus

import lxml
import lxml.html


# config
INPUT_TUTORIAL_INDEX_FP = './build/preview/tutorials/fmt-cdiff/index.html'
INPUT_TUTORIAL_DATA_FP = './build/html/data/tutorials/fmt-cdiff'
OUTPUT_TUTORIAL_FP = './build/fmt-cdiff'
TITLE = 'FMT CDiff Tutorial'
SEARCH_URL = 'https://docs.qiime2.org/2019.1/data/tutorials/fmt-cdiff/'
BASE_URL = ('https://s3-us-west-2.amazonaws.com/qiime2-workshops/'
            'fmt-cdiff/')
DATA_URL = BASE_URL + 'data/'


shutil.rmtree(OUTPUT_TUTORIAL_FP, ignore_errors=True)
os.mkdir(OUTPUT_TUTORIAL_FP)
tree = lxml.html.parse(INPUT_TUTORIAL_INDEX_FP)

for node in tree.xpath('//title'):
    node.text = TITLE

for node in tree.xpath('//link'):
    if node.attrib['rel'] in ['author', 'top', 'up', 'next', 'prev']:
        node.getparent().remove(node)

for misc in ['DOCUMENTATION_OPTIONS', 'UA-86671044-2']:
    for node in tree.xpath('//script'):
        if node.text is not None and misc in node.text:
            node.getparent().remove(node)

# Drop sidebar for this tutorial, as well as some other misc nodes
for id_ in ['sidebar', 'header', 'github-banner']:
    for node in tree.xpath("//*[@id='%s']" % id_):
        node.getparent().remove(node)
for node in tree.xpath("//*[@class='footer']"):
    node.getparent().remove(node)

# Clean up assets
for href in ['style.css', 'pygments.css', 'basic.css', 'favicon.ico']:
    for node in tree.xpath("//*[@href='../../_static/%s']" % href):
        node.attrib['href'] = href
    # TODO: os.path.join
    shutil.copy('./build/preview/_static/%s' % href, OUTPUT_TUTORIAL_FP)
for href in ['bootstrap.min.css', 'normalize.css']:
    for node in tree.xpath("//*[@href='../../_static/css/%s']" % href):
        node.attrib['href'] = href
    # TODO: os.path.join
    shutil.copy('./build/preview/_static/css/%s' % href, OUTPUT_TUTORIAL_FP)
for src in ['jquery.js', 'underscore.js', 'doctools.js', 'external-links.js',
            'bootstrap-dropdown.js', 'bootstrap.min.js', 'clipboard.min.js',
            'clipboard-driver.js']:
    for node in tree.xpath("//*[@src='../../_static/%s']" % src):
        node.attrib['src'] = src
    # TODO: os.path.join
    shutil.copy('./build/preview/_static/%s' % src, OUTPUT_TUTORIAL_FP)

# Clean up q2view links
for node in tree.xpath('//a'):
    if quote_plus(SEARCH_URL) in node.attrib['href']:
        node.attrib['href'] = node.attrib['href'].replace(
            quote_plus(SEARCH_URL), quote_plus(DATA_URL))
        node.attrib['target'] = '_blank'

# Clean up download links
for node in tree.xpath('//a'):
    if SEARCH_URL in node.attrib['href']:
        node.attrib['href'] = node.attrib['href'].replace(SEARCH_URL, DATA_URL)

# Clean up xrefs
for node in tree.xpath('//a'):
    if node.attrib['href'].startswith('../'):
        node.attrib['href'] = node.attrib['href'].replace('../', SEARCH_URL, 1)

# Copy all built data outputs
shutil.copytree(INPUT_TUTORIAL_DATA_FP,
                os.path.join(OUTPUT_TUTORIAL_FP, 'data'))
# Copy fonts
shutil.copytree('./build/preview/_static/fonts',
                os.path.join(OUTPUT_TUTORIAL_FP, 'fonts'))
# Update font paths
with fileinput.FileInput(os.path.join(OUTPUT_TUTORIAL_FP, 'bootstrap.min.css'),
        inplace=True, backup='.bak') as fh:
    for line in fh:
        print(line.replace('../fonts/', './fonts/'), end='')

# Write out HTML
tree.write(os.path.join(OUTPUT_TUTORIAL_FP, 'index.html'), method='html')
