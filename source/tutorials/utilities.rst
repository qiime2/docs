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
   :url: https://data.qiime2.org/2021.10/tutorials/utilities/taxa-barplot.qzv
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
   :url: https://data.qiime2.org/2021.10/tutorials/utilities/faith-pd-vector.qza
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
   :url: https://data.qiime2.org/2021.10/tutorials/pd-mice/sample_metadata.tsv
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
   :url: https://data.qiime2.org/2021.10/tutorials/utilities/jaccard-pcoa.qza
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
   :url: https://data.qiime2.org/2021.10/tutorials/pd-mice/sample_metadata.tsv
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
Unlike q2cli, the :doc:`/interfaces/artifact-api` does not have a single central location for
utility functions. Rather, utilities are often bound to objects as methods
which operate on those objects.

Discovering Actions registered to a plugin
..........................................
When working with a new plugin, it may be useful to check what Actions are available.
We first import the plugin, and then query its ``actions`` attribute.
This gives us a list of public methods, and details of whether they are
:term:`methods<method>`, :term:`visualizers<visualizer>`, or :term:`pipelines<pipeline>`.

.. code-block:: python

   >>> from qiime2.plugins import feature_table
   >>> help(feature_table.actions)
   Help on module qiime2.plugins.feature_table.actions in qiime2.plugins.feature_table:

   NAME
       qiime2.plugins.feature_table.actions

   DATA
       __plugin__ = <qiime2.plugin.plugin.Plugin object>
       core_features = <visualizer qiime2.plugins.feature_table.visualizers.c...
       filter_features = <method qiime2.plugins.feature_table.methods.filter_...
       ...

If you already know that you are looking for a method, pipeline, or visualizer,
you can get that subgroup of actions directly:

.. code-block:: python

   >>> help(feature_table.methods)

If you are working in a Jupyter Notebook or in iPython,
you may prefer tab-complete to running `help()`:

.. code-block:: python

   >>> feature_table.visualizers.  # press tab after the . for tab-complete...

Getting help with an Action
............................
Once you have imported a plugin, action helptext is accessible in interactive sessions
with the iPython ``?`` operator:

.. code-block::

   >>> feature_table.methods.merge?
   Call signature:
   feature_table.methods.merge(
       tables: List[FeatureTable[Frequency]¹ | FeatureTable[RelativeFrequency]²],
       overlap_method: Str % Choices('average', 'error_on_overlapping_feature', 'error_on_overlapping_sample', 'sum')¹ | Str % Choices('average', 'error_on_overlapping_feature', 'error_on_overlapping_sample')² = 'error_on_overlapping_sample',
   ) -> (FeatureTable[Frequency]¹ | FeatureTable[RelativeFrequency]²,)
   Type:           Method
   String form:    <method qiime2.plugins.feature_table.methods.merge>
   File:           ~/miniconda/envs/q2-dev/lib/python3.8/site-packages/qiime2/sdk/action.py
   Docstring:      QIIME 2 Method
   Call docstring:
   Combine multiple tables

   Combines feature tables using the `overlap_method` provided.

   Parameters
   ----------
   tables : List[FeatureTable[Frequency]¹ | FeatureTable[RelativeFrequency]²]
   overlap_method : Str % Choices('average', 'error_on_overlapping_feature', 'error_on_overlapping_sample', 'sum')¹ | Str % Choices('average', 'error_on_overlapping_feature', 'error_on_overlapping_sample')², optional
       Method for handling overlapping ids.

   Returns
   -------
   merged_table : FeatureTable[Frequency]¹ | FeatureTable[RelativeFrequency]²
       The resulting merged feature table.

Retrieving Citations
....................
The Artifact API does not provide a utility for getting all citations from a plugin.
Per-action citations are accessible in each action's ``citations`` attribute,
in BibTeX format.

.. code-block:: python

   >>> feature_table.actions.rarefy.citations
   (CitationRecord(type='article', fields={'doi': '10.1186/s40168-017-0237-y', 'issn': '2049-2618', 'pages': '27', 'number': '1', 'volume': '5', 'month': 'Mar', 'year': '2017', 'journal': 'Microbiome', 'title': 'Normalization and microbial differential abundance strategies depend upon data characteristics', 'author': 'Weiss, Sophie and Xu, Zhenjiang Zech and Peddada, Shyamal and Amir, Amnon and Bittinger, Kyle and Gonzalez, Antonio and Lozupone, Catherine and Zaneveld, Jesse R. and Vázquez-Baeza, Yoshiki and Birmingham, Amanda and Hyde, Embriette R. and Knight, Rob'}),)

