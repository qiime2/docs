Evaluating and controlling data quality with q2-quality-control
===============================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

This tutorial will demonstrate how to use the ``q2-quality-control`` plugin to evaluate data quality based on mock communities (or other samples with known compositions) and filter sequence data.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir quality-control-tutorial
   cd quality-control-tutorial

Let's download some example data and get started.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/quality-control/query-seqs.qza
   :saveas: query-seqs.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/quality-control/reference-seqs.qza
   :saveas: reference-seqs.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/quality-control/query-table.qza
   :saveas: query-table.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/quality-control/qc-mock-3-expected.qza
   :saveas: qc-mock-3-expected.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/quality-control/qc-mock-3-observed.qza
   :saveas: qc-mock-3-observed.qza


Excluding sequences by alignment
--------------------------------

The ``exclude-seqs`` method aligns a set of query sequences contained in a ``FeatureData[Sequence]`` file against a set of reference sequences. This method employs a number of different alignment criteria (BLAST evalue, percent identity to top reference sequence, and percent of query that aligns to top reference sequence) to decide whether that sequence "hits" the reference sequences, and outputs separate files of sequences that hit/do not hit the reference sequences. This method can be used for a variety of applications, including removing known contaminant sequences, excluding host sequences (e.g., human DNA), or removing non-target sequences (e.g., non-bacterial) from your data.

First, we will separate a small set of query sequences into those that hit/do not hit a set of reference sequences.

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
     --o-filtered-table no-hits-filtered-table.qza \
     --p-exclude-ids

Enjoy.


Evaluating quality of samples with known composition
----------------------------------------------------
`Mock communities`_ consist of known microbial strains that are intentionally mixed at defined proportions, such that the composition of the sample is known. Mock communities are useful for benchmarking bioinformatics methods, e.g., to determine how well a given method or pipeline estimates the expected composition. Many investigators also include mock communities or other samples with known compositions on sequencing runs to determine run quality and method optimization on a per-run basis. The q2-quality-control plugin contains two actions to assess mock community accuracy in each of these use cases. ``evaluate_composition`` assesses the accuracy with which the expected taxonomic composition (or other feature composition) is reconstructed. ``evaluate_seqs`` assesses the similarity of observed sequences to expected sequences, e.g., to determine the accuracy of denoising or OTU picking methods, and is described in the next section.

``evaluate_composition`` compares the feature composition of pairs of observed and expected samples containing the same sample ID in two separate feature tables. Typically, feature composition will consist of taxonomy classifications or other semicolon-delimited feature annotations. Let's give it a spin.

.. command-block::

   qiime quality-control evaluate-composition \
     --i-expected-features qc-mock-3-expected.qza \
     --i-observed-features qc-mock-3-observed.qza \
     --o-visualization qc-mock-3-comparison.qzv

Taxon accuracy rate, taxon detection rate, and linear regression scores between expected and observed feature abundances are calculated at each semicolon-delimited rank, and plots of per-level accuracy and observation correlations are plotted. A histogram of distance between false positive observations and the nearest expected feature is also generated, where distance equals the number of rank differences between the observed feature and the nearest common lineage in the expected feature. Finally, lists of false positive (misclassified and underclassified) and false negative features are given at the bottom of the visualization. Misclassifications are features that do not match any expected features at the deepest level of classification (e.g., species level), and usually represent either sample contaminants or sub-optimal bioinformatics pipelines (e.g., the presence of chimeric sequences or the use of an overconfident taxonomic classifier). Underclassifications are observed features that match expected features, but are not classified to the expected taxonomic depth (e.g., they are only classified to genus level but that genus classification is correct); these are often valid features (i.e., not contaminants) but are not classified to the desired level either because of technical limitations (e.g., sequences too short), degraded sequence quality, or sub-optimal methods (only a poor carpenter blames his/her tools, but one tool can do better than another). False negatives are features that were expected to be observed, but were not; these can be compared to the false-positives to get an idea of what features may have been mis-/underclassified.


Evaluating sequence quality
---------------------------
``evaluate_seqs`` aligns a set of query (e.g., observed) sequences against a set of reference (e.g., expected) sequences to evaluate the quality of alignment. The intended use is to align observed sequences against expected sequences (e.g., from a mock community) to determine the frequency of mismatches between observed sequences and the most similar expected sequences, e.g., as a measure of sequencing/method errors. However, any sequences may be provided as input to generate a report on pairwise alignment quality against a set of reference sequences. 

.. command-block::

   qiime quality-control evaluate-seqs \
     --i-query-sequences query-seqs.qza \
     --i-reference-sequences reference-seqs.qza \
     --o-visualization eval-seqs-test.qzv

This visualization shows the alignment results for each query sequence, the number of mismatches between expected and observed sequences, and finally pairwise alignments between each query sequence and its closest match among the reference sequences (if ``--p-show-alignments`` is set). This ouptut is still quite basic, but is planned for expansion in the near future. Keep your eyes peeled!



.. _Mock communities: https://doi.org/10.1128/mSystems.00062-16
