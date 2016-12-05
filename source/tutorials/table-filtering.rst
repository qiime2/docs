Filtering feature tables
========================

.. note:: This guide assumes you have performed the steps in the :doc:`install guide <../install>`.

This tutorial covers filtering (i.e., removing) samples and features from `FeatureTable` objects. Feature tables have two axes: the sample axis and the feature axis. The filtering operations described in this tutorial are applicable to either axis, and support filtering based on sample or feature frequencies and/or based on sample or feature identifiers.

The two methods covered in this tutorial are implemented in the `q2-feature-table` plugin. The `filter-samples` method is used for filtering samples from a feature table, and the `filter-features` method is used for filtering features from a feature table.

In this document we'll work with the feature table and sample metadata from the :doc:`Moving Pictures tutorial <./moving-pictures.rst>`. As a first step, download both of these files as follows.

.. command-block::

    curl -sL "https://docs.google.com/spreadsheets/d/1_3ZbqCtAYx-9BJYHoWlICkVJ4W_QGMfJRPLedt_0hws/export?gid=0&format=tsv" > sample-metadata.tsv
    curl -sLO https://dl.dropboxusercontent.com/u/2868868/data/qiime2/tutorials/filtering-feature-tables/table.qza

Frequency-based filtering
-------------------------

Frequency-based filtering is used to filter samples based on their total frequency. This is most commonly applied to filter samples whose total frequency is an outlier in the distribution of sample frequencies. For example, in many 16S surveys, only a few (perhaps tens) of sequences will be obtained for some samples, possibly due to low biomass of the sample resulting in low DNA extraction yield. In this case, the user may want to filter samples based on their minimum total frequency (i.e., total number of sequences obtained, in this example). This can be achieved as follows.

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --o-filtered-table filtered-table --p-min-features 1500



Sample-identifier-based filtering
---------------------------------

Metadata-based filtering
------------------------

Filter to only subject-1 samples:

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1'" --o-filtered-table filtered-table

Filter to only subject-1 gut samples:

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1' AND BodySite='gut'" --o-filtered-table filtered-table

Filter to only subject-1 non-gut samples:

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1' AND NOT BodySite='gut'" --o-filtered-table filtered-table
