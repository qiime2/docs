Parkinson's Mouse Tutorial
--------------------------

This tutorial will demonstrate a "typical" QIIME 2 analysis of 16S rRNA gene amplicon data, using a set of fecal samples from `humanized`_ mice. The original study, `Sampson et al, 2016`_, was designed to determine whether the fecal microbiome contributed to the development of Parkinson's Disease (PD). Several observation studies showed a difference in the microbiome between PD patients and controls, although the organisms identified across studies were not consistent. However, this was sufficient evidence to suggest that there might be a relationship between PD and the fecal microbiome.

To determine whether that relationship was incidental or actually disease associated, a second study was needed. A human cohort study was not feasible; the disease only affects about 1% of the population over 60 years old, PD takes a long time to develop and to be diagnosed, and it would be difficult to determine when to collect the samples. Therefore, a gnotobiotic mouse study was utilized to evaluate the role of the microbiome in the development of PD symptoms. Feces were collected from six donors with Parkinson's disease and six age- and sex-matched neurologically health controls, and then transplanted into mice who were either predisposed to developing Parkinson's disease due to a mutation ("aSyn") or resistant wild type mice ("BDF1"). Mice from different donors were kept in separate cages, but mice from different genetic backgrounds were co-housed. The mice were followed for 7 weeks to see if they developed symptoms of Parkinson's disease.

We'll look a subset of data from two human donors (one healthy and one with PD) whose samples were each transplanted into three separate cages of mice from the susceptible genotype. For this tutorial, a subset of the metadata has been prepared, and the sequences have been subsampled to approximately 5000 sequences per sample to allow the tutorial to run in a short time. The sequences for the full study are accessible at EBI with accession `PRJEB17694`_; processed tables from the full study can be downloaded from the `Qiita`_  database from study 10483.

Hypothesis
==========

This tutorial will explore the hypothesis that the genetic background of a humanized mouse influences the microbial community. However, we'll also need to consider other confounders which might drive the shape of the microbiome instead of the mouse genotype.

.. end L2 Hypothesis

Set up
======

This tutorial assumes that you have QIIME 2 installed according to the :doc:`installation instructions <../install/index>`.

Before running the tutorial, you will need to make a directory for the tutorial data and navigate into that directory.

.. command-block::
   :no-exec:

   mkdir ./mouse_tutorial
   cd ./mouse_tutorial

.. end L2 Set up

Metadata
========

Before starting any analysis, it's important to be familiar with the metadata. In this study, the metadata file contains 7 columns.

+-------------------------+--------------------+-----------------+------------------+
| variable                | description        | data type       | values           |
+=========================+====================+=================+==================+
| sample-id               | unique sample      | —               | unique for each  |
|                         | identifier         |                 | sample           |
+-------------------------+--------------------+-----------------+------------------+
| mouse_id                | the unique         | categorical     | ``435``;         |
|                         | identifier for     |                 | ``437``;         |
|                         | each mouse         |                 | ``456``;         |
|                         |                    |                 | ``457``;         |
|                         |                    |                 | ``468``;         |
|                         |                    |                 | ``469``;         |
|                         |                    |                 | ``536``;         |
|                         |                    |                 | ``537``;         |
|                         |                    |                 | ``538``;         |
|                         |                    |                 | ``539``;         |
|                         |                    |                 | ``546``;         |
|                         |                    |                 | ``547``          |
+-------------------------+--------------------+-----------------+------------------+
| genotype                | the genetic        | categorical     | ``wild_type``;   |
|                         | background of      |                 | ``susceptible``  |
|                         | the mouse. The     |                 |                  |
|                         | Thy1-aSyn          |                 |                  |
|                         | (``susceptible``)  |                 |                  |
|                         | mice are           |                 |                  |
|                         | genetically        |                 |                  |
|                         | predisposed to     |                 |                  |
|                         | disease;           |                 |                  |
|                         | ``wild_type``      |                 |                  |
|                         | from the BDF1      |                 |                  |
|                         | background do      |                 |                  |
|                         | not have any       |                 |                  |
|                         | additional risk    |                 |                  |
+-------------------------+--------------------+-----------------+------------------+
| cage_id                 | the unique         | categorical     | ``C31``;         |
|                         | identifier for     |                 | ``C35``;         |
|                         | each cage of       |                 | ``C42``;         |
|                         | mice               |                 | ``C43``;         |
|                         |                    |                 | ``C44``;         |
|                         |                    |                 | ``C49``          |
+-------------------------+--------------------+-----------------+------------------+
| donor                   | A unique           | categorical     | ``hc_1``         |
|                         | identifier for     |                 | ``pd_1``         |
|                         | the human who      |                 |                  |
|                         | donated the        |                 |                  |
|                         | feces              |                 |                  |
+-------------------------+--------------------+-----------------+------------------+
| donor_status            | whether the        | categorical     | ``Healthy``;     |
|                         | donor has          |                 | ``PD``           |
|                         | Parkinson's        |                 |                  |
|                         | disease or not     |                 |                  |
|                         | (Donor             |                 |                  |
|                         | ``pd_1`` had       |                 |                  |
|                         | Parkinson's        |                 |                  |
|                         | disease;           |                 |                  |
|                         | ``hc_1``           |                 |                  |
|                         | was                |                 |                  |
|                         | neurologically     |                 |                  |
|                         | healthy)           |                 |                  |
+-------------------------+--------------------+-----------------+------------------+
| days_post_transplant    | the number of      | numeric         | 7, 14, 21, 49    |
|                         | days after the     |                 |                  |
|                         | mice were          |                 |                  |
|                         | humanized          |                 |                  |
+-------------------------+--------------------+-----------------+------------------+

Even though the mouse ID looks like a number, we will specify that it is categorical using the ``#q2_type`` directive.

The metadata is available as a `Google Sheet`_, or you can download it directly and save it as a TSV (tab-separated values) file.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/sample_metadata.tsv
   :saveas: metadata.tsv

The sample metadata will be used throughout the tutorial. Let's run our first QIIME 2 command, to summarize and explore the metadata.

.. command-block::

   qiime metadata tabulate \
     --m-input-file metadata.tsv \
     --o-visualization metadata.qzv

.. end L2 Metadata

Importing data into QIIME 2
===========================

In QIIME 2, all data is structured as an Artifact of a specific semantic type. Artifacts contain the data as well as information about the data, including a record of the original data and the tools used to process it. This allows for better tracking of how you actually got to where you are in your analysis. You can learn more about common QIIME 2 Artifacts and semantic types :doc:`here <../semantic-types/>`.

Our samples were amplified using the `EMP 515f-806r`_ primers and sequenced on an Illumina MiSeq with a 2x150bp kit. The hypervariable region covered by the primers we used is 290bp long, so with 150bp reads our sequences will be slightly too short to be able to do paired-end analysis downstream. Therefore, we're going to work with single-end sequences. We will work with a version of the samples which have already been demultiplexed, for example, by the sequencing center. If you need to demultiplex your sequences, the :doc:`Moving Pictures tutorial <moving-pictures>` describes how to demultiplex sequences if they were sequenced using the Earth Microbiome Project protocol.

