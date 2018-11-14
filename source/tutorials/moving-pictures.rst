"Moving Pictures" tutorial
==========================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

In this tutorial you'll use QIIME 2 to perform an analysis of human microbiome samples from two individuals at four body sites at five timepoints, the first of which immediately followed antibiotic usage. A study based on these samples was originally published in `Caporaso et al. (2011)`_. The data used in this tutorial were sequenced on an Illumina HiSeq using the `Earth Microbiome Project`_ hypervariable region 4 (V4) 16S rRNA sequencing protocol.

.. qiime1-users::
   These are the same data that are used in the QIIME 1 `Illumina Overview Tutorial`_.

Before beginning this tutorial, create a new directory and change to that directory.

.. command-block::
   :no-exec:

   mkdir qiime2-moving-pictures-tutorial
   cd qiime2-moving-pictures-tutorial

Sample metadata
---------------

Before starting the analysis, explore the sample metadata to familiarize yourself with the samples used in this study. The `sample metadata`_ is available as a Google Sheet. You can download this file as tab-separated text by selecting ``File`` > ``Download as`` > ``Tab-separated values``. Alternatively, the following command will download the sample metadata as tab-separated text and save it in the file ``sample-metadata.tsv``. This ``sample-metadata.tsv`` file is used throughout the rest of the tutorial.

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

.. tip:: `Keemei`_ is a Google Sheets add-on for validating sample metadata. Validation of sample metadata is important before beginning any analysis. Try installing Keemei following the instructions on its website, and then validate the sample metadata spreadsheet linked above. The spreadsheet also includes a sheet with some invalid data to try out with Keemei.

.. tip:: To learn more about metadata, including how to format your metadata for use with QIIME 2, check out :doc:`the metadata tutorial <metadata>`.

Obtaining and importing data
----------------------------

Download the sequence reads that we'll use in this analysis. In this tutorial we'll work with a small subset of the complete sequence data so that the commands will run quickly.

.. command-block::

   mkdir emp-single-end-sequences

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/moving-pictures/emp-single-end-sequences/barcodes.fastq.gz
   :saveas: emp-single-end-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/moving-pictures/emp-single-end-sequences/sequences.fastq.gz
   :saveas: emp-single-end-sequences/sequences.fastq.gz

All data that is used as input to QIIME 2 is in form of QIIME 2 artifacts, which contain information about the type of data and the source of the data. So, the first thing we need to do is import these sequence data files into a QIIME 2 artifact.

The semantic type of this QIIME 2 artifact is ``EMPSingleEndSequences``. ``EMPSingleEndSequences`` QIIME 2 artifacts contain sequences that are multiplexed, meaning that the sequences have not yet been assigned to samples (hence the inclusion of both ``sequences.fastq.gz`` and ``barcodes.fastq.gz`` files, where the ``barcodes.fastq.gz`` contains the barcode read associated with each sequence in ``sequences.fastq.gz``.) To learn about how to import sequence data in other formats, see the :doc:`importing data tutorial <importing>`.

.. command-block::

   qiime tools import \
     --type EMPSingleEndSequences \
     --input-path emp-single-end-sequences \
     --output-path emp-single-end-sequences.qza

.. tip::
   Links are included to view and download precomputed QIIME 2 artifacts and visualizations created by commands in the documentation. For example, the command above created a single ``emp-single-end-sequences.qza`` file, and a corresponding precomputed file is linked above. You can view precomputed QIIME 2 artifacts and visualizations without needing to install additional software (e.g. QIIME 2).

