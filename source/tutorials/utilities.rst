Utilities in QIIME 2
====================

There are many non-plugin-based utilities available in QIIME 2. The following
document attempts to demonstrate many of these functions. This document is
divided by interface<LINK>, and attempts to cross-reference similar
functionality available in other interfaces.

``q2cli``
---------

.. citations
.. inspect-metadata
.. peek
.. validate
.. view

Most of the interesting utilities can be found in the ``tools`` subcommand of
``q2cli``:

.. command-block::
   :stdout:

   qiime tools --help


Let's get our hands on some data so that we can learn more about this
functionality! First, we will take a look at the taxonomic bar charts from the
Moving Pictures Tutorial<LINK>:

.. TODO: data.qiime2.org link
.. download::
   :url: https://docs.qiime2.org/2019.4/data/tutorials/moving-pictures/taxa-bar-plots.qzv
   :saveas: mp-taxa-bp.qzv

Citations
.........

Now that we have some results, let's learn more about the citations relevant to
the creation of this visualization. First, we can check the help text for the
``qiime tools citations`` command:

.. command-block::
   :stdout:

   qiime tools citations --help

Now that we know how to use the command, we will run the following:

.. command-block::
   :stdout:

   qiime tools citations mp-taxa-bp.qzv

As you can see, the citations for this particular visualization are presented
above in bibtex format.

Artifact API
------------

Coming soon, please stay tuned!