We will import the sequences as ``SampleData[SequencesWithQuality]``, which is the demultiplexed single-end sequence format. If we wanted to import paired-sequences, we would specify the semantic type ``SampleData[PairedEndSequencesWithQuality]``. We will import the sequences using the sample :ref:`manifest format <manifest file>`, a versatile way to import demultiplexed data in QIIME 2. We create a tab-separated sample manifest file that maps the sample name we want to use in QIIME 2 to the path of the sequence file. The benefit is that the demultiplexed sequence files can be named anything you want; there are not fixed assumptions about the conventions, and the file names do not dictate the final name. When QIIME 2 reads the file, it ignores any line prefixed with the ``#`` symbol. The first line that doesn't contain a ``#`` is the header line and must be ``sample-id<TAB>absolute-filepath``. The sample order after the header line does not matter. Read more about importing data into QIIME 2 artifacts :doc:`here <importing>` and more about sample metadata formatting requirements :doc:`here <metadata/>`.

Let's start by downloading the manifest and corresponding sequences.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/manifest
   :saveas: manifest.tsv

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/demultiplexed_seqs.zip
   :saveas: demultiplexed_seqs.zip

You'll need to unzip sequence archive you just downloaded:

.. command-block::

   unzip demultiplexed_seqs.zip

You can use the ``head`` command to check the first few lines of the sample manifest.

.. command-block::
   :stdout:

   head manifest.tsv

When using this manifest format, a sample name can only appear in one line and can only map to one sequencing file per column (one column for single-end, two columns for paired-end). The **absolute-filepath** for each sample must be an `absolute path`_, which specifies the "complete" location of the file. We do that here using the ``$PWD`` variable, which expands the current directory in absolute terms.

We'll use the manifest to import our data.

.. command-block::

   qiime tools import \
     --type "SampleData[SequencesWithQuality]" \
     --input-format SingleEndFastqManifestPhred33V2 \
     --input-path ./manifest.tsv \
     --output-path ./demux_seqs.qza

Let's check the sequences and the sequencing depth of the samples using the ``qiime demux summarize`` command. It provides information about the number of sequences in each sample, as well as the quality of the sequences.

Before running the command, let's review the help documentation to make sure we understand the arguments for the command.

.. command-block::

   qiime demux summarize --help

Based on the documentation, we should specify the file (Artifact) with the demultiplexed sequences for the ``--i-data`` argument, since this expects data of semantic type ``SampleData[SequencesWithQuality]``. We'll specify the location we want to save the visualization to by specifying the output path to ``--o-visualization``.

The help documentation is a good reference for any command, and the first place to look if you're getting errors, especially errors about parameters.

.. command-block::

   qiime demux summarize \
     --i-data ./demux_seqs.qza \
     --o-visualization ./demux_seqs.qzv

.. question::

   1. After demultiplexing, which sample has the lowest sequencing depth?
   2. What is the median sequence length?
   3. What is the median quality score at position 125?
   4. If you are working on this tutorial alongside someone else, why does your plot look slightly different from your neighbors? If you aren't working alongside someone else, try running this command a few times and compare the results.


.. checkpoint::

   What are good positions to consider trimming and/or truncating at?

.. lowest sequencing depth: 4237 seqs, recip.460.WT.HC3.D14
.. median length: 150 nt
.. median qual score at 125: 38

.. end of L2 Importing data into QIIME 2

Sequence quality control and feature table
==========================================

There are several ways to construct a feature table in QIIME 2. The first major choice to make is to work with Operational Taxonomic Units (OTUs) or Absolute Sequence Variants (ASVs). OTUs have been widely used in microbiome research since the mid 2010s, and assign sequences to clusters either based on a reference database or de novo assignment. QIIME 2 offers clustering through :doc:`q2-vsearch<otu-clustering>` and `q2-dbOTU`_ plug-ins, currently.

ASVs are a more recent development and provide better resolution in features than traditional OTU-based methods. ASVs can separate features based on differences of a single nucleotide in sequences of 400 bp or more, a resolution not possibly even with 99% identity OTU clustering. QIIME 2 currently offers denoising via `DADA2`_ (``q2-dada2``) and `Deblur`_ (``q2-deblur``). The major differences in the algorithms and motivation for denoising are nicely described in `Nearing et al, 2018`_.

It is worth noting in either case that denoising to ASVs and clustering to OTUs are separate, but parallel steps. A choice should be made for a single pathway: either denoising or OTU based clustering; it is not recommended to combine the steps.

In this tutorial, we'll denoise with DADA2 (using single-end sequences). Please see the :doc:`Atacama Soil tutorial <atacama-soils>` for an example of using DADA2 on paired-end sequences. For those interested in using Deblur, you can refer to the :doc:`Moving Pictures tutorial  <moving-pictures>` and :doc:`Alternative methods of read joining <read-joining>` tutorial for running Deblur on single- and paired-end sequences, respectively.

The ``qiime dada2 denoise-single`` method requires us to set the ``--p-trunc-len`` parameter. This controls the length of the sequences and should be selected based on a drop in quality scores. In our dataset, the quality scores are relatively evenly distributed along the sequencing run, so we'll use the full 150 bp sequences. However, the selection of the trim length is a relatively subjective measurement and relies on the decision making capacity of the analyst.

.. command-block::

   qiime dada2 denoise-single \
     --i-demultiplexed-seqs ./demux_seqs.qza \
     --p-trunc-len 150 \
     --o-table ./dada2_table.qza \
     --o-representative-sequences ./dada2_rep_set.qza \
     --o-denoising-stats ./dada2_stats.qza

We can also review the denoising statistics using the ``qiime metadata tabulate`` command.

.. command-block::

    qiime metadata tabulate \
      --m-input-file ./dada2_stats.qza  \
      --o-visualization ./dada2_stats.qzv

Feature table summary
+++++++++++++++++++++

After we finish denoising the data, we can check the results by looking at the summary of the feature table. This will provide us with the counts associated with each sequence and each feature, as well as other useful plots and metrics.

.. command-block::

   qiime feature-table summarize \
     --i-table ./dada2_table.qza \
     --m-sample-metadata-file ./metadata.tsv \
     --o-visualization ./dada2_table.qzv

.. question::

   1. How many total features remain after denoising?
   2. Which sample has the highest total count of features? How many sequences did that sample have prior to DADA2 denoising?
   3. How many samples have fewer than 4250 total features?
   4. Which features are observed in at least 47 samples?
   5. Which sample has the fewest features? How many does it have?

   If you open the denoising summary, can you find the step where the sample with the fewest sequences fails?

.. After denoising: 287 features
.. Most sequences: recip.539.ASO.PD4.D14, 4996
.. With 4250 seqs/sample, we retain 26 of 48 samples => 22 samples remain
.. 3 features are found in 47 samples: 04c8be5a3a6ba2d70446812e99318905, ea2b0e4a93c24c6c3661cbe347f93b74, 1ad289cd8f44e109fd95de0382c5b252
.. Sample recip.460.WT.HC3.D49 has the lowest final depth with 347 sequences
.. the sample fails in the denoising stage

