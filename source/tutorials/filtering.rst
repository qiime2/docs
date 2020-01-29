Filtering data
==============

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial describes how to filter feature tables, sequences, and distance matrices in QIIME 2, and will be expanded as more filtering functionality becomes available.

Obtain the data
---------------

First, create a directory to work in and change to that directory.

.. command-block::
   :no-exec:

   mkdir qiime2-filtering-tutorial
   cd qiime2-filtering-tutorial

Download the data we'll use in the tutorial. This includes sample metadata, a feature table, and a distance matrix:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/filtering/table.qza
   :saveas: table.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/filtering/distance-matrix.qza
   :saveas: distance-matrix.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/filtering/taxonomy.qza
   :saveas: taxonomy.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/filtering/sequences.qza
   :saveas: sequences.qza

Filtering feature tables
------------------------
In this section of the tutorial we'll see how to filter (i.e., remove) samples and features from a feature table. Feature tables have two axes: the sample axis and the feature axis. The filtering operations described in this tutorial are generally applicable to the sample axis and the feature axis using the ``filter-samples`` and ``filter-features`` methods, respectively. Both of these methods are implemented in the ``q2-feature-table`` plugin. Taxonomy-based filtering can also be applied to filter features from a feature table using the ``filter-table`` method in the ``q2-taxa`` plugin.

Total-frequency-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Total-frequency-based filtering is used to filter samples or features based on how frequently they are represented in the feature table.

When filtering samples this can be used, for example, to filter samples whose total frequency is an outlier in the distribution of sample frequencies. In many 16S surveys, only a few (perhaps tens) of sequences will be obtained for some samples, possibly due to low biomass of the sample resulting in low DNA extraction yield. In this case, the user may want to remove samples based on their minimum total frequency (i.e., total number of sequences obtained for the sample, in this example). This can be achieved as follows (in this example, samples with a total frequency less than 1500 will be filtered).

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --p-min-frequency 1500 \
     --o-filtered-table sample-frequency-filtered-table.qza

This filter can be applied to the feature axis to remove low abundance features from a table. For example, you can remove all features with a total abundance (summed across all samples) of less than 10 as follows.

.. command-block::
   qiime feature-table filter-features \
     --i-table table.qza \
     --p-min-frequency 10 \
     --o-filtered-table feature-frequency-filtered-table.qza

Both of these methods can also be applied to filter based on the maximum total frequency using the ``--p-max-frequency``. The ``--p-min-frequency`` and ``--p-max-frequency`` can be combined to filter based on lower and upper limits of total frequency.

Contingency-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contingency-based filtering is used to filter samples from a table contingent on the number of features they contain, or to filter features from a table contingent on the number of samples they're observed in.

This filtering is commonly used for filtering features that show up in only one or a few samples, based on the suspicion that these may not represent real biological diversity but rather PCR or sequencing errors (such as PCR chimeras). Features that are present in only a single sample could be filtered from a feature table as follows.

.. command-block::
   qiime feature-table filter-features \
     --i-table table.qza \
     --p-min-samples 2 \
     --o-filtered-table sample-contingency-filtered-table.qza

Similarly, samples that contain only a few features could be filtered from a feature table as follows.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --p-min-features 10 \
     --o-filtered-table feature-contingency-filtered-table.qza

Both of these methods can also be applied to filter contingent on the maximum number of features or samples, using the ``--p-max-features`` and ``--p-max-samples`` parameters, and these can optionally be used in combination with ``--p-min-features`` and ``--p-min-samples``.

.. _identifier-based-filtering:

Identifier-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~~~

Identifier-based filtering is used to retain only a user-specified list of samples or features based on their identifiers (IDs) in a QIIME 2 metadata file. To filter by IDs, the user will provide a QIIME 2 metadata file as input with the ``--m-metadata-file`` parameter (for ``filter-samples`` or ``filter-features``) where the first column in the file contains the IDs that should be retained. Only the first column in this file will be used to filter IDs; all other columns (if any are present) will be ignored. Identifier-based filtering can be applied as follows to remove samples from a feature table.

Let's create a simple QIIME 2 metadata file that consists of a single column containing the IDs to filter by. We'll write a header line and two sample IDs to a new file called ``samples-to-keep.tsv``. If you already have a metadata file containing the IDs of the samples that you want to keep, you can skip this step. Otherwise, in practice, you'd probably create this file in a spreadsheet program or text editor, not on the command line as is being done here.

.. command-block::
   echo SampleID > samples-to-keep.tsv
   echo L1S8 >> samples-to-keep.tsv
   echo L1S105 >> samples-to-keep.tsv