.. qiime1-users::
   In QIIME 1, we generally suggested performing demultiplexing through QIIME (e.g., with ``split_libraries.py`` or ``split_libraries_fastq.py``) as this step also performed quality control of sequences. We now separate the demultiplexing and quality control steps, so you can begin QIIME 2 with either multiplexed sequences (as we're doing here) or demultiplexed sequences.

.. _`moving pics demux`:

Demultiplexing sequences
------------------------

To demultiplex sequences we need to know which barcode sequence is associated with each sample. This information is contained in the `sample metadata`_ file. You can run the following commands to demultiplex the sequences (the ``demux emp-single`` command refers to the fact that these sequences are barcoded according to the `Earth Microbiome Project`_ protocol, and are single-end reads). The ``demux.qza`` QIIME 2 artifact will contain the demultiplexed sequences.

.. command-block::

    qiime demux emp-single \
      --i-seqs emp-single-end-sequences.qza \
      --m-barcodes-file sample-metadata.tsv \
      --m-barcodes-column BarcodeSequence \
      --o-per-sample-sequences demux.qza

After demultiplexing, it's useful to generate a summary of the demultiplexing results. This allows you to determine how many sequences were obtained per sample, and also to get a summary of the distribution of sequence qualities at each position in your sequence data.

.. command-block::

    qiime demux summarize \
      --i-data demux.qza \
      --o-visualization demux.qzv

.. note::
   All QIIME 2 visualizers (i.e., commands that take a ``--o-visualization`` parameter) will generate a ``.qzv`` file. You can view these files with ``qiime tools view``. We provide the command to view this first visualization, but for the remainder of this tutorial we'll tell you to *view the resulting visualization* after running a visualizer, which means that you should run ``qiime tools view`` on the .qzv file that was generated.

   .. command-block::
      :no-exec:

      qiime tools view demux.qzv

   Alternatively, you can view QIIME 2 artifacts and visualizations at `view.qiime2.org <https://view.qiime2.org>`__ by uploading files or providing URLs. There are also precomputed results that can be viewed or downloaded after each step in the tutorial. These can be used if you're reading the tutorial, but not running the commands yourself.

Sequence quality control and feature table construction
-------------------------------------------------------

QIIME 2 plugins are available for several quality control methods, including `DADA2`_, `Deblur`_, and `basic quality-score-based filtering`_. In this tutorial we present this step using `DADA2`_ and `Deblur`_. These steps are interchangeable, so you can use whichever of these you prefer. The result of both of these methods will be a ``FeatureTable[Frequency]`` QIIME 2 artifact, which contains counts (frequencies) of each unique sequence in each sample in the dataset, and a ``FeatureData[Sequence]`` QIIME 2 artifact, which maps feature identifiers in the ``FeatureTable`` to the sequences they represent.

.. note::
   As you work through one or both of the options in this section, you'll create artifacts with filenames that are specific to the method that you're running (e.g., the feature table that you generate with ``dada2 denoise-single`` will be called ``table-dada2.qza``). After creating these artifacts you'll rename the artifacts from one of the two options to more generic filenames (e.g., ``table.qza``). This process of creating a specific name for an artifact and then renaming it is only done to allow you to choose which of the two options you'd like to use for this step, and then complete the tutorial without paying attention to that choice again. It's important to note that in this step, or any step in QIIME 2, the filenames that you're giving to artifacts or visualizations are not important.

.. qiime1-users::
   The ``FeatureTable[Frequency]`` QIIME 2 artifact is the equivalent of the QIIME 1 OTU or BIOM table, and the ``FeatureData[Sequence]`` QIIME 2 artifact is the equivalent of the QIIME 1 *representative sequences* file. Because the "OTUs" resulting from `DADA2`_ and `Deblur`_ are created by grouping unique sequences, these are the equivalent of 100% OTUs from QIIME 1, and are generally referred to as *sequence variants*. In QIIME 2, these OTUs are higher resolution than the QIIME 1 default of 97% OTUs, and they're higher quality since these quality control steps are better than those implemented in QIIME 1. This should therefore result in more accurate estimates of diversity and taxonomic composition of samples than was achieved with QIIME 1.

Option 1: DADA2
~~~~~~~~~~~~~~~

`DADA2`_ is a pipeline for detecting and correcting (where possible) Illumina amplicon sequence data. As implemented in the ``q2-dada2`` plugin, this quality control process will additionally filter any phiX reads (commonly present in marker gene Illumina sequence data) that are identified in the sequencing data, and will filter chimeric sequences.

The ``dada2 denoise-single`` method requires two parameters that are used in quality filtering: ``--p-trim-left m``, which trims off the first ``m`` bases of each sequence, and ``--p-trunc-len n`` which truncates each sequence at position ``n``. This allows the user to remove low quality regions of the sequences. To determine what values to pass for these two parameters, you should review the *Interactive Quality Plot* tab in the ``demux.qzv`` file that was generated by ``qiime demux summarize`` above.

.. question::
   Based on the plots you see in ``demux.qzv``, what values would you choose for ``--p-trunc-len`` and ``--p-trim-left`` in this case?

In the ``demux.qzv`` quality plots, we see that the quality of the initial bases seems to be high, so we won't trim any bases from the beginning of the sequences. The quality seems to drop off around position 120, so we'll truncate our sequences at 120 bases. This next command may take up to 10 minutes to run, and is the slowest step in this tutorial.

.. command-block::

   qiime dada2 denoise-single \
     --i-demultiplexed-seqs demux.qza \
     --p-trim-left 0 \
     --p-trunc-len 120 \
     --o-representative-sequences rep-seqs-dada2.qza \
     --o-table table-dada2.qza \
     --o-denoising-stats stats-dada2.qza

.. command-block::

   qiime metadata tabulate \
     --m-input-file stats-dada2.qza \
     --o-visualization stats-dada2.qzv

If you'd like to continue the tutorial using this FeatureTable (opposed to the Deblur feature table generated in *Option 2*), run the following commands.

.. command-block::

   mv rep-seqs-dada2.qza rep-seqs.qza
   mv table-dada2.qza table.qza

.. _`moving pictures deblur`:

Option 2: Deblur
~~~~~~~~~~~~~~~~

`Deblur`_ uses sequence error profiles to associate erroneous sequence reads with the true biological sequence from which they are derived, resulting in high quality sequence variant data. This is applied in two steps. First, an initial quality filtering process based on quality scores is applied. This method is an implementation of the quality filtering approach described by `Bokulich et al. (2013)`_.

.. command-block::

   qiime quality-filter q-score \
    --i-demux demux.qza \
    --o-filtered-sequences demux-filtered.qza \
    --o-filter-stats demux-filter-stats.qza

.. note:: In the `Deblur`_ paper, the authors used different quality-filtering parameters than what `they currently recommend after additional analysis <https://qiita.ucsd.edu/static/doc/html/deblur_quality.html>`_. The parameters used here are based on those more recent recommendations.

Next, the Deblur workflow is applied using the ``qiime deblur denoise-16S`` method. This method requires one parameter that is used in quality filtering, ``--p-trim-length n`` which truncates the sequences at position ``n``. In general, the Deblur developers recommend setting this value to a length where the median quality score begins to drop too low. On these data, the quality plots (prior to quality filtering) suggest a reasonable choice is in the 115 to 130 sequence position range. This is a subjective assessment. One situation where you might deviate from that recommendation is when performing a meta-analysis across multiple sequencing runs. In this type of meta-analysis, it is critical that the read lengths be the same for all of the sequencing runs being compared to avoid introducing a study-specific bias. Since we already using a trim length of 120 for ``qiime dada2 denoise-single``, and since 120 is reasonable given the quality plots, we'll pass ``--p-trim-length 120``. This next command may take up to 10 minutes to run.

.. command-block::

   qiime deblur denoise-16S \
     --i-demultiplexed-seqs demux-filtered.qza \
     --p-trim-length 120 \
     --o-representative-sequences rep-seqs-deblur.qza \
     --o-table table-deblur.qza \
     --p-sample-stats \
     --o-stats deblur-stats.qza

.. note:: The two commands used in this section generate QIIME 2 artifacts containing summary statistics. To view those summary statistics, you can visualize them using ``qiime metadata tabulate`` and ``qiime deblur visualize-stats``, respectively:

.. command-block::

   qiime metadata tabulate \
     --m-input-file demux-filter-stats.qza \
     --o-visualization demux-filter-stats.qzv
   qiime deblur visualize-stats \
     --i-deblur-stats deblur-stats.qza \
     --o-visualization deblur-stats.qzv

If you'd like to continue the tutorial using this FeatureTable (opposed to the DADA2 feature table generated in *Option 1*), run the following commands.

.. command-block::
   :no-exec:

   mv rep-seqs-deblur.qza rep-seqs.qza
   mv table-deblur.qza table.qza

FeatureTable and FeatureData summaries
--------------------------------------

After the quality filtering step completes, you'll want to explore the resulting data. You can do this using the following two commands, which will create visual summaries of the data. The ``feature-table summarize`` command will give you information on how many sequences are associated with each sample and with each feature, histograms of those distributions, and some related summary statistics. The ``feature-table tabulate-seqs`` command will provide a mapping of feature IDs to sequences, and provide links to easily BLAST each sequence against the NCBI nt database. The latter visualization will be very useful later in the tutorial, when you want to learn more about specific features that are important in the data set.

.. command-block::

   qiime feature-table summarize \
     --i-table table.qza \
     --o-visualization table.qzv \
     --m-sample-metadata-file sample-metadata.tsv
   qiime feature-table tabulate-seqs \
     --i-data rep-seqs.qza \
     --o-visualization rep-seqs.qzv

Generate a tree for phylogenetic diversity analyses
---------------------------------------------------

QIIME supports several phylogenetic diversity metrics, including Faith's Phylogenetic Diversity and weighted and unweighted UniFrac. In addition to counts of features per sample (i.e., the data in the ``FeatureTable[Frequency]`` QIIME 2 artifact), these metrics require a rooted phylogenetic tree relating the features to one another. This information will be stored in a ``Phylogeny[Rooted]`` QIIME 2 artifact. To generate a phylogenetic tree we will use ``sepp`` from the ``q2-fragment-insertion`` plugin.

The following single command will produce two outputs: 1) `rooted-tree.qza` is the `Phylogeny[Rooted]` and 2) `placements.qza` provides placement distributions for the fragments (you will most likely ignore this output) (Computation might take some 10 minutes):