.. end of L2 Sequence quality control and feature table

Generating a phylogenetic tree for diversity analysis
=====================================================

QIIME 2 analysis allows the use of phylogenetic trees for diversity metrics such as Faith's Phylogenetic Diversity and UniFrac distance as well as feature-based analyses in Gneiss. The tree provides an inherent structure to the data, allowing us to consider an evolutionary relationship between organisms.

QIIME 2 offers several ways to construct a phylogenetic tree. For this tutorial, we're going to create a fragment insertion tree using the ``q2-fragment-insertion`` plugin. The authors of the fragment insertion plugin suggest that it can outperform traditional alignment based methods based on short Illumina reads by alignment against a reference tree built out of larger sequences. Our command, ``qiime fragment-insertion sepp`` will use the representative sequences (a ``FeatureData[Sequence]`` artifact) we generated during denoising to create a phylogenetic tree where the sequences have been inserted into the greengenes 13_8 99% identity reference tree backbone.

First, we will download the reference database:

.. download::
   :url: https://data.qiime2.org/2020.2/common/sepp-refs-gg-13-8.qza
   :saveas: sepp-refs-gg-13-8.qza

.. note::
   This command is resource intensive - if your computation environment supports it, we suggest including an appropriately-set ``--p-threads`` parameter.

.. command-block::

   qiime fragment-insertion sepp \
     --i-representative-sequences ./dada2_rep_set.qza \
     --i-reference-database sepp-refs-gg-13-8.qza \
     --o-tree ./tree.qza \
     --o-placements ./tree_placements.qza \
     --p-threads 1  # update to a higher number if you can

.. end L2 Generating a phylogenetic tree for diversity analysis

Alpha Rarefaction and Selecting a Rarefaction Depth
===================================================

We now have a feature table (observation matrix) of ASVs in each sample, and a phylogenetic tree representing those ASVs, so are almost ready to perform various analyses of microbial diversity. However, first we must normalize our data to account for uneven sequencing depth between samples.

Although sequencing depth in a microbiome sample does not directly relate to the original biomass in a community, the relative sequencing depth has a large impact on observed communities (`Weiss et al, 2017`_). Therefore, for most diversity metrics, a normalization approach is needed.

Current best practices suggest the use of rarefaction, a normalization via sub-sampling without replacement. Rarefaction occurs in two steps: first, samples which are below the rarefaction depth are filtered out of the feature table. Then, all remaining samples are subsampled without replacement to get to the specified sequencing depth. It's both important and sometimes challenging to select a rarefaction depth for diversity analyses. Several strategies exist to figure out an appropriate rarefaction depth - we will primarily consider alpha rarefaction in this tutorial, because it is a data-driven way to approach the problem.

We'll use ``qiime diversity alpha-rarefaction`` to subsample the ASV table at different depths (between ``--p-min-depth`` and
``--p-max-depth``) and calculate the alpha diversity using one or more metrics (``--p-metrics``). When we checked the feature table, we found that the sample with the fewest sequences in the denoised table has 85 features and that the sample with the most has 4996 features. We want to set a maximum depth close to the maximum number of sequences. We also know that if we look at a sequencing depth around 4250 sequences per sample, we'll be looking at information from 22 samples. So, let's set this as our maximum sequencing depth.

At each sampling depth, 10 rarefied tables are usually calculated to provide an error estimate, although this can be adjusted using the ``--p-iterations`` parameter. We can check and see if there is a relationship between the alpha diversity and metadata by specifying the metadata file for the ``--m-metadata-file`` parameter.

.. command-block::

   qiime diversity alpha-rarefaction \
     --i-table ./dada2_table.qza \
     --m-metadata-file ./metadata.tsv \
     --o-visualization ./alpha_rarefaction_curves.qzv \
     --p-min-depth 10 \
     --p-max-depth 4250

The visualization file will display two plots. The upper plot will display the alpha diversity (observed OTUs or shannon) as a function of the sampling depth. This is used to determine whether the richness or evenness has saturated based on the sampling depth. The rarefaction curve should “level out” as you approach the maximum sampling depth. Failure to do so, especially with a diversity-only metric such as observed OTUs or Faith's PD diversity, may indicate that the richness in the samples has not been fully saturated.

The second plot shows the number of samples in each metadata category group at each sampling depth. This is useful to determine the sampling depth where samples are lost, and whether this may be biased by metadata column group values. Remember that rarefaction is a two-step process and samples that do not meet the rarefaction depth are filtered out of the table. We can use the curves to look at the number of samples by different metadata columns.

If you're still unsure of the rarefaction depth, you can also use the sample summary to look at which samples are lost by supplying sample metadata to the feature table summary.

.. question::

   Start by opening the alpha rarefaction visualization.

   1. Are all metadata columns represented in the visualization? If not, which columns were excluded and why?
   2. Which metric shows saturation and stabilization of the diversity?
   3. Which mouse genetic background has higher diversity, based on the curve? Which has shallower sampling depth?

   Now, let's check the feature table summary.

   4. What percentage of samples are lost if we set the rarefaction depth to 2500 sequences per sample?
   5. Which mice did the missing samples come from?

.. 1. We can't look at the days since transplant (this is a numeric column)
.. 2. shannon. Always shannon. Shannon is a good justification for rarefaction. Just ignore the observed ASVs behind the curtain
.. 3. susceptible has higher diversity, wild type had a shallower sequencing depth
.. 4. we lose 8% of samples (4 samples).
.. 5. The samples come from mouse 457, 469, 537, and 538.

After we've looked through the data, we need to select a rarefaction depth. In general, selecting a rarefaction depth is a subjective process that requires that analyst's discretion. Selecting a rarefaction depth is an exercise in minimizing sequence loss while maximizing the sequences retained for diversity analysis. For high-biomass samples (fecal, oral, etc), a general best estimate is a rarefaction depth of no less than 1000 sequences per sample. In low biomass samples where sequencing is shallower, a lower rarefaction depth may be selected although it's important to keep in mind that the diversity measurements on these samples will be quite noisy and the overall quality will be low.

.. checkpoint::

   *Based on the current rarefaction curve and sample summary, what sequencing depth would you pick? Why?*

   In this case, we can retain 47 samples with a rarefaction depth of 2000 sequences/sample.

   Based on the sequencing depth and distribution of samples, we'll use 2000 sequences/sample for this analysis. This will let us keep 47 of 48 high quality samples (discarding the one sample with sequencing depth below 1000 sequences/sample).

Diversity analysis
==================

The first step in hypothesis testing in microbial ecology is typically to look at within- (alpha) and between-sample (beta) diversity. We can calculate diversity metrics, apply appropriate statistical tests, and visualize the data using the ``q2-diversity`` plugin.

