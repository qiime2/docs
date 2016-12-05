Filtering feature tables
========================

.. note:: This guide assumes you have performed the steps in the :doc:`install guide <../install>`.

.. qiime1-users:: The methods described in this tutorial mirror the functionality in ``filter_samples_from_otu_table.py`` and ``filter_otus_from_otu_table.py``.

This tutorial covers filtering (i.e., removing) samples and features from feature tables. Feature tables have two axes: the sample axis and the feature axis. The filtering operations described in this tutorial are all applicable to the sample axis and the feature axis using the ``filter-samples`` and ``filter-features`` methods, respectively. Both of these methods are implemented in the ``q2-feature-table`` plugin.

In this document we'll work with the feature table and sample metadata from the :doc:`Moving Pictures tutorial <./moving-pictures>`. As a first step, download both of these files.

.. command-block::

    curl -sL "https://docs.google.com/spreadsheets/d/1_3ZbqCtAYx-9BJYHoWlICkVJ4W_QGMfJRPLedt_0hws/export?gid=0&format=tsv" > sample-metadata.tsv
    curl -sLO https://data.qiime2.org/2.0.6/tutorials/filtering-feature-tables/table.qza

Frequency-based filtering
-------------------------

Frequency-based filtering is used to filter samples or features based on their total frequency.

When filtering samples this can be used, for example, to filter samples whose total frequency is an outlier in the distribution of sample frequencies. In many 16S surveys, only a few (perhaps tens) of sequences will be obtained for some samples, possibly due to low biomass of the sample resulting in low DNA extraction yield. In this case, the user may want to remove samples based on their minimum total frequency (i.e., total number of sequences obtained for the sample, in this example). This can be achieved as follows (in this example, samples with a total frequency less than 1500 will be filtered).

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --o-filtered-table filtered-table --p-min-frequency 1500

This filter can be applied to the feature axis to remove low abundance features from a table. For example, you can remove all features with a total abundance (summed across all samples) of less than 10 as follows.

.. command-block::
    qiime feature-table filter-features --i-table table.qza --o-filtered-table filtered-table --p-min-frequency 10

Both of these methods can also be applied to filter based on the maximum total frequency using the ``--p-max-frequency``. The ``--p-min-frequency`` and ``--p-max-frequency`` can be combined to filter based on lower and upper limits of frequency.

Contingency-based filtering
---------------------------

Contingency-based filtering is used to filter samples from a table contingent on the number of features they contain, or to filter features from a table contingent on the number of samples they're observed in.

This filtering is commonly used for filtering features that show up in only one or a few samples, based on the suspicion that these may not represent real biological diversity but rather experimental artifacts such as PCR chimeras. Features that are present in only a single sample could be filtered from a feature table as follows.

.. command-block::
    qiime feature-table filter-features --i-table table.qza --o-filtered-table filtered-table --p-min-samples 2

Similarly, samples that contain only a few features could be filtered from a feature table as follows.

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --o-filtered-table filtered-table --p-min-features 10

Both of these methods can also be applied to filter contingent on the maximum number of features or samples, using the ``--p-max-features`` and ``--p-max-samples`` parameters.

Identifier-based filtering
--------------------------

Identifier-based filtering is used to retain only a user-specified list of samples or features. In this case, the user will provide a tab-separated text file as input with the ``--m-sample-metadata-file`` or ``--m-feature-metadata-file`` parameter (for ``filter-samples`` or ``filter-features``, respectively) where the first column in the file contains that identifiers that should be retained, and the first row contains headers or names for each column. Only the first column in this file will be used, so there are no requirements on subsequent columns (if any are present). As a result, sample or feature metadata files can be used with this parameter. Identifier-based filtering can be applied as follows to remove samples from a feature table.

First, we'll write a header line and two sample identifiers to a new file called ``samples-to-keep.tsv``. (If you already have a tsv file containing a header line and the identifiers of the samples that you want to keep, you can skip this step. Otherwise, in practice, you'd probably create this file in a text editor, not on the command line as is being done here.)

.. command-block::
    echo Identifier > samples-to-keep.tsv
    echo L1S8 >> samples-to-keep.tsv
    echo L1S105 >> samples-to-keep.tsv

Then, we'll call the ``filter-samples`` method with the parameter ``--m-sample-metadata-file samples-to-keep.tsv``. The resulting table will contain only the two samples whose identifiers are listed in ``samples-to-keep.tsv``.

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file samples-to-keep.tsv --o-filtered-table filtered-table

Metadata-based filtering
------------------------

Metadata-based filtering is similar to identifier-based filtering, except that the list of identifiers to keep is determined based on metadata rather than being provided by the user directly. This is achieved using the ``--m-sample-metadata-file`` or ``--m-feature-metadata-file`` parameter (for ``filter-samples`` or ``filter-features``, respectively) and the ``--p-where`` parameter. The user provides a description of the samples that should be retained based on their metadata using ``--p-where``, where the syntax for this description is the SQLite where-clause syntax.

For example, filtering the table to contain only samples from subject 1 is performed as follows. Here, the ``--p-where`` parameter is specifying that we want to retain all of the samples whose ``Subject`` is ``subject-1`` in ``sample-metadata.tsv``.

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1'" --o-filtered-table filtered-table

``--p-where`` expressions can be made more complex as follows. Here, the ``--p-where`` parameter is specifying that we want to retain only the samples whose ``Subject`` is ``subject-1`` *and* whose ``BodySite`` is ``gut`` in ``sample-metadata.tsv``.

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1' AND BodySite='gut'" --o-filtered-table filtered-table

This syntax also supports negating individual clauses of the ``--p-where`` expression (or the whole expression). Here, the ``--p-where`` parameter is specifying that we want to retain only the samples whose ``Subject`` is ``subject-1`` and whose ``BodySite`` is *not* ``gut`` in ``sample-metadata.tsv``.

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1' AND NOT BodySite='gut'" --o-filtered-table filtered-table

.. note:: Currently, the most common metadata-based filtering of features is based on feature taxonomy, such as filtering all features that are annotated as being in a particular genus. This can currently be achieved using ``filter-features`` if taxonomy is provided in a feature metadata file. We are working on adding more direct support for this functionality, which will be made available in a new method of the ``q2-taxa`` plugin. You can track progress on this `here <https://github.com/qiime2/q2-taxa/issues/40>`_.
