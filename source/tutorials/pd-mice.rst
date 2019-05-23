Parkinson’s Mouse Tutorial
------------------------------------

This tutorial will demonstrate a "typical" QIIME 2 analysis, using a set of fecal samples from humanized mice. The original study, `Sampson et al, 2016`_, was designed to determine whether the fecal microbiome contributed to the development of Parkinson’s Disease (PD). Several observation studies showed a difference in the microbiome between PD patients and controls, although the organisms identified across studies were not consistent. However, this was sufficient evidence to suggest that there might be a relationship between PD and the fecal microbiome.

To determine whether that relationship was incidental or actually disease associated, a second study was needed. A human cohort study was not feasible; the disease only affects about 1% of the population over 60, PD takes a long time to develop and to be diagnosed, and it would be difficult to determine when to collect the samples.

Therefore, a gnotobiotic mouse study was utilized to evaluate the role of the microbiome in the development of PD symptoms. Feces were collected from six donors with Parkinson’s disease and six age- and sex-matched neurologically health controls, and then transplanted into mice who were either predisposed to developing Parkinson’s disease due to a mutation ("aSyn") or resistant wild type mice ("BDF1"). Mice from different donors were kept in seperate cages, but mix from different genetic backgrounds were co-housed. The mice were followed for 7 weeks to see if they developed symptoms of Parkinson’s disease.

We’ll look a subset of data from two human donors (one healthy and one with PD) whose samples were transplanted into two cages of mice from the susceptible genotype.

For this tutorial, a subset of the metadata has been pulled from the full file, and the sequences have also been subsampled down to around 5000 sequences per sample from a much larger distribution to allow the tutorial to run in a short time. The sequences for the full study were deposited in EBI with accession `PRJEB17694`_; processed tables can be downloaded from the `qiita`_  database from study 10483.

Hypothesis
==========

This tutorial will explore the hypothesis that the genetic background of a humanized mouse influences the microbial community. However, we'll also need to consider other confounders which might drive the shape of the microbiome instead of the mouse genotype.


Set up
======

This tutorial assumes that you have QIIME 2 installed according to the :doc:`installation instructions <../install/index>`.

Before running the tutorial, you will need to make a directory for the tutorial data and navigate into that directory.

.. command-block::
   :no-exec:

   mkdir ./mouse_tutorial
   cd ./mouse_tutorial

Metadata
========

Before starting any analysis, it's important to be familiar with the metadata. In this study, the metadata file contains 7 columns.