We'll start by using the ``qiime diversity core-metrics-phylogenetic`` method, which ratifies the input feature table, calculates several commonly used alpha- and beta-diversity metrics, and produces principal coordinate analysis (PCoA) visualizations in Emperor for the beta diversity metrics. By default, the metrics computed are:

-  **Alpha Diversity**

   -  Shannon's diversity index
   -  Observed OTUs
   -  Faith's phylogenetic diversity
   -  Pielou's evenness

-  **Beta Diversity**

   -  Jaccard distance
   -  Bray-Curtis distance
   -  Unweighted UniFrac distance
   -  Weighted UniFrac distance

There is a very good discussion of diversity metrics and their meanings in a `forum post by Stephanie Orchanian`_.

The ``qiime diversity core-metrics-phylogenetic`` method wraps several other methods, and it's worthwhile to note that the steps can also be executed independently.

One important consideration for diversity calculations is the rarefaction depth. Above, we used the alpha rarefaction visualization and the sample summary visualization to pick a rarefaction depth. So, for these analyses, we'll use a depth of 2000 sequences per sample.

.. command-block::

   qiime diversity core-metrics-phylogenetic \
     --i-table ./dada2_table.qza \
     --i-phylogeny ./tree.qza \
     --m-metadata-file ./metadata.tsv \
     --p-sampling-depth 2000 \
     --output-dir ./core-metrics-results

.. question::

   Where did we get the value ``2000`` from? Why did we pick that?

Alpha diversity
+++++++++++++++

Alpha diversity asks whether the distribution of features within a sample (or groups of samples) differs between different conditions. The comparison makes no assumptions about the features that are shared between samples; two samples can have the same alpha diversity and not share any features. The rarefied alpha diversity produced by ``q2-diversity`` is a univariate, continuous value and can be tested using common non-parametric statistical tests.

We can test our covariates of interest against Faith's phylogenetic diversity and Pielou's evenness value by running:

.. command-block::

   qiime diversity alpha-group-significance \
     --i-alpha-diversity ./core-metrics-results/faith_pd_vector.qza \
     --m-metadata-file ./metadata.tsv \
     --o-visualization ./core-metrics-results/faiths_pd_statistics.qzv

.. command-block::

    qiime diversity alpha-group-significance \
     --i-alpha-diversity ./core-metrics-results/evenness_vector.qza \
     --m-metadata-file ./metadata.tsv \
     --o-visualization ./core-metrics-results/evenness_statistics.qzv

.. question::

   1. Is there a difference in **evenness** between genotype? Is there a difference in **phylogenetic diversity** between genotype?
   2. Based on the group significance test, is there a difference in phylogenetic diversity by genotype? Is there a difference based on the donor?

.. There is no difference in evenness by genotype, but the difference in phylogenetic diversity is borderline significant (p=0.0508)
.. there is a difference in both evenness and PD by donor

If we had a continuous covariate that we thought was associated with the alpha diversity, we could test that using ``qiime diversity alpha-correlation``. However, the only continuous variable in this dataset is the ``days_since_transplant``.

In some experiments, multiple interacting factors may impact alpha diversity together. If our alpha diversity estimates follow a normal distribution, we may use analysis of variance (ANOVA) to test whether multiple effects significantly impact alpha diversity. This test is present in the ``q2-longitudinal`` plugin:

.. command-block::

   qiime longitudinal anova \
     --m-metadata-file ./core-metrics-results/faith_pd_vector.qza \
     --m-metadata-file ./metadata.tsv \
     --p-formula 'faith_pd ~ genotype * donor_status' \
     --o-visualization ./core-metrics-results/faiths_pd_anova.qzv


Beta diversity
++++++++++++++

Next, we'll compare the structure of the microbiome communities using beta diversity. Start by making a visual inspection of the principle coordinates plots (PCoA) plots that were generated by ``q2-emperor`` and ``core-metrics-results/weighted_unifrac_emperor.qzv``.

.. question::

   1. Open the unweighted UniFrac emperor plot (``core-metrics-results/unweighted_unifrac_emperor.qzv``) first. Can you find separation in the data? If so, can you find a metadata factor that reflects the separation? What if you used weighted UniFrac distance (``core-metrics-results/weighted_unifrac_emperor.qzv``)?
   2. One of the major concerns in mouse studies is that sometimes differences in communities are due to natural variation in cages. Do you see clustering by cage?

.. The major separation in unweighted UniFrac should be due to donor.
.. we see some clustering by cage, but the points are mixed

Now, let's analyze the statistical trends using `PERMANOVA`_. PERMANOVA tests the hypothesis that samples within a group are more similar to each other than they are to samples in another group. To put it another way, it tests whether the within-group distances from each group are different from the between group distance. We expect samples that are similar to have smaller distances from each other, so if our hypothesis that one group is different from another is true, we'd expect the within-group distances to be smaller than the between group distance.

Let's use the ``beta-group-significance`` command to test whether the donor identity (which we qualitatively identified as a major separator in PCoA space) is associated with significant differences in weighted and unweighted UniFrac distance.

.. command-block::

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --m-metadata-column donor \
     --o-visualization core-metrics-results/unweighted-unifrac-donor-significance.qzv

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/weighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --m-metadata-column donor \
     --o-visualization core-metrics-results/weighted-unifrac-donor-significance.qzv

Let's also check whether there's a relationship between the cage in which a mouse lives and the beta diversity, since "cage effect" is often an important technical effect to consider. Since we have several cages, we'll use the ``--p-pairwise`` parameter that will let us check whether there are individual differences between the cages driving the difference. This may be useful, since if we check the metadata, we may find that cage is nested by donor.

.. command-block::

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --m-metadata-column cage_id \
     --o-visualization core-metrics-results/unweighted-unifrac-cage-significance.qzv \
     --p-pairwise

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/weighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --m-metadata-column cage_id \
     --o-visualization core-metrics-results/weighted-unifrac-cage-significance.qzv \
     --p-pairwise

.. question::

   1. Is there a significant effect of donor?
   2. From the metadata, we know that cage C31, C32, and C42 all house mice transplanted from one donor, and that cages C43, C44, and C49 are from the other. Is there a significant difference in the microbial communities between samples collected in cage C31 and C32? How about between C31 and C43? Do the results look the way you expect, based on the boxplots for donor?

.. Yep, donor is a significant and large effect, as we expected from the PCoA
.. Overall, cage is significant but some of this is drive by between donor differences.

A significant difference in PERMANOVA can reflect a large difference between the group or differences in variances within a group. This means that we might see a statistically significant difference even if it's caused by variation within one group. Distance boxplots can help give a visual sense of this, but it's nice to use a statistical test to confirm this. We can use the `permdisp`_ to help rule out differences due to a high degree of dispersion (within-group variance) in one of the groups of interest.

We can specify that we want to use permdisp using the ``--p-method`` flag in ``qiime diversity beta-group-significance``. Let's explore dispersion based on ``cage_id`` to check whether are cage-related differences are due to large within-cage variance.

