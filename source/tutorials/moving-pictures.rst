"Moving Pictures" tutorial
==========================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

.. note:: This guide uses QIIME 2-specific terminology, please see the :doc:`glossary <../glossary>` for more details.

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
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

.. tip:: `Keemei`_ is a Google Sheets add-on for validating sample metadata. Validation of sample metadata is important before beginning any analysis. Try installing Keemei following the instructions on its website, and then validate the sample metadata spreadsheet linked above. The spreadsheet also includes a sheet with some invalid data to try out with Keemei.

.. tip:: To learn more about metadata, including how to format your metadata for use with QIIME 2, check out :doc:`the metadata tutorial <metadata>`.

Obtaining and importing data
----------------------------

Download the sequence reads that we'll use in this analysis. In this tutorial we'll work with a small subset of the complete sequence data so that the commands will run quickly.

.. command-block::

   mkdir emp-single-end-sequences

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/emp-single-end-sequences/barcodes.fastq.gz
   :saveas: emp-single-end-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/emp-single-end-sequences/sequences.fastq.gz
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

To demultiplex sequences we need to know which barcode sequence is associated with each sample. This information is contained in the `sample metadata`_ file. You can run the following commands to demultiplex the sequences (the ``demux emp-single`` command refers to the fact that these sequences are barcoded according to the `Earth Microbiome Project`_ protocol, and are single-end reads). The ``demux.qza`` QIIME 2 artifact will contain the demultiplexed sequences. The second output (``demux-details.qza``) presents Golay error correction details, and will not be explored in this tutorial (you can visualize these data using ``qiime metadata tabulate``).

.. command-block::

    qiime demux emp-single \
      --i-seqs emp-single-end-sequences.qza \
      --m-barcodes-file sample-metadata.tsv \
      --m-barcodes-column barcode-sequence \
      --o-per-sample-sequences demux.qza \
      --o-error-correction-details demux-details.qza

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

QIIME supports several phylogenetic diversity metrics, including Faith's Phylogenetic Diversity and weighted and unweighted UniFrac. In addition to counts of features per sample (i.e., the data in the ``FeatureTable[Frequency]`` QIIME 2 artifact), these metrics require a rooted phylogenetic tree relating the features to one another. This information will be stored in a ``Phylogeny[Rooted]`` QIIME 2 artifact. To generate a phylogenetic tree we will use ``align-to-tree-mafft-fasttree`` pipeline from the ``q2-phylogeny`` plugin.

First, the pipeline uses the ``mafft`` program to perform a multiple sequence alignment of the sequences in our ``FeatureData[Sequence]`` to create a ``FeatureData[AlignedSequence]`` QIIME 2 artifact.
Next, the pipeline masks (or filters) the alignment to remove positions that are highly variable. These positions are generally considered to add noise to a resulting phylogenetic tree.
Following that, the pipeline applies FastTree to generate a phylogenetic tree from the masked alignment.
The FastTree program creates an unrooted tree, so in the final step in this section midpoint rooting is applied to place the root of the tree at the midpoint of the longest tip-to-tip distance in the unrooted tree.

.. command-block::

   qiime phylogeny align-to-tree-mafft-fasttree \
     --i-sequences rep-seqs.qza \
     --o-alignment aligned-rep-seqs.qza \
     --o-masked-alignment masked-aligned-rep-seqs.qza \
     --o-tree unrooted-tree.qza \
     --o-rooted-tree rooted-tree.qza


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

An important parameter that needs to be provided to this script is ``--p-sampling-depth``, which is the even sampling (i.e. rarefaction) depth. Because most diversity metrics are sensitive to different sampling depths across different samples, this script will randomly subsample the counts from each sample to the value provided for this parameter. For example, if you provide ``--p-sampling-depth 500``, this step will subsample the counts in each sample without replacement so that each sample in the resulting table has a total count of 500. If the total count for any sample(s) are smaller than this value, those samples will be dropped from the diversity analysis. Choosing this value is tricky. We recommend making your choice by reviewing the information presented in the ``table.qzv`` file that was created above. Choose a value that is as high as possible (so you retain more sequences per sample) while excluding as few samples as possible.

.. question::
   View the ``table.qzv`` QIIME 2 artifact, and in particular the *Interactive Sample Detail* tab in that visualization. What value would you choose to pass for ``--p-sampling-depth``? How many samples will be excluded from your analysis based on this choice? How many total sequences will you be analyzing in the ``core-metrics-phylogenetic`` command?