+-------------------------+--------------------+-----------------+------------------+
| variable                | description        | data type       | values           |
+=========================+====================+=================+==================+
| sample-id               | unique sample      | —               | unique for each  |
|                         | identifier         |                 | sample           |
+-------------------------+--------------------+-----------------+------------------+
| mouse_id                | the unique         | categorical     | ``"435"``;       |
|                         | identifier for     |                 | ``"437"``;       |
|                         | each mouse         |                 | ``"456"``;       |
|                         |                    |                 | ``"457"``;       |
|                         |                    |                 | ``"468"``;       |
|                         |                    |                 | ``"469"``;       |
|                         |                    |                 | ``"536"``;       |
|                         |                    |                 | ``"537"``;       |
|                         |                    |                 | ``"538"``;       |
|                         |                    |                 | ``"539"``;       |
|                         |                    |                 | ``"546"``;       |
|                         |                    |                 | ``"547"``        |
+-------------------------+--------------------+-----------------+------------------+
| genotype                | the genetic        | categorical     | ``"wild_type"``; |
|                         | background of      |                 | ``"susceptible"``|
|                         | the mouse. The     |                 |                  |
|                         | Thy1-aSyn          |                 |                  |
|                         | (``"susceptible``) |                 |                  |
|                         | mice are           |                 |                  |
|                         | genetically        |                 |                  |
|                         | predisposed to     |                 |                  |
|                         | disease;           |                 |                  |
|                         | ``"wild_type"``    |                 |                  |
|                         | from the BDF1      |                 |                  |
|                         | background do      |                 |                  |
|                         | not have any       |                 |                  |
|                         | additional risk    |                 |                  |
+-------------------------+--------------------+-----------------+------------------+
| cage_id                 | the unique         | categorical     | ``"C31"``;       |
|                         | identifier for     |                 | ``"C35"``;       |
|                         | each cage of       |                 | ``"C42"``;       |
|                         | mice               |                 | ``"C43"``;       |
|                         |                    |                 | ``"C44"``;       |
|                         |                    |                 | ``"C49"``        |
+-------------------------+--------------------+-----------------+------------------+
| donor                   | A unique           | categorical     | ``"hc_1"``       |
|                         | identifier for     |                 | ``"pd_1"``       |
|                         | the human who      |                 |                  |
|                         | donated the        |                 |                  |
|                         | feces              |                 |                  |
+-------------------------+--------------------+-----------------+------------------+
| donor_status            | whether the        | categorical     | ``"Healthy"``;   |
|                         | donor has          |                 | ``"PD"``         |
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


Even though the mouse ID looks like a number, we will specify the type using the ``#q2_type`` column in the data.

The metadata is avaliable as a `Google Sheet`_, or ou can download it directly from and save it as a tsv.

.. download::
   :url: https://data.qiime2.org/2019.7/tutorials/pd-mice/sample_metadata.tsv
   :saveas: metadata.tsv

The sample metadata will be used through out the tutorial.

Loading the data into QIIME 2
=============================

In QIIME 2, all data is structured as an Artifact of a specific semantic type. The artifacts contain the data as well as information about the data, including a record of the original data, the tools used to process it. This allows for better tracking of how you actually got to where you are in your analysis. You can learn more about common QIIME 2 Artifacts and types of artifacts :doc:`here <../semantic-types/>`.

Our samples were amplified using the `EMP 515f-806r`_ primers and sequenced on an Illumina MiSeq with a 2x150bp kit. The hypervariable
region covered by the primers we used 290bp and so with 150bp reads, our sequences will be slightly too short to be able to do paired-end analysis downstream. Therefore, we’re going to work with single-end sequences. We will work with a version of the samples which have already been demultiplexed, for example, by the sequencing center. If you need to demultiplex your sequences, the doc: `moving pictures tutorial <moving-pictures>` describes how to demultiplex your sequences if they were sequenced using the Earth Microbiome Project protocol.

We will import the sequences as ``SampleData[SequencesWithQuality]``, which is the single end sequence demultiplexed format. If we wanted to import paired sequences, we would choose the ``SampleData[PairedEndSequencesWithQuality]`` type. We will import the sequences using the sample manifest format. This is one of the most versatile ways to import demultiplexed data in QIIME 2. We create a tab-separated sample manifest file that maps the sample name we want to use in QIIME 2 to the path to the sequence file. The benefit is that the demultiplexed sequence files can be named anything you want; there are not fixed assumptions about the conventions, and the file names do not dictate the final name. When QIIME 2 reads the file, it ignores any line prefixed with the ``#`` symbol. The first line that doesn’t contain a ``#`` is the header line and must be ``sample-id\tabsolute-filepath``. The sample order after the header line does not matter.

.. My vote is to merge the manifest with the sample metadata

Let's start by downloading the manifest and corresponding sequences.

.. download::
   :url: https://data.qiime2.org/2019.7/tutorials/pd-mice/manifest
   :saveas: manifest

.. download::
   :url: https://data.qiime2.org/2019.7/tutorials/pd-mice/demultiplexed_seqs.zip
   :saveas: demuliplexed_seqs.zip

You'll need to unzip the directory of sequences.

.. command-block::

   unzip demuliplexed_seqs.zip

You can use the ``head`` command to check the first five lines of the sample manifest.

.. command-block::
   :no-exec:

   head -n 6 manifest

When using the manifest formats, a sample name can only appear in one line and can only map to one sequencing file per column (one column for single-end, two columns for paired-end). The **absolute-filepath** for each sample must be an `absolute path`_, which specifies the "full" location of the file. We do that here using the ``$PWD`` variable, which uses the local absolute directory.

We’ll use the manifest to import our data.

.. command-block::

   qiime tools import \
     --type "SampleData[SequencesWithQuality]" \
     --input-format SingleEndFastqManifestPhred33V2 \
     --input-path ./manifest \
     --output-path ./demux_seqs.qza

Let’s check the sequences and the sequencing depth of the samples using the ``qiime demux summarize`` command. It provides information about the number of sequences in each sample, as well as the quality of the sequences.

Before running the command, let’s review the help documentation to make sure we understand the arguments.

.. command-block::
   :no-exec:

   qiime demux summarize --help

Based on the documentation, we should pass the demultiplexed sequences that we imported as the ``--i-data`` argument, since this takes a ``SequencesWithQuality]`` semantic type, and that’s the type of data we imported. We’ll specify the location we want the visualization by passing the output path to ``--o-visualization``.

The help documentation is a good reference for any command, and the first place to look if you’re getting errors, especially errors about parameters.

.. command-block::

   qiime demux summarize \
     --i-data ./demux_seqs.qza \
     --o-visualization ./demux_seqs.qzv

You can view the .qzv visualization file at `view.qiime2.org`_. Just drag and drop the file into the viewer window.

.. question::

   1. After demultiplexing, which sample has the lowest sequencing depth?
   2. What is the median sequence length?
   3. What is the median quality score at position 125?

.. lowest sequecing depth: 4237 seqs, recip.460.WT.HC3.D14
.. median length: 150 nt
.. median qual score at 125: 38


Sequence quality control and feature table
==========================================

There are several ways to construct a feature table in QIIME 2. The first major separation is between Operational Taxonomic Units (OTUs) and Absolute Sequence Variants (ASVs). OTUs have been widely used in microbiome research since the mid 2010s, and assign sequences to taxonomic clusters either based on a reference database or de novo assignment. QIIME 2 offers clustering through :doc:`q2-vsearch<otu-clustering>` and `q2-dbOTU_` plug-ins, currently.

