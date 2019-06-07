Utilities in QIIME 2
====================

There are many non-plugin-based utilities available in QIIME 2. The following
document attempts to demonstrate many of these functions. This document is
divided by interface<LINK>, and attempts to cross-reference similar
functionality available in other interfaces.

``q2cli``
---------

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

Viewing Visualizations
......................

What if we want to view our bar plots? One option is to load the visualization
at https://view.qiime2.org. Another option is to use ``qiime tools view`` to
accomplish the job (please note, provenance viewing is only available at
https://view.qiime2.org.

.. command-block::
   :no-exec:

   qiime tools view mp-taxa-bp.qzv

This will open a browser window with your visualization loaded in it. When you
are done, you can close the browser window and press ``ctrl-c`` on yoru
keyboard to terminate the command.

Peeking at Results
..................

Oftentimes we need to verify the type and uuid of an artifact. We can use the
``qiime tools peek`` command to view a brief summary report of those facts. First,
let's get some data to look at:

.. TODO: data.qiime2.org link
.. download::
   :url: https://docs.qiime2.org/2019.4/data/tutorials/moving-pictures/core-metrics-results/faith_pd_vector.qza
   :saveas: faith_pd_alpha_div.qza

Now that we have data, we can learn more about the file:

.. command-block::
   :stdout:

   qiime tools peek faith_pd_alpha_div.qza

Here we can see that the type of the Artifact is
``SampleData[AlphaDiversity] % Properties('phylogenetic')``, as well as the
Artifact's UUID, format, and filename.

Validating Results
..................

We can also validate the integrity of the file by running
``qiime tools validate``:

.. command-block::
   :stdout:

   qiime tools validate faith_pd_alpha_div.qza

If there was an issue with the file, this command will usually do a good job
of reporting *what* the problem is (within reason).

Inspecting Metadata
...................

In the Metadata tutorial<LINK> we learned about the ``metadata tabulate``
command, and the resulting visualization it creates. Oftentimes we don't care
so much about the *values* of the Metadata, but rather, just the shape of it:
how many columns? What are their names? What are their types? How many rows
are in the file?

We can demonstrate this by first downloading some sample metadata:

.. download::
   :url: https://data.qiime2.org/2019.7/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: mp-sample-metadata.tsv

Then, we can run the ``qiime tools inspect-metadata`` command:

.. command-block::
   :stdout:

   qiime tools inspect-metadata mp-sample-metadata.tsv

As you can see, LOREM IPSUM.

This tool can be very helpful for learning about Metadata column names for
files that are *viewable* as Metadata.

.. TODO: data url
.. download::
   :url: https://docs.qiime2.org/2019.4/data/tutorials/moving-pictures/core-metrics-results/jaccard_pcoa_results.qza
   :saveas: jaccard_pcoa.qza

The file we just downloaded is a Jaccard PCoA (from the Moving Pictures
tutorial<LINK>), which, can be used in place of the "typical" TSV-formatted
Metadata file. We might need to know about column names for commands we wish to
run, using ``inspect-metadata``, we can learn all about it:

.. command-block::
   :stdout:

   qiime tools inspect-metadata jaccard_pcoa.qza

Artifact API
------------

Coming soon, please stay tuned!
