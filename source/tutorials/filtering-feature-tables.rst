Filtering feature tables
========================

.. note:: This guide assumes you have performed the steps in the :doc:`install guide <../install>` and uses data from the :doc:`Moving Pictures tutorial <./moving-pictures.rst>`.

This tutorial covers filtering samples and features from `FeatureTable` objects. In this document we'll work with the feature table and sample metadata from the :doc:`Moving Pictures tutorial <./moving-pictures.rst>`. As a first step, download both of these files as follows.

.. command-block::

    curl -sL "https://docs.google.com/spreadsheets/d/1_3ZbqCtAYx-9BJYHoWlICkVJ4W_QGMfJRPLedt_0hws/export?gid=0&format=tsv" > sample-metadata.tsv
    curl -sLO https://dl.dropboxusercontent.com/u/2868868/data/qiime2/tutorials/filtering-feature-tables/table.qza

Filtering samples from a feature table
--------------------------------------

Count-based filtering
~~~~~~~~~~~~~~~~~~~~~

Index-based filtering
~~~~~~~~~~~~~~~~~~~~~

Metadata-based filtering
~~~~~~~~~~~~~~~~~~~~~~~~

Filter to only subject-1 samples:

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1'" --o-filtered-table filtered-table

Filter to only subject-1 gut samples:

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1' AND BodySite='gut'" --o-filtered-table filtered-table

Filter to only subject-1 non-gut samples:

.. command-block::
    qiime feature-table filter-samples --i-table table.qza --m-sample-metadata-file sample-metadata.tsv --p-where "Subject='subject-1' AND NOT BodySite='gut'" --o-filtered-table filtered-table

Filtering features from a feature table
--------------------------------------