ASVs are a more recent development and provide better resolution in features than traditional OTU-based methods. ASVs can separate features based on differences of a single nucleotide in sequences of 400 bp or more, a resolution not possibly even with 99% identity OTU clustering. QIIME 2 currently offers denoising via `Dada2`_ (``q2-dada2``) and `Deblur`_ (``q2-deblur``). The major differences in the algorithms and motivation for denoising are nicely described in `Nearing et al, 2018`_.

It is worth noting in either case that denoising to ASVs and clustering to OTUs are seperate, but parallel steps. A choice should be made for a single pathway: either denoising or OTU based clustering; it is not recommended to combine the steps.

In this tutorial, we’ll denoise using Dada2 with single end sequences. The :doc:`Atacama soil tutorial <atacama-soils>` describes Dada2 on paired end sequences. Those interested in Deblur can refer to the :doc:`moving pictures tutorial  <moving-pictures/>` and :doc:`Alternative methods of read joining <read-joining/>` tutorial for running Deblur on single and paired end sequences, respectively. 

The ``qiime dada2 denoise-single`` method requires us to set the ``--p-trunc-len`` paramter. This controls the length of the sequences and should be selected based on a drop in quality scores. In our dataset, the quality scores are relatively evenly distributed along the sequencing run, so we’ll use the full 150 bp sequences. However, the selection of the trim length is a relatively subjective measurement and relies on the decision making capacity of the analyst.

.. command-block::

   qiime dada2 denoise-single \
     --i-demultiplexed-seqs ./demux_seqs.qza \
     --p-trunc-len 150 \
     --o-table ./dada2_table.qza \
     --o-representative-sequences ./dada2_rep_set.qza \
     --o-denoising-stats ./dada2_stats.qza

We can also review the denoising statitics using the ``qiime metadata tabulate`` command.

.. command-block::

    qiime metadata tabulate \
      --m-input-file ./dada2_stats.qza  \
      --o-visualization ./dada2_stats.qzv

Feature Table Summary
---------------------

After we finish denoising the data, we can check the quality filtering results. We can use two commands to explore the sequence data. First, we’ll look at the summary of the feature table. This will provide us with the counts associated with each sequence and each feature, as well as a histogram of the features.

.. command-block::

   qiime feature-table summarize \
     --i-table ./dada2_table.qza \
     --m-sample-metadata-file ./metadata.tsv \
     --o-visualization ./dada2_table.qzv

.. question::

   Start with the feature table summary. 

   1. How many features remain after denoising?
   2. Which sample has the most? How many sequences does that sample have?
   3. If we chose to filter the data to retain only samples with 4250 sequences, how many samples would we lose?
   4. Which features are observed in at least 47 samples?
   5. Which sample has the fewest sequences? How many does it have?

   If you open the denoising summary, can you find the step where the sample with the fewest sequences fails? 

.. JWD: Adding answers for my own reference 
.. After denoising: 287 features
.. Most sequences: recip.539.ASO.PD4.D14, 4996
.. With 4250 seqs/sample, we retain 26 of 48 samples => 22 samples remain
.. 3 features are found in 47 samples: 04c8be5a3a6ba2d70446812e99318905, ea2b0e4a93c24c6c3661cbe347f93b74, 1ad289cd8f44e109fd95de0382c5b252
.. Sample recip.460.WT.HC3.D49 has the lowest final depth with 347 sequences
.. the sample fails in the denoising stage

Generating a Phylogenetic Tree for Diversity Analysis
=====================================================

QIIME 2 analysis allows the use of phylogenetic trees for both diversity metrics such as PD whole tree and UniFrac distance as well as feature-based analyses in Gneiss. The tree provides an inherent structure to the data, allowing us to consider an evolutionary relationship between organisms.

QIIME 2 offers several ways to construct a phylogenetic tree. For this tutorial, we’re going to use a fragment insertion tree using the ``fragment-insertion`` plugin. The authors of the fragment insertion plugin suggest that it can outperform traditional alignment based methods based on short illumina reads by alignment against a reference tree built out of larger sequences. Our command, ``qiime fragment-insertion sepp`` will take the representative sequences (a ``FeatureData[Sequence]`` object) we generated during deblurring and return a phylogenetic tree where the sequences have been inserted into the greengenes 13_8 99% identity reference tree backbone.

.. note:: 
   This command can take a fair bit of time to run. If your computation environment supports it, we suggest including an appropriately-set ``--p-threads`` parameter.

.. command-block::

   qiime fragment-insertion sepp \
     --i-representative-sequences ./dada2_rep_set.qza \
     --o-tree ./tree.qza \
     --o-placements ./tree_placements.qza \
     --p-threads 1


Taxonomic Classification
========================

Let’s do one more preparation step before we dig into the analysis! To be able to identify ASVs and give them "names", we need to somehow determine taxonomy. To do this, we’ll use the ``q2-feature-classifier`` plugin.

