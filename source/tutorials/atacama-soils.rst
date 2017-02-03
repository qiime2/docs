"Atacama soil microbiome" tutorial
==================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial is designed to be a self-guided exercise that could be run after :doc:`the moving pictures tutorial <moving-pictures>` to gain more experience with QIIME 2. The data in this tutorial is paired-end Illumina MiSeq data, so this tutorial is also useful for learning how to work with paired-end data in QIIME 2.

In this tutorial you'll use QIIME 2 to perform an analysis of soil samples from the Atacama Desert in northern Chile...

Download data files
-------------------

Before starting the analysis, explore the sample metadata to familiarize yourself with the samples used in this study. The `sample metadata`_ is available as a Google Sheet. This ``sample-metadata.tsv`` file is used throughout the rest of the tutorial.

.. download::
   :url: https://docs.google.com/spreadsheets/d/1xMP1EjKZDrzdKLnQr7LGVAY35ongxrreT28k0EACtfg/export?gid=0&format=tsv
   :saveas: sample-metadata.tsv

.. command-block::

   mkdir emp-paired-end-sequences

.. download::
   :url: https://dl.dropboxusercontent.com/u/2868868/data/qiime2/tutorials/importing-sequence-data/2017.2/emp-paired-end-sequences/atacama-10p/forward.fastq.gz
   :saveas: emp-paired-end-sequences/forward.fastq.gz

.. download::
   :url: https://dl.dropboxusercontent.com/u/2868868/data/qiime2/tutorials/importing-sequence-data/2017.2/emp-paired-end-sequences/atacama-10p/reverse.fastq.gz
   :saveas: emp-paired-end-sequences/reverse.fastq.gz

.. download::
   :url: https://dl.dropboxusercontent.com/u/2868868/data/qiime2/tutorials/importing-sequence-data/2017.2/emp-paired-end-sequences/atacama-10p/barcodes.fastq.gz
   :saveas: emp-paired-end-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2.0.6/common/silva-119-99-full-length-nb-classifier.qza
   :saveas: silva-119-99-full-length-nb-classifier.qza

Analysis commands
-----------------

.. command-block::

   qiime tools import \
      --type EMPPairedEndSequences \
      --input-path emp-paired-end-sequences \
      --output-path emp-paired-end-sequences.qza

   qiime demux emp-paired \
     --m-barcodes-file sample-metadata.tsv \
     --m-barcodes-category BarcodeSequence \
     --i-seqs emp-paired-end-sequences.qza \
     --o-per-sample-sequences demux \
     --p-rev-comp-mapping-barcodes

   qiime demux summarize \
     --i-data demux.qza \
     --o-visualization demux.qzv \
     --p-n 10

   qiime dada2 denoise-paired \
     --i-demultiplexed-seqs demux.qza \
     --o-table table \
     --o-representative-sequences rep-seqs \
     --p-trim-left-f 10 \
     --p-trim-left-r 10 \
     --p-trunc-len-f 150 \
     --p-trunc-len-r 150 \
     --p-n-threads 0 \
     --p-n-reads-learn 100000

   qiime feature-table summarize \
     --i-table table.qza \
     --o-visualization table.qzv

   qiime feature-table tabulate-seqs \
     --i-data rep-seqs.qza \
     --o-visualization rep-seqs.qzv

   qiime alignment mafft \
     --i-sequences rep-seqs.qza \
     --o-alignment aligned-rep-seqs.qza

   qiime alignment mask \
     --i-alignment aligned-rep-seqs.qza \
     --o-masked-alignment masked-aligned-rep-seqs.qza

   qiime phylogeny fasttree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --o-tree unrooted-tree.qza

   qiime phylogeny midpoint-root \
     --i-tree unrooted-tree.qza \
     --o-rooted-tree rooted-tree.qza

   qiime diversity core-metrics \
     --i-phylogeny rooted-tree.qza \
     --i-table table.qza \
     --p-sampling-depth 2026 \
     --output-dir cm2026

   qiime diversity alpha-group-significance \
     --i-alpha-diversity cm2026/faith_pd_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/faith-pd-group-significance.qzv

   qiime diversity alpha-group-significance \
     --i-alpha-diversity cm2026/observed_otus_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/observed-otus-group-significance.qzv

   qiime diversity alpha-group-significance \
     --i-alpha-diversity cm2026/evenness_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/evenness-group-significance.qzv

   qiime diversity alpha-correlation \
     --i-alpha-diversity cm2026/faith_pd_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/faith-pd-correlation.qzv

   qiime diversity alpha-correlation \
     --i-alpha-diversity cm2026/evenness_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/evenness-correlation.qzv

   qiime emperor plot \
     --i-pcoa cm2026/unweighted_unifrac_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/unweighted-unifrac-emperor.qzv

   qiime diversity bioenv \
     --i-distance-matrix cm2026/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization cm2026/unweighted-unifrac-bioenv.qzv

   qiime feature-classifier classify \
     --i-classifier silva-119-99-full-length-nb-classifier.qza \
     --i-reads rep-seqs.qza \
     --o-classification taxonomy.qza

   qiime taxa tabulate \
     --i-data taxonomy.qza \
     --o-visualization taxonomy.qzv

   qiime taxa barplot \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization taxa-bar-plots.qzv

   qiime taxa collapse \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --p-level 2 \
     --o-collapsed-table table-l2.qza

   qiime composition add-pseudocount \
     --i-table table-l2.qza \
     --o-composition-table comp-table-l2.qza

   qiime composition ancom \
     --i-table comp-table-l2.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-category Vegetation \
     --o-visualization l2-ancom-Vegetation.qzv

Sequence processing and diversity analyses
------------------------------------------

Use the following questions to guide your analyses of the data.

#. What value would you choose to pass for ``--p-sampling-depth``? How many samples will be excluded from your analysis based on this choice? Approximately how many total sequences will you be analyzing in the ``core-metrics`` command?

#. What sample metadata or combinations of sample metadata are most strongly associated with the differences in microbial composition of the samples? Are these associations stronger with unweighted UniFrac or with Bray-Curtis? Based on what you know about these metrics, what does that difference suggest?

#. What do you conclude about the associations between continuous sample metadata and the richness and evenness of these samples?

#. What discrete sample metadata categories are most strongly associated with the differences in microbial community richness or evenness? Are these differences statistically significant?

#. What differences do you observe between the unweighted UniFrac and Bray-Curtis PCoA plots?

#. In taxonomic composition bar plots, sort the samples by their average soil relative humidity, and visualize them at the phylum level. What are the dominant phyla in these samples? Which phyla increase and which decrease with increasing average soil relative humidity?

#. What phyla differ in abundance across vegetated and unvegetated sites?

.. _sample metadata: https://docs.google.com/spreadsheets/d/1xMP1EjKZDrzdKLnQr7LGVAY35ongxrreT28k0EACtfg/edit?usp=sharing
