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
   :url: https://data.qiime2.org/2021.8/tutorials/utilities/taxa-barplot.qzv
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
at https://view.qiime2.org. All QIIME 2 Results may be opened this way.
This will present the visualization (assuming the file is a ``.qzv``), Result
details (e.g. filename, uuid, type, format, citations), and a provenance graph
showing how the Visualization or Artifact was created.

.. note::
   Provenance viewing is only available at https://view.qiime2.org.

Another option is to use ``qiime tools view`` to accomplish the job. This command
may only be used with Visualizations, and will not display Visualization details
(see :ref:`Peek`) or provenence, but provides a quick and easy way to view your
results from the command line.

.. command-block::
   :no-exec:

   qiime tools view taxa-barplot.qzv

This will open a browser window with your visualization loaded in it. When you
are done, you can close the browser window and press ``ctrl-c`` on the
keyboard to terminate the command.

.. _Peek:

Peeking at Results
..................

Oftentimes we need to verify the ``type`` and ``uuid`` of an Artifact. We can use the
``qiime tools peek`` command to view a brief summary report of those facts. First,
let's get some data to look at:

.. download::
   :url: https://data.qiime2.org/2021.8/tutorials/utilities/faith-pd-vector.qza
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
   :url: https://data.qiime2.org/2021.8/tutorials/pd-mice/sample_metadata.tsv
   :saveas: sample-metadata.tsv

Then, we can run the ``qiime tools inspect-metadata`` command:

.. command-block::
   :stdout:

   qiime tools inspect-metadata sample-metadata.tsv

.. question::

   How many metadata columns are there in ``sample-metadata.tsv``? How many IDs?
   Identify how many categorical columns are present. Now do the same for numeric
   columns.

This tool can be very helpful for learning about Metadata column names for
files that are *viewable* as Metadata.

.. download::
   :url: https://data.qiime2.org/2021.8/tutorials/utilities/jaccard-pcoa.qza
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

Casting Metadata Column Types
.............................

In the :doc:`Metadata tutorial <metadata>` we learned about column types and utilizing the
``qiime tools cast-metadata`` tool to specifiy column types within a provided metadata file.
Below we will go through a few scenarios of how this tool can be used, and some common
mistakes that may come up.

We'll start by first downloading some sample metadata. **Note**: This is the same sample
metadata used in the **Inspect Metadata** section, so you can skip this step if you have
already downloaded the ``sample_metadata.tsv`` file from above.

.. download::
   :url: https://data.qiime2.org/2021.8/tutorials/pd-mice/sample_metadata.tsv
   :saveas: sample_metadata.tsv

In this example, we will cast the ``days_post_transplant`` column from ``numeric`` to
``categorical``, and the ``mouse_id`` column from ``categorical`` to ``numeric``. The rest of
the columns contained within our metadata will be left as-is.

.. command-block::
   :stdout:

   qiime tools cast-metadata sample_metadata.tsv \
     --cast days_post_transplant:categorical \
     --cast mouse_id:numeric

If the ``--output-file`` flag is enabled, the specified output file will contain the modified
column types that we cast above, along with the rest of the columns and associated data
contained in ``sample_metadata.tsv``.

If you do not wish to save your cast metadata to an output file, you can omit the
``--output-file`` parameter and the results will be output to ``sdtout`` (as shown in the
example above).

The ``--ignore-extra`` and ``--error-on-missing`` flags are used to handle cast columns not
contained within the original metadata file, and columns contained within the metadata file
that aren't included in the cast call, respectively. We can take a look at how these flags can
be used below:

In the first example, we'll take a look at utilizing the ``--ignore-extra`` flag when a column
is cast that is not included within the original metadata file. Let's start by looking at what
will happen if an extra column is included and this flag is not enabled.

.. command-block::
   :stderr:
   :allow-error:

   qiime tools cast-metadata sample_metadata.tsv \
     --cast spleen:numeric

Notice that the ``spleen`` column included in the cast call results in a raised error. If we
want to ignore any extra columns that are not present in the original metadata file, we can
enable the ``--ignore-extra`` flag.

.. command-block::
   :no-exec:

   qiime tools cast-metadata sample_metadata.tsv \
     --cast spleen:numeric \
     --ignore-extra

When this flag is enabled, all columns included in the cast that are not present in the
original metadata file will be ignored. Note that ``stdout`` for this example has been omitted
since we will not see a raised error with this flag enabled.

In our second example, we'll take a look at the ``--error-on-missing`` flag, which handles
columns that are present within the metadata that are not included in the cast call.

The default behavior permits a subset of the full metadata file to be included in the cast
call (e.g. not all columns within the metadata must be present in the cast call). If the
``--error-on-missing`` flag is enabled, all metadata columns must be included in the cast
call, otherwise an error will be raised.

.. command-block::
   :stderr:
   :allow-error:

   qiime tools cast-metadata sample_metadata.tsv \
     --cast mouse_id:numeric \
     --error-on-missing

Artifact API
------------

.. TODO: finish this section

Coming soon, please stay tuned!