.. command-block::

   qiime fragment-insertion sepp \
     --i-representative-sequences rep-seqs.qza \
     --o-tree rooted-tree.qza \
     --o-placements insertion-placements.qza --verbose

.. note:: Fragment insertion can fail for fragments that are too remotely related to everything in the reference phylogeny. As a result it may be necessary to filter the feature table to prevent downstream diversity analyses from failing. Please refer to the `q2-fragment-insertion` documentation for step-by-step instructions. 

.. _`moving pics diversity`:

Alpha and beta diversity analysis
---------------------------------

QIIME 2's diversity analyses are available through the ``q2-diversity`` plugin, which supports computing alpha and beta diversity metrics, applying related statistical tests, and generating interactive visualizations. We'll first apply the ``core-metrics-phylogenetic`` method, which rarefies a ``FeatureTable[Frequency]`` to a user-specified depth, computes several alpha and beta diversity metrics, and generates principle coordinates analysis (PCoA) plots using Emperor for each of the beta diversity metrics. The metrics computed by default are:

* Alpha diversity

  * Shannon's diversity index (a quantitative measure of community richness)
  * Observed OTUs (a qualitative measure of community richness)
  * Faith's Phylogenetic Diversity (a qualitiative measure of community richness that incorporates phylogenetic relationships between the features)
  * Evenness (or Pielou's Evenness; a measure of community evenness)

* Beta diversity

  * Jaccard distance (a qualitative measure of community dissimilarity)
  * Bray-Curtis distance (a quantitative measure of community dissimilarity)
  * unweighted UniFrac distance (a qualitative measure of community dissimilarity that incorporates phylogenetic relationships between the features)
  * weighted UniFrac distance (a quantitative measure of community dissimilarity that incorporates phylogenetic relationships between the features)

An important parameter that needs to be provided to this script is ``--p-sampling-depth``, which is the even sampling (i.e. rarefaction) depth. Because most diversity metrics are sensitive to different sampling depths across different samples, this script will randomly subsample the counts from each sample to the value provided for this parameter. For example, if you provide ``--p-sampling-depth 500``, this step will subsample the counts in each sample without replacement so that each sample in the resulting table has a total count of 500. If the total count for any sample(s) are smaller than this value, those samples will be dropped from the diversity analysis. Choosing this value is tricky. We recommend making your choice by reviewing the information presented in the ``table.qzv`` file that was created above and choosing a value that is as high as possible (so you retain more sequences per sample) while excluding as few samples as possible.

.. question::
   View the ``table.qzv`` QIIME 2 artifact, and in particular the *Interactive Sample Detail* tab in that visualization. What value would you choose to pass for ``--p-sampling-depth``? How many samples will be excluded from your analysis based on this choice? How many total sequences will you be analyzing in the ``core-metrics-phylogenetic`` command?

.. command-block::

   qiime diversity core-metrics-phylogenetic \
     --i-phylogeny rooted-tree.qza \
     --i-table table.qza \
     --p-sampling-depth 1109 \
     --m-metadata-file sample-metadata.tsv \
     --output-dir core-metrics-results

Here we set the ``--p-sampling-depth`` parameter to 1109. This value was chosen based on the number of sequences in the ``L3S341`` sample because it's close to the number of sequences in the next few samples that have higher sequence counts, and because it is considerably higher (relatively) than the number of sequences in the one sample that has fewer sequences. This will allow us to retain most of our samples. The one sample that has fewer sequences will be dropped from the ``core-metrics-phylogenetic`` analyses and anything that uses these results.

.. note:: The sampling depth of 1109 was chosen based on the DADA2 feature table summary. If you are using a Deblur feature table rather than a DADA2 feature table, you might want to choose a different even sampling depth. Apply the logic from the previous paragraph to help you choose an even sampling depth.

.. note:: In many Illumina runs you'll observe a few samples that have very low sequence counts. You will typically want to exclude those from the analysis by choosing a larger value for the sampling depth at this stage.

After computing diversity metrics, we can begin to explore the microbial composition of the samples in the context of the sample metadata. This information is present in the `sample metadata`_ file that was downloaded earlier.

We'll first test for associations between categorical metadata columns and alpha diversity data. We'll do that here for the Faith Phylogenetic Diversity (a measure of community richness) and evenness metrics.

.. command-block::

   qiime diversity alpha-group-significance \
     --i-alpha-diversity core-metrics-results/faith_pd_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization core-metrics-results/faith-pd-group-significance.qzv

   qiime diversity alpha-group-significance \
     --i-alpha-diversity core-metrics-results/evenness_vector.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization core-metrics-results/evenness-group-significance.qzv

.. question::
   Which categorical sample metadata columns are most strongly associated with the differences in microbial community **richness**? Are these differences statistically significant?

.. question::
   Which categorical sample metadata columns are most strongly associated with the differences in microbial community **evenness**? Are these differences statistically significant?

In this data set, no continuous sample metadata columns (e.g., ``DaysSinceExperimentStart``) are correlated with alpha diversity, so we won't test for those associations here. If you're interested in performing those tests (for this data set, or for others), you can use the ``qiime diversity alpha-correlation`` command.

Next we'll analyze sample composition in the context of categorical metadata using PERMANOVA (first described in `Anderson (2001)`_) using the ``beta-group-significance`` command. The following commands will test whether distances between samples within a group, such as samples from the same body site (e.g., gut), are more similar to each other then they are to samples from the other groups (e.g., tongue, left palm, and right palm). If you call this command with the ``--p-pairwise`` parameter, as we'll do here, it will also perform pairwise tests that will allow you to determine which specific pairs of groups (e.g., tongue and gut) differ from one another, if any. This command can be slow to run, especially when passing ``--p-pairwise``, since it is based on permutation tests. So, unlike the previous commands, we'll run this on specific columns of metadata that we're interested in exploring, rather than all metadata columns that it's applicable to. Here we'll apply this to our unweighted UniFrac distances, using two sample metadata columns, as follows.

.. command-block::

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column BodySite \
     --o-visualization core-metrics-results/unweighted-unifrac-body-site-significance.qzv \
     --p-pairwise

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column Subject \
     --o-visualization core-metrics-results/unweighted-unifrac-subject-group-significance.qzv \
     --p-pairwise

.. question::
   Are the associations between subjects and differences in microbial composition statistically significant? How about body sites? What specific pairs of body sites are significantly different from each other?

Again, none of the continuous sample metadata that we have for this data set are correlated with sample composition, so we won't test for those associations here. If you're interested in performing those tests, you can use the ``qiime metadata distance-matrix`` in combination with ``qiime diversity mantel`` and ``qiime diversity bioenv`` commands.

Finally, ordination is a popular approach for exploring microbial community composition in the context of sample metadata. We can use the `Emperor`_ tool to explore principal coordinates (PCoA) plots in the context of sample metadata. While our ``core-metrics-phylogenetic`` command did already generate some Emperor plots, we want to pass an optional parameter, ``--p-custom-axes``, which is very useful for exploring time series data. The PCoA results that were used in ``core-metrics-phylogeny`` are also available, making it easy to generate new visualizations with Emperor. We will generate Emperor plots for unweighted UniFrac and Bray-Curtis so that the resulting plot will contain axes for principal coordinate 1, principal coordinate 2, and days since the experiment start. We will use that last axis to explore how these samples changed over time.

.. command-block::

   qiime emperor plot \
     --i-pcoa core-metrics-results/unweighted_unifrac_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-custom-axes DaysSinceExperimentStart \
     --o-visualization core-metrics-results/unweighted-unifrac-emperor-DaysSinceExperimentStart.qzv

   qiime emperor plot \
     --i-pcoa core-metrics-results/bray_curtis_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-custom-axes DaysSinceExperimentStart \
     --o-visualization core-metrics-results/bray-curtis-emperor-DaysSinceExperimentStart.qzv

.. question::
    Do the Emperor plots support the other beta diversity analyses we've performed here? (Hint: Experiment with coloring points by different metadata.)

.. question::
    What differences do you observe between the unweighted UniFrac and Bray-Curtis PCoA plots?


.. _`moving pics taxonomy`:

Taxonomic analysis
------------------

In the next sections we'll begin to explore the taxonomic composition of the samples, and again relate that to sample metadata. The first step in this process is to assign taxonomy to the sequences in our ``FeatureData[Sequence]`` QIIME 2 artifact. We'll do that using a pre-trained Naive Bayes classifier and the ``q2-feature-classifier`` plugin. This classifier was trained on the Greengenes 13_8 99% OTUs, where the sequences have been trimmed to only include 250 bases from the region of the 16S that was sequenced in this analysis (the V4 region, bound by the 515F/806R primer pair). We'll apply this classifier to our sequences, and we can generate a visualization of the resulting mapping from sequence to taxonomy.

.. note:: Taxonomic classifiers perform best when they are trained based on your specific sample preparation and sequencing parameters, including the primers that were used for amplification and the length of your sequence reads. Therefore in general you should follow the instructions in :doc:`Training feature classifiers with q2-feature-classifier <../tutorials/feature-classifier>` to train your own taxonomic classifiers. We provide some common classifiers on our :doc:`data resources page <../data-resources>`, including Silva-based 16S classifiers, though in the future we may stop providing these in favor of having users train their own classifiers which will be most relevant to their sequence data.


.. download::
   :url: https://data.qiime2.org/2018.11/common/gg-13-8-99-515-806-nb-classifier.qza
   :saveas: gg-13-8-99-515-806-nb-classifier.qza

.. command-block::

   qiime feature-classifier classify-sklearn \
     --i-classifier gg-13-8-99-515-806-nb-classifier.qza \
     --i-reads rep-seqs.qza \
     --o-classification taxonomy.qza

   qiime metadata tabulate \
     --m-input-file taxonomy.qza \
     --o-visualization taxonomy.qzv

.. question::
    Recall that our ``rep-seqs.qzv`` visualization allows you to easily BLAST the sequence associated with each feature against the NCBI nt database. Using that visualization and the ``taxonomy.qzv`` visualization created here, compare the taxonomic assignments with the taxonomy of the best BLAST hit for a few features. How similar are the assignments? If they're dissimilar, at what *taxonomic level* do they begin to differ (e.g., species, genus, family, ...)?

Next, we can view the taxonomic composition of our samples with interactive bar plots. Generate those plots with the following command and then open the visualization.

.. command-block::

   qiime taxa barplot \
     --i-table table.qza \
     --i-taxonomy taxonomy.qza \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization taxa-bar-plots.qzv

.. question::
    Visualize the samples at *Level 2* (which corresponds to the phylum level in this analysis), and then sort the samples by BodySite, then by Subject, and then by DaysSinceExperimentStart. What are the dominant phyla in each in BodySite? Do you observe any consistent change across the two subjects between DaysSinceExperimentStart ``0`` and the later timepoints?


.. _`sample classifier`:

Predicting sample metadata values with q2-sample-classifier
===========================================================

.. note:: Documentation for using all plugin actions through the Python API and command line interface is available in the q2-sample-classifier :doc:`reference documentation <../plugins/available/sample-classifier/index>`.

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

.. warning:: Just as with any statistical method, the actions described in this plugin require adequate sample sizes to achieve meaningful results. As a rule of thumb, a minimum of `approximately 50 samples`_ should be provided. Categorical metadata columns that are used as classifier targets should have a minimum of 10 samples per unique value, and continuous metadata columns that are used as regressor targets should not contain many outliers or grossly uneven distributions. Smaller counts will result in inaccurate models, and may result in errors.

This tutorial will demonstrate how to use ``q2-sample-classifier`` to predict sample metadata values. Supervised learning methods predict sample data (e.g., metadata values) as a function of other sample data (e.g., microbiota composition). The predicted targets may be discrete sample classes (for classification problems) or continuous values (for regression problems). Any other data may be used as predictive features, but for the purposes of q2-sample-classifier this will most commonly be microbial sequence variant, operational taxonomic unit (OTU), or taxonomic composition data. However, any features contained in a feature table may be used — for non-microbial data, just `convert your observation tables to biom format`_ and :doc:`import the feature table data into qiime2 <importing>`.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir sample-classifier-tutorial
   cd sample-classifier-tutorial

Predicting categorical sample data
----------------------------------

Supervised learning classifiers predict the categorical metadata classes of unlabeled samples by learning the composition of labeled training samples. For example, we may use a classifier to diagnose or predict disease susceptibility based on stool microbiome composition, or predict sample type as a function of the sequence variants, microbial taxa, or metabolites detected in a sample. In this tutorial, we will use the :doc:`moving pictures tutorial data <moving-pictures>` to train a classifier that predicts the body site from which a sample was collected.

Next, we will train and test a classifier that predicts which body site a sample originated from based on its microbial composition. We will do so using the ``classify-samples`` pipeline, which performs a series of steps under the hood:

1. The input samples are randomly split into a ``training`` set and a ``test`` set. The test set is held out until the end of the pipeline, allowing us to test accuracy on a set of samples that was not used for model training. The fraction of input samples to include in the test set is adjusted with the ``--p-test-size`` parameter.

2. We train the learning model using the training set samples. The model is trained to predict a specific ``target`` value for each sample (contained in a metadata column) based on the feature data associated with that sample. A range of different estimators can be selected using the ``estimator`` parameter; more details on individual estimators can be found in the `scikit-learn documentation`_ (not sure which to choose? See the `estimator selection flowchart`_).

3. K-fold `cross-validation`_ is performed during automatic feature selection and parameter optimization steps to tune the model. Five-fold cross-validation is performed by default, and this value can be adjusted using the ``--p-cv`` parameter.

4. The trained model is used to predict the target values for each test sample, based on the feature data associated with that sample.

5. Model accuracy is calculated by comparing each test sample's predicted value to the true value for that sample.

.. image:: images/sample-classifier.png

:ref:`Figure key<key>`


.. command-block::

   qiime sample-classifier classify-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column BodySite \
     --p-optimize-feature-selection \
     --p-parameter-tuning \
     --p-estimator RandomForestClassifier \
     --p-n-estimators 20 \
     --output-dir moving-pictures-classifier


This pipeline produces several outputs. First let's check out ``accuracy_results.qzv``, which presents classification accuracy results in the form of a confusion matrix. This matrix indicates how frequently a sample is classified with the correct class vs. all other classes. The confusion matrix is displayed at the top of the visualization in the form of a heatmap, and below that as a table containing overall accuracy (the fraction of times that test samples are assigned the correct class).

.. question::
   What other metadata can we predict with ``classify-samples``? Take a look at the metadata columns in the ``sample-metadata`` and try some other categorical columns. Not all metadata can be easily learned by the classifier!

This pipeline also reports the actual predictions made for each test sample in the ``predictions.qza`` output. This is a ``SampleData[ClassifierPredictions]`` artifact, which is viewable as metadata. So we can take a peak with ``metadata tabulate``:

.. command-block::

   qiime metadata tabulate \
     --m-input-file moving-pictures-classifier/predictions.qza \
     --o-visualization moving-pictures-classifier/predictions.qzv


Another really useful output of supervised learning methods is *feature selection*, i.e., they report which features (e.g., ASVs or taxa) are most predictive. A list of all features, and their relative importances (or feature weights or model coefficients, depending on the learning model used), will be reported in ``feature_importance.qza``. Features with higher importance scores were more useful for distinguishing classes. Feature importance scores are assigned directly by the scikit-learn learning estimator that was used; more details on individual estimators and their importance scores should refer to the `scikit-learn documentation`_. Note that some estimators — notably K-nearest neighbors models — do not report feature importance scores, so this output will be meaningless if you are using such an estimator. Feature importances are of the semantic type ``FeatureData[Importance]``, and can be interpreted as (feature) metadata so we can take a look at these feature importances (and/or :ref:`merge with other feature metadata <exploring feature metadata>`) using ``metadata tabulate``:

.. command-block::

   qiime metadata tabulate \
     --m-input-file moving-pictures-classifier/feature_importance.qza \
     --o-visualization moving-pictures-classifier/feature_importance.qzv


If ``--p-optimize-feature-selection`` is enabled, only the selected features (i.e., the most important features, which maximize model accuracy, as determined using `recursive feature elimination`_) will be reported in this artifact, and all other results (e.g., model accuracy and predictions) that are output use the final, optimized model that utilizes this reduced feature set. This allows us to not only see which features are most important (and hence used by the model), but also use that information to filter out uninformative features from our feature table for other downstream analyses outside of q2-sample-classifier:

.. command-block::

   qiime feature-table filter-features \
     --i-table table.qza \
     --m-metadata-file moving-pictures-classifier/feature_importance.qza \
     --o-filtered-table moving-pictures-classifier/important-feature-table.qza


This pipeline also produces a visualization containing a summary of the model parameters used by the supervised learning estimator in ``model_summary.qzv``. If ``--p-optimize-feature-selection`` is enabled, the visualization will also display a `recursive feature elimination`_ plot, which illustrates how model accuracy changes as a function of feature count. The combination of features that maximize accuracy are automatically selected for the final model, which is used for sample prediction results that are displayed in the other outputs.

.. question::
   What happens when feature optimization is disabled with the option ``--p-no-optimize-feature-selection``? How does this impact classification accuracy?

Finally, the trained classification model is saved for convenient re-use in the ``sample_estimator.qza`` artifact! This allows us to predict metadata values for additional samples. For example, imagine we just received a shipment of new samples and wanted to use our pre-trained Body Site classifier to figure out what type of samples these new samples are. For the sake of convenience in this example, we will just pretend we have new samples and predict the values of the same samples that we used to train the model but **NEVER do this in practice** because:

.. warning:: Testing a supervised learning model on the same samples used to train the model will give unrealistic estimates of performance! 🦄


.. command-block::

   qiime sample-classifier predict-classification \
     --i-table table.qza \
     --i-sample-estimator moving-pictures-classifier/sample_estimator.qza \
     --o-predictions moving-pictures-classifier/new_predictions.qza

We can view these ``new_predictions.qza`` using ``metadata tabulate``, as described above... or if these aren't actually "unknown" samples we can re-test model accuracy using this new batch of samples:

.. command-block::

   qiime sample-classifier confusion-matrix \
     --i-predictions moving-pictures-classifier/new_predictions.qza \
     --m-truth-file sample-metadata.tsv \
     --m-truth-column BodySite \
     --o-visualization moving-pictures-classifier/new_confusion_matrix.qzv


Pretty cool! Accuracy should be inordinately high in these results because we ignored the warning above about testing on our training data, giving you a pretty good idea why you should follow the directions on the box! 😑

.. note:: The model we trained here is a toy example containing very few samples from a single study and will probably not be useful for predicting other unknown samples. But if you have samples from one of these body sites, it could be a fun exercise to give it a spin!

.. question::
   Try to figure out what the ``--p-parameter-tuning`` parameter does. What happens when it is disabled with the option ``--p-no-parameter-tuning``? How does this impact classification accuracy?

.. question::
   Many different classifiers can be trained via the ``--p-estimator`` parameter in ``classify-samples``. Try some of the other classifiers. How do these methods compare?

.. question::
   Sequence variants are not the only feature data that can be used to train a classifier or regressor. Taxonomic composition is another feature type that can be easily created using the tutorial data provided in QIIME2. Try to figure out how this works (hint: you will need to assign taxonomy, as described in the :doc:`moving pictures tutorial <moving-pictures>`, and :doc:`collapse taxonomy <../plugins/available/taxa/collapse/>` to create a new feature table). Try using feature tables collapsed to different taxonomic levels. How does taxonomic specificity (e.g., species-level is more specific than phylum-level) impact classifier performance?

.. question::
   The ``--p-n-estimators`` parameter adjusts the number of trees grown by ensemble estimators, such as random forest classifiers (this parameter will have no effect on non-ensemble methods), which increases classifier accuracy up to a certain point, but at the cost of increased computation time. Try the same command above with different numbers of estimators, e.g., 10, 50, 100, 250, and 500 estimators. How does this impact the overall accuracy of predictions? Are more trees worth the time?

.. _`ancom`:

Differential abundance testing with ANCOM
-----------------------------------------

ANCOM can be applied to identify features that are differentially abundant (i.e. present in different abundances) across sample groups. As with any bioinformatics method, you should be aware of the assumptions and limitations of ANCOM before using it. We recommend reviewing the `ANCOM paper`_ before using this method.

.. note::
   Differential abundance testing in microbiome analysis is an active area of research. There are two QIIME 2 plugins that can be used for this: ``q2-gneiss`` and ``q2-composition``. This section uses ``q2-composition``, but there is :doc:`another tutorial which uses gneiss <gneiss>` on a different dataset if you are interested in learning more.

ANCOM is implemented in the ``q2-composition`` plugin. ANCOM assumes that few (less than about 25%) of the features are changing between groups. If you expect that more features are changing between your groups, you should not use ANCOM as it will be more error-prone (an increase in both Type I and Type II errors is possible). Because we expect a lot of features to change in abundance across body sites, in this tutorial we'll filter our full feature table to only contain gut samples. We'll then apply ANCOM to determine which, if any, sequence variants and genera are differentially abundant across the gut samples of our two subjects.

We'll start by creating a feature table that contains only the gut samples. (To learn more about filtering, see the :doc:`Filtering Data <filtering>` tutorial.)

.. command-block::

   qiime feature-table filter-samples \
     --i-table table.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-where "BodySite='gut'" \
     --o-filtered-table gut-table.qza

ANCOM operates on a ``FeatureTable[Composition]`` QIIME 2 artifact, which is based on frequencies of features on a per-sample basis, but cannot tolerate frequencies of zero. To build the composition artifact, a ``FeatureTable[Frequency]``  artifact must be provided to ``add-pseudocount`` (an imputation method), which will produce the ``FeatureTable[Composition]`` artifact.

.. command-block::

   qiime composition add-pseudocount \
     --i-table gut-table.qza \
     --o-composition-table comp-gut-table.qza

We can then run ANCOM on the ``Subject`` column to determine what features differ in abundance across the gut samples of the two subjects.

.. command-block::

   qiime composition ancom \
     --i-table comp-gut-table.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column Subject \
     --o-visualization ancom-Subject.qzv

.. question::
   Which sequence variants differ in abundance across Subject? In which subject is each sequence variant more abundant? What are the taxonomies of some of these sequence variants? (To answer the last question you'll need to refer to another visualization that was generated in this tutorial.)

We're also often interested in performing a differential abundance test at a specific taxonomic level. To do this, we can collapse the features in our ``FeatureTable[Frequency]`` at the taxonomic level of interest, and then re-run the above steps. In this tutorial, we collapse our feature table at the genus level (i.e. level 6 of the Greengenes taxonomy).

.. command-block::

   qiime taxa collapse \
     --i-table gut-table.qza \
     --i-taxonomy taxonomy.qza \
     --p-level 6 \
     --o-collapsed-table gut-table-l6.qza

   qiime composition add-pseudocount \
     --i-table gut-table-l6.qza \
     --o-composition-table comp-gut-table-l6.qza

   qiime composition ancom \
     --i-table comp-gut-table-l6.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column Subject \
     --o-visualization l6-ancom-Subject.qzv

.. question::
   Which genera differ in abundance across Subject? In which subject is each genus more abundant?


.. _sample metadata: https://data.qiime2.org/2018.11/tutorials/moving-pictures/sample_metadata
.. _Keemei: https://keemei.qiime2.org
.. _DADA2: https://www.ncbi.nlm.nih.gov/pubmed/27214047
.. _Illumina Overview Tutorial: http://nbviewer.jupyter.org/github/biocore/qiime/blob/1.9.1/examples/ipynb/illumina_overview_tutorial.ipynb
.. _Caporaso et al. (2011): https://www.ncbi.nlm.nih.gov/pubmed/21624126
.. _Earth Microbiome Project: http://earthmicrobiome.org
.. _Clarke and Ainsworth (1993): http://www.int-res.com/articles/meps/92/m092p205.pdf
.. _PERMANOVA: http://onlinelibrary.wiley.com/doi/10.1111/j.1442-9993.2001.01070.pp.x/full
.. _Anderson (2001): http://onlinelibrary.wiley.com/doi/10.1111/j.1442-9993.2001.01070.pp.x/full
.. _Emperor: http://emperor.microbio.me
.. _Bergmann et al. (2011): https://www.ncbi.nlm.nih.gov/pubmed/22267877
.. _Mandal et al. (2015): https://www.ncbi.nlm.nih.gov/pubmed/26028277
.. _Deblur: http://msystems.asm.org/content/2/2/e00191-16
.. _basic quality-score-based filtering: http://www.nature.com/nmeth/journal/v10/n1/abs/nmeth.2276.html
.. _Bokulich et al. (2013): http://www.nature.com/nmeth/journal/v10/n1/abs/nmeth.2276.html
.. _ANCOM paper: https://www.ncbi.nlm.nih.gov/pubmed/26028277