Then, we'll run the ``filter-samples`` method with the parameter ``--m-metadata-file samples-to-keep.tsv``. The resulting table will contain only the two samples whose IDs are listed in ``samples-to-keep.tsv``.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file samples-to-keep.tsv \
     --o-filtered-table id-filtered-table.qza

.. _metadata-based-filtering:

Metadata-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~

Metadata-based filtering is similar to identifier-based filtering, except that the list of IDs to keep is determined based on metadata search criteria rather than being provided by the user directly. This is achieved using the ``--p-where`` parameter in combination with the ``--m-metadata-file`` parameter. The user provides a description of the samples that should be retained based on their metadata using ``--p-where``, where the syntax for this description is the SQLite `WHERE-clause <https://en.wikipedia.org/wiki/Where_(SQL)>`_ syntax.

For example, filtering the table to contain only samples from subject 1 is performed as follows. Here, the ``--p-where`` parameter is specifying that we want to retain all of the samples whose ``subject`` is ``subject-1`` in ``sample-metadata.tsv``. Note that the value ``subject-1`` must be enclosed in single quotes, and the column name (``subject``) should be quoted with square brackets to ensure SQLite interprets the column name correctly.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "[subject]='subject-1'" \
     --o-filtered-table subject-1-filtered-table.qza

If there are multiple values that should be retained from a single metadata column, the ``IN`` clause can be used to specify those values. For example, the following command can be used to retain all skin samples. Again, the values ``left palm`` and ``right palm`` are enclosed in single quotes.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "[body-site] IN ('left palm', 'right palm')" \
     --o-filtered-table skin-filtered-table.qza

``--p-where`` expressions can be combined using the ``AND`` and ``OR`` keywords. Here the ``--p-where`` parameter is specifying that we want to retain only the samples whose ``subject`` is ``subject-1`` *and* whose ``body-site`` is ``gut`` in ``sample-metadata.tsv``. With the ``AND`` keyword, both of the expressions being evaluated must be true for a sample to be retained. This means that samples whose ``body-site`` is ``gut`` but whose ``subject`` is ``subject-2`` would not be in the resulting table. Similarly, samples whose ``subject`` is ``subject-1`` but whose ``body-site`` is *not* ``gut`` would not be in the resulting table.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "[subject]='subject-1' AND [body-site]='gut'" \
     --o-filtered-table subject-1-gut-filtered-table.qza

The ``OR`` keyword syntax is similar to the ``AND`` keyword syntax, but specifies that either of the expressions can be true for a sample to be retained. For lack of a more relevant application to the example data being used here, the ``OR`` keyword in this example is applied to retain all of the samples where ``body-site`` is ``gut`` *or* ``reported-antibiotic-usage`` is ``Yes`` in ``sample-metadata.tsv``. In contrast to ``AND``, this means that samples whose ``body-site`` is ``gut`` but whose ``reported-antibiotic-usage`` is ``No`` would be in the resulting table. Similarly, samples whose ``reported-antibiotic-usage`` is ``Yes`` but whose ``body-site`` is *not* ``gut`` would also be in the resulting table.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "[body-site]='gut' OR [reported-antibiotic-usage]='Yes'" \
     --o-filtered-table gut-abx-positive-filtered-table.qza

This syntax also supports negating individual clauses of the ``--p-where`` expression (or the whole expression). Here, the ``--p-where`` parameter is specifying that we want to retain only the samples whose ``subject`` is ``subject-1`` and whose ``body-site`` is *not* ``gut`` in ``sample-metadata.tsv``.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "[subject]='subject-1' AND NOT [body-site]='gut'" \
     --o-filtered-table subject-1-non-gut-filtered-table.qza

Taxonomy-based filtering of tables and sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Taxonomy-based filtering is a very common type of feature-metadata-based filtering, so the ``q2-taxa`` plugin provides the ``filter-table`` method to simplify this process. Filtering can be applied to retain only specific taxa using ``--p-include`` and/or to remove specific taxa using ``--p-exclude``.

Removing a feature if its taxonomic annotation contains some specific text is achieved with the ``--p-exclude`` parameter. For example, ``--p-exclude`` is used here to remove all features annotated as ``mitochondria`` from a table. When searching with ``--p-mode contains`` (the default), search terms are case insensitive, so the search term ``mitochondria`` would return the same results as the search term ``Mitochondria``.

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-exclude mitochondria \
     --o-filtered-table table-no-mitochondria.qza

Removing features that match more than one search term is achieved by providing the search terms in a comma-separated list. The following command will remove all features that contain either ``mitochondria`` or ``chloroplast`` in their taxonomic annotation.

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-exclude mitochondria,chloroplast \
     --o-filtered-table table-no-mitochondria-no-chloroplast.qza