Peeking at Results
..................
The Artifact API provides a ``.peek`` method that displays the
:term:`UUID`, :term:`Semantic Type`, and :term: `data format` of any QIIME 2 archive.

.. code-block:: python

   >>> from qiime2 import Artifact
   >>> Artifact.peek('observed_features_vector.qza')
   ResultMetadata(uuid='2e96b8f3-8f0a-4f6e-b07e-fbf8326232e9', type='SampleData[AlphaDiversity]', format='AlphaDiversityDirectoryFormat')

If you have already loaded an artifact into memory and you're not concerned with the data format,
the artifact's string representation will give you its UUID and Semantic Type.

.. code-block:: python

   >>> from qiime2 import Artifact
   >>> table = Artifact.load('table.qza')
   >>> table
   <artifact: FeatureTable[Frequency] uuid: 2e96b8f3-8f0a-4f6e-b07e-fbf8326232e9>


Validating Results
..................
Artifacts may be validated by loading them and then running the ``validate`` method.
``validate`` takes one parameter, ``level``, which may be set to ``max`` or ``min``,
defaulting to ``max``. Min validation is useful for quick checks,
while max validation generally trades comprehensiveness for longer runtimes.

The validate method returns ``None`` if validation is successful;
simply running ``x.validate()`` in the interpreter will output a blank line.
If the artifact is invalide, a ``ValidationError`` or ``NotImplementedError`` is raised.

.. code-block:: python

   >>> from qiime2 import Artifact
   >>> table = Artifact.load('table.qza')
   >>> table.validate(level='min')

   >>> print(table.validate())  # equivalent to print(table.validate(level='max'))
   None

Viewing Data
...............................
The view API allows us to review many types of data
without the need to save it as a ``.qza``.

.. code-block:: python

   >>> art = artifact.load('some.qza')

   ...  # perform some analysis, producing a result

   >>> myresult.view(pd.Series)
   s00000001   74
   s00000002   48
   s00000003   79
   s00000004   113
   s00000005   111
   Name: observed_otus, Length: 471, dtype: int64

Viewing data in a specific format is only possible if there is a transformer
registered from the current view type to the type you want.
We get an error if there's no transformer.
E.g. if we try to view this SampleData[AlphaDiversity] as a DataFrame.

.. code-block:: python

   >>> myresult.view(pd.Series)
   ---------------------------------------------------------------------------
   Exception                                 Traceback (most recent call last)
   /tmp/ipykernel_18201/824837086.py in <module>
        12 # Note: Views are only possible if there are transformers registered from the default
        13 # view type to the type you want. We get an error if there's no tranformer
   ---> 14 art.view(pd.DataFrame)

   ... # traceback Here

   Exception: No transformation from <class 'q2_types.sample_data._format.AlphaDiversityDirectoryFormat'> to <class 'pandas.core.frame.DataFrame'>

Some Artifacts are viewable as metadata. If you'd like to check, try:

.. code-block:: python

   >>> art.has_metadata()
   True

   >>> art_as_md = art.view(Metadata)
   >>> art_as_md
   Metadata
   --------
   471 IDs x 1 column
   observed_otus: ColumnProperties(type='numeric')

   Call to_dataframe() for a tabular representation.

Viewing Visualizations
.......................
The Artifact API does not provide utilities for viewing QIIME 2 visualizations.
Users generally save visualizations and use `QIIME 2 View <https://view.qiime2.org>`_
to explore.

.. code-block:: python

   art.save('obs_features.qza')

Inspecting Metadata
...................

Metadata sheets can be viewed in summary or displayed nicely in DataFrame format,
once they have been loaded.

.. code-block:: python

   >>> from qiime2 import Metadata
   >>> metadata = Metadata.load('simple-metadata.tsv')
   Metadata
   --------
   516 IDs x 3 columns
   barcode:               ColumnProperties(type='categorical')
   days:                  ColumnProperties(type='numeric')
   extraction:            ColumnProperties(type='categorical')

   >>> print(metadata)
   >>> metadata.to_dataframe()
                 barcode   days  extraction
   sampleid
   s00000001     806rcbc0   1       1
   s00000002     806rcbc1   3       1
   s00000003     806rcbc2   7       1
   s00000004     806rcbc3   1       1
   s00000005     806rcbc4   11      1
   ...           ...        ...     ...


Casting Metadata Column Types
.............................

The Artifact API does not provide a dedicated utility for casting metadata column type,
and ``Metadata.columns`` is a read-only property.
However, it is possible to edit your ``.tsv`` and re-load it with ``Metadata.load``,
or to cast your Metadata to a Pandas.DataFrame,
cast the columns whose properties you need to change,
and reload as Metadata with the types corrected.
Here's a walkthrough of the latter approach.

