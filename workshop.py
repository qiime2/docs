import os
import shutil

import lxml, lxml.html


tutorial_fp = './build/fmt-cdiff-s3'
shutil.rmtree(tutorial_fp, ignore_errors=True)
os.mkdir(tutorial_fp)



tree = lxml.html.parse('./build/preview/tutorials/fmt-cdiff/index.html')

# First, drop sidebar for this tutorial, as well as some other misc nodes
for node in tree.xpath("//*[@id='sidebar']"):
    node.getparent().remove(node)
for node in tree.xpath("//*[@class='footer']"):
    node.getparent().remove(node)
for node in tree.xpath("//*[@id='header']"):
    node.getparent().remove(node)
for node in tree.xpath("//*[@id='github-banner']"):
    node.getparent().remove(node)

# Next, clean up CSS URIs
for href in ['style', 'pygments', 'basic']:
    for node in tree.xpath("//*[@href='../../_static/%s.css']" % href):
        node.attrib['href'] = '%s.css' % href
    shutil.copy('./build/preview/_static/%s.css' % href, tutorial_fp)

for href in ['bootstrap.min', 'normalize']:
    for node in tree.xpath("//*[@href='../../_static/css/%s.css']" % href):
        node.attrib['href'] = '%s.css' % href
    shutil.copy('./build/preview/_static/css/%s.css' % href, tutorial_fp)

# Next, clean up JS URIs
for href in ['jquery', 'underscore', 'doctools', 'external-links',
             'bootstrap-dropdown']:
    for node in tree.xpath("//*[@src='../../_static/%s.js']" % href):
        node.attrib['src'] = '%s.js' % href
    shutil.copy('./build/preview/_static/%s.js' % href, tutorial_fp)

# Finally, write out HTML
tree.write(os.path.join(tutorial_fp, 'index.html'), method='html')