.. command-block::

   qiime diversity core-metrics-phylogenetic \
     --i-phylogeny rooted-tree.qza \
     --i-table table.qza \
     --p-sampling-depth 1103 \
     --m-metadata-file sample-metadata.tsv \
     --output-dir core-metrics-results

Here we set the ``--p-sampling-depth`` parameter to 1103. This value was chosen based on the number of sequences in the ``L3S313`` sample because it's close to the number of sequences in the next few samples that have higher sequence counts, and because it is considerably higher (relatively) than the number of sequences in the samples that have fewer sequences. This will allow us to retain most of our samples. The three samples that have fewer sequences will be dropped from the ``core-metrics-phylogenetic`` analyses and anything that uses these results. It is worth noting that all three of these samples are "right palm" samples. Losing a disproportionate number of samples from one metadata category is not ideal. However, we are dropping a small enough number of samples here that this felt like the best compromise between total sequences analyzed and number of samples retained.

.. note:: The sampling depth of 1103 was chosen based on the DADA2 feature table summary. If you are using a Deblur feature table rather than a DADA2 feature table, you might want to choose a different even sampling depth. Apply the logic from the previous paragraph to help you choose an even sampling depth.

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

In this data set, no continuous sample metadata columns (e.g., ``days-since-experiment-start``) are correlated with alpha diversity, so we won't test for those associations here. If you're interested in performing those tests (for this data set, or for others), you can use the ``qiime diversity alpha-correlation`` command.

Next we'll analyze sample composition in the context of categorical metadata using PERMANOVA (first described in `Anderson (2001)`_) using the ``beta-group-significance`` command. The following commands will test whether distances between samples within a group, such as samples from the same body site (e.g., gut), are more similar to each other then they are to samples from the other groups (e.g., tongue, left palm, and right palm). If you call this command with the ``--p-pairwise`` parameter, as we'll do here, it will also perform pairwise tests that will allow you to determine which specific pairs of groups (e.g., tongue and gut) differ from one another, if any. This command can be slow to run, especially when passing ``--p-pairwise``, since it is based on permutation tests. So, unlike the previous commands, we'll run ``beta-group-significance`` on specific columns of metadata that we're interested in exploring, rather than all metadata columns to which it is applicable. Here we'll apply this to our unweighted UniFrac distances, using two sample metadata columns, as follows.

.. command-block::

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column body-site \
     --o-visualization core-metrics-results/unweighted-unifrac-body-site-significance.qzv \
     --p-pairwise

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column subject \
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
     --p-custom-axes days-since-experiment-start \
     --o-visualization core-metrics-results/unweighted-unifrac-emperor-days-since-experiment-start.qzv

   qiime emperor plot \
     --i-pcoa core-metrics-results/bray_curtis_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --p-custom-axes days-since-experiment-start \
     --o-visualization core-metrics-results/bray-curtis-emperor-days-since-experiment-start.qzv

.. question::
    Do the Emperor plots support the other beta diversity analyses we've performed here? (Hint: Experiment with coloring points by different metadata.)

.. question::
    What differences do you observe between the unweighted UniFrac and Bray-Curtis PCoA plots?

Alpha rarefaction plotting
--------------------------

In this section we'll explore alpha diversity as a function of sampling depth using the ``qiime diversity alpha-rarefaction`` visualizer. This visualizer computes one or more alpha diversity metrics at multiple sampling depths, in steps between 1 (optionally controlled with ``--p-min-depth``) and the value provided as ``--p-max-depth``. At each sampling depth step, 10 rarefied tables will be generated, and the diversity metrics will be computed for all samples in the tables. The number of iterations (rarefied tables computed at each sampling depth) can be controlled with ``--p-iterations``. Average diversity values will be plotted for each sample at each even sampling depth, and samples can be grouped based on metadata in the resulting visualization if sample metadata is provided with the ``--m-metadata-file`` parameter.

.. command-block::

   qiime diversity alpha-rarefaction \
     --i-table table.qza \
     --i-phylogeny rooted-tree.qza \
     --p-max-depth 4000 \
     --m-metadata-file sample-metadata.tsv \
     --o-visualization alpha-rarefaction.qzv

The visualization will have two plots. The top plot is an alpha rarefaction plot, and is primarily used to determine if the richness of the samples has been fully observed or sequenced. If the lines in the plot appear to "level out" (i.e., approach a slope of zero) at some sampling depth along the x-axis, that suggests that collecting additional sequences beyond that sampling depth would not be likely to result in the observation of additional features. If the lines in a plot don't level out, this may be because the richness of the samples hasn't been fully observed yet (because too few sequences were collected), or it could be an indicator that a lot of sequencing error remains in the data (which is being mistaken for novel diversity).

