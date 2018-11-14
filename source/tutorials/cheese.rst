Training a taxonomic classifier
=========================================

This tutorial gives a deliberately-complicated example of how to train a naive Bayes classifier for short read taxonomic classification.

It includes

- trimming the reference sequences to the region of interest and
- assembling class weights from custom data and using them to train a classifier.

Off-the-shelf classifiers are available in the `QIIME 2 docs <https://docs.qiime2.org/2018.11/data-resources/>`_. A tutorial that just covers trimming reference sequences is also available in the `docs <https://docs.qiime2.org/2018.11/tutorials/feature-classifier/>`_. A tutorial that covers downloading community-sourced data from `Qiita <https://qiita.ucsd.edu/>`_ for a range of habitat types is available on the `forum <https://forum.qiime2.org/t/using-q2-clawback-to-assemble-taxonomic-weights/5859>`_.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir training-feature-classifiers
   cd training-feature-classifiers

Importing reference data sets
-----------------------------

We assume that the data is in a single `biom` table with multiple samples and where the features are ASVs. The example we use here is the deblur output for `Study ID 11488 <https://qiita.ucsd.edu/study/description/11488#>`_ in Qiita, which contains 362 samples from cheese rinds. We import it into `cheese-table.qza`

.. download::
   :url: https://s3-us-west-2.amazonaws.com/qiime2-data/workshops/monash18/cheese-data/cheese.biom
   :saveas: cheese.biom

.. command-block::

   qiime tools import \
      --input-path cheese.biom \
      --input-format BIOMV210Format \
      --type FeatureTable[Frequency] \
      --output-path cheese-table.qza

We will also require the Greengenes 99% OTU sequences and taxonomies.

.. download::
   :url: ftp://greengenes.microbio.me/greengenes_release//gg_13_8_otus/taxonomy/99_otu_taxonomy.txt
   :saveas: 99_otu_taxonomy.txt

.. download::
   :url: ftp://greengenes.microbio.me/greengenes_release//gg_13_8_otus/rep_set/99_otus.fasta
   :saveas: 99_otus.fasta

.. command-block::

   qiime tools import \
      --input-path 99_otu_taxonomy.txt \
      --input-format HeaderlessTSVTaxonomyFormat \
      --type FeatureData[Taxonomy] \
      --output-path gg-99-ref-taxa.qza

   qiime tools import \
      --input-path 99_otus.fasta \
      --input-format DNAFASTAFormat \
      --type FeatureData[Sequence] \
      --output-path gg-99-ref-seqs.qza

To save some time we will download the off-the-shelf naive Bayes classifier that has been trained on the 16S V4 region.

.. download::
   :url: https://data.qiime2.org/2018.11/common/gg-13-8-99-515-806-nb-classifier.qza
   :saveas: gg-13-8-99-515-806-nb-classifier.qza

Trim the reads
--------------

It turns out that trimming the 16S sequences is important for generating class weights, so we will do that first. This is the slowest command (~ 10 minutes).

.. command-block::

   qiime feature-classifier extract-reads \
      --p-f-primer GTGCCAGCMGCCGCGGTAA \
      --p-r-primer GGACTACHVGGGTWTCTAAT \
      --o-reads gg-99-ref-seqs-515f-806r.qza \
      --i-sequences gg-99-ref-seqs.qza


Assemble the class weights
--------------------------

First pull the ASVs out of the data and force them to be classified all the way to species level.

.. command-block::

   qiime clawback sequence-variants-from-samples \
      --o-sequences cheese-seqs.qza \
      --i-samples cheese-table.qza

   qiime feature-classifier classify-sklearn \
      --p-confidence -1.0 \
      --o-classification full-confidence.qza \
      --i-reads cheese-seqs.qza \
      --i-classifier gg-13-8-99-515-806-nb-classifier.qza

Next aggregate the results into a single weights vector.

.. command-block::

   qiime clawback generate-class-weights \
      --o-class-weight cheese-weight.qza \
      --i-reference-taxonomy gg-99-ref-taxa.qza \
      --i-reference-sequences gg-99-ref-seqs-515f-806r.qza \
      --i-samples cheese-table.qza \
      --i-taxonomy-classification full-confidence.qza

Finally, train the classifier.

.. command-block::

   qiime feature-classifier fit-classifier-naive-bayes \
      --o-classifier cheese-classifier.qza \
      --i-reference-reads gg-99-ref-seqs-515f-806r.qza \
      --i-reference-taxonomy gg-99-ref-taxa.qza \
      --i-class-weight cheese-weight.qza


Try classifying the original samples
------------------------------------

We will try classifying the sequences using uniform and bespoke class weights.

.. note:: Re-classifying sequences that we have used in the process of training our classifier is *not* good experimental design. We do it here as a rough demonstration of the difference that it makes to classification.

First using the off-the-shelf classifier (which has been trained using uniform weights):

.. command-block::

   qiime feature-classifier classify-sklearn \
      --o-classification uniform-cheese.qza \
      --i-reads cheese-seqs.qza \
      --i-classifier gg-13-8-99-515-806-nb-classifier.qza

Now use the bespoke classifier:

.. command-block::

   qiime feature-classifier classify-sklearn \
      --o-classification bespoke-cheese.qza \
      --i-reads cheese-seqs.qza \
      --i-classifier cheese-classifier.qza

Now compare the results
-----------------------

Using a fairly unorthidox pipeline we can compare the results. We presumptiously call bespoke "expected" and uniform "observed" in the following comparison.

.. command-block::

   qiime taxa collapse \
      --p-level 7 \
      --o-collapsed-table uniform-collapsed.qza \
      --i-table cheese-table.qza \
      --i-taxonomy uniform-cheese.qza

   qiime feature-table relative-frequency \
      --o-relative-frequency-table uniform-collapsed-relative.qza \
      --i-table uniform-collapsed.qza

   qiime taxa collapse \
      --p-level 7 \
      --o-collapsed-table bespoke-collapsed.qza \
      --i-table cheese-table.qza \
      --i-taxonomy bespoke-cheese.qza

   qiime feature-table relative-frequency \
      --o-relative-frequency-table bespoke-collapsed-relative.qza \
      --i-table bespoke-collapsed.qza

   qiime quality-control evaluate-composition \
      --o-visualization diff.qzv \
      --i-expected-features bespoke-collapsed-relative.qza \
      --i-observed-features uniform-collapsed-relative.qza

Now `diff.qza` should contain a comparison between the taxonomic classifications using the two methods.
