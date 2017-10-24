Filtering data
==============

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial describes how to filter feature tables and distance matrices in QIIME 2, and will be expanded as more filtering functionality becomes available.

.. qiime1-users:: The methods described in this tutorial mirror the functionality in ``filter_samples_from_otu_table.py``, ``filter_otus_from_otu_table.py``, ``filter_taxa_from_otu_table.py``, and ``filter_distance_matrix.py``.

Obtain the data
---------------

First, create a directory to work in and change to that directory.

.. command-block::
   :no-exec:

   mkdir qiime2-filtering-tutorial
   cd qiime2-filtering-tutorial

Download the data we'll use in the tutorial. This includes sample metadata, a feature table, and a distance matrix:

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/filtering/table.qza
   :saveas: table.qza

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/filtering/distance-matrix.qza
   :saveas: distance-matrix.qza

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/filtering/taxonomy.qza
   :saveas: taxonomy.qza

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

.. _index-based-filtering:

Index-based filtering
~~~~~~~~~~~~~~~~~~~~~

Index-based filtering is used to retain only a user-specified list of samples or features based on their indices (i.e., identifiers). In this case, the user will provide a tab-separated text file as input with the ``--m-metadata-file`` parameter (for ``filter-samples`` or ``filter-features``) where the first column in the file contains the indices that should be retained, and the first row contains headers or names for each column. Only the first column in this file will be used, so there are no requirements on subsequent columns (if any are present). As a result, sample or feature metadata files can be used with this parameter. Index-based filtering can be applied as follows to remove samples from a feature table.

First, we'll write a header line and two sample indices to a new file called ``samples-to-keep.tsv``. (If you already have a tsv file containing a header line and the indices of the samples that you want to keep, you can skip this step. Otherwise, in practice, you'd probably create this file in a text editor, not on the command line as is being done here.)

.. command-block::
   echo Index > samples-to-keep.tsv
   echo L1S8 >> samples-to-keep.tsv
   echo L1S105 >> samples-to-keep.tsv

Then, we'll call the ``filter-samples`` method with the parameter ``--m-metadata-file samples-to-keep.tsv``. The resulting table will contain only the two samples whose indices are listed in ``samples-to-keep.tsv``.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file samples-to-keep.tsv \
     --o-filtered-table index-filtered-table.qza

.. _metadata-based-filtering:

Metadata-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~

Metadata-based filtering is similar to index-based filtering, except that the list of indices to keep is determined based on metadata rather than being provided by the user directly. This is achieved using the ``--p-where`` parameter in combination with the ``--m-metadata-file`` parameter. The user provides a description of the samples that should be retained based on their metadata using ``--p-where``, where the syntax for this description is the SQLite `WHERE-clause <https://en.wikipedia.org/wiki/Where_(SQL)>`_ syntax.

For example, filtering the table to contain only samples from subject 1 is performed as follows. Here, the ``--p-where`` parameter is specifying that we want to retain all of the samples whose ``Subject`` is ``subject-1`` in ``sample-metadata.tsv``. Note that the value ``subject-1`` must be enclosed in single quotes.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "Subject='subject-1'" \
     --o-filtered-table subject-1-filtered-table.qza

If there are multiple values that should be retained from a single metadata category, the ``IN`` clause can be used to specify those values. For example, the following command can be used to retain all skin samples. Again, the values ``left palm`` and ``right palm`` are enclosed in single quotes.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "BodySite IN ('left palm', 'right palm')" \
     --o-filtered-table skin-filtered-table.qza

``--p-where`` expressions can be combined using the ``AND`` and ``OR`` keywords. Here the ``--p-where`` parameter is specifying that we want to retain only the samples whose ``Subject`` is ``subject-1`` *and* whose ``BodySite`` is ``gut`` in ``sample-metadata.tsv``. With the ``AND`` keyword, both of the expressions being evaluated must be true for a sample to be retained. This means that samples whose ``BodySite`` is ``gut`` but whose ``Subject`` is ``subject-2`` would not be in the resulting table. Similarly, samples whose ``Subject`` is ``subject-1`` but whose ``BodySite`` is *not* ``gut`` would not be in the resulting table.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "Subject='subject-1' AND BodySite='gut'" \
     --o-filtered-table subject-1-gut-filtered-table.qza

The ``OR`` keyword syntax is similar to the ``AND`` keyword syntax, but specifies that either of the expressions can be true for a sample to be retained. For lack of a more relevant application to the example data being used here, the ``OR`` keyword in this example is applied to retain all of the samples where ``BodySite`` is ``gut`` *or* ``ReportedAntibioticUsage`` is ``Yes`` in ``sample-metadata.tsv``. In contrast to ``AND``, this means that samples whose ``BodySite`` is ``gut`` but whose ``ReportedAntibioticUsage`` is ``No`` would be in the resulting table. Similarly, samples whose ``ReportedAntibioticUsage`` is ``Yes`` but whose ``BodySite`` is *not* ``gut`` would also be in the resulting table.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "BodySite='gut' OR ReportedAntibioticUsage='Yes'" \
     --o-filtered-table gut-abx-positive-filtered-table.qza

This syntax also supports negating individual clauses of the ``--p-where`` expression (or the whole expression). Here, the ``--p-where`` parameter is specifying that we want to retain only the samples whose ``Subject`` is ``subject-1`` and whose ``BodySite`` is *not* ``gut`` in ``sample-metadata.tsv``.

.. command-block::
   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "Subject='subject-1' AND NOT BodySite='gut'" \
     --o-filtered-table subject-1-non-gut-filtered-table.qza

Taxonomy-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-exclude mitochondria \
     --o-filtered-table table-no-mitochondria.qza

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-exclude mitochondria,chloroplast \
     --o-filtered-table table-no-mitochondria-no-chloroplasts.qza

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-include p__ \
     --o-filtered-table table-with-phyla.qza

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-include p__ \
     --p-exclude mitochondria,chloroplast \
     --o-filtered-table table-with-phyla-no-mitochondria-no-chloroplasts.qza

.. command-block::
   qiime taxa filter-table \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-mode exact \
     --p-exclude "k__Bacteria; p__Proteobacteria; c__Alphaproteobacteria; o__Rickettsiales; f__mitochondria" \
     --o-filtered-table table-no-mitochondria-exact.qza

Filtering distance matrices
---------------------------
In this section of the tutorial we'll see how to filter (i.e., remove) samples from a distance matrix using the ``filter-distance-matrix`` method provided by the ``q2-diversity`` plugin.

.. note:: Filtering distance matrices works the same way as filtering feature tables by indices or sample metadata. The examples provided in this section are brief; please refer to :ref:`index-based-filtering` and :ref:`metadata-based-filtering` above for more details.

A distance matrix can be filtered based on indices. For example, to filter a distance matrix to retain the two samples specified in ``samples-to-keep.tsv`` above (see :ref:`index-based-filtering`):

.. command-block::
   qiime diversity filter-distance-matrix \
     --i-distance-matrix distance-matrix.qza \
     --m-metadata-file samples-to-keep.tsv \
     --o-filtered-distance-matrix index-filtered-distance-matrix.qza

A distance matrix can also be filtered based on sample metadata. For example, to filter a distance matrix to retain only samples from subject 2:

.. command-block::
   qiime diversity filter-distance-matrix \
     --i-distance-matrix distance-matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "Subject='subject-2'" \
     --o-filtered-distance-matrix subject-2-filtered-distance-matrix.qza