The bottom plot in this visualization is important when grouping samples by metadata. It illustrates the number of samples that remain in each group when the feature table is rarefied to each sampling depth. If a given sampling depth ``d`` is larger than the total frequency of a sample ``s`` (i.e., the number of sequences that were obtained for sample ``s``), it is not possible to compute the diversity metric for sample ``s`` at sampling depth ``d``. If many of the samples in a group have lower total frequencies than ``d``, the average diversity presented for that group at ``d`` in the top plot will be unreliable because it will have been computed on relatively few samples. When grouping samples by metadata, it is therefore essential to look at the bottom plot to ensure that the data presented in the top plot is reliable.

.. note::
    The value that you provide for ``--p-max-depth`` should be determined by reviewing the "Frequency per sample" information presented in the ``table.qzv`` file that was created above. In general, choosing a value that is somewhere around the median frequency seems to work well, but you may want to increase that value if the lines in the resulting rarefaction plot don't appear to be leveling out, or decrease that value if you seem to be losing many of your samples due to low total frequencies closer to the minimum sampling depth than the maximum sampling depth.

.. question::
    When grouping samples by "body-site" and viewing the alpha rarefaction plot for the "observed_otus" metric, which body sites (if any) appear to exhibit sufficient diversity coverage (i.e., their rarefaction curves level off)? How many sequence variants appear to be present in those body sites?

.. question::
    When grouping samples by "body-site" and viewing the alpha rarefaction plot for the "observed_otus" metric, the line for the "right palm" samples appears to level out at about 40, but then jumps to about 140. What do you think is happening here? (Hint: be sure to look at both the top and bottom plots.)


.. _`moving pics taxonomy`:

Taxonomic analysis
------------------

In the next sections we'll begin to explore the taxonomic composition of the samples, and again relate that to sample metadata. The first step in this process is to assign taxonomy to the sequences in our ``FeatureData[Sequence]`` QIIME 2 artifact. We'll do that using a pre-trained Naive Bayes classifier and the ``q2-feature-classifier`` plugin. This classifier was trained on the Greengenes 13_8 99% OTUs, where the sequences have been trimmed to only include 250 bases from the region of the 16S that was sequenced in this analysis (the V4 region, bound by the 515F/806R primer pair). We'll apply this classifier to our sequences, and we can generate a visualization of the resulting mapping from sequence to taxonomy.

.. note:: Taxonomic classifiers perform best when they are trained based on your specific sample preparation and sequencing parameters, including the primers that were used for amplification and the length of your sequence reads. Therefore in general you should follow the instructions in :doc:`Training feature classifiers with q2-feature-classifier <../tutorials/feature-classifier>` to train your own taxonomic classifiers. We provide some common classifiers on our :doc:`data resources page <../data-resources>`, including Silva-based 16S classifiers, though in the future we may stop providing these in favor of having users train their own classifiers which will be most relevant to their sequence data.


.. download::
   :url: https://data.qiime2.org/2020.2/common/gg-13-8-99-515-806-nb-classifier.qza
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
    Visualize the samples at *Level 2* (which corresponds to the phylum level in this analysis), and then sort the samples by ``body-site``, then by ``subject``, and then by ``days-since-experiment-start``. What are the dominant phyla in each in ``body-site``? Do you observe any consistent change across the two subjects between ``days-since-experiment-start`` ``0`` and the later timepoints?


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
     --p-where "[body-site]='gut'" \
     --o-filtered-table gut-table.qza

ANCOM operates on a ``FeatureTable[Composition]`` QIIME 2 artifact, which is based on frequencies of features on a per-sample basis, but cannot tolerate frequencies of zero. To build the composition artifact, a ``FeatureTable[Frequency]``  artifact must be provided to ``add-pseudocount`` (an imputation method), which will produce the ``FeatureTable[Composition]`` artifact.

.. command-block::

   qiime composition add-pseudocount \
     --i-table gut-table.qza \
     --o-composition-table comp-gut-table.qza

We can then run ANCOM on the ``subject`` column to determine what features differ in abundance across the gut samples of the two subjects.

.. command-block::

   qiime composition ancom \
     --i-table comp-gut-table.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column subject \
     --o-visualization ancom-subject.qzv

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
     --m-metadata-column subject \
     --o-visualization l6-ancom-subject.qzv

.. question::
   Which genera differ in abundance across subject? In which subject is each genus more abundant?


.. _sample metadata: https://data.qiime2.org/2020.2/tutorials/moving-pictures/sample_metadata
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