For this analysis, we'll use a pretrained classifier using 99% Greengenes 13_8 reference set trimmed to 250 bp of the V4 hypervariable region (corresponding to the 515F-806R primers). The classifier is a specific semantic type, ``TaxonomicClassifier``, and it is actually the object that does the classification.

.. download::
   :url: https://data.qiime2.org/2019.4/common/gg-13-8-99-515-806-nb-classifier.qza
   :saveas: gg-13-8-99-515-806-nb-classifier.qza

It’s worth noting that Naive Bayes classifiers perform best when they’re trained for the specific hypervariable region amplified. You can train a classifier specific for your dataset based on the :doc:`training classifiers tutorial <feature-classifier>` or download classifiers for other datasets from the :doc:`QIIME 2 resource page <../data-resources>`. Classifiers can be re-used for consistent versions of the underlying packages, database and region of interest.

.. command-block::

   qiime feature-classifier classify-sklearn \
     --i-reads ./dada2_rep_set.qza \
     --i-classifier ./gg-13-8-99-515-806-nb-classifier.qza \
     --o-classification ./taxonomy.qza

.. TODO: add clawback?

Now, let’s review the taxonomy associated with the sequences using the ``qiime metadata tabulate`` method.

.. command-block::

   qiime metadata tabulate \
     --m-input-file ./taxonomy.qza \
     --o-visualization ./taxonomy.qzv

Let’s also tabulate the representative sequences (``FeatureData[Sequence]``). Tabulating the representative sequences will allow us to see the sequence assigned to the identifier and interactively blast the sequence against the NCBI database.

.. command-block::

   qiime feature-table tabulate-seqs \
     --i-data ./dada2_rep_set.qza \
     --o-visualization ./dada2_rep_set.qzv

.. to update with Dada2 -- jwd 20190521

.. question::

   Find the feature, ``59196a586276f0be745d0e334fc071c6``. What is the taxonomic classification of this sequence? What’s the confidence for the assignment?

   How many sequences are mapped to g__Akkermansia?

   Use the tabulated representative sequences to look up these features. If you blast them against NCBI, do you get the same taxonomic identifier?

.. 1. 59196a586276f0be745d0e334fc071c6 maps to k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Blautia; s__ with a confidence of 0.99928
.. 2. Two sequences map to g__Akkermansia
.. 3. They both should blast. ...Potentially tricky note here is that it's hard to cross ref the ID with the taxa viewer. Can't visualized easily. 


Alpha Rarefaction and Selecting a Rarefaction Depth
===================================================

Although sequencing depth in a microbiome sample does not directly relate to the original biomass in a community, the relative sequencing depth has a large impact on observed communities (`Weiss et al, 2017`_). Therefore, for most diversity metrics, a normalization approach is needed.

Current best practices suggest the use of rarefaction, a normalizational via sub-sampling without replacement. Rarefaction occurs in two steps: first, samples which are below the rarefaction depth are filtered out of the feature table. Then, all remaining samples are subsampled without replacement to get to the sequencing depth. It’s both important and sometimes challenging to select a rarefaction depth for diversity analyses. Several strategies exist to figure out an appropriate rarefaction depth - we will primarily consider alpha rarefaction in this tutorial, because it is a data-driven way to approach the problem.

We’ll use ``qiime diversity alpha-rarefaction`` to subsample the ASV table at different depths (between ``--p-min-depth`` and
``--p-max-depth``) and calculate the alpha diversity using one or more metrics (``--p-metrics``). When we checked the feature table,  we found that the sample with the fewest sequences in the deblurred table has 85 sequences and that the sample with the most has 4996 sequences. We want to set a maximum depth close to the maximum number of sequences. We also know that if we look at a sequencing depth around 4250 sequences per sample, we’ll be looking at information from  22 samples. So, let’s set this as our maximum sequencing depth.

At each sampling depth, 10 rarified tables are usually calculated to provide an error estimate, although this can be adjusted using the ``--p-iterations`` parameter. We can check and see if there is a relationship between the alpha diversity and metadata by passing the metadata file into the ``--m-metadata-file`` parameter.

.. command-block::

   qiime diversity alpha-rarefaction \
     --i-table ./dada2_table.qza \
     --m-metadata-file ./metadata.tsv \
     --o-visualization ./alpha_rarefaction_curves.qzv \
     --p-min-depth 10 \
     --p-max-depth 4250

The visualization file will give us two curves. The top curve will give the alpha diversity (observed OTUs or shannon) as a function of the sequencing depth. This is used to determine whether the richness or evenness has saturated based on the sequencing depth. The rarefaction curve should “level out” as you approach a sequencing depth. Failure to do so, especially with a diversity-only metric such as observed OTUs or Faith’s PD diversity, may indicate that the richness in the samples has not been fully saturated.