Filtering a table to retain only specific features is achieved using the ``--p-include`` parameter. For example, ``--p-include`` can be used to retain only features that were at least annotated to the phylum level. In the Greengenes taxonomy (which was used to generate the ``FeatureTable[Taxonomy]`` being provided here), all phylum annotations begin with the text ``p__``. If a feature wasn't assigned to a phylum (i.e., it contained at most a kingdom/domain annotation) it shouldn't contain the text ``p__``. We can therefore use ``p__`` as a ``--p-include`` include term here to retain only features that contain a phylum-level annotation. In practice, this filter might be useful for filtering features that are unlikely to be taxonomically informative about your samples.

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-include p__ \
     --o-filtered-table table-with-phyla.qza

The ``--p-include`` and ``--p-exclude`` parameters can be combined. The following command will retain all features that contain a phylum-level annotation, but exclude all features that contain either ``mitochondria`` or ``chloroplast`` in their taxonomic annotation.

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-include p__ \
     --p-exclude mitochondria,chloroplast \
     --o-filtered-table table-with-phyla-no-mitochondria-no-chloroplast.qza

By default, the term(s) provided for ``--p-include`` or ``--p-exclude`` match if they are contained in a taxonomic annotation. If you'd like your terms to match only if they are the complete taxonomic annotation, that can be achieved by passing ``--p-mode exact`` (to indicate the search should require an exact match). When searching with ``-p-mode exact``, search terms are case sensitive, so the search term ``mitochondria`` would not return the same results as the search term ``Mitochondria``.

Removing mitochondrial sequences with an exact match could be achieved as follows. (In the Greengenes taxonomy, there are sometimes genus and species annotations associated with mitochondria annotations, so this command may not remove all features annotated as mitochondria.)

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-mode exact \
     --p-exclude "k__Bacteria; p__Proteobacteria; c__Alphaproteobacteria; o__Rickettsiales; f__mitochondria" \
     --o-filtered-table table-no-mitochondria-exact.qza

Taxonomy-based filtering of tables can also be achieved using ``qiime feature-table filter-features`` with the ``--p-where`` parameter. If your filtering query is more complex than those supported through ``qiime taxa filter-table``, you should use ``qiime feature-table filter-features``.

Filtering sequences
-------------------

The ``q2-taxa`` plugin provides a method, ``filter-seqs``, for filtering ``FeatureData[Sequence]`` based on a feature's taxonomic annotation. The functionality is very similar to that provided in ``qiime taxa filter-table``, so you should refer to the ``qiime taxa filter-table`` examples above to learn more about taxonomy-based filtering. Briefly, ``filter-seqs`` can be applied as follows to retain all features that contain a phylum-level annotation, but exclude all features that contain either ``mitochondria`` or ``chloroplast`` in their taxonomic annotation.

.. command-block::
   qiime taxa filter-seqs \
     --i-sequences sequences.qza \
     --i-taxonomy taxonomy.qza \
     --p-include p__ \
     --p-exclude mitochondria,chloroplast \
     --o-filtered-sequences sequences-with-phyla-no-mitochondria-no-chloroplast.qza


The ``q2-feature-table`` plugin also has a ``filter-seqs`` method, which allows users to remove sequences based on various criteria, including which features are present within a feature table.

See also the :doc:`q2-quality-control plugin <quality-control>`, which has an ``exclude-seqs`` action for filtering sequences based on alignment to a set of reference sequences or primers.


Filtering distance matrices
---------------------------
In this section of the tutorial we'll see how to filter (i.e., remove) samples from a distance matrix using the ``filter-distance-matrix`` method provided by the ``q2-diversity`` plugin.

.. note:: Filtering distance matrices works the same way as filtering feature tables by identifiers or sample metadata. The examples provided in this section are brief; please refer to :ref:`identifier-based-filtering` and :ref:`metadata-based-filtering` above for more details.

A distance matrix can be filtered based on identifiers. For example, to filter a distance matrix to retain the two samples specified in ``samples-to-keep.tsv`` above (see :ref:`identifier-based-filtering`):

.. command-block::
   qiime diversity filter-distance-matrix \
     --i-distance-matrix distance-matrix.qza \
     --m-metadata-file samples-to-keep.tsv \
     --o-filtered-distance-matrix identifier-filtered-distance-matrix.qza

A distance matrix can also be filtered based on sample metadata. For example, to filter a distance matrix to retain only samples from subject 2:

.. command-block::
   qiime diversity filter-distance-matrix \
     --i-distance-matrix distance-matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "[subject]='subject-2'" \
     --o-filtered-distance-matrix subject-2-filtered-distance-matrix.qza
