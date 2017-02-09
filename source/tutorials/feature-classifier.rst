Training feature classifiers with q2-feature-classifier
=======================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial will demonstrate how to train ``q2-feature-classifier`` for a particular dataset. We will train the `Naive Bayes`_ classifier using `Greengenes`_ reference sequences and classify the representative sequences from the `Moving Pictures`_ dataset.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir training-feature-classifiers
   cd training-feature-classifiers

Obtaining and importing reference data sets
-------------------------------------------

Two elements are required for training the classifier: the reference sequences and the corresponding taxonomic classifications. To reduce computation time for this tutorial we will use the relatively small `Greengenes`_ 13_8 85% OTU data set.

We will also download the representative sequences from the `Moving Pictures`_ tutorial to test our classifier.

.. download::
   :url: https://data.qiime2.org/2017.2/tutorials/training-feature-classifiers/85_otus.fasta
   :saveas: 85_otus.fasta

.. download::
   :url: https://data.qiime2.org/2017.2/tutorials/training-feature-classifiers/85_otu_taxonomy.txt
   :saveas: 85_otu_taxonomy.txt

.. download::
   :url: https://data.qiime2.org/2017.2/tutorials/training-feature-classifiers/rep-seqs.qza
   :saveas: rep-seqs.qza

Next we import these data into QIIME 2 Artifacts.

.. command-block::

   qiime tools import \
     --type FeatureData[Sequence] \
     --input-path 85_otus.fasta \
     --output-path 85_otus.qza

   qiime tools import \
     --type FeatureData[Taxonomy] \
     --input-path 85_otu_taxonomy.txt \
     --output-path ref-taxonomy.qza


Extract reference reads
-----------------------

It has been shown that taxonomic classification accuracy improves when a Naive Bayes classifier is trained on only the region of the target sequences that was sequenced `(Werner et al., 2012)`_. We know from the `Moving Pictures`_ tutorial that the sequence reads that we're trying to classify are 100-base single-end reads that were amplified with the 515F/806R primer pair. We optimize for that here by extracting reads from the reference database based on matches to this primer pair, and then slicing the result to 100 bases.

.. command-block::

   qiime feature-classifier extract-reads \
     --i-sequences 85_otus.qza \
     --p-f-primer GTGCCAGCMGCCGCGGTAA \
     --p-r-primer GGACTACHVGGGTWTCTAAT \
     --p-length 100 \
     --o-reads ref-seqs.qza


Train the classifier
--------------------

We can now train a `Naive Bayes`_ classifier as follows, using the reference reads and taxonomy that we just created.

.. command-block::

   qiime feature-classifier fit-classifier-naive-bayes \
     --i-reference-reads ref-seqs.qza \
     --i-reference-taxonomy ref-taxonomy.qza \
     --o-classifier classifier.qza

Test the classifier
-------------------

Finally, we verify that the classifier works by classifying the representative sequences from the `Moving Pictures`_ tutorial and visualizing the resulting taxonomic assignments.

.. command-block::

   qiime feature-classifier classify \
     --i-classifier classifier.qza \
     --i-reads rep-seqs.qza \
     --o-classification taxonomy.qza

   qiime taxa tabulate \
     --i-data taxonomy.qza \
     --o-visualization taxonomy.qzv

.. _Moving Pictures: ../moving-pictures/index.html
.. _Naive Bayes: http://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes
.. _Greengenes: http://qiime.org/home_static/dataFiles.html
.. _(Werner et al., 2012): https://www.ncbi.nlm.nih.gov/pubmed/21716311
