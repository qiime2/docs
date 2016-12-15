Training feature classifiers with q2-feature-classifier
=======================================================

.. note:: This guide assumes you have performed the steps in the :doc:`install guide <../install>`.

This tutorial will demonstrate how to train ``q2-feature-classifier`` for a particular dataset. We will train the `Naive Bayes`_ classifier using `Greengenes`_ reference sequences and classify the representative sequences from the `Moving Pictures`_ dataset.

We will download and create several files, so first create a working directory.

.. command-block::
    :no-exec:

    mkdir training-feature-classifiers
    cd training-feature-classifiers

Obtaining and importing reference data sets
-------------------------------------------

Two elements are required for training the classifier: the aligned reference sequences and the corresponding taxonomic classifications. To reduce computation time for this tutorial we will use the relatively small `Greengenes`_ 13_8 85% OTU data set.

.. note:: We require aligned references sequences for this process so we can trim the training sequences to the region of the gene that was amplified and sequenced. Training a classifier on only this region improves performance over training on the full length gene sequence, but does mean that the resulting classifier will only be applicable to sequences that were obtained using the same primers.

.. note:: The aligned sequences that are available in the Greengenes OTUs datasets sets have been filtered to remove very low conservation positions, which would adversely affect the performance of the classifier. If you are starting from scratch, download the unaligned reference sequences and align them yourself.

We will also download the representative sequences from the `Moving Pictures`_ tutorial to test our classifier.

.. command-block::

    curl -sLO https://data.qiime2.org/2.0.6/tutorials/training-feature-classifiers/aligned_85_otu_sequences.fasta.gz
    curl -sLO https://data.qiime2.org/2.0.6/tutorials/training-feature-classifiers/85_otu_taxonomy.txt
    curl -sLO https://data.qiime2.org/2.0.6/tutorials/training-feature-classifiers/rep-seqs.qza

Next we import the raw data into QIIME 2 Artifacts. Note that we will load the reference sequences into a ``FeatureData[Sequence]``. In the next release of QIIME 2 we will load them into a more appropriate ``FeatureData[AlignedSequence]`` Artifact.

.. command-block::

    qiime tools import \
      --type FeatureData[Sequence] \
      --input-path aligned_85_otu_sequences.fasta.gz \
      --output-path 85_otus.qza

    qiime tools import \
      --type FeatureData[Taxonomy] \
      --input-path 85_otu_taxonomy.txt \
      --output-path ref-taxonomy.qza \


Extract reference reads
-----------------------

It has been shown that taxonomic assignment improves when the classifier is trained on data that is trimmed to resemble the reads that it will be used to classify, at least for one Naive Bayes classifier `(Werner et al., 2012)`_. We know from the `Moving Pictures`_ tutorial that the sequences we want to classify are 100-base single-end reads that were amplified with the 515F/806R primer pair, so we try to reflect that here.

.. command-block::

    qiime feature-classifier extract-reads \
      --i-sequences 85_otus.qza \
      --p-f-primer GTGCCAGCMGCCGCGGTAA \
      --p-r-primer GGACTACHVGGGTWTCTAAT \
      --p-read-length 100 \
      --o-reads ref-seqs.qza


Train the classifier
--------------------

Training the classifier is now straightforward. We can now train a `Naive Bayes`_ classifier as follows, using the reference reads that we just created and the reference taxonomy:

.. command-block::

    qiime feature-classifier fit-classifier-naive-bayes \
      --i-reference-reads ref-seqs.qza \
      --i-reference-taxonomy ref-taxonomy.qza \
      --o-classifier classifier.qza

Test the classifier
-------------------

Finally, we verify that the classifier works by classifying the representative sequences from the `Moving Pictures`_ tutorial. More extensive information on this step is available in that tutorial.

.. command-block::

    qiime feature-classifier classify \
      --i-classifier classifier.qza \
      --i-reads rep-seqs.qza \
      --o-classification taxonomy.qza

.. _Moving Pictures: ../moving-pictures/index.html
.. _Naive Bayes: http://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes
.. _Greengenes: http://qiime.org/home_static/dataFiles.html
.. _(Werner et al., 2012): https://www.ncbi.nlm.nih.gov/pubmed/21716311
