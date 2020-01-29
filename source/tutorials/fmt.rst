Fecal microbiota transplant (FMT) study: an exercise
====================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install guides <../install/index>`.

This document is intended to be run after :doc:`the moving pictures tutorial <moving-pictures>`. It is designed to introduce a few new ideas, and to be an exercise in applying the tools that were explored in that document.

The data used in this tutorial is derived from a `Fecal Microbiome Transplant study`_ where children under the age of 18 with autism and gastrointestinal disorders, as measured by the Autism Diagnostic Interview-Revised (ADI-R) and Gastrointestinal Symptom Rating Scale (GSRS), respectively, were treated with fecal microbiota transplant in attempt to reduce the severity of their behavioral and gastrointestinal symptoms. We tracked changes in their microbiome, several metrics of the severity of autism including the Parent Global Impressions-III (PGI-III) and the Childhood Autism Rating Scale (CARS), and the severity of their gastrointestinal symptoms through their GSRS score over an eighteen week period. The microbiome was tracked through collection of weekly fecal swab samples (collected by swabbing used toilet paper) and less frequent stool samples (collected as whole stool). In the full study, which was a phase 1 clinical trial designed to test safety of the treatment, eighteen individuals received the treatment, and twenty individuals were followed as controls. The controls did not receive the treatment, but were monitored to track normal temporal variation in the gut microbiome. The fecal material that was transplanted during treatment was also sequenced in this study.

This tutorial dataset is a subsample of the data generated for this study. It includes data from five individuals who received treatment and five controls. Between six and sixteen samples are included per individual, including stool and fecal swab samples for each individual, and samples before and after FMT treatment. Five samples of the transplanted fecal material are also included.

These data were sequenced on two Illumina MiSeq sequencing runs. As in the Moving Pictures tutorial, we'll use `DADA2`_ to perform initial quality control and generate our ``FeatureTable[Frequency]`` and ``FeatureData[Sequence]`` objects. However, the DADA2 denoising process is only applicable to a single sequencing run at a time, so we need to run this on a per sequencing run basis and then merge the results. We'll work through this initial step, and then pose several questions that can be answered as an exercise.

Obtain data files
-----------------

Create a directory to work in called ``qiime2-fmt-tutorial`` and change to that directory:

.. command-block::
   :no-exec:

   mkdir qiime2-fmt-tutorial
   cd qiime2-fmt-tutorial

As in the Moving Pictures study, you should begin your analysis by familiarizing yourself with the sample metadata. You can again access the `sample metadata`_ as a Google Spreadsheet. Notice that there are three tabs in this spreadsheet. This first tab (called sample-metadata) contains all of the clinical metadata.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/fmt/sample_metadata.tsv
   :saveas: sample-metadata.tsv

Next, download the *demultiplexed sequences* that we'll use in this analysis. To learn how to start a QIIME 2 analysis from fastq-formatted sequence data, see the :doc:`importing data tutorial <importing>`. We'll need to download two sets of demultiplexed sequences, each corresponding to one of the sequencing runs.

In this tutorial we'll work with a small subsample of the complete sequence data so that the commands will run quickly. You can choose either a 1% subsample of the reads or a 10% subsample of the reads. If you're just trying to gain experience with preparing and combining multiple sequencing runs of data, you can work with the 1% subsample data so that the commands will run very quickly. If you're using this tutorial to gain additional experience in generating and interpreting QIIME 2 analysis results, you should work with the 10% subsample data so that the results will be supported by more sequence data (1% of the reads is likely not sufficient to support some of the findings of the original study).


10% subsample data
~~~~~~~~~~~~~~~~~~

.. download::
   :no-exec:
   :url: https://data.qiime2.org/2020.2/tutorials/fmt/fmt-tutorial-demux-1-10p.qza
   :saveas: fmt-tutorial-demux-1.qza

.. download::
   :no-exec:
   :url: https://data.qiime2.org/2020.2/tutorials/fmt/fmt-tutorial-demux-2-10p.qza
   :saveas: fmt-tutorial-demux-2.qza

1% subsample data
~~~~~~~~~~~~~~~~~

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/fmt/fmt-tutorial-demux-1-1p.qza
   :saveas: fmt-tutorial-demux-1.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/fmt/fmt-tutorial-demux-2-1p.qza
   :saveas: fmt-tutorial-demux-2.qza

Sequence quality control
------------------------

We'll begin by performing quality control on the demultiplexed sequences using `DADA2`_, but this time we'll run the ``denoise-single`` command on each set of demultiplexed sequences individually. Again, we'll want to start by visualizing sequence quality for some of the samples in each run. When we run ``denoise-single``, we need to use the same values for ``--p-trunc-len`` and ``--p-trim-left`` for both runs, so when looking at the visualizations that result from these two commands, think about what values would make sense for these parameters for both commands.

.. command-block::

   qiime demux summarize \
     --i-data fmt-tutorial-demux-1.qza \
     --o-visualization demux-summary-1.qzv
   qiime demux summarize \
     --i-data fmt-tutorial-demux-2.qza \
     --o-visualization demux-summary-2.qzv

.. question::
   Based on the plots you see in ``demux-summary-1.qzv`` and ``demux-summary-2.qzv``, what values would you choose for ``--p-trunc-len`` and ``--p-trim-left`` in this case? How does these plots compare to those generated in the :doc:`the moving pictures tutorial <moving-pictures>`?

Here the quality seems relatively low in the first few bases, and then seems to stay relatively high through the end of the reads. We'll therefore trim the first 13 bases from each sequence and truncate the sequences at 150 bases. Since the reads are 151 bases long, this results in very little truncation of the sequences.

.. command-block::

   qiime dada2 denoise-single \
     --p-trim-left 13 \
     --p-trunc-len 150 \
     --i-demultiplexed-seqs fmt-tutorial-demux-1.qza \
     --o-representative-sequences rep-seqs-1.qza \
     --o-table table-1.qza \
     --o-denoising-stats stats-1.qza
   qiime dada2 denoise-single \
     --p-trim-left 13 \
     --p-trunc-len 150 \
     --i-demultiplexed-seqs fmt-tutorial-demux-2.qza \
     --o-representative-sequences rep-seqs-2.qza \
     --o-table table-2.qza \
     --o-denoising-stats stats-2.qza

Viewing denoising stats
-----------------------

The ``denoise-single`` commands return basic statistics about the denoising process, and can be visualized with the following:

.. command-block::

   qiime metadata tabulate \
     --m-input-file stats-1.qza \
     --o-visualization denoising-stats-1.qzv
   qiime metadata tabulate \
     --m-input-file stats-2.qza \
     --o-visualization denoising-stats-2.qzv

Merging denoised data
---------------------

The ``denoise-single`` command is the last step in this analysis that needs to be run on a per sequencing run basis. We're therefore ready to merge the artifacts generated by those two commands. First we'll merge the two ``FeatureTable[Frequency]`` artifacts, and then we'll merge the two ``FeatureData[Sequence]`` artifacts. This is possible because the feature ids generated in each run of ``denoise-single`` are directly comparable (in this case, the feature id is the md5 hash of the sequence defining the feature).

.. command-block::

   qiime feature-table merge \
     --i-tables table-1.qza \
     --i-tables table-2.qza \
     --o-merged-table table.qza
   qiime feature-table merge-seqs \
     --i-data rep-seqs-1.qza \
     --i-data rep-seqs-2.qza \
     --o-merged-data rep-seqs.qza

Next, we'll generate a summary of the merged ``FeatureTable[Frequency]`` artifact.

.. command-block::

   qiime feature-table summarize \
     --i-table table.qza \
     --o-visualization table.qzv \
     --m-sample-metadata-file sample-metadata.tsv

.. question::
   Based on the information in ``table.qzv``, what value will you choose for the ``--p-sampling-depth`` parameter when you run ``qiime diversity core-metrics-phylogenetic``?

.. question::
   Generate summaries of the tables for the individual runs of ``qiime dada2 denoise-single``. How many features were defined in the first run? How many features were defined in the second run? How do these numbers compare to total number of features after merging?

We'll also generate a summary of the merged ``FeatureData[Sequence]`` artifact. You can use this summary to obtain additional information about specific features of interest as you proceed through the analysis.

.. command-block::

   qiime feature-table tabulate-seqs \
     --i-data rep-seqs.qza \
     --o-visualization rep-seqs.qzv


.. _`fmt diversity`:

Diversity analysis
------------------

Now that you have ``FeatureTable[Frequency]`` and ``FeatureData[Sequence]`` objects, you're ready to begin exploring the composition of these samples in the context of their metadata. Refer to :doc:`the moving pictures tutorial <moving-pictures>` to derive the specific commands that you'll run. Several questions concern longitudinal changes in the microbiome of individuals; review the actions described in the :doc:`q2-longitudinal tutorial <longitudinal>` to learn about methods for longitudinal analysis that are supported in QIIME 2.

Below are some specific questions to answer about this data, grouped into a few categories. Try to collect at least one specific result to support your answer to each question.

1. The personal human microbiome.

   a. Do samples differ in composition by subject-id (i.e., across individual)?
   #. Do samples differ in richness by subject-id?
   #. Do samples differ in evenness by subject-id?
   #. Do richness, evenness, composition, and UniFrac distance change in individuals between baseline and the end of the study? Does this differ between individuals receiving FMT and control subjects? (Hint: try the paired difference/distance methods described in the :doc:`q2-longitudinal tutorial <longitudinal>`.)
   #. Do richness, evenness, composition, and UniFrac distance change over time and in relation to FMT treatment and other subject metadata? Are these metrics more variable over time in treatment or control groups? (Hint: these questions concern longitudinal measurements.)

#. Microbiota engraftment.

   a. At approximately what week in the study do microbiome samples in individuals who receive treatment appear most similar to FMT donors in terms of unweighted UniFrac distances? (Hint: Try plotting the data with ``qiime emperor plot``. Pay close attention to the *color* tab and *visibility* menu.)
   #. At approximately what week in the study do microbiome samples in individuals who receive treatment appear most similar to FMT donors in terms of Bray-Curtis distances?
   #. Is this pattern stronger based on unweighted UniFrac or Bray-Curtis distance? Based on how you know about these metrics, what does this suggest to you about what is changing in the microbiome with fecal microbiota transplant? Use the Jaccard and weighted UniFrac distance Emperor plots to help you refine this idea.

#. Experimental design: Comparing stool and swab sample collection methods.

   a. What feature(s) differ most in abundance between the stool and swab samples? What taxonomy is associated with those feature ids based on their best BLAST hits, and based on the results of Naive Bayes feature classification with the QIIME 2 ``q2-feature-classifier`` plugin?
   #. Is the microbial composition of stool and swab samples significantly different based on either unweighted UniFrac or Bray-Curtis distances between samples (*yes*, *no*, or *not possible to say with the current information*)?
   #. Do the donated fecal material samples appear more similar in composition to the stool or swab samples?
   #. Does community richness differ between stool samples and swab samples? Does community evenness differ between stool samples and swab samples?

#. How many samples were sequenced in each sequencing run? Do you observe any systematic differences in the samples across sequencing runs?

Acknowledgements
----------------

The data in this tutorial was initially presented in: Microbiota Transfer Therapy alters gut ecosystem and improves gastrointestinal and autism symptoms: an open-label study. Dae-Wook Kang, James B. Adams, Ann C. Gregory, Thomas Borody, Lauren Chittick, Alessio Fasano, Alexander Khoruts, Elizabeth Geis, Juan Maldonado, Sharon McDonough-Means, Elena L. Pollard, Simon Roux, Michael J. Sadowsky, Karen Schwarzberg Lipson, Matthew B. Sullivan, J. Gregory Caporaso and Rosa Krajmalnik-Brown. Microbiome (2017) 5:10. DOI: 10.1186/s40168-016-0225-7.

.. _DADA2: https://www.ncbi.nlm.nih.gov/pubmed/27214047
.. _sample metadata: https://data.qiime2.org/2020.2/tutorials/fmt/sample_metadata
.. _Fecal Microbiome Transplant study: http://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-016-0225-7
