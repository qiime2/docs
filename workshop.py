import os
import shutil

import lxml, lxml.html


tutorial_fp = './build/fmt-cdiff-s3'
shutil.rmtree(tutorial_fp, ignore_errors=True)
os.mkdir(tutorial_fp)

tree = lxml.html.parse('./build/preview/tutorials/fmt-cdiff/index.html')

# TODO: title
# TODO: remove `link` tags
# TODO: fix links to tutorial xrefs

# Drop sidebar for this tutorial, as well as some other misc nodes
for id_ in ['sidebar', 'header', 'github-banner']:
    for node in tree.xpath("//*[@id='%s']" % id_):
        node.getparent().remove(node)
for node in tree.xpath("//*[@class='footer']"):
    node.getparent().remove(node)

# Clean up assets
for href in ['style.css', 'pygments.css', 'basic.css']:
    for node in tree.xpath("//*[@href='../../_static/%s']" % href):
        node.attrib['href'] = href
    # TODO: os.path.join
    shutil.copy('./build/preview/_static/%s' % href, tutorial_fp)
for href in ['bootstrap.min.css', 'normalize.css']:
    for node in tree.xpath("//*[@href='../../_static/css/%s']" % href):
        node.attrib['href'] = href
    # TODO: os.path.join
    shutil.copy('./build/preview/_static/css/%s' % href, tutorial_fp)
for src in ['jquery.js', 'underscore.js', 'doctools.js', 'external-links.js',
             'bootstrap-dropdown.js', 'bootstrap.min.js', 'clipboard.min.js',
             'clipboard-driver.js']:
    for node in tree.xpath("//*[@src='../../_static/%s']" % src):
        node.attrib['src'] = src
    # TODO: os.path.join
    shutil.copy('./build/preview/_static/%s' % src, tutorial_fp)


# Clean up q2view links
search_url = ('https%3A%2F%2Fdocs.qiime2.org%2F2018.11%2Fdata%2Ftutorials'
              '%2Ffmt-cdiff')
base_url = ('https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fqiime2-workshops'
            '%2Ffmt-cdiff%2Fdata')
for node in tree.xpath('//a'):
    if search_url in node.attrib['href']:
        node.attrib['href'] = node.attrib['href'].replace(search_url, base_url)

# Clean up download links
search_url = 'https://docs.qiime2.org/2018.11/data/tutorials/fmt-cdiff/'
base_url = ('https://s3-us-west-2.amazonaws.com/qiime2-workshops/'
            'fmt-cdiff/data/')
for node in tree.xpath('//a'):
    if search_url in node.attrib['href']:
        node.attrib['href'] = node.attrib['href'].replace(search_url, base_url)

# Clean up xrefs
base_url = 'https://docs.qiime2.org/2018.10/'
for node in tree.xpath('//a'):
    if node.attrib['href'].startswith('../'):
        node.attrib['href'] = node.attrib['href'].replace('../', base_url)

# Copy all built data outputs
shutil.copytree('./build/html/data/tutorials/fmt-cdiff',
                os.path.join(tutorial_fp, 'data'))

# Write out HTML
tree.write(os.path.join(tutorial_fp, 'index.html'), method='html')