.. command-block::

   qiime diversity beta-group-significance \
     --i-distance-matrix core-metrics-results/weighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --m-metadata-column cage_id \
     --o-visualization core-metrics-results/unweighted-unifrac-cage-significance_disp.qzv \
     --p-method permdisp

.. question::

   Is there a significant difference in variance for any of the cages?

.. No! Whoo! p ~ 0.2

We can also use the adonis action to look at a multivariate model. The ``adonis`` action uses a PERMANOVA test, but a different implementation that permits multiple effects to be tested simultaneously (similar to how we used ANOVA earlier for multivariate effects on alpha diversity). Let's look at the intersection between donor and genotype.

.. command-block::

   qiime diversity adonis \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --o-visualization core-metrics-results/unweighted_adonis.qzv \
     --p-formula genotype+donor

.. question::

   1. Is there a significant effect of donor?
   2. From the metadata, we know that cage C31, C32, and C42 all house mice transplanted from one donor, and that cages C43, C44, and C49 are from the other. Is there a significant difference in the microbial communities between samples collected in cage C31 and C32? How about between C31 and C43? Do the results look the way you expect, based on the boxplots for donor?
   3. If you adjust for donor in the adonis model, do you retain an effect of genotype? What percentage of the variation does genotype explain?

.. genotype is significant after adjusting for donor (p=~0.02) and explains about 4.25% of the variation, but heck, we'll take it

.. end L2 Diversity analysis

Taxonomic classification
========================

Up until now we have been performing diversity analyses directly on ASVs; in other words, we have assessed the similarity between samples based purely on the unique sequence variants that were observed in each sample. In most experiments we would like to get a sense of what microbial taxa are present — to identify ASVs and give them "names". To do this, we'll use the ``q2-feature-classifier`` plugin to classify ASVs taxonomically.

For this analysis, we'll use a pre-trained naive Bayes machine-learning classifier that was trained to differentiate taxa present in the 99% Greengenes 13_8 reference set trimmed to 250 bp of the V4 hypervariable region (corresponding to the 515F-806R primers). `This classifier works`_ by identifying k-mers that are diagnostic for particular taxonomic groups, and using that information to predict the taxonomic affiliation of each ASV. We can download the pre-trained classifier here:

.. download::
   :url: https://data.qiime2.org/2020.2/common/gg-13-8-99-515-806-nb-classifier.qza
   :saveas: gg-13-8-99-515-806-nb-classifier.qza

It's worth noting that Naive Bayes classifiers perform best when they're trained for the specific hypervariable region amplified. You can train a classifier specific for your dataset based on the :doc:`training classifiers tutorial <feature-classifier>` or download classifiers for other datasets from the :doc:`QIIME 2 resource page <../data-resources>`. Classifiers can be re-used for consistent versions of the underlying packages, database, and region of interest.

.. command-block::

   qiime feature-classifier classify-sklearn \
     --i-reads ./dada2_rep_set.qza \
     --i-classifier ./gg-13-8-99-515-806-nb-classifier.qza \
     --o-classification ./taxonomy.qza

Now, let's review the taxonomy associated with the sequences using the ``qiime metadata tabulate`` method.

.. command-block::

   qiime metadata tabulate \
     --m-input-file ./taxonomy.qza \
     --o-visualization ./taxonomy.qzv

Let's also tabulate the representative sequences (``FeatureData[Sequence]``). Tabulating the representative sequences will allow us to see the sequence assigned to the identifier and interactively blast the sequence against the NCBI database.

.. command-block::

   qiime feature-table tabulate-seqs \
     --i-data ./dada2_rep_set.qza \
     --o-visualization ./dada2_rep_set.qzv

.. question::

   1. Find the feature, ``07f183edd4e4d8aef1dcb2ab24dd7745``. What is the taxonomic classification of this sequence? What's the confidence for the assignment?
   2. How many features are classified as ``g__Akkermansia``?
   3. Use the tabulated representative sequences to look up these features. If you blast them against NCBI, do you get the same taxonomic identifier as you obtained with q2-feature-classifier?

.. 1. 07f183edd4e4d8aef1dcb2ab24dd7745 maps k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Christensenellaceae; g__; s__ with a confidence of 0.990905. This is an update because
.. 2. Two sequences map to g__Akkermansia
.. 3. They both should blast. ...Potentially tricky here is that it's hard to cross ref the ID with the taxa viewer. Can't visualize easily.

.. _`why-classification-underlines-only`:

.. note::

   You might notice that some features do not have taxonomic assignments, which for the Greengenes database is indicated by a blank string at the level (e.g., ``"g__"``). These indicate that there is not enough information for the Greengenes database to differentiate members of that clade, either due to ambiguity in the database or because the gene region being sequenced doesn't provide the resolution to distinguish members of that clade. This is distinct from cases where ``q2-feature-classifier`` cannot reliably classify the ASV to a deeper level: in those cases, an incomplete taxonomy string will be provided. Hence, you may see two different types of "underclassification" in your data: e.g., ``k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Christensenellaceae; g__; s__`` (genus and species annotations are missing in Greengenes) as well as ``k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Christensenellaceae`` (``q2-feature-classifier`` could not confidently classify that ASV at genus level).

.. note::

    You may also notice that more than one ASV has the same taxonomic assignment. This is normal — unique ASVs do not necessarily map to unique taxonomic groups! We visualize the frequency of each taxonomic group in barplots (as described below) or use the ``q2-taxa`` plugin to ``collapse`` our feature table based on taxonomic affiliation.

.. end L2 Taxonomic classification

Taxonomy barchart
=================

Since we saw a difference in diversity in this dataset, we may want to look at the taxonomic composition of these samples. To visualize this, we will build a taxonomic barchart of the samples we analyzed in the diversity dataset.

Before doing this, we will first filter out any samples with fewer features than our rarefaction threshold (``2000``). We can filter samples using the ``q2-feature-table`` plugin with the ``filter-samples`` method. This lets us filter our table based on a variety of criteria such as the number of counts (frequency, ``--p-min-frequency`` and ``--p-max-frequency``), number of features (``--p-min-features`` and ``--p-max-features``), or sample metadata (``--p-where``). See the :doc:`filtering tutorial <filtering>` for more details and examples.

For this example, we need to filter out samples with fewer sequences than our rarefaction depth.

.. command-block::

   qiime feature-table filter-samples \
     --i-table ./dada2_table.qza \
     --p-min-frequency 2000 \
     --o-filtered-table ./table_2k.qza

Now, let's use the filtered table to build an interactive barplot of the taxonomy in each sample.

.. command-block::

   qiime taxa barplot \
     --i-table ./table_2k.qza \
     --i-taxonomy ./taxonomy.qza \
     --m-metadata-file ./metadata.tsv \
     --o-visualization ./taxa_barplot.qzv

.. question::

   Visualize the data at level 2 (phylum level) and sort the samples by donor, then by genotype. Can you observe a consistent difference in phylum between the donors? Does this surprising you? Why or why not?

.. No clear difference by phylum by donor. Not shocking given these are based on fecal samples from adults. Hopefully also maybe highlights the fact that phylum level isn't necessarily a good way to compare differential abundance.