The second curve shows the number of samples in each group at each sequencing depth. This is useful to determine the sampling depth where samples are lost, and whether this may be biased by metadata group. Remember that rarefaction is a two step process and samples which do not meet the rarefaction depth are filtered out of the table. So, we can use the curves to look at the number of samples by different metadata categories.

If you’re still unsure of the rarefaction depth, you can also use the sample summary to look at which samples are lost by supplying sample metadata to the feature table summary.

*Hint*: We generated this after we built the feature table.

.. question::

   Start by opening the rarefaction curves.

   1. Are all metadata columns represented in the visualization? If not, which columns were excluded and why?
   2. Which metric shows saturation and stabilization of the diversity?
   3. Which mouse genetic background has higher diversity, based on the curve? Which has shallower sequencing depth?

   Now, let's check the feature table summary.

   4. What percentage of samples are lost if we set the rarefaction depth to 2500 sequences per sample?
   5. Which mice did the missing samples come from?

.. 1. We can't look at the days since transplant (this is a numeric column)
.. 2. shannon. Always shannon. Shannon is a good justification for rarefaction. Just ignore the observed ASVs behind the curtain
.. 3. suspectible has higher diversity, wild type had a shallower sequencing depth
.. 4. we lose 8% of samples (4 samples).
.. 5. The samples come from mouse 457, 469, 537, and 538.

After we've looked through the data, we need to select a rarefaction depth. In general, rarefaction depth is a place where an analyst needs to use their discretion. Selecting a rarefaction depth is an exercise in minimizing sequence loss while maximizing the sequences retained for diversity analysis. For high biomass samples (fecal, oral, etc), a general best estimate is a rarefaction depth of no less than 1000 sequences per sample. In low biomass samples where sequencing is shallower, a lower rarefaction depth may be selected although it’s important to keep in mind that the diversity measurements on these samples will be quite noisy and the overall quality will be low.

.. checkpoint::

   *Based on the current rarefaction curve and sample summary, what sequencing depth would you pick? Why?*

   In this case, we can retain 47 samples with a rarefaction depth of 2000 sequences/sample. 

   Based on the sequencing depth and distribution of samples, we'll use 2000 sequences/sample for this analysis. This will let us keep 47 of 48 high quality samples (discarding the one sample with sequencing depth below 1000 sequences/sample).


Diversity Analysis
==================

The first step in hypothesis testing in microbial ecology should be looking at within- (alpha) and between sample (beta) diversity. We can calculate diversity metrics, apply appropriate statistical tests, and visualize the data using the ``q2-diversity`` plug in.

We’ll start by using the ``qiime diversity core-metrics-phylogenetic`` method which ratifies the input feature table, calculates several commonly used alpha and beta diversity metrics, and produces PCoA visualizations in Emperor for the beta diversity metrics. By default, the metrics computed are:

-  **Alpha Diversity**

   -  Shannon’s diversity index
   -  Observed OTUs
   -  Faith’s phylogenetic Diversity
   -  Pielou’s Evenness

-  **Beta Diversity**

   -  Jaccard distance
   -  Bray Curtis distance
   -  Unweighted UniFrac distance
   -  Weighted UniFrac distance

There is a very good discussion of diversity metrics and their meanings in a `qiime forum by Stephanie Orchanian`_.

This method wraps several other methods, and it’s worthwhile to note that the steps in ``qiime diversity core-metrics-phylogenetic`` can be executed independently.

One important consideration for diversity calculations is the rarefaction depth. Above, we used the alpha rarefaction visualization and the sample summary visualization to pick a rarefaction depth. So, for these analyses, we’ll use a depth of 1000 sequences per sample.

.. command-block::

   qiime diversity core-metrics-phylogenetic \
     --i-table ./dada2_table.qza \
     --i-phylogeny ./tree.qza \
     --m-metadata-file ./metadata.tsv \
     --p-sampling-depth 2000 \
     --output-dir ./core-metrics-results

Alpha Diversity
---------------

Alpha diversity asks whether the distribution of features within a sample differ between different conditions. The comparison makes no assumptions about the features that are shared between samples; two samples can have the same alpha diversity and not share any features. The rarified alpha diversity produced by ``q2-diversity`` is a univariate, continuous value and can be tested using common non-parametric statistical tests.

Let’s test the relationship between the phylogenetic alpha diversity and evenness and our covariates of interest.

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

   For this exercise, we'll look at the group significance results for Faith's phylogenetic diversity and evenness.

   Based on the group significance test, is there a difference in phylogenetic diversity by genotype? Is there a difference based on the donor?

.. There is no difference in evenness by genotype, but hte difference in phylogenetic diversity is borderline signfiicant (p=0.0508)
.. there is a difference in both evenness and PD by donor

If we had a continuous covariate that we thought was associated with the alpha diversity, we could test that using ``qiime diversity alpha-correlation``. However, the only continuous variable in this dataset is the days since transplant.

Beta Diversity
--------------

Next, we’ll compare the structure of the microbiome communities using beta diversity. Start by making a visual inspection of the principle coordinates plots (PCoA) plots that were generated by emperor and ``core-metrics-results/weighted_unifrac_emperor.qzv``.

