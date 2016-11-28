feature-classifier tutorial
===========================

.. note:: This guide assumes you have performed the steps in the :doc:`install guide <../install>`.

This tutorial will demonstrate how to retrain the ``feature-classifier`` for a particular dataset. We will retrain the `Naive Bayes`_ classifier using `Greengenes`_ reference sequences and classify the representative sequences from the `Moving Pictures`_ dataset.

We will download and create several files, so first create a working directory.

.. command-block::
    :no-exec:

    mkdir feature-classifier-tutorial
    cd feature-classifier-tutorial

Obtaining and importing reference data sets
-------------------------------------------

Two elements are required for training the classifier: the reference sequences and the corresponding taxonomic classifications. To reduce computation time for this tutorial we will use the relatively small `Greengenes`_ 13_8 85% OTU data set. The next step will require aligned reference sequences. The ones that we will download here are already aligned.

.. note:: The aligned sequences that are available in the standard Greengenes data sets have had some columns removed, which would adversely affect the performance of the classifier. If you are starting from scratch, download the unaligned reference sequences and align them yourself.

We will also download the representative sequences from the `Moving Pictures`_ tutorial to check that the classifier classifies.

.. command-block::

    curl -sL https://zenodo.org/record/179385/files/aligned_85_otu_sequences.fasta.gz > aligned_85_otu_sequences.fasta.gz
    curl -sL https://zenodo.org/record/179385/files/85_otu_taxonomy.txt > 85_otu_taxonomy.txt
    curl -sL https://zenodo.org/record/179385/files/rep-seqs.qza > rep-seqs.qza

Next we import the raw data into QIIME 2 Artifacts. Note that we will load the reference sequences into a ``FeatureData[Sequence]``. In the next release of QIIME 2 we will load them into a more appropriate ``FeatureData[AlignedSequence]`` Artifact.

.. command-block::
    
    qiime tools import --type FeatureData[Sequence] --input-path aligned_85_otu_sequences.fasta.gz --output-path 85_otus.qza
    qiime tools import --type FeatureData[Taxonomy] --input-path 85_otu_taxonomy.txt --output-path taxonomy.qza


Extract reference reads
-----------------------

When training a machine learning classifier it is best for the training set to resemble the unseen data as closely as possible. We therefore extract reads from the reference sequences that resemble those in the sample data. We know from the `Moving Pictures`_ tutorial that the single-ended samples were extracted using the 515F/806R primer pair and truncated to 100 bases, so we try to reflect that here.

If classifying paired-end reads it is necessary to extract paired-end reference sequences at this stage using ``qiime feature-classifier extract-paired-end-reads`` instead.

.. command-block::

    qiime feature-classifier extract-reads --i-sequences 85_otus.qza --p-f-primer GTGCCAGCMGCCGCGGTAA --p-r-primer GGACTACHVGGGTWTCTAAT --p-read-length 100 --o-reads ref-seqs.qza


Train the classifier
--------------------

Retraining the classifier is now straightforward. We ask the ``feature-classifier`` to train a `Naive Bayes`_ classifier using the reference reads, the reference taxonomy, and the default parameters. 

.. command-block::

    qiime feature-classifier fit-classifier-naive-bayes --i-reference-reads ref-seqs.qza --i-reference-taxonomy taxonomy.qza --o-classifier classifier.qza

Classify a sample
-----------------

Finally, we verify that the classifier works by classifying the representative sequences from the `Moving Pictures`_ tutorial. More extensive information on this step is available in that tutorial.

.. command-block::

    qiime feature-classifier classify --i-classifier classifier.qza --i-reads rep-seqs.qza --o-classification classification.qza

.. _Moving Pictures: ../moving-pictures/index.html
.. _Naive Bayes: http://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes
.. _Greengenes: http://qiime.org/home_static/dataFiles.html
