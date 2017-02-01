Fecal microbiota transplant (FMT) study: an exercise
====================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install guides <../install/index>`.

This document is intended to be run after :doc:`the moving pictures tutorial <moving-pictures>`. It is designed to introduce a few new ideas, and to be an exercise in applying the tools that were explored in that document.

.. note::
   The data used in this study is currently under review for publication and we have been asked to not discuss some details of the study until its publication. We will expand the level of detail in this exercise, as well as the questions being addressed, upon publication. In the meantime, you should consider this to be a draft of this exercise.

The data used in this tutorial is derived from a Fecal Microbiome Transplant study where children under the age of 18 with gastrointestinal disorders, as measured by the Gastrointestinal Symptom Rating Scale (GSRS), were treated with fecal microbiota transplant. We tracked the change in their microbiome and GSRS score over an eighteen week period by collecting weekly fecal swab samples (collected by swabbing used toilet paper) and less frequent stool samples (collected as whole stool). In the full study, which was a phase 1 clinical trial designed to test safety of the treatment, eighteen individuals received the treatment, and twenty individuals were followed as controls. The controls did not receive the treatment, but were monitored to track normal temporal variation in the gut microbiome. The fecal material that was transplanted during treatment was also sequenced in this study.

This tutorial dataset is a subsample of the data generated for this study. It includes data from five individuals who received treatment and five controls. Between six and sixteen samples are included per individual, including stool and fecal swab samples for each individual, and samples before and after FMT treatment. Five samples of the transplanted fecal material are also included.

These data were sequenced on two Illumina MiSeq sequencing runs. As in the Moving Pictures tutorial, we'll use DADA2 to perform initial quality control and generate our ``FeatureTable[Frequency]`` and ``FeatureData[Sequence]`` objects. However, the DADA2 denoising process is only applicable to a single sequencing run at a time, so we need to run this on a per sequencing run basis and then merge the results. We'll work through this initial step, and then pose several questions that can be answered as an exercise.

Prepare for the analysis
------------------------

Create a directory to work in called ``qiime2-fmt-tutorial`` and change to that directory:

.. command-block::
   :no-exec:

   mkdir qiime2-fmt-tutorial
   cd qiime2-fmt-tutorial

As in the Moving Pictures study, you should begin your analysis by familiarizing yourself with the sample metadata. You can again access the `sample metadata`_ as a Google Spreadsheet. Notice that there are three tabs in this spreadsheet. This first tab (called sample-metadata) contains all of the clinical metadata. While you’re in the sample-metadata tab, you should download this file as a .tsv file by selecting “File > Download as > Tab-separated text”. Name the file ``sample-metadata.tsv`` and save it to the ``qiime2-fmt-tutorial`` directory that you created. (The first two tabs of the spreadsheet include the barcodes that would be used for demultiplexing.)

Alternatively, the following command will download the sample metadata as tab-separated text and save it in the file ``sample-metadata.tsv``.

.. download::
   :url: https://docs.google.com/spreadsheets/d/15kqZlUrIp9FV4U7OSzeCzteuWMtbkaXgYvD_hTZZ9pw/export?gid=0&format=tsv
   :saveas: sample-metadata.tsv

Next, download the *demultiplexed sequences* that we'll use in this analysis. In this tutorial we'll work with a small subset (10%) of the complete sequence data so that the commands will run quickly. To learn how to start a QIIME 2 analysis from raw sequence data, see the :doc:`importing data tutorial <importing>`. We'll need to download two sets of demultiplexed sequences, each corresponding to one of the sequencing runs.

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/fmt/fmt-tutorial-demux-1-10p.qza
   :saveas: fmt-tutorial-demux-1-10p.qza

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/fmt/fmt-tutorial-demux-2-10p.qza
   :saveas: fmt-tutorial-demux-2-10p.qza

Sequence quality control
------------------------

We'll begin by performing quality control on the demultiplexed sequences using `DADA2`_, but this time we'll run the ``denoise`` command on each set of demultiplexed sequences individually. Again, we'll want to start by visualizing sequence quality for some of the samples in each run. When we run ``denoise``, we need to use the same values for ``--p-trunc-len`` and ``--p-trim-left`` for both runs, so when looking at the visualizations that result from these two commands, think about what values would make sense for these parameters for both commands.

.. command-block::

   qiime dada2 plot-qualities \
     --i-demultiplexed-seqs fmt-tutorial-demux-1-10p.qza \
     --p-n 10 \
     --o-visualization demux-qual-plots-1.qzv
   qiime dada2 plot-qualities \
     --i-demultiplexed-seqs fmt-tutorial-demux-2-10p.qza \
     --p-n 10 \
     --o-visualization demux-qual-plots-2.qzv

.. question::
   Based on the plots you see in ``demux-qual-plots-1.qzv`` and ``demux-qual-plots-2.qzv``, what values would you choose for ``--p-trunc-len`` and ``--p-trim-left`` in this case? How does these plots compare to those generated in the :doc:`the moving pictures tutorial <moving-pictures>`?

Here the quality seems relatively low in the first few bases, and seems to decrease again around 130 bases. We'll therefore trim the first 10 bases from each sequence and truncate the sequences at 130 bases. Each of the following commands will take a few minutes to complete.

.. command-block::

   qiime dada2 denoise \
     --p-trim-left 10 \
     --p-trunc-len 130 \
     --i-demultiplexed-seqs fmt-tutorial-demux-1-10p.qza \
     --o-representative-sequences rep-seqs-1.qza \
     --o-table table-1.qza
   qiime dada2 denoise \
     --p-trim-left 10 \
     --p-trunc-len 130 \
     --i-demultiplexed-seqs fmt-tutorial-demux-2-10p.qza \
     --o-representative-sequences rep-seqs-2.qza \
     --o-table table-2.qza

Merging denoised sequence variant data
--------------------------------------

The ``denoise`` command is the last step in this analysis that needs to be run on a per sequencing run basis. We're therefore ready to merge the artifacts generated by those two commands. First we'll merge the two ``FeatureTable[Frequency]`` artifacts, and then we'll merge the two ``FeatureData[Sequence]`` artifacts. This is possible because the feature ids generated in each run of ``denoise`` are directly comparable (in this case, the feature id is the md5 hash of the sequence defining the feature).

.. command-block::

   qiime feature-table merge \
     --i-table1 table-1.qza \
     --i-table2 table-2.qza \
     --o-merged-table table.qza
   qiime feature-table merge-seq-data \
     --i-data1 rep-seqs-1.qza \
     --i-data2 rep-seqs-2.qza \
     --o-merged-data rep-seqs.qza

Next, we'll generate a summary of the merged ``FeatureTable[Frequency]`` artifact.

.. command-block::

   qiime feature-table summarize \
     --i-table table.qza \
     --o-visualization table.qzv

.. question::
   Based on the information in ``table.qzv``, what value will you choose for the ``--p-sampling-depth`` parameter when you run ``qiime diversity core-metrics``?

.. question::
   Generate summaries of the tables for the individual runs of ``qiime dada2 denoise``. How many features were defined in the first run? How many features were defined in the second run? How do these numbers compare to total number of features after merging?

We'll also generate a summary of the merged ``FeatureData[Sequence]`` artifact. You can use this summary to obtain additional information about specific features of interest as you proceed through the analysis.

.. command-block::

   qiime feature-table tabulate-seqs \
     --i-data rep-seqs.qza \
     --o-visualization rep-seqs.qzv

Diversity analysis
------------------

Now that you have ``FeatureTable[Frequency]`` and ``FeatureData[Sequence]`` objects, you're ready to begin exploring the composition of these samples in the context of their metadata. Refer to :doc:`the moving pictures tutorial <moving-pictures>` to derive the specific commands that you'll run.

.. note::
   One limitation in QIIME 2 as of this writing is a lack of paired tests (those are available in QIIME 1 - see ``identify_paired_differences.py``). Some of the questions that we would want to answer for this study, such as do all individuals who receive treatment experience the same change (either an increase or decrease) in community richness before and after treatment, require these types of tests. These are planned for addition to QIIME 2 in the near future, and we will update this tutorial at that time.

Below are some specific questions to answer about this data, grouped into a few categories. Try to collect at least one specific result to support your answer to each question.

1. The personal human microbiome.

   a. Do samples differ in composition by subject-id (i.e., across individual)?
   #. Do samples differ in richness by subject-id?
   #. Do samples differ in evenness by subject-id?

#. Microbiota engraftment.

   a. At approximately what week in the study do microbiome samples in individuals who receive treatment appear most similar to FMT donors in terms of unweighted UniFrac distances? (Hint: See the note above about ``qiime emperor plot``. The *color* and *visibility* tabs are also very important in this Emperor plot.)
   #. At approximately what week in the study do microbiome samples in individuals who receive treatment appear most similar to FMT donors in terms of Bray-Curtis distances?
   #. Is this pattern stronger based on unweighted UniFrac or Bray-Curtis distance? Based on how you know about these metrics, what does this suggest to you about what is changing in the microbiome with fecal microbiota transplant? Use the Jaccard and weighted UniFrac distance Emperor plots to help you refine this idea.

#. Experimental design: Comparing stool and swab sample collection methods.

   a. What feature(s) differ most in abundance between the stool and swab samples? What taxonomy is associated with those feature ids based on their best BLAST hits, and based on the results of Naive Bayes feature classification with the QIIME 2 ``q2-feature-classifier`` plugin?
   #. Is the microbial composition of stool and swab samples significantly different based on either unweighted UniFrac or Bray-Curtis distances between samples (*yes*, *no*, or *not possible to say with the current information*)?
   #. Do the donated fecal material samples appear more similar in composition to the stool or swab samples?
   #. Does community richness differ between stool samples and swab samples? Does community evenness differ between stool samples and swab samples?

#. How many samples were sequenced in each sequencing run? Do you observe any systematic differences in the samples across sequencing runs?


.. _DADA2: https://www.ncbi.nlm.nih.gov/pubmed/27214047
.. _sample metadata: https://docs.google.com/spreadsheets/d/15kqZlUrIp9FV4U7OSzeCzteuWMtbkaXgYvD_hTZZ9pw/edit?usp=sharing
