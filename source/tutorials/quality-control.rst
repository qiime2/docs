Removing contaminant sequence data with q2-quality-control
==========================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

This tutorial will demonstrate how to use the ``q2-quality-control`` plugin to filter sequence data.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir quality-control-tutorial
   cd quality-control-tutorial

Excluding sequences by alignment
--------------------------------

The ``exclude-seqs`` method aligns a set of query sequences contained in a ``FeatureData[Sequence]`` file against a set of reference sequences. This method employs a number of different alignment criteria (BLAST evalue, percent identity to top reference sequence, and percent of query that aligns to top reference sequence) to decide whether that sequence "hits" the reference sequences, and outputs separate files of sequences that hit/do not hit the reference sequences. This method can be used for a variety of applications, including removing known contaminant sequences, excluding host sequences (e.g., human DNA), or removing non-target sequences (e.g., non-bacterial) from your data.

Let's download some example data and get started.

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/quality-control/query-seqs.qza
   :saveas: query-seqs.qza

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/quality-control/reference-seqs.qza
   :saveas: reference-seqs.qza

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/quality-control/query-table.qza
   :saveas: query-table.qza

Next, we will separate a small set of query sequences into those that hit/do not hit a set of reference sequences.

.. command-block::

   qiime quality-control exclude-seqs \
     --i-query-sequences query-seqs.qza \
     --i-reference-sequences reference-seqs.qza \
     --p-method blast \
     --p-perc-identity 0.97 \
     --p-perc-query-aligned 0.97 \
     --o-sequence-hits hits.qza \
     --o-sequence-misses misses.qza

This method currently supports ``blast``, ``vsearch``, and ``blastn-short`` as alignment methods. Note that ``blastn-short`` should be used if the query sequences include very short sequences (< 30 nt).

Now that you have split your sequences into groups of sequences that hit/miss the reference sequences, you will most likely want to filter your feature table to remove hits or misses prior to further analysis. Filtering features from feature tables is fully covered in the :doc:`filtering tutorial <filtering>`, but here we will demonstrate an example of filtering a feature table using sequence data. In some cases, you may want to remove the `misses` from your feature table, e.g., if you are trying to select sequences that align to bacterial sequences (or a more specific clade). In other cases, you may want to remove the `hits` from your feature table, e.g., if you are trying to filter out contaminants or sequences that align to host DNA. Here we will filter out `hits` to demonstrate how to filter sequences from a filter table; one can replace ``hits.qza`` with ``misses.qza`` in the following command to filter out misses instead.

.. command-block::
   qiime feature-table filter-features \
     --i-table query-table.qza \
     --m-metadata-file hits.qza \
     --o-filtered-table hits-filtered-table.qza

Enjoy.