.. question::

   Open the unweighted UniFrac emperor plot (``core-metrics-results/unweighted_unifrac_emperor.qzv``) first. Can you find separation in the data? If so, can you find a metadata factor that reflects the seperation? What if you used weighted UniFrac distance (``core-metrics-results/weighted_unifrac_emperor.qzv``)?

   One of the major concerns in mouse studies is that sometimes differences in communities are due to natural variation in cages. Do you see clustering by cage?

.. The major seperation in unweighted UniFrac dhsould be due to donor. 
.. we see some clustering by cage, but the points are mixed

Now, let’s analyze the statistical trends using `PERMANOVA`_. Permanova tests the hypothesis that samples within a group are more similar to each other than they are to samples in another group. To put it another way, it tests whether the within-group distances from each group are different from the between group distance. We expect samples that are similar to have smaller distances from each other, so if our hypothesis that one group is different from another is true, we’d expect the within-group distances to be smaller than the between group distance.

Let’s use the command to test whether the donor identity (which we identified as a major separator in PCoA space) is associated with significant differences in weighted and unweighted UniFrac distance.

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

Let’s also check whether there’s a relationship between cage where a mouse lives and the beta diversity, since this is often an important technical effect to consider. Since we have several cages, we’ll use the ``--p-pairwise`` parameter that will let us check whether there are individual differences between the cages driving the difference. This may be useful, since if we check the metadata, we may find that cage is nested by donor.

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

We can use the adonis function to look at a multivariate model. Let’s look at the intersection between donor and genotype.

.. command-block::

   qiime diversity adonis \
     --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file metadata.tsv \
     --o-visualization core-metrics-results/unweighted_adonis.qzv \
     --p-formula genotype+donor

.. do we also want permadisp here?

.. question::
   Is there a significant effect of donor?

   From the metadata, we know that cage C31, C32, and C42 all belong to the same donor, and that cages C43, C44, and C49 belong to the other. Is there a significant difference in the microbial communities between samples collected in cage C31 and C32? How about between C31 and C43? Do the results look the way you expect, based on the boxplots for donor?

   If you adjust for donor in the adonis model, do you retain an effect of genotype? What percentage of the variation does genotype explain?

.. Yep, donor is a significant and large effect, as we expected from the PCoA
.. Overall, cage is significant but some of this is drive by between donor differences. 
.. genotype is significant after adjusting for donor (p=~0.02) and explains about 4.25% of the variation, but heck, we'll take it


Taxonomy Barchart
=================

Since we see a difference in diversity, we may want to look at the taxonomy associated with the features. Now, let’s build a taxonomic barchart of the samples we analyzed in the diversity dataset.

To do this, we first need to filter out any samples with fewer sequences than our rarefaction threshold. We can filter samples using the ``q2-feature-table`` plugin with the ``filter-samples`` method. This is a dynamic function that lets us filter our table based on a variety of criteria such as the number of counts (frequency, ``--p-min-frequency`` and ``--p-max-frequency``), number of features (``--p-min-features`` and ``--p-max-features``), on sample metadata (``--p-where``).

For this example, we need to filter out samples with fewer sequences than our rarefaction depth.

.. command-block::

   qiime feature-table filter-samples \
     --i-table ./dada2_table.qza \
     --p-min-frequency 2000 \
     --o-filtered-table ./table_2k.qza

Now, let’s use the filtered table to build an interactive barplot of the taxonomy in the sample.

.. command-block::

   qiime taxa barplot \
     --i-table ./table_2k.qza \
     --i-taxonomy ./taxonomy.qza \
     --m-metadata-file ./metadata.tsv \
     --o-visualization ./taxa_barplot.qzv

.. question::

   Visualize the data at level 2 (phylum level) and sort the samples by donor, then by genotype. Can you observe a consistent difference in phylum between the donors? Does this surprising you? Why or why not?

.. No clear difference by phylum by donor. Not shocking given these are based on fecal samples from adults. Hopefully also maybe highlights the fact that phylum level isn't necessarily a good way to compare differential abundance. 

Differential Abundance with ANCOM
=================================

Microbiome data is inherently sparse (has a lot of zeros) and compositional (everything adds up to 1). Because of this, traditional statistical methods that you may be familiar with such as anova or t-test are not appropriate for the data and lead to a high false positive rate. ANCOM is a compositionally aware alternative that allows to test for differentially abundant features. If you’re unfamiliar with the technique, it’s worthwhile to review the `ANCOM paper`_ to better understand the method.

Before we being, we're going to filter out low abundance/low prevelance ASVs. Filtering can provide better resolution and limit FDR penalty on features that are too far below the noise threshhold to be applicable to a statistical test. A feature that shows up with 10 counts may be a real feature that is present only in htat sample, may be a feature that's present in several samples but only got amplified and sequenced in one sample because PCR is a somewhat stocahastic process, or it may be noise. It's not possible to tell, so feature-based analysis may be better after filtering low abundance features. However, filtering also shifts the composition of a sample further disrupting the relationship. Here, the filtering is performed as trade off between the model, computation, and statistical 