Load some Metadata
~~~~~~~~~~~~~~~~~~

.. code-block :: python

   # Imagine you have loaded a tsv as metadata
   >>> md = Metadata.load('md.tsv')
   >>> print(md)

   Metadata
   --------
   3 IDs x 5 columns
   strCatOnly: ColumnProperties(type='categorical')
   intNum:     ColumnProperties(type='numeric')
   intCat:     ColumnProperties(type='categorical')
   floatNum:   ColumnProperties(type='numeric')
   floatCat:   ColumnProperties(type='categorical')

   Call to_dataframe() for a tabular representation.

We have defined three columns of categorical data in the tsv, and two numeric.
The column IDs describe the data values (e.g. ``int``)
and the declared column type (e.g. Num for ``numeric``).

Limitations on casting
~~~~~~~~~~~~~~~~~~~~~~

The sequences in ``strCatOnly`` are read in as python strings,
and represented in the Numpy/Pandas stack as "objects".
Loading the metadata would fail with an error if we typed this column ``numeric``,
because we don't have a good way to represent strings as numbers.
Similarly, you won't have much luck casting string data to ``int`` or ``float``
in Pandas.

Convert to DataFrame
~~~~~~~~~~~~~~~~~~~~

.. code-block :: python

   >>> md = md.to_dataframe()

   >>> print(md)
   >>> print()
   >>> print("intCat should be an object (because categorical): ", str(md['intCat'].dtype))
   >>> print("floatNum should be a float (because numerical): ", str(md['floatNum'].dtype))
   >>> print("intNum should be a float, not an int (because categorical): ", str(md['intCat'].dtype))

               strCatOnly  intNum intCat  floatNum floatCat
   sampleid
   S1        TCCCTTGTCTCC     1.0      1      1.01     1.01
   S2        ACGAGACTGATT     3.0      3      3.01     3.01
   S3        GCTGTACGGATT     7.0      7      7.01     7.01

   intCat should be an object (because categorical):  object
   floatNum should be a float (because numerical):  float64
   intNum should be a float, not an int (because categorical): float64


The ``intNum`` and ``intCat`` columns of the original .tsv contained integer data.
MetadataColumns typed as ``categorical`` are represented in Pandas as ``object``.
MetadataColumns typed as ``numeric`` are represented in Pandas as ``float``.
As such, ``intNum`` is rendered as floating point data when ``to_dataframe`` is called,
and ``intCat`` is represented as an ``object`` in the DataFrame.

These behaviors roundtrip cleanly.
If we cast our DataFrame back to Metadata without making any changes,
the new Metadata will be identical to the original Metadata we loaded from the tsv.
We're here to see how DataFrames allow us to cast metadata column types, though,
so let's give it a shot.

Cast columns
~~~~~~~~~~~~

.. code-block :: python

   >>> md['intCat'] = md['intCat'].astype("int")
   >>> md['floatNum'] = md['floatNum'].astype('str')

   >>> print(md)
   >>> print()
   >>> print("intCat should be an int now: ", str(md['intCat'].dtype))
   >>> print("floatNum should be an object now: ", str(md['floatNum'].dtype))

               strCatOnly  intNum  intCat floatNum floatCat
   sampleid
   S1        TCCCTTGTCTCC     1.0       1     1.01     1.01
   S2        ACGAGACTGATT     3.0       3     3.01     3.01
   S3        GCTGTACGGATT     7.0       7     7.01     7.01

   intCat should be an int now:  int64
   floatNum should be an object now:  object

The DataFrame *looks* the same, but the column dtypes have changed as expected.
When we turn this DataFrame back into Metadata,
the ``ColumnProperties`` have changed accordingly.
Columns represented in Pandas as ``objects`` (including ``strs``) are ``categorical``.
Columns represented in Pandas as ``ints`` or ``floats`` are ``numeric``.

Cast the DataFrame back to Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block :: python

   >>> md = Metadata(md)
   >>> md

   Metadata
   --------
   3 IDs x 5 columns
   strCatOnly: ColumnProperties(type='categorical')
   intNum:     ColumnProperties(type='numeric')
   intCat:     ColumnProperties(type='numeric')
   floatNum:   ColumnProperties(type='categorical')
   floatCat:   ColumnProperties(type='categorical')

   Call to_dataframe() for a tabular representation.

Note that ``intCat``, formerly ``categorical``, is now ``numeric``,
while ``floatNum`` has changed from ``numeric`` to ``categorical``.