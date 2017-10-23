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

The `exclude-seqs` method aligns a series of query sequences contained in a ``FeatureData[Sequences]`` file against a series of reference sequences. This method employs a number of different alignment criteria (BLAST evalue, percent identity to top reference sequence, and percent of query that aligns to top reference sequence) to decide whether that sequence "hits" the reference sequences, and outputs separate files of sequences that hit/do not hit the reference sequences. This method can be used for a variety of applications, including removing known contaminant sequences, excluding host sequences (e.g., human DNA), or removing non-target sequences (e.g., non-bacterial) from your data.

Let's download some example data and get started.

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/quality-control/query-seqs.qza
   :saveas: query-seqs.qza

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/quality-control/reference-seqs.qza
   :saveas: reference-seqs.qza

Next, we will separate a small set of query sequences into those that hit/do not hit a set of reference sequences.

.. command-block::

   qiime quality-control exclude-seqs \
     --i-feature-sequences query-seqs.qza \
     --i-reference-sequences reference-seqs.qza \
     --p-method blast \
     --p-perc-identity 0.97 \
     --p-perc-query-aligned 0.97 \
     --o-sequence-hits hits \
     --o-sequence-misses misses

This method currently supports ``BLAST``, ``vsearch``, and ``blastn-short`` as alignment methods. Note that ``blastn-short`` should be used if the query sequences include very short sequences (< 30 nt).