.. end L2 Taxonomy barchart

Differential abundance with ANCOM
=================================

Many microbiome investigators are interested in testing whether individual ASVs or taxa are more or less abundant in different sample groups. This is known as *differential abundance*. Microbiome data present several challenges for performing differential abundance using convential methods. Microbiome abundance data are inherently sparse (have a lot of zeros) and compositional (everything adds up to 1). Because of this, traditional statistical methods that you may be familiar with, such as ANOVA or t-tests, are not appropriate for performing differential abundance tests of microbiome data and lead to a high false-positive rate. ANCOM is a compositionally aware alternative that allows to test for differentially abundant features. If you're unfamiliar with the technique, it's worthwhile to review the `ANCOM paper`_ to better understand the method.

Before we begin, we will filter out low abundance/low prevalence ASVs. Filtering can provide better resolution and limit false discovery rate (FDR) penalty on features that are too far below the noise threshhold to be applicable to a statistical test. A feature that shows up with 10 counts may be a real feature that is present only in that sample, may be a feature that's present in several samples but only got amplified and sequenced in one sample because PCR is a somewhat stochastic process, or it may be noise. It's not possible to tell, so feature-based analysis may be better after filtering low abundance features. However, filtering also shifts the composition of a sample, further disrupting the relationship. Here, the filtering is performed as a trade off between the model, computational efficiency, and statistical practicality.

.. command-block::

   qiime feature-table filter-features \
     --i-table ./table_2k.qza \
     --p-min-frequency 50 \
     --p-min-samples 4 \
     --o-filtered-table ./table_2k_abund.qza

