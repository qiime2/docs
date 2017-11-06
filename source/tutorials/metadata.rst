Metadata in QIIME 2
===================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

Metadata provides the key to gaining biological insight from your raw data. In QIIME 2, sample metadata includes technical details, such as the DNA barcodes that were used for each sample, or descriptions of the samples, such as which subject, time point and body site each sample came from in a human microbiome time series. Feature metadata is often a feature annotation, such as the taxonomy assigned to a sequence variant. Sample and feature metadata are used by many methods and visualizers in QIIME 2.

.. qiime1-users:: In QIIME 1, metadata (also known as the *metadata mapping file*) was a user-defined TSV file that contained these study-specific fields. QIIME 2 expands upon this idea, allowing users to provide their own study metadata via a TSV file or by viewing QIIME 2 artifacts as metadata. Examples of both are presented in the following sections.

Metadata from a text file
-------------------------

Metadata is typically defined in a *sample* (or *feature*; more on that below) *metadata mapping file*. The QIIME 2 development team hasn't adopted a standard set of criteria for the sample metadata mapping file, but at present the following minimum requirements are enforced:

- The file must be a tab-separated text file (TSV).
- Comment lines (i.e. lines that begin with ``#``) may appear anywhere in the file and are ignored.
- Blank lines (i.e. empty or whitespace-only lines) may appear anywhere in the file and are ignored.
- The first non-comment, non-blank line of the file is used as the header (i.e. column labels). See note below if you're using a QIIME 1 mapping file.
- The column labels must be unique (i.e. no duplicate values) and cannot contain certain special characters (e.g. ``/``, ``\``, ``*``, ``?``, etc.).
- There must be at least one line of data in addition to the header.
- The first column in the table is the "identifier" column (either sample ID or feature ID, depending on the axis).
- All of the values in the first column must be unique (i.e. no duplicate values) and cannot contain certain special characters (e.g. ``/``, ``\``, ``*``, ``?``, etc.).

Sample (and feature) metadata mapping files can be validated using Keemei_, which will help identify issues while creating these files. Select *Add-ons > Keemei > Validate QIIME 2 mapping file*.

.. qiime1-users:: Generally speaking, sample/feature metadata mapping files `that work in QIIME 1`_ should work in QIIME 2. If the first line in the metadata file starts with ``#SampleID``, that line will be treated as the header, even though it is a comment line. This exception to the comment line rule described above is necessary to be backwards-compatible with QIIME 1 mapping files. Besides treating the first line as the header, all other rules described above apply to QIIME 1 mapping files, including ignoring comments and blank lines that appear elsewhere in the file.

To get started with understanding sample metadata mapping files, download an example TSV file:

.. command-block::
   :no-exec:

   mkdir qiime2-metadata-tutorial
   cd qiime2-metadata-tutorial

.. download::
   :url: https://data.qiime2.org/2017.11/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

Since this is a TSV file, it can be opened and edited in a variety of applications, including text editors, Microsoft Excel, and Google Sheets (e.g. if you plan to validate your metadata with Keemei_).

QIIME 2 also provides a visualizer for viewing metadata in an interactive table:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv \
     --o-visualization tabulated-sample-metadata.qzv

.. question::
   Based on the table in ``tabulated-sample-metadata.qzv``, how many samples are associated with ``subject-1``? How many samples are associated with the ``gut`` body site? Hint: use the search box and/or the column sorting options to assist with this query.

Metadata from a QIIME 2 artifact
--------------------------------

As eluded to above, QIIME 2 also supports the notion of viewing some artifacts as metadata. An example of this is artifacts of ``SampleData[AlphaDiversity]``.

To get started with understanding artifacts as metadata, first download an example artifact:

.. download::
   :url: https://data.qiime2.org/2017.11/tutorials/metadata/faith_pd_vector.qza
   :saveas: faith_pd_vector.qza

To view this artifact as metadata, simply pass it in to any method or visualizer that expects to see metadata (e.g. ``metadata tabulate`` or ``emperor plot``):

.. command-block::
   qiime metadata tabulate \
     --m-input-file faith_pd_vector.qza \
     --o-visualization tabulated-faith-pd-metadata.qzv

.. question::
   What is the largest value of Faith's PD? What is the smallest? Hint: use the column sorting functions to assist with this query.

When an artifact is viewed as metadata, the result includes that artifact's provenance in addition to its own.

.. question::
   Try inspecting ``tabulated-faith-pd-metadata.qzv`` at https://view.qiime2.org and locate this artifact in the interactive provenance graph.

Combining metadata
------------------

Because metadata can come from many different sources, QIIME 2 supports metadata merging when running commands. Building upon the examples above, simply passing ``--m-input-file`` multiple times will combine the metadata in the specified files:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv \
     --m-input-file faith_pd_vector.qza \
     --o-visualization tabulated-combined-metadata.qzv

The resulting metadata after the merge will contain the intersection of the identifiers across all of the specified files. In other words, the merged metadata will only contain identifiers that are shared across all provided metadata files. This is an *inner join* using database terminology.

.. question::
   Modify the command above to merge the `evenness vector`_ of ``SampleData[AlphaDiversity]`` after the Faith's PD vector. What happens when merging the three artifacts? How many columns are present in the resulting metadata visualization? How many of those columns represent the sample IDs? How many of those columns represent ``SampleData[AlphaDiversity]`` metrics? What happens to the visualization if the order of the metadata files is reversed? Hint, take a closer look at the column ordering.

Metadata merging is supported anywhere that metadata is accepted in QIIME 2. For example, it might be interesting to color an Emperor plot based on the study metadata, or the sample alpha diversities. This can be accomplished by providing both the sample metadata mapping file *and* the ``SampleData[AlphaDiversity]`` artifact:

.. download::
   :url: https://data.qiime2.org/2017.11/tutorials/metadata/unweighted_unifrac_pcoa_results.qza
   :saveas: unweighted_unifrac_pcoa_results.qza

.. command-block::
   qiime emperor plot \
     --i-pcoa unweighted_unifrac_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-file faith_pd_vector.qza \
     --o-visualization unweighted-unifrac-emperor-with-alpha.qzv

.. question::
   What body sites are associated with the highest Faith's phylogentic diversity value? Hint: first color by body site, and then color by Faith's PD using a continuous color scheme.

Exploring feature metadata
--------------------------

Metadata in QIIME 2 can be applied to sample or features --- so far we have only dealt with sample metadata. This section will focus on feature metadata, specifically how to view ``FeatureData`` as metadata.

To get started with feature metadata, first download the example files:

.. download::
   :url: https://data.qiime2.org/2017.11/tutorials/metadata/rep-seqs.qza
   :saveas: rep-seqs.qza

.. download::
   :url: https://data.qiime2.org/2017.11/tutorials/metadata/taxonomy.qza
   :saveas: taxonomy.qza

We have downloaded a ``FeatureData[Sequence]`` file (``rep-seqs.qza``) and a ``FeatureData[Taxonomy]`` file (``taxonomy.qza``). We can merge (and ``tabulate``) these files to associate the representative sequences with their taxonomic annotations:

.. command-block::
   qiime metadata tabulate \
     --m-input-file rep-seqs.qza \
     --m-input-file taxonomy.qza \
     --o-visualization tabulated-feature-metadata.qzv

The resulting table shows the joined metadata files with a column of the the feature IDs, a column of the representative sequences, a column of the taxonomic assignments, and lastly, a column of the assignment confidence.

.. question::
   Are all artifacts (``.qza`` files) viewable as metadata? Hint: try tabulating a `feature table artifact`_. Are all metadata files stored as ``.qza`` files?

Finally, there are export options available in the visualizations produced from ``metadata tabulate``. Using the results from ``tabulated-feature-metadata.qzv``, export the data as a new TSV. Open that file in a TSV viewer or text editor and note that the contents are the same as the interactive metadata table in the visualization.

.. question::
   Can the exported TSV from the above step be used as metadata? What are some benefits of being able to export metadata (hint: see the discussion above about metadata merging)? What about some potential drawbacks (hint: what happens to data :doc:`provenance <../concepts>` when data is exported from QIIME 2)?

.. LINKS:
.. _Keemei: http://keemei.qiime.org/
.. _`That work in QIIME 1`: http://qiime.org/documentation/file_formats.html#metadata-mapping-files
.. _`evenness vector`: https://docs.qiime2.org/2017.11/data/tutorials/moving-pictures/core-metrics-results/evenness_vector.qza
.. _`feature table artifact`: https://docs.qiime2.org/2017.11/data/tutorials/moving-pictures/table.qza
