Metadata in QIIME 2
===================

Metadata enables users of QIIME 2 to supplement their analyses with information relevant to their study. This manifests itself in many ways: indicating the barcode sequence when demultiplexing sequences, sorting and grouping taxonomic assignments in the taxonomic bar plots, or exploring diversity metrics with visualizations like ``alpha-group-significance`` or ``beta-group-significance``. In QIIME 1, metadata (also known as the metadata mapping file), was a user-defined file that contained these study-specific fields. QIIME 2 expands upon this idea, allowing users to provide their own study metadata (via a TSV file), or, by viewing other study-specific artifacts as metadata. Examples of both are presented in the following.

Begin by creating a directory to conduct the work in:

.. command-block::
   :no-exec:

   mkdir qiime2-metadata-tutorial
   cd qiime2-metadata-tutorial

Metadata from a mapping file
----------------------------

Metadata is typically defined in a mapping file, similar to the QIIME 1 mapping file. The QIIME 2 development team hasn't adopted a standard set of criteria for the metadata mapping file, but at present the following minimum requirements are enforced:

- The file must be a tab-separated text file
- The first line of the file is the column labels, tab-separated
- The header values in the first line must be unique (i.e. no duplicate values)
- There is at least one line of data following the header line
- The first column is the "identifier" column (either Sample ID or Feature ID, depending on the axis)
- All of the values in the first column must be unique (i.e. no duplicate values)

Metadata mapping files can be validated using Keemei_. Generally speaking, metadata mapping files `that work in QIIME 1`_ should work in QIIME 2.

To get started with understanding metadata mapping files, first download a sample mapping file:

.. TODO: Update this link
.. download::
   :url: https://data.qiime2.org/2017.5/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

This file can be opened and edited in a text editor, Google Sheets, or Keemei_. There is also a ``metadata tabulate`` visualization in QIIME 2 that allows for interactive sorting and filtering of metadata:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv
     --o-visualization tabulated-sample-md.qzv

.. question::
   Based on the table in ``tabulated-sample-md.qzv``, how many samples are associated with Subject 1? How many samples are associated with the ``gut`` body site? Hint: use the search box and/or the column sorting options to assist with this query.

Metadata from a QIIME 2 artifact
--------------------------------

As eluded to above, QIIME 2 also supports the notion of viewing artifacts as metadata (where it makes sense). An example of this is alpha-diversity output artifacts.

To get started with understanding metadata mapping files, first download a sample mapping file:

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/core-metrics-results/faith_pd_vector.qza
   :saveas: faith_pd_vector.qza

To view this artifact as metadata, simply pass it in to any method or visualizer that expects to see metadata (e.g. ``metadata tabulate``):

.. command-block::
   qiime metadata tabulate \
     --m-input-file faith_pd_vector.qza
     --o-visualization tabulated-faith-pd-md.qzv

.. question::
   What is the largest value of Faith's PD? What is the smallest? Hint: use the column sorting functions to assist with this query.

Combining metadata
------------------

Because metadata can come from many different sources, QIIME 2 supports metadata merging when running commands. Building upon the examples above, simply passing ``--m-input-file`` multiple times will combine the metadata in the specified files:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv
     --m-input-file faith_pd_vector.qza
     --o-visualization tabulated-combined-md.qzv

Merging is based on the identifiers specified in the first column of each metadata file (e.g. Sample IDs or Feature IDs). The resulting metadata after the merge represents the intersection of the identifiers in all of the specified files. Note, merging is non-destructive, and does not modify any of the input files.

.. question::
   Using another alpha diversity QZA, what happens when merging three files? How many columns are present in the resulting metadata file? How many of those columns represent the Sample IDs? How many of those columns represent alpha diversity metrics?

Metadata merging is supported anywhere that metadata is accepted within the QIIME 2 ecosystem. For example, it might be interesting to consider coloring an Emperor plot based on the study metadata, or the results of one of the study's alpha diversity metrics. This can be accomplished by providing both the sample metadata mapping file *and* the Faith's PD QZA:

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/core-metrics-results/unweighted_unifrac_pcoa_results.qza
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

As noted above, metadata can be viewed in the context of one of two axes: sample-specific or feature-specific. The previous examples in this tutorial were focused on sample-oriented metadata.

To get started with feature-oriented metadata, first download the example files:

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/rep-seqs.qza
   :saveas: rep-seqs.qza

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/taxonomy.qza
   :saveas: taxonomy.qza

For the sake of illustration, merge the two metadata files, and ``tabulate`` them:

.. command-block::
   qiime metadata tabulate \
     --m-input-file rep-seqs.qza
     --m-input-file taxonomy.qza
     --o-visualization tabulated-feature-assignments.qzv

The resulting table shows the joined metadata files with a column of the the Feature IDs, a column of the representative sequences, and finally a column of the taxonomic assignments .

.. question::
   Are all QZA files metadata? Are all metadata files QZAs?

Finally, there are additional export options available in the visualizations produced from ``metadata tabulate``. Using the results from ``tabulated-feature-assignments.qzv``, export the data as a new TSV. Open that file in a TSV viewer or text editor and note that the contents are the same as the interactive metadata table in the visualization.

.. question::
   Can the exported TSV from the above step be used as metadata? What are some benefits of being able to export metadata (hint: see the discussion above about metadata merging)? What about some potential drawbacks (hint: see the overview about provenance_ in QIME 2)?

.. LINKS:
.. _Keemei: http://http://keemei.qiime.org/
.. _`That work in QIIME 1`: http://qiime.org/documentation/file_formats.html#metadata-mapping-files
.. _provenance: https://docs.qiime2.org/2017.5/concepts
