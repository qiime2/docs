Metadata in QIIME 2
===================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

Metadata provides the key to gaining biological insight from your raw data. In QIIME 2, sample metadata includes technical details, such as the DNA barcodes that were used for each sample, or descriptions of the samples, such as which subject, time point and body site each sample came from in a human microbiome time series. Feature metadata is often a feature annotation, such as the taxonomy assigned to a sequence variant. Sample and feature metadata are used by many methods and visualizers in QIIME 2.

.. qiime1-users:: In QIIME 1, metadata (also known as the metadata mapping file), was a user-defined file that contained these study-specific fields. QIIME 2 expands upon this idea, allowing users to provide their own study metadata (via a TSV file), or, by viewing other study-specific artifacts as metadata. Examples of both are presented in the following.

Begin by creating a directory to conduct the work in:

.. command-block::
   :no-exec:

   mkdir qiime2-metadata-tutorial
   cd qiime2-metadata-tutorial

Metadata from a text file
-------------------------

Metadata is typically defined in a sample (or feature; more on that below) metadata mapping file. The QIIME 2 development team hasn't adopted a standard set of criteria for the sample metadata mapping file, but at present the following minimum requirements are enforced:

- The file must be a tab-separated text file
- Comment lines (e.g. lines that begin with ``#``) are ignored
- The first non-comment line of the file is used as the column labels
- The column label values must be unique (i.e. no duplicate values)
- There must be at least one line of data following the column label line
- The first column in the table is the "identifier" column (either sample ID or feature ID, depending on the axis)
- All of the values in the first column must be unique (i.e. no duplicate values)

Sample (and feature) metadata mapping files can be validated using Keemei_, which will help identify issues while creating these files.

.. qiime1-users:: Generally speaking, sample/feature metadata mapping files `that work in QIIME 1`_ should work in QIIME 2.

To get started with understanding sample metadata mapping files, first download an example TSV file:

.. download::
   :url: https://data.qiime2.org/2017.6/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

This file can be opened and edited in a text editor, Google Sheets, or Keemei_. You can also generate a QIIME 2 visualization of metadata mapping files as follows:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv \
     --o-visualization tabulated-sample-metadata.qzv

.. question::
   Based on the table in ``tabulated-sample-metadata.qzv``, how many samples are associated with ``subject 1``? How many samples are associated with the ``gut`` body site? Hint: use the search box and/or the column sorting options to assist with this query.

Metadata from a QIIME 2 artifact
--------------------------------

As eluded to above, QIIME 2 also supports the notion of viewing some artifacts as metadata. An example of this is artifacts of ``SampleData[AlphaDiversity]``.

To get started with understanding artifacts as metadata, first download an example artifact:

.. download::
   :url: https://docs.qiime2.org/2017.6/data/tutorials/moving-pictures/core-metrics-results/faith_pd_vector.qza
   :saveas: faith_pd_vector.qza

To view this artifact as metadata, simply pass it in to any method or visualizer that expects to see metadata (e.g. ``metadata tabulate`` or ``emperor plot``):

.. command-block::
   qiime metadata tabulate \
     --m-input-file faith_pd_vector.qza \
     --o-visualization tabulated-faith-pd-metadata.qzv

.. question::
   What is the largest value of Faith's PD? What is the smallest? Hint: use the column sorting functions to assist with this query.

Combining metadata
------------------

Because metadata can come from many different sources, QIIME 2 supports metadata merging when running commands. Building upon the examples above, simply passing ``--m-input-file`` multiple times will combine the metadata in the specified files:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv \
     --m-input-file faith_pd_vector.qza \
     --o-visualization tabulated-combined-metadata.qzv

Merging is based on the identifiers specified in the first column of each metadata file (i.e. sample IDs or feature IDs). The resulting metadata after the merge will contain the intersection of the identifiers across all of the specified files. Merging does not modify any of the input files.

.. question::
   Modify the command above to merge the `evenness vector`_ of ``SampleData[AlphaDiversity]`` after the Faith's PD vector. What happens when merging the three artifacts? How many columns are present in the resulting metadata visualization? How many of those columns represent the sample IDs? How many of those columns represent ``SampleData[AlphaDiversity]`` metrics?

Metadata merging is supported anywhere that metadata is accepted in QIIME 2. For example, it might be interesting to color an Emperor plot based on the study metadata, or the sample alpha diversities. This can be accomplished by providing both the sample metadata mapping file *and* the ``SampleData[AlphaDiversity]`` artifact:

.. download::
   :url: https://docs.qiime2.org/2017.6/data/tutorials/moving-pictures/core-metrics-results/unweighted_unifrac_pcoa_results.qza
   :saveas: unweighted_unifrac_pcoa_results.qza

.. command-block::
   qiime emperor plot \
     --i-pcoa unweighted_unifrac_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-file faith_pd_vector.qza \
     --o-visualization unweighted-unifrac-emperor-with-alpha.qzv

.. question::
   What happens to the visualization if the order of the metadata files is reversed in the above ``emperor plot``? What about in the ``metadata tabulate`` example above?

Exploring feature metadata
--------------------------

As noted above, metadata can exist for either axis of a ``FeatureTable``: the sample axis or the feature axis. The previous examples in this tutorial were focused on sample-oriented metadata.

To get started with feature metadata, first download the example files:

.. download::
   :url: https://docs.qiime2.org/2017.6/data/tutorials/moving-pictures/rep-seqs.qza
   :saveas: rep-seqs.qza

.. download::
   :url: https://docs.qiime2.org/2017.6/data/tutorials/moving-pictures/taxonomy.qza
   :saveas: taxonomy.qza

Next, merge the two metadata files, and ``tabulate`` them:

.. command-block::
   qiime metadata tabulate \
     --m-input-file rep-seqs.qza \
     --m-input-file taxonomy.qza \
     --o-visualization tabulated-feature-metadata.qzv

The resulting table shows the joined metadata files with a column of the the feature IDs, a column of the representative sequences, a column of the taxonomic assignments, and lastly, a column of the assignment confidence.

.. question::
   Are all QZA files metadata? Are all metadata files QZAs?

Finally, there are export options available in the visualizations produced from ``metadata tabulate``. Using the results from ``tabulated-feature-metadata.qzv``, export the data as a new TSV. Open that file in a TSV viewer or text editor and note that the contents are the same as the interactive metadata table in the visualization.

.. question::
   Can the exported TSV from the above step be used as metadata? What are some benefits of being able to export metadata (hint: see the discussion above about metadata merging)? What about some potential drawbacks (hint: what happens to data provenance_ when data is exported from QIIME 2)?

.. LINKS:
.. _Keemei: http://http://keemei.qiime.org/
.. _`That work in QIIME 1`: http://qiime.org/documentation/file_formats.html#metadata-mapping-files
.. _`evenness vector`: https://docs.qiime2.org/2017.6/data/tutorials/moving-pictures/core-metrics-results/evenness_vector.qza
.. _provenance: https://docs.qiime2.org/2017.6/concepts