.. command-block::

   qiime feature-table filter-features \
     --i-table ./table_2k.qza \
     --p-min-frequency 50 \
     --p-min-samples 4 \
     --o-filtered-table ./table_2k_abund.qza

ANCOM fundamentally operates on a ``FeatureTable[Frequency]`` which is based on the frequencies of features on a per-sample basis. However, ANCOM cannot tolerate zeros (because compositional methods typically use a log-transform or a ratio and you can’t take the log or divide by zeros). To remove the zeros from our table, we add a pseudocount to the ``FeatureTable[Frequency]`` object, creating a ``FeatureTable[Composition]`` in its place.

.. command-block::

   qiime composition add-pseudocount \
     --i-table ./table_2k_abund.qza \
     --o-composition-table ./table2k_abund_comp.qza

Let’s use ANCOM to check whether there is a difference in the mice based on their donor and then by their genetic background. The test will calculate the number of ratios between pairs of ASVs are significantly different with fdr-corrected p < 0.05.

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

When you open the ANCOM visualizations, you’ll see a volcano plot on top which relates the ANCOM W statistical to the CLR (center log transform) for the groups. The W statistic is the number of tests whether the ratio between a given pair of ASVs is significant at the test threshold (typically FDR-adjusted p < 0.05). Because differential abundance in ANCOM is based on the ratio between tests, it does not produce a traditional p-value.

.. question::

   Open the ANCOM visualizations for the donor and genotype and the taxonomy visualization artifact.

   1. Are there more differentially abundant features between the donors or the mouse genotype? Did you expect this result based on the beta diversity?
   2. Are there any features that are differentially abundant in both the donors and by genotype?
   3. How many differentially abundant features are there between the two genotypes? Using the percentile abundances and volcano plot as a guide, can you tell if they are more abundant in wild type or susceptible mice?
   4. Use taxonomy metadata visualization and search sequence identifiers for the significantly different features by genotype. What genera do they belong to?

.. More differentially abundant features by donor than genotype. Not suprising given the size of donor in b-div vs the size of genotype
.. Nope. Whoo! :celebrate:
.. There are three 3 features that are differentially abundant. All three are more abundant in WT mice
.. ac5402de1ddf427ab8d2b0a8a0a44f19: g__Bacteriodetes; 79280cea51a6fe8a3432b2f266dd34db: g__Faecalibacterium (prausnitzii); 3017f87a3b0f5200ed54eca17eef3cbb: f__[Mogibacteriaceae]

Longitudinal Analysis
=====================

This study includes a longitudinal component; samples from each mouse were collected 7, 14, 21, and 49 days post fecal transplant. We can use the ``q2-longitudinal`` plug-in to explore the hypothesis that a mouse’s genetic background affected the change in the microbial community of each mouse. For this longitudinal analysis, we’re going to focus on beta diversity. Alpha diversity changes wildly in infants, but it’s often stable in adults over short time periods. We’re dealing with an adult fecal community over a relatively short time period, and there is no difference in alpha diversity with time. The :doc:`longitudinal analysis tutorial <longitudinal>` is an excellent resource for exploring changes samples.

PCoA-based analyses
-------------------

We can start by exploring temporal change in the PCoA using the animations tab.

.. question::

   Open the unweighted UniFrac emperor plot and color the samples by mouse id. Click on the “animations” tab and animate using the ``day_post_transplant`` as your gradient and ``mouse_id`` as your trajectory. Do you observe any clear temporal trends based on the PCoA?

   What happens if you color by ``day_post_transplant``? Do you see a difference based on the day? *Hint: Trying changing the colormap to a sequential colormap like viridis.*

.. No clear pattern based on animations


A volitility plot will let us look at patterns of variation variation along principle coordinate axes starting from same point. This can be helpful since inter-individual variation can be large and instead lets of focus instead of the changes. 

Let's use the ``q2-longitudinal`` plugin to look at how samples from an individual move along each PC. The ``--m-metadata-file`` column can take several types, including a metadata file (like our ``metadata.tsv``) as well as a ``SampleData[AlphaDiversity]``, ``SampleData[Distance]`` (which we’ll use later), or a ``PCoA`` artifact.

.. command-block::

   qiime longitudinal volatility \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-file ./core-metrics-results/unweighted_unifrac_pcoa_results.qza \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id \
     --o-visualization ./pc_vol.qzv

.. question::

    Using the controls, look at variation in cage along PCs 1, 2, and 3. What kind of patterns do you see with time along each axis?

.. In this version, there's seperation, but not a lot of temporal trends.

Distance-based analysis
-----------------------

Now, let’s try looking directly at the distance. Here, we’ll test the hypothesis that genotype affects the magnitude of the change in the distance from the first sample (7 days post transplant). We assume that given the rate of turn over in a microbial community, we might expect to see a change in the community over time. However, here we’ll ask if the genotype changes things.

