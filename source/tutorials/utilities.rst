Utilities in QIIME 2
====================

.. contents::
   :depth: 3

There are many non-plugin-based utilities available in QIIME 2. The following
document attempts to demonstrate many of these functions. This document is
divided by :doc:`interface <../interfaces/index>`, and attempts to cross-reference similar
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
:doc:`PD Mice Tutorial <pd-mice>`:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/utilities/taxa-barplot.qzv
   :saveas: taxa-barplot.qzv

Retrieving Citations
....................

Now that we have some results, let's learn more about the citations relevant to
the creation of this visualization. First, we can check the help text for the
``qiime tools citations`` command:

.. command-block::
   :stdout:

   qiime tools citations --help

Now that we know how to use the command, we will run the following:

.. command-block::
   :stdout:

   qiime tools citations taxa-barplot.qzv

As you can see, the citations for this particular visualization are presented
above in `BibTeX format <http://www.bibtex.org/>`_.

We can also :ref:`see the citations for a specific plugin<plugin-specific-citations>`:

.. command-block::
   :stdout:

   qiime vsearch --citations

And also for a specific action of a plugin:

.. command-block::
   :stdout:

   qiime vsearch cluster-features-open-reference --citations

Viewing Visualizations
......................

What if we want to view our taxa bar plots? One option is to load the visualization
at https://view.qiime2.org. Another option is to use ``qiime tools view`` to
accomplish the job

.. note::
   Provenance viewing is only available at https://view.qiime2.org.

.. command-block::
   :no-exec:

   qiime tools view taxa-barplot.qzv

This will open a browser window with your visualization loaded in it. When you
are done, you can close the browser window and press ``ctrl-c`` on the
keyboard to terminate the command.

Peeking at Results
..................

Oftentimes we need to verify the ``type`` and ``uuid`` of an Artifact. We can use the
``qiime tools peek`` command to view a brief summary report of those facts. First,
let's get some data to look at:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/utilities/faith-pd-vector.qza
   :saveas: faith-pd-vector.qza

Now that we have data, we can learn more about the file:

.. command-block::
   :stdout:

   qiime tools peek faith-pd-vector.qza

Here we can see that the type of the Artifact is
``SampleData[AlphaDiversity] % Properties('phylogenetic')``, as well as the
Artifact's UUID and format.

Validating Results
..................

We can also validate the integrity of the file by running
``qiime tools validate``:

.. command-block::
   :stdout:

   qiime tools validate faith-pd-vector.qza

If there was an issue with the file, this command will usually do a good job
of reporting *what* the problem is (within reason).

Inspecting Metadata
...................

In the :doc:`Metadata tutorial <metadata>` we learned about the ``metadata tabulate``
command, and the resulting visualization it creates. Oftentimes we don't care
so much about the *values* of the Metadata, but rather, just the shape of it:
how many columns? What are their names? What are their types? How many rows (or IDs)
are in the file?

We can demonstrate this by first downloading some sample metadata:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/sample_metadata.tsv
   :saveas: sample-metadata.tsv

Then, we can run the ``qiime tools inspect-metadata`` command:

.. command-block::
   :stdout:

   qiime tools inspect-metadata sample-metadata.tsv

.. question::

   How many metadata columns are there in ``sample-metadata.tsv``? How many IDs?
   Identify how many categorical columns are present. Now do the same for numerical
   columns.

This tool can be very helpful for learning about Metadata column names for
files that are *viewable* as Metadata.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/utilities/jaccard-pcoa.qza
   :saveas: jaccard-pcoa.qza

The file we just downloaded is a Jaccard PCoA (from the
:doc:`PD Mice Tutorial <pd-mice>`), which, can be used in place of the "typical" TSV-formatted
Metadata file. We might need to know about column names for commands we wish to
run, using ``inspect-metadata``, we can learn all about it:

.. command-block::
   :stdout:

   qiime tools inspect-metadata jaccard-pcoa.qza

.. question::

   How many IDs are there? How many columns? Are there any categorical columns? Why?

Artifact API
------------

.. TODO: finish this section

Coming soon, please stay tuned!