ANCOM fundamentally operates on a ``FeatureTable[Frequency]``, which contains the frequencies of features in each sample. However, ANCOM cannot tolerate zeros (because compositional methods typically use a log-transform or a ratio and you can't take the log or divide by zeros). To remove the zeros from our table, we add a pseudocount to the ``FeatureTable[Frequency]`` Artifact, creating a ``FeatureTable[Composition]`` in its place.

.. command-block::

   qiime composition add-pseudocount \
     --i-table ./table_2k_abund.qza \
     --o-composition-table ./table2k_abund_comp.qza

Let's use ANCOM to check whether there is a difference in the mice based on their donor and then by their genetic background. The test will calculate the number of ratios between pairs of ASVs that are significantly different with FDR-corrected p < 0.05.

.. command-block::

   qiime composition ancom \
     --i-table ./table2k_abund_comp.qza \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-column donor \
     --o-visualization ./ancom_donor.qzv

   qiime composition ancom \
     --i-table ./table2k_abund_comp.qza \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-column genotype \
     --o-visualization ./ancom_genotype.qzv

When you open the ANCOM visualizations, you'll see a `volcano plot`_ on top, which relates the ANCOM W statistic to the CLR (center log transform) for the groups. The W statistic is the number of ANCOM subhypotheses that have passed for each individual taxon, indicating that the ratios of that taxon’s relative abundance to the relative abundances of ``W`` other taxa were detected to be significantly different (typically FDR-adjusted p < 0.05). Because differential abundance in ANCOM is based on the ratio between tests, it does not produce a traditional p-value.

.. question::

   Open the ANCOM visualizations for the donor and genotype and the taxonomy visualization artifact.

   1. Are there more differentially abundant features between the donors or the mouse genotype? Did you expect this result based on the beta diversity?
   2. Are there any features that are differentially abundant in both the donors and by genotype?
   3. How many differentially abundant features are there between the two genotypes? Using the percentile abundances and volcano plot as a guide, can you tell if they are more abundant in wild type or susceptible mice?
   4. Use taxonomy metadata visualization and search sequence identifiers for the significantly different features by genotype. What genera do they belong to?

.. More differentially abundant features by donor than genotype. Not surprising given the size of donor in b-div vs the size of genotype
.. Nope. Whoo! :celebrate:
.. There are three 3 features that are differentially abundant. All three are more abundant in WT mice
.. ac5402de1ddf427ab8d2b0a8a0a44f19: g__Bacteriodetes; 79280cea51a6fe8a3432b2f266dd34db: g__Faecalibacterium (prausnitzii); 3017f87a3b0f5200ed54eca17eef3cbb: f__[Mogibacteriaceae]

.. end L2 Differential abundance with ANCOM

Taxonomic classification again
==============================

It is possible to `increase taxonomic classification accuracy`_ by showing the taxonomic classifier what a typical animal stool sample looks like before attempting classification. To do that we will have to retrain the naive Bayes classifier. Fortunately, a representation of a typical stool sample that is derived from `Qiita`_ data is available from the `readytowear collection`_.

If you feel that these samples are not typical stool samples, it is possible to, for instance, assemble data on just mouse or just human (or just human and mouse) stool samples using `q2-clawback`_. We will not attempt that here because it takes a while to run, but details are available in the `tutorial`_.

Start by downloading the stool data, along with the 99% Greengene 13_8 reference data.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/ref_seqs_v4.qza
   :saveas: ref_seqs_v4.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/ref_tax.qza
   :saveas: ref_tax.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/pd-mice/animal_distal_gut.qza
   :saveas: animal_distal_gut.qza

Next retrain the classifier.

.. command-block::

   qiime feature-classifier fit-classifier-naive-bayes \
     --i-reference-reads ./ref_seqs_v4.qza \
     --i-reference-taxonomy ./ref_tax.qza \
     --i-class-weight ./animal_distal_gut.qza \
     --o-classifier ./bespoke.qza

We can use the new classifier in exactly the same way as the standard classifier that we downloaded above.

.. command-block::

   qiime feature-classifier classify-sklearn \
     --i-reads ./dada2_rep_set.qza \
     --i-classifier ./bespoke.qza \
     --o-classification ./bespoke_taxonomy.qza

   qiime metadata tabulate \
     --m-input-file ./bespoke_taxonomy.qza \
     --o-visualization ./bespoke_taxonomy.qzv

.. question::

   Open up the old ``taxonomy.qzv`` visualization and compare it to the ``bespoke_taxonomy.qzv`` visualization.

   1. Search for "ovatus" in both. Is there an ASV in the new taxonomy that wasn't present in the original?
   2. Revisit the ``ancom_donor.qzv`` visualization. Can you find that ASV?

.. c162a4f3943238810eba8a25f0563cca
.. it's differentially abundant (W=87)

When analyzing ANCOM results, it is possible to trace the ASVs that we found using the taxonomies that we have created. It is also possible to run ANCOM directly on taxonomic groups that we have discovered in our samples by counting features according to taxonomic classification. This has the advantage of pooling feature counts across taxonomically similar ASVs, for instance allowing exact species substitution between samples. The output is also more readable. On the down side, it has all the inaccuracies that come with automated taxonomic classification.

We will run through the pipeline twice, once with our original taxonomy and once with the new taxonomy, for the purpose of comparison. First using the original taxonomy:

.. command-block::

   qiime taxa collapse \
     --i-table ./table_2k.qza \
     --i-taxonomy ./taxonomy.qza \
     --o-collapsed-table ./uniform_table.qza \
     --p-level 7 # means that we group at species level

   qiime feature-table filter-features \
     --i-table ./uniform_table.qza \
     --p-min-frequency 50 \
     --p-min-samples 4 \
     --o-filtered-table ./filtered_uniform_table.qza

   qiime composition add-pseudocount \
     --i-table ./filtered_uniform_table.qza \
     --o-composition-table ./cfu_table.qza

   qiime composition ancom \
     --i-table ./cfu_table.qza \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-column donor \
     --o-visualization ./ancom_donor_uniform.qzv

Now redo with the new taxonomy:

.. command-block::

   qiime taxa collapse \
     --i-table ./table_2k.qza \
     --i-taxonomy ./bespoke_taxonomy.qza \
     --p-level 7 \
     --o-collapsed-table ./bespoke_table.qza

   qiime feature-table filter-features \
     --i-table ./bespoke_table.qza \
     --p-min-frequency 50 \
     --p-min-samples 4 \
     --o-filtered-table ./filtered_bespoke_table.qza

   qiime composition add-pseudocount \
     --i-table ./filtered_bespoke_table.qza \
     --o-composition-table ./cfb_table.qza

   qiime composition ancom \
     --i-table ./cfb_table.qza \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-column donor \
     --o-visualization ./ancom_donor_bespoke.qzv

.. question::

   Compare final ANCOM visualizations. They are fairly similar, which is good.

   1. Is *Bacteroides ovatus* present in the ANCOM results derived from our original taxonomy?
   2. Is *B. ovatus* present in the new ANCOM results?
   3. Why is that?

.. no
.. yes
.. The original taxonomy lumped it in with g__Bacteroides; __ and the effect was washed out.

.. end L2 Taxonomic classification again

Longitudinal analysis
=====================

This study includes a longitudinal component; samples from each mouse were collected 7, 14, 21, and 49 days post fecal transplant. We can use the ``q2-longitudinal`` plug-in to explore the hypothesis that a mouse's genetic background affected the change in the microbial community of each mouse. For this longitudinal analysis, we're going to focus on beta diversity. Alpha diversity changes wildly in infants, but it's often stable in adults over short time periods. We're dealing with an adult fecal community over a relatively short time period, and there is no difference in alpha diversity with time. The :doc:`longitudinal analysis tutorial <longitudinal>` is an excellent resource for exploring longitudinal analyses of microbiome samples.

PCoA-based analyses
+++++++++++++++++++

We can start by exploring temporal change in the PCoA using the animations tab.

.. question::

   1. Open the unweighted UniFrac emperor plot and color the samples by mouse id. Click on the “animations” tab and animate using the ``day_post_transplant`` as your gradient and ``mouse_id`` as your trajectory. Do you observe any clear temporal trends based on the PCoA?
   2. What happens if you color by ``day_post_transplant``? Do you see a difference based on the day? *Hint: Trying changing the colormap to a sequential colormap like viridis.*

.. No clear pattern based on animations

A volatility plot will let us look at patterns of variation along principle coordinate axes starting from the same point. This can be helpful since inter-individual variation can be large and this visualizations lets us focus instead on magnitude of change in each group and in each individual.

Let's use the ``q2-longitudinal`` plugin to look at how samples from an individual move along each PC. The ``--m-metadata-file`` column can take several types, including a metadata file (like our ``metadata.tsv``) as well as a ``SampleData[AlphaDiversity]``, ``SampleData[Distance]`` (files "viewable" as metadata), or a ``PCoA`` artifact.

.. command-block::

   qiime longitudinal volatility \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-file ./core-metrics-results/unweighted_unifrac_pcoa_results.qza \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id \
     --p-default-group-column 'donor_status' \
     --p-default-metric 'Axis 2' \
     --o-visualization ./pc_vol.qzv

.. question::

    Using the controls, look at variation in cage along PCs 1, 2, and 3. What kind of patterns do you see with time along each axis?

.. In this version, there's separation, but not a lot of temporal trends.

Distance-based analysis
+++++++++++++++++++++++

Now, let's try looking directly at the pairwise distances between samples. Here, we'll test the hypothesis that genotype affects the magnitude of change in the distance from the first sample collected from each mouse (7 days post transplant). We assume that given the rate of turnover in a microbial community, we might expect to see a change in the community over time. However, here we'll ask if these changes are associated with host genotype.

We'll start this analysis by looking at how much the microbial community of each mouse changes from 7 days post transplant. We use the ``baseline`` parameter to specify a static time point against which all other time points are compared; if we remove this parameter from the command, we look instead at the *rate of change* for each individual between each time point. See the :doc:`longitudinal analysis tutorial <longitudinal>` for more details.

.. command-block::

   qiime longitudinal first-distances \
     --i-distance-matrix ./core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file ./metadata.tsv \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id \
     --p-baseline 7 \
     --o-first-distances ./from_first_unifrac.qza

We can again use volatility analysis to visualize the change in beta diversity based on distance.

.. command-block::

   qiime longitudinal volatility \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-file ./from_first_unifrac.qza \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id \
     --p-default-metric Distance \
     --p-default-group-column 'donor_status' \
     --o-visualization ./from_first_unifrac_vol.qzv

.. question::

   Based on the volatility plot, does one donor change more over time than the other? What about by genotype? Cage?

.. samples from the hc change more over time; cage42 shows a lot of volatility. there isn't as much temporal change by genotype but there is some separation

A linear mixed effects (LME) model lets us test whether there's a relationship between a dependent variable and one or more independent variables in an experiment using repeated measures. Since we're interested in genotype, we should use this as an independent predictor.

For our experiment, we're currently interested in the change in distance from the initial timepoint, so we'll use this as our outcome variable (given by ``--p-metric``).

The ``linear-mixed-effects`` action also requires a state column (``--p-state-column``) which designates the time component in the metadata, and an individual identifier (``--p-individual-id-column``). Which columns should we use in our data?

We can build a model either using the ``--p-formula`` parameter or the ``--p-group-columns`` parameter. For this analysis, we're interested in whether genotype affects the longitudinal change in the microbial community. However, we also know from our cross sectional analysis that donor plays a large role in shaping the fecal community. So, we should also probably include that in this analysis. We may also want to consider cage effect in our experiment, since this is a common confounder in rodent studies. However, the original experimental design here was clever: although cages were grouped by donor (mice are coprophagic), they were of mixed genotype. This partial randomization helps limit some of the cage effects we might otherwise see.

Based on the experimental design, what group columns should we choose?

.. command-block::

   qiime longitudinal linear-mixed-effects \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-file ./from_first_unifrac.qza \
     --p-metric Distance \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id \
     --p-group-columns genotype,donor \
     --o-visualization ./from_first_unifrac_lme.qzv

Now, let's look at the results of the models.

.. question::

   1. Is there a significant association between the genotype and temporal change?
   2. Which genotype is more stable (has lower variation)?
   3. Is there a temporal change associated with the donor? Did you expect or not expect this based on the volatility plot results?
   4. Can you find an interaction between the donor and genotype?

.. yes, there's a significant association. The susceptible mice are more stable. There isn't a statistically significant difference based on donor though. the interaction between donor and genotype is significant.

.. note::

    Importantly, LME models also allow us to distinguish between two types of independent variables: fixed effects (e.g., experimental treatments) and random effects (e.g., biological factors that cannot be controlled in the experiment). By default, the ``linear-mixed-effects`` action in ``q2-longitudinal`` uses the ``individual_id_column`` as a random effect, since we can expect that biological differences between individual subjects will impact the baseline values of the dependent variable we are testing. The rate of change — slope — is another inter-individual effect that we often might want to consider as a random effect in longitudinal experiments. See the :doc:`longitudinal analysis tutorial <longitudinal>` for more details and discussion of LME tests and effect types.

.. end L2 Longitudinal analysis

Machine-learning classifiers for predicting sample characteristics
==================================================================
As an alternative (or complementary) approach to the methods we have used in this tutorial for testing if and how samples are different from one another, we can utilize :doc:`machine-learning methods <sample-classifier>` to determine how *predictive* microbiome composition is of other characteristics about a sample. For example, we may use machine-learning classifiers to predict a patient's susceptibility to disease, or predict the treatment group that a sample belongs to. Additionally, many machine-learning methods report which features are most important for predicting sample characteristics, making this a useful approach for determining which features (ASVs, species, etc) are associated with a particular treatment, disease state, or other category of interest. All of this and much more can be found in the ``q2-sample-classifier`` plugin. Here we will use this plugin to predict each mouse's genotype and donor status based on their ASV composition using a Random Forest classifier (this pipeline can access many different machine-learning methods via the ``estimator`` parameter, but Random Forest classifiers are used by default).

.. command-block::

    qiime sample-classifier classify-samples \
      --i-table ./dada2_table.qza \
      --m-metadata-file ./metadata.tsv \
      --m-metadata-column genotype_and_donor_status \
      --p-random-state 666 \
      --p-n-jobs 1 \
      --output-dir ./sample-classifier-results/

This pipeline generates a number of output artifacts and visualizations. You can read more about these in the :doc:`sample classifier tutorial <sample-classifier>` but right now let's just focus on ``./sample-classifier-results/accuracy_results.qzv``. This visualization tells you how well your sample classifier performed via a `confusion matrix`_ and accompanying table of accuracy scores. This tells you how frequently each sample type is classified to each sample class, including the correct class label. Overall error rates are also reported in the table below.

.. question::

    How did we do? Just for fun, try predicting some of the other metadata columns to see how easily ``cage_id`` and other columns can be predicted.

.. a whopping 90% accuracy rate for distinguishing 4 different class labels! Looks like BOTH genotype AND donor status are strong drivers of the microbiome.

Looks like we did pretty well! So we can see what features are most predictive of each sample class (donor and genotype groups). The importance scores are stored in the ``./sample-classifier-results/feature_importance.qza`` artifact (pro tip: this can be view with the ``qiime metadata tabulate`` command we covered earlier). Here we will generate a heatmap showing the mean abundance of the 100 most important ASVs in each genotype and donor group.

.. command-block::

    qiime sample-classifier heatmap \
      --i-table ./dada2_table.qza \
      --i-importance ./sample-classifier-results/feature_importance.qza \
      --m-sample-metadata-file ./metadata.tsv \
      --m-sample-metadata-column genotype_and_donor_status \
      --p-group-samples \
      --p-feature-count 100 \
      --o-heatmap ./sample-classifier-results/heatmap.qzv \
      --o-filtered-table ./sample-classifier-results/filtered-table.qza

.. question::

    What features appear to differentiate genotypes? What about donors? Are any ASVs specific to a single sample group?


.. end Machine-learning classifiers for predicting sample characteristics


Synthesis
=========

Based on the results of the analysis, we can say that there is a difference in the microbial communities of these mice based on their donor and genetic background. (This recapitulates the results of the original analysis.)

We found that the donor is the primary driver of alpha diversity.

But, we saw differences by donor and genotype based on beta diversity. Using the PCoA emperor plots, we can see clear separation between the mice from the two donors. After adjusting for the donor, we saw a significant difference between the genotypes.

Although there wasn't a clear pattern in the barchart at the phylum level between donors or genotypes, we were still able to find ASVs which differentiated the genotypes using ANCOM and Random Forest classification. There was no overlap between these ASVs in the donor and genetic background, supporting the hypothesis that the difference due to genotype is separate from the difference due to donor.

The volatility plots and temporal analysis showed that the microbiome in different genetic backgrounds changed differently over time.

This suggests that there is a genotype-specific effect on the microbiome of mice receiving fecal transplants.

💩🐁

.. References

.. _humanized: https://en.wikipedia.org/wiki/Humanized_mouse
.. _Sampson et al, 2016: https://www.ncbi.nlm.nih.gov/pubmed/27912057
.. _PRJEB17694: https://www.ebi.ac.uk/ena/data/view/PRJEB17694
.. _Qiita: https://qiita.ucsd.edu
.. _EMP 515f-806r: http://www.earthmicrobiome.org/protocols-and-standards/16s/
.. _absolute path: https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths
.. _q2-dbOTU: https://library.qiime2.org/plugins/q2-dbotu/4/
.. _DADA2: https://www.ncbi.nlm.nih.gov/pubmed/27214047
.. _Deblur: https://www.ncbi.nlm.nih.gov/pubmed/28289731
.. _Nearing et al, 2018: https://www.ncbi.nlm.nih.gov/pubmed/30123705
.. _Bokulich et al, 2013: https://www.ncbi.nlm.nih.gov/pubmed/23202435
.. _Weiss et al, 2017: https://www.ncbi.nlm.nih.gov/pubmed/28253908
.. _forum post by Stephanie Orchanian: https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282/
.. _view.qiime2.org: http://www.view.qiime2.org/
.. _PERMANOVA: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1442-9993.2001.01070.pp.x
.. _This classifier works: https://doi.org/10.1186/s40168-018-0470-z
.. _ancom paper: https://www.ncbi.nlm.nih.gov/pubmed/26028277
.. _Google Sheet: https://data.qiime2.org/2020.2/tutorials/pd-mice/sample_metadata
.. _permdisp: https://www.ncbi.nlm.nih.gov/pubmed/16706913
.. _volcano plot: https://en.wikipedia.org/wiki/Volcano_plot_(statistics)
.. _confusion matrix: https://en.wikipedia.org/wiki/Confusion_matrix
.. _readytowear collection: https://github.com/BenKaehler/readytowear
.. _q2-clawback: https://library.qiime2.org/plugins/q2-clawback/7/
.. _increase taxonomic classification accuracy: https://www.biorxiv.org/content/10.1101/406611v2
.. _tutorial: https://forum.qiime2.org/t/using-q2-clawback-to-assemble-taxonomic-weights/5859