We’ll start this analysis by looking at how much the microbial community of each mouse changes from the the first sample (7 days post transplant).

.. command-block::

   qiime longitudinal first-distances \
     --i-distance-matrix ./core-metrics-results/unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file ./metadata.tsv \
     --o-first-distances ./from_first_unifrac.qza \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id

We can again use volatility analysis to visualize the change in beta diversity based on distance.

.. command-block::

   qiime longitudinal volatility \
     --m-metadata-file ./metadata.tsv \
     --m-metadata-file ./from_first_unifrac.qza \
     --p-state-column days_post_transplant \
     --p-individual-id-column mouse_id \
     --p-default-metric Distance \
     --o-visualization ./from_first_unifrac_vol.qzv

.. question::

   Based on the volatility plot, does one donor change more over time than the other? What about by genotype? Cage?

.. samples from the hc change more over time; cage42 shows a lot of volitility. there isnt as much temporal change by genotype but there is some seperation

A linear mixed effects (LME) model lets us test whether there’s a relationship between a dependent variable and one or more independent variables in an experiment using repeated measures. Since we’re interested in genotype, we should use this as an independent predictor.

For our experiment, we’re currently interested in the change in distance from the initial timepoint, so we’ll use this as our outcome variable (given by ``--p-metric``).

``q2-longitudinal`` also requires a state column (``--p-state-column``) which designates the time component in the metadata, and an individual identifier (``--p-individual-id-column``). Which columns should we use in our data?

We can build a model either using the ``--p-formula`` parameter or the ``--p-group-columns`` parameter. For this analysis, we’re interested in whether genotype affects the longitudinal change in the microbial community. However, we also know from our cross sectional analysis that donor plays a large role in shaping the fecal community. So, we should also probably include that in this analysis. We may also want to consider cage effect in our experiment, since this is a common confounder in rodent studies. However, the original experimental design here was clever: although cages were grouped by donor (mice are coprophagic), they were of mixed genotype. This partial randomization helps limit some of the cage effects we might otherwise see.

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

Now, let’s look at the results of the models.

.. question::

   Now, let’s open the linear mixed effects model. Is there a significant association between the genotype and temporal change? Which genotype is more stable (has lower variation)? Is there a temporal change associated with the donor? Did you expect or not expect this based on the volatility plot results? Can you find an interaction between the donor and genotype?

.. yes, there's a significant association. The susceptable mice are more stable. There isn't a statistically significant difference based on donor though. the interaction between donor and genotype is significant.

Synthesis
=========

Based on the results of the analysis, we can say that there is a difference in the microbial communities of these mice based on their donor and genetic background. (This recapitulates the results of the original analysis.)

We found that the donor is the primary driver of alpha diversity.

But, we saw differences by donor and genotype based on beta diversity. Using the PCoA, we can see clear separation between the mice from the two donors (this recapitulates the results of the original paper). After adjusting for the donor, we saw a significant difference between the genotypes.

Although there wasn’t a clear pattern in the barchart at the phylum level between donors or genotypes, we were still able to find ASVs which differentiated the genotypes at using ANCOM. There was no overlap between these ASVs in the donor and genetic background, supporting the hypothesis that the difference due to genotype is seperate from the difference due to donor.

The volatility plots and temporal analysis showed the microbiome in different genetic backgrounds changed differently over time.

This suggests that there is an effect on the microbiome of mice receiving fecal transplants due to genotype.

.. Next steps?
.. ===========

.. Refereences

.. _Sampson et al, 2016:  https://www.ncbi.nlm.nih.gov/pubmed/27912057
.. _PRJEB17694: https://www.ebi.ac.uk/ena/data/view/PRJEB17694
.. _qiita: www.qiita.ucsd.edu
.. _EMP 515f-806r: http://www.earthmicrobiome.org/protocols-and-standards/16s/
.. _absolute path: https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths
.. _q2-dbOTU: https://library.qiime2.org/plugins/q2-dbotu/4/
.. _Dada2: https://www.ncbi.nlm.nih.gov/pubmed/27214047
.. _Deblur: https://www.ncbi.nlm.nih.gov/pubmed/28289731
.. _Nearing et al, 2018: https://www.ncbi.nlm.nih.gov/pubmed/30123705
.. _Bokulich et al, 2013: https://www.ncbi.nlm.nih.gov/pubmed/23202435
.. _Weiss et al, 2017: https://www.ncbi.nlm.nih.gov/pubmed/28253908
.. _qiime forum by Stephanie Orchanian: https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282/
.. _view.qiime2.org: http://www.view.qiime2.org/
.. _PERMANOVA: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1442-9993.2001.01070.pp.x
.. _ancom paper: https://www.ncbi.nlm.nih.gov/pubmed/26028277
.. _Google Sheet: https://data.qiime2.org/2019.7/tutorials/pd-mice/sample_metadata
