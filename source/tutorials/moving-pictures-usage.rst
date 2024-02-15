"Moving Pictures" tutorial - Multiple Interface Edition
=======================================================

Beta preview note
-----------------

This guide is a beta preview of new functionality in QIIME 2 that aims to
support development of multi-interface tutorials.

Introduction
------------

.. note::
   This guide assumes you have installed QIIME 2 using one of the procedures in
   the :doc:`install documents <../install/index>`.

.. note::
   This guide uses QIIME 2-specific terminology, please see the :doc:`glossary
   <../glossary>` for more details.

In this tutorial you'll use QIIME 2 to perform an analysis of human microbiome
samples from two individuals at four body sites at five timepoints, the first
of which immediately followed antibiotic usage. A study based on these samples
was originally published in `Caporaso et al. (2011)`_. The data used in this
tutorial were sequenced on an Illumina HiSeq using the `Earth Microbiome
Project`_ hypervariable region 4 (V4) 16S rRNA sequencing protocol.

.. qiime1-users::
   These are the same data that are used in the QIIME 1 `Illumina Overview
   Tutorial`_.

Sample metadata
---------------

.. usage-selector::

Before starting the analysis, explore the sample metadata to familiarize
yourself with the samples used in this study. The `sample metadata`_ is
available as a Google Sheet. You can download this file as tab-separated text
by selecting ``File`` > ``Download as`` > ``Tab-separated values``.
Alternatively, the following command will download the sample metadata as
tab-separated text and save it in the file ``sample-metadata.tsv``. This
``sample-metadata.tsv`` file is used throughout the rest of the tutorial.

.. usage::

   def md_factory():
       from urllib import request
       from qiime2 import Metadata
       fp, _ = request.urlretrieve(
           'https://data.qiime2.org/2024.2/tutorials/moving-pictures/sample_metadata.tsv',
       )

       return Metadata.load(fp)

   sample_metadata = use.init_metadata('sample_metadata', md_factory)

.. tip::
   `Keemei`_ is a Google Sheets add-on for validating sample metadata.
   Validation of sample metadata is important before beginning any analysis.
   Try installing Keemei following the instructions on its website, and then
   validate the sample metadata spreadsheet linked above. The spreadsheet also
   includes a sheet with some invalid data to try out with Keemei.

.. tip::
   To learn more about metadata, including how to format your metadata for use
   with QIIME 2, check out :doc:`the metadata tutorial <metadata>`.

Obtaining and importing data
----------------------------

.. usage-selector::

Download the sequence reads that we'll use in this analysis. In this tutorial
we'll work with a small subset of the complete sequence data so that the
commands will run quickly.

.. usage::
   def emp_factory():
       import os
       import tempfile
       from urllib import request

       from q2_demux._format import EMPSingleEndDirFmt
       from q2_types.per_sample_sequences import FastqGzFormat

       base_url = 'https://data.qiime2.org/2024.2/tutorials/moving-pictures/'
       bc_url = base_url + 'emp-single-end-sequences/barcodes.fastq.gz'
       seqs_url = base_url + 'emp-single-end-sequences/sequences.fastq.gz'

       fmt = EMPSingleEndDirFmt(mode='w')

       with tempfile.TemporaryDirectory() as tmpdir:
           bc_fp = os.path.join(tmpdir, 'barcodes.fastq.gz')
           bc_fn, _ = request.urlretrieve(bc_url, bc_fp)

           seqs_fp = os.path.join(tmpdir, 'sequences.fastq.gz')
           seqs_fn, _ = request.urlretrieve(seqs_url, seqs_fp)

           fmt.barcodes.write_data(bc_fn, FastqGzFormat)
           fmt.sequences.write_data(seqs_fn, FastqGzFormat)

       fmt.validate()
       return fmt

   raw_seqs = use.init_format('emp-single-end-sequences', emp_factory)


All data that is used as input to QIIME 2 is in form of QIIME 2 artifacts,
which contain information about the type of data and the source of the data.
So, the first thing we need to do is import these sequence data files into a
QIIME 2 artifact.

The semantic type of this QIIME 2 artifact is ``EMPSingleEndSequences``.
``EMPSingleEndSequences`` QIIME 2 artifacts contain sequences that are
multiplexed, meaning that the sequences have not yet been assigned to samples
(where the ``barcodes.fastq.gz`` contains the barcode read associated
with each sequence in ``sequences.fastq.gz``.) To learn about how to import
sequence data in other formats, see the :doc:`importing data tutorial
<importing>`.

.. usage::

   emp_single_end_sequences = use.import_from_format(
       'emp_single_end_sequences',
       'EMPSingleEndSequences',
       raw_seqs,
   )

It is possible to check the UUID, type, and format of your newly-imported
sequences, confirming that your import worked as expected:

.. usage::

   use.peek(emp_single_end_sequences)

.. tip::
   Links are included to view and download precomputed QIIME 2 artifacts and
   visualizations created by commands in the documentation. For example, the
   command above created a single ``emp-single-end-sequences.qza`` file, and a
   corresponding precomputed file is linked above. You can view precomputed
   QIIME 2 artifacts and visualizations without needing to install additional
   software (e.g. QIIME 2).

.. qiime1-users::
   In QIIME 1, we generally suggested performing demultiplexing through QIIME
   (e.g., with ``split_libraries.py`` or ``split_libraries_fastq.py``) as this
   step also performed quality control of sequences. We now separate the
   demultiplexing and quality control steps, so you can begin QIIME 2 with
   either multiplexed sequences (as we're doing here) or demultiplexed
   sequences.

.. TODO: uncomment when/if this doc becomes canon:  .. _`moving pics demux`:

Demultiplexing sequences
------------------------

.. usage-selector::

To demultiplex sequences we need to know which barcode sequence is associated
with each sample. This information is contained in the `sample metadata`_ file.
You can run the following commands to demultiplex the sequences (the ``demux
emp-single`` command refers to the fact that these sequences are barcoded
according to the `Earth Microbiome Project`_ protocol, and are single-end
reads). The ``demux.qza`` QIIME 2 artifact will contain the demultiplexed
sequences. The second output (``demux-details.qza``) presents Golay error
correction details, and will not be explored in this tutorial (you can
visualize these data using ``qiime metadata tabulate``).

.. usage::

   barcode_sequence = use.get_metadata_column(
       'barcode_sequence', 'barcode-sequence', sample_metadata)

   demux, demux_details = use.action(
       use.UsageAction(plugin_id='demux', action_id='emp_single'),
       use.UsageInputs(
           seqs=emp_single_end_sequences,
           barcodes=barcode_sequence,
       ),
       use.UsageOutputNames(
           per_sample_sequences='demux',
           error_correction_details='demux_details',
       ),
   )

After demultiplexing, it's useful to generate a summary of the demultiplexing
results. This allows you to determine how many sequences were obtained per
sample, and also to get a summary of the distribution of sequence qualities at
each position in your sequence data.

.. usage::

   use.action(
       use.UsageAction(plugin_id='demux', action_id='summarize'),
       use.UsageInputs(data=demux),
       use.UsageOutputNames(visualization='demux'),
   )

.. note::
   All QIIME 2 visualizers (i.e., commands that take a ``--o-visualization``
   parameter) will generate a ``.qzv`` file. You can view these files in q2cli
   with ``qiime tools view``. We provide the command to view this first
   visualization, but for the remainder of this tutorial we'll tell you to
   *view the resulting visualization* after running a visualizer, which means
   that you should run ``qiime tools view`` on the .qzv file that was
   generated.

   .. command-block::
      :no-exec:

      qiime tools view demux.qzv

   Alternatively, you can view QIIME 2 artifacts and visualizations at
   `view.qiime2.org <https://view.qiime2.org>`__ by uploading files or
   providing URLs. There are also precomputed results that can be viewed or
   downloaded after each step in the tutorial. These can be used if you're
   reading the tutorial, but not running the commands yourself.

Sequence quality control and feature table construction
-------------------------------------------------------

.. usage-selector::

QIIME 2 plugins are available for several quality control methods, including
`DADA2`_, `Deblur`_, and `basic quality-score-based filtering`_. In this
tutorial we present this step using `DADA2`_ and `Deblur`_. These steps are
interchangeable, so you can use whichever of these you prefer. The result of
both of these methods will be a ``FeatureTable[Frequency]`` QIIME 2 artifact,
which contains counts (frequencies) of each unique sequence in each sample in
the dataset, and a ``FeatureData[Sequence]`` QIIME 2 artifact, which maps
feature identifiers in the ``FeatureTable`` to the sequences they represent.

.. note::
   As you work through one or both of the options in this section, you'll
   create artifacts with filenames that are specific to the method that you're
   running (e.g., the feature table that you generate with ``dada2
   denoise-single`` will be called ``table-dada2.qza``). After creating these
   artifacts you'll rename the artifacts from one of the two options to more
   generic filenames (e.g., ``table.qza``). This process of creating a specific
   name for an artifact and then renaming it is only done to allow you to
   choose which of the two options you'd like to use for this step, and then
   complete the tutorial without paying attention to that choice again. It's
   important to note that in this step, or any step in QIIME 2, the filenames
   that you're giving to artifacts or visualizations are not important.

.. qiime1-users::
   The ``FeatureTable[Frequency]`` QIIME 2 artifact is the equivalent of the
   QIIME 1 OTU or BIOM table, and the ``FeatureData[Sequence]`` QIIME 2
   artifact is the equivalent of the QIIME 1 *representative sequences* file.
   Because the "OTUs" resulting from `DADA2`_ and `Deblur`_ are created by
   grouping unique sequences, these are the equivalent of 100% OTUs from QIIME
   1, and are generally referred to as *sequence variants*. In QIIME 2, these
   OTUs are higher resolution than the QIIME 1 default of 97% OTUs, and they're
   higher quality since these quality control steps are better than those
   implemented in QIIME 1. This should therefore result in more accurate
   estimates of diversity and taxonomic composition of samples than was
   achieved with QIIME 1.

Option 1: DADA2
~~~~~~~~~~~~~~~

`DADA2`_ is a pipeline for detecting and correcting (where possible) Illumina
amplicon sequence data. As implemented in the ``q2-dada2`` plugin, this quality
control process will additionally filter any phiX reads (commonly present in
marker gene Illumina sequence data) that are identified in the sequencing data,
and will filter chimeric sequences.

The ``dada2 denoise-single`` method requires two parameters that are used in
quality filtering: ``--p-trim-left m``, which trims off the first ``m`` bases
of each sequence, and ``--p-trunc-len n`` which truncates each sequence at
position ``n``. This allows the user to remove low quality regions of the
sequences. To determine what values to pass for these two parameters, you
should review the *Interactive Quality Plot* tab in the ``demux.qzv`` file that
was generated by ``qiime demux summarize`` above.

.. question::
   Based on the plots you see in ``demux.qzv``, what values would you choose
   for ``--p-trunc-len`` and ``--p-trim-left`` in this case?

In the ``demux.qzv`` quality plots, we see that the quality of the initial
bases seems to be high, so we won't trim any bases from the beginning of the
sequences. The quality seems to drop off around position 120, so we'll truncate
our sequences at 120 bases. This next command may take up to 10 minutes to run,
and is the slowest step in this tutorial.

.. usage::

   rep_seqs_dada2, table_dada2, stats_dada2 = use.action(
       use.UsageAction(plugin_id='dada2', action_id='denoise_single'),
       use.UsageInputs(demultiplexed_seqs=demux, trim_left=0, trunc_len=120),
       use.UsageOutputNames(representative_sequences='rep_seqs',
                            table='table', denoising_stats='stats')
   )

.. usage::

   stats_as_md = use.view_as_metadata('stats_dada2_md', stats_dada2)

   use.action(
       use.UsageAction(plugin_id='metadata', action_id='tabulate'),
       use.UsageInputs(input=stats_as_md),
       use.UsageOutputNames(visualization='stats')
   )

.. TODO: uncomment when/if this doc becomes canon:  .. _`moving pictures deblur`:

Option 2: Deblur
~~~~~~~~~~~~~~~~

`Deblur`_ uses sequence error profiles to associate erroneous sequence reads
with the true biological sequence from which they are derived, resulting in
high quality sequence variant data. This is applied in two steps. First, an
initial quality filtering process based on quality scores is applied. This
method is an implementation of the quality filtering approach described by
`Bokulich et al. (2013)`_.

.. usage::

   filtered_seqs, filter_stats = use.action(
       use.UsageAction(plugin_id='quality_filter', action_id='q_score'),
       use.UsageInputs(demux=demux),
       use.UsageOutputNames(filtered_sequences='demux_filtered',
                            filter_stats='demux_filter_stats')
   )

.. note::
   In the `Deblur`_ paper, the authors used different quality-filtering
   parameters than what `they currently recommend after additional analysis
   <https://qiita.ucsd.edu/static/doc/html/deblur_quality.html>`_. The
   parameters used here are based on those more recent recommendations.

Next, the Deblur workflow is applied using the ``qiime deblur denoise-16S``
method. This method requires one parameter that is used in quality filtering,
``--p-trim-length n`` which truncates the sequences at position ``n``. In
general, the Deblur developers recommend setting this value to a length where
the median quality score begins to drop too low. On these data, the quality
plots (prior to quality filtering) suggest a reasonable choice is in the 115 to
130 sequence position range. This is a subjective assessment. One situation
where you might deviate from that recommendation is when performing a
meta-analysis across multiple sequencing runs. In this type of meta-analysis,
it is critical that the read lengths be the same for all of the sequencing runs
being compared to avoid introducing a study-specific bias. Since we already
using a trim length of 120 for ``qiime dada2 denoise-single``, and since 120 is
reasonable given the quality plots, we'll pass ``--p-trim-length 120``. This
next command may take up to 10 minutes to run.

.. usage::

   rep_seqs_deblur, table_deblur, stats_deblur = use.action(
        use.UsageAction(plugin_id='deblur', action_id='denoise_16S'),
        use.UsageInputs(demultiplexed_seqs=filtered_seqs, trim_length=120,
                        sample_stats=True),
        use.UsageOutputNames(representative_sequences='rep_seqs_deblur',
                             table='table_deblur', stats='deblur_stats'),
   )

.. note::
   The two commands used in this section generate QIIME 2 artifacts containing
   summary statistics. To view those summary statistics, you can visualize them
   using ``qiime metadata tabulate`` and ``qiime deblur visualize-stats``,
   respectively:

.. usage::

   filter_stats_as_md = use.view_as_metadata('filter_stats', filter_stats)

   use.action(
        use.UsageAction(plugin_id='metadata', action_id='tabulate'),
        use.UsageInputs(input=filter_stats_as_md),
        use.UsageOutputNames(visualization='demux_filter_stats'),
   )

   use.action(
        use.UsageAction(plugin_id='deblur', action_id='visualize_stats'),
        use.UsageInputs(deblur_stats=stats_deblur),
        use.UsageOutputNames(visualization='deblur_stats'),
   )

If you'd like to continue the tutorial using this ``FeatureTable`` (as opposed
to the DADA2 feature table generated in *Option 1*), run the following
commands.

.. usage::

   use.comment('q2cli:')
   use.comment('mv rep-seqs-deblur.qza rep-seqs.qza')
   use.comment('mv table-deblur.qza table.qza')
   use.comment('')
   use.comment('Artifact API:')
   use.comment('table = table_deblur')
   use.comment('rep_seqs = rep_seqs_deblur')

FeatureTable and FeatureData summaries
--------------------------------------

.. usage-selector::

After the quality filtering step completes, you'll want to explore the
resulting data. You can do this using the following two commands, which will
create visual summaries of the data. The ``feature-table summarize`` command
will give you information on how many sequences are associated with each sample
and with each feature, histograms of those distributions, and some related
summary statistics. The ``feature-table tabulate-seqs`` command will provide a
mapping of feature IDs to sequences, and provide links to easily BLAST each
sequence against the NCBI nt database. The latter visualization will be very
useful later in the tutorial, when you want to learn more about specific
features that are important in the data set.

.. usage::

   use.action(
        use.UsageAction(plugin_id='feature_table', action_id='summarize'),
        use.UsageInputs(table=table_dada2, sample_metadata=sample_metadata),
        use.UsageOutputNames(visualization='table'),
   )

   use.action(
        use.UsageAction(plugin_id='feature_table', action_id='tabulate_seqs'),
        use.UsageInputs(data=rep_seqs_dada2),
        use.UsageOutputNames(visualization='rep_seqs'),
   )

Generate a tree for phylogenetic diversity analyses
---------------------------------------------------

.. usage-selector::

QIIME supports several phylogenetic diversity metrics, including Faith's
Phylogenetic Diversity and weighted and unweighted UniFrac. In addition to
counts of features per sample (i.e., the data in the
``FeatureTable[Frequency]`` QIIME 2 artifact), these metrics require a rooted
phylogenetic tree relating the features to one another. This information will
be stored in a ``Phylogeny[Rooted]`` QIIME 2 artifact. To generate a
phylogenetic tree we will use ``align-to-tree-mafft-fasttree`` pipeline from
the ``q2-phylogeny`` plugin.

First, the pipeline uses the ``mafft`` program to perform a multiple sequence
alignment of the sequences in our ``FeatureData[Sequence]`` to create a
``FeatureData[AlignedSequence]`` QIIME 2 artifact. Next, the pipeline masks (or
filters) the alignment to remove positions that are highly variable. These
positions are generally considered to add noise to a resulting phylogenetic
tree. Following that, the pipeline applies FastTree to generate a phylogenetic
tree from the masked alignment. The FastTree program creates an unrooted tree,
so in the final step in this section midpoint rooting is applied to place the
root of the tree at the midpoint of the longest tip-to-tip distance in the
unrooted tree.

.. usage::

   _, _, _, rooted_tree = use.action(
        use.UsageAction(plugin_id='phylogeny', action_id='align_to_tree_mafft_fasttree'),
        use.UsageInputs(sequences=rep_seqs_dada2),
        use.UsageOutputNames(alignment='aligned_rep_seqs',
                             masked_alignment='masked_aligned_rep_seqs',
                             tree='unrooted_tree', rooted_tree='rooted_tree'),
   )

.. TODO: uncomment when/if this doc becomes canon:  .. _`moving pics diversity`:

Alpha and beta diversity analysis
---------------------------------

.. usage-selector::

QIIME 2's diversity analyses are available through the ``q2-diversity`` plugin,
which supports computing alpha and beta diversity metrics, applying related
statistical tests, and generating interactive visualizations. We'll first apply
the ``core-metrics-phylogenetic`` method, which rarefies a
``FeatureTable[Frequency]`` to a user-specified depth, computes several alpha
and beta diversity metrics, and generates principle coordinates analysis (PCoA)
plots using Emperor for each of the beta diversity metrics. The metrics
computed by default are:

* Alpha diversity

  * Shannon's diversity index (a quantitative measure of community richness)
  * Observed Features (a qualitative measure of community richness)
  * Faith's Phylogenetic Diversity (a qualitative measure of community
    richness that incorporates phylogenetic relationships between the features)
  * Evenness (or Pielou's Evenness; a measure of community evenness)

* Beta diversity

  * Jaccard distance (a qualitative measure of community dissimilarity)
  * Bray-Curtis distance (a quantitative measure of community dissimilarity)
  * unweighted UniFrac distance (a qualitative measure of community
    dissimilarity that incorporates phylogenetic relationships between the
    features)
  * weighted UniFrac distance (a quantitative measure of community
    dissimilarity that incorporates phylogenetic relationships between the
    features)

An important parameter that needs to be provided to this script is
``--p-sampling-depth``, which is the even sampling (i.e. rarefaction) depth.
Because most diversity metrics are sensitive to different sampling depths
across different samples, this script will randomly subsample the counts from
each sample to the value provided for this parameter. For example, if you
provide ``--p-sampling-depth 500``, this step will subsample the counts in each
sample without replacement so that each sample in the resulting table has a
total count of 500. If the total count for any sample(s) are smaller than this
value, those samples will be dropped from the diversity analysis. Choosing this
value is tricky. We recommend making your choice by reviewing the information
presented in the ``table.qzv`` file that was created above. Choose a value that
is as high as possible (so you retain more sequences per sample) while
excluding as few samples as possible.

.. question::
   View the ``table.qzv`` QIIME 2 artifact, and in particular the *Interactive
   Sample Detail* tab in that visualization. What value would you choose to
   pass for ``--p-sampling-depth``? How many samples will be excluded from your
   analysis based on this choice? How many total sequences will you be
   analyzing in the ``core-metrics-phylogenetic`` command?

.. usage::

   core_metrics_results = use.action(
        use.UsageAction(plugin_id='diversity', action_id='core_metrics_phylogenetic'),
        use.UsageInputs(phylogeny=rooted_tree, table=table_dada2,
                        sampling_depth=1103, metadata=sample_metadata),
        use.UsageOutputNames(rarefied_table='rarefied_table',
                             faith_pd_vector='faith_pd_vector',
                             observed_features_vector='observed_features_vector',
                             shannon_vector='shannon_vector',
                             evenness_vector='evenness_vector',
                             unweighted_unifrac_distance_matrix='unweighted_unifrac_distance_matrix',
                             weighted_unifrac_distance_matrix='weighted_unifrac_distance_matrix',
                             jaccard_distance_matrix='jaccard_distance_matrix',
                             bray_curtis_distance_matrix='bray_curtis_distance_matrix',
                             unweighted_unifrac_pcoa_results='unweighted_unifrac_pcoa_results',
                             weighted_unifrac_pcoa_results='weighted_unifrac_pcoa_results',
                             jaccard_pcoa_results='jaccard_pcoa_results',
                             bray_curtis_pcoa_results='bray_curtis_pcoa_results',
                             unweighted_unifrac_emperor='unweighted_unifrac_emperor',
                             weighted_unifrac_emperor='weighted_unifrac_emperor',
                             jaccard_emperor='jaccard_emperor',
                             bray_curtis_emperor='bray_curtis_emperor'),
   )
   faith_pd_vec = core_metrics_results.faith_pd_vector
   evenness_vec = core_metrics_results.evenness_vector
   unweighted_unifrac_dm = core_metrics_results.unweighted_unifrac_distance_matrix
   unweighted_unifrac_pcoa = core_metrics_results.unweighted_unifrac_pcoa_results
   bray_curtis_pcoa=core_metrics_results.bray_curtis_pcoa_results

Here we set the ``--p-sampling-depth`` parameter to 1103. This value was chosen
based on the number of sequences in the ``L3S313`` sample because it's close to
the number of sequences in the next few samples that have higher sequence
counts, and because it is considerably higher (relatively) than the number of
sequences in the samples that have fewer sequences. This will allow us to
retain most of our samples. The three samples that have fewer sequences will be
dropped from the ``core-metrics-phylogenetic`` analyses and anything that uses
these results. It is worth noting that all three of these samples are "right
palm" samples. Losing a disproportionate number of samples from one metadata
category is not ideal. However, we are dropping a small enough number of
samples here that this felt like the best compromise between total sequences
analyzed and number of samples retained.

.. note::
   The sampling depth of 1103 was chosen based on the DADA2 feature table
   summary. If you are using a Deblur feature table rather than a DADA2 feature
   table, you might want to choose a different even sampling depth. Apply the
   logic from the previous paragraph to help you choose an even sampling depth.

.. note::
   In many Illumina runs you'll observe a few samples that have very low
   sequence counts. You will typically want to exclude those from the analysis
   by choosing a larger value for the sampling depth at this stage.

After computing diversity metrics, we can begin to explore the microbial
composition of the samples in the context of the sample metadata. This
information is present in the `sample metadata`_ file that was downloaded
earlier.

We'll first test for associations between categorical metadata columns and
alpha diversity data. We'll do that here for the Faith Phylogenetic Diversity
(a measure of community richness) and evenness metrics.

.. usage::

   use.action(
        use.UsageAction(plugin_id='diversity', action_id='alpha_group_significance'),
        use.UsageInputs(alpha_diversity=faith_pd_vec, metadata=sample_metadata),
        use.UsageOutputNames(visualization='faith_pd_group_significance'),
   )

   use.action(
        use.UsageAction(plugin_id='diversity', action_id='alpha_group_significance'),
        use.UsageInputs(alpha_diversity=evenness_vec, metadata=sample_metadata),
        use.UsageOutputNames(visualization='evenness_group_significance'),
   )

.. question::
   Which categorical sample metadata columns are most strongly associated with
   the differences in microbial community **richness**? Are these differences
   statistically significant?

.. question::
   Which categorical sample metadata columns are most strongly associated with
   the differences in microbial community **evenness**? Are these differences
   statistically significant?

In this data set, no continuous sample metadata columns (e.g.,
``days-since-experiment-start``) are correlated with alpha diversity, so we
won't test for those associations here. If you're interested in performing
those tests (for this data set, or for others), you can use the ``qiime
diversity alpha-correlation`` command.

Next we'll analyze sample composition in the context of categorical metadata
using PERMANOVA (first described in `Anderson (2001)`_) using the
``beta-group-significance`` command. The following commands will test whether
distances between samples within a group, such as samples from the same body
site (e.g., gut), are more similar to each other then they are to samples from
the other groups (e.g., tongue, left palm, and right palm). If you call this
command with the ``--p-pairwise`` parameter, as we'll do here, it will also
perform pairwise tests that will allow you to determine which specific pairs of
groups (e.g., tongue and gut) differ from one another, if any. This command can
be slow to run, especially when passing ``--p-pairwise``, since it is based on
permutation tests. So, unlike the previous commands, we'll run
``beta-group-significance`` on specific columns of metadata that we're
interested in exploring, rather than all metadata columns to which it is
applicable. Here we'll apply this to our unweighted UniFrac distances, using
two sample metadata columns, as follows.

.. usage::

   body_site_col = use.get_metadata_column('body_site', 'body-site', sample_metadata)

   use.action(
        use.UsageAction(plugin_id='diversity', action_id='beta_group_significance'),
        use.UsageInputs(distance_matrix=unweighted_unifrac_dm,
                        metadata=body_site_col, pairwise=True),
        use.UsageOutputNames(visualization='unweighted_unifrac_body_site_group_significance'),
   )

   subject_col = use.get_metadata_column('subject', 'subject', sample_metadata)

   use.action(
        use.UsageAction(plugin_id='diversity', action_id='beta_group_significance'),
        use.UsageInputs(distance_matrix=unweighted_unifrac_dm,
                        metadata=subject_col, pairwise=True),
        use.UsageOutputNames(visualization='unweighted_unifrac_subject_group_significance'),
   )

.. question::
   Are the associations between subjects and differences in microbial
   composition statistically significant? How about body sites? What specific
   pairs of body sites are significantly different from each other?

Again, none of the continuous sample metadata that we have for this data set
are correlated with sample composition, so we won't test for those associations
here. If you're interested in performing those tests, you can use the ``qiime
metadata distance-matrix`` in combination with ``qiime diversity mantel`` and
``qiime diversity bioenv`` commands.

Finally, ordination is a popular approach for exploring microbial community
composition in the context of sample metadata. We can use the `Emperor`_ tool
to explore principal coordinates (PCoA) plots in the context of sample
metadata. While our ``core-metrics-phylogenetic`` command did already generate
some Emperor plots, we want to pass an optional parameter, ``--p-custom-axes``,
which is very useful for exploring time series data. The PCoA results that were
used in ``core-metrics-phylogeny`` are also available, making it easy to
generate new visualizations with Emperor. We will generate Emperor plots for
unweighted UniFrac and Bray-Curtis so that the resulting plot will contain axes
for principal coordinate 1, principal coordinate 2, and days since the
experiment start. We will use that last axis to explore how these samples
changed over time.

.. usage::

   use.action(
        use.UsageAction(plugin_id='emperor', action_id='plot'),
        use.UsageInputs(pcoa=unweighted_unifrac_pcoa, metadata=sample_metadata,
                        custom_axes=['days-since-experiment-start']),
        use.UsageOutputNames(visualization='unweighted-unifrac-emperor-days-since-experiment-start'),
   )

   use.action(
        use.UsageAction(plugin_id='emperor', action_id='plot'),
        use.UsageInputs(pcoa=bray_curtis_pcoa, metadata=sample_metadata,
                        custom_axes=['days-since-experiment-start']),
        use.UsageOutputNames(visualization='bray-curtis-emperor-days-since-experiment-start'),
   )

.. question::
   Do the Emperor plots support the other beta diversity analyses we've
   performed here? (Hint: Experiment with coloring points by different
   metadata.)

.. question::
   What differences do you observe between the unweighted UniFrac and
   Bray-Curtis PCoA plots?

Alpha rarefaction plotting
--------------------------

.. usage-selector::

In this section we'll explore alpha diversity as a function of sampling depth
using the ``qiime diversity alpha-rarefaction`` visualizer. This visualizer
computes one or more alpha diversity metrics at multiple sampling depths, in
steps between 1 (optionally controlled with ``--p-min-depth``) and the value
provided as ``--p-max-depth``. At each sampling depth step, 10 rarefied tables
will be generated, and the diversity metrics will be computed for all samples
in the tables. The number of iterations (rarefied tables computed at each
sampling depth) can be controlled with ``--p-iterations``. Average diversity
values will be plotted for each sample at each even sampling depth, and samples
can be grouped based on metadata in the resulting visualization if sample
metadata is provided with the ``--m-metadata-file`` parameter.

.. usage::

   use.action(
       use.UsageAction(plugin_id='diversity', action_id='alpha_rarefaction'),
       use.UsageInputs(table=table_dada2, phylogeny=rooted_tree,
                       max_depth=4000, metadata=sample_metadata),
       use.UsageOutputNames(visualization='alpha_rarefaction'),
   )

The visualization will have two plots. The top plot is an alpha rarefaction
plot, and is primarily used to determine if the richness of the samples has
been fully observed or sequenced. If the lines in the plot appear to "level
out" (i.e., approach a slope of zero) at some sampling depth along the x-axis,
that suggests that collecting additional sequences beyond that sampling depth
would not be likely to result in the observation of additional features. If the
lines in a plot don't level out, this may be because the richness of the
samples hasn't been fully observed yet (because too few sequences were
collected), or it could be an indicator that a lot of sequencing error remains
in the data (which is being mistaken for novel diversity).

The bottom plot in this visualization is important when grouping samples by
metadata. It illustrates the number of samples that remain in each group when
the feature table is rarefied to each sampling depth. If a given sampling depth
``d`` is larger than the total frequency of a sample ``s`` (i.e., the number of
sequences that were obtained for sample ``s``), it is not possible to compute
the diversity metric for sample ``s`` at sampling depth ``d``. If many of the
samples in a group have lower total frequencies than ``d``, the average
diversity presented for that group at ``d`` in the top plot will be unreliable
because it will have been computed on relatively few samples. When grouping
samples by metadata, it is therefore essential to look at the bottom plot to
ensure that the data presented in the top plot is reliable.

.. note::
   The value that you provide for ``--p-max-depth`` should be determined by
   reviewing the "Frequency per sample" information presented in the
   ``table.qzv`` file that was created above. In general, choosing a value that
   is somewhere around the median frequency seems to work well, but you may
   want to increase that value if the lines in the resulting rarefaction plot
   don't appear to be leveling out, or decrease that value if you seem to be
   losing many of your samples due to low total frequencies closer to the
   minimum sampling depth than the maximum sampling depth.

.. question::
   When grouping samples by "body-site" and viewing the alpha rarefaction plot
   for the "observed_features" metric, which body sites (if any) appear to
   exhibit sufficient diversity coverage (i.e., their rarefaction curves level
   off)? How many sequence variants appear to be present in those body sites?

.. question::
   When grouping samples by "body-site" and viewing the alpha rarefaction plot
   for the "observed_features" metric, the line for the "right palm" samples
   appears to level out at about 40, but then jumps to about 140. What do you
   think is happening here? (Hint: be sure to look at both the top and bottom
   plots.)

.. TODO: uncomment when/if this doc becomes canon: .. _`moving pics taxonomy`:

Taxonomic analysis
------------------

.. usage-selector::

In the next sections we'll begin to explore the taxonomic composition of the
samples, and again relate that to sample metadata. The first step in this
process is to assign taxonomy to the sequences in our ``FeatureData[Sequence]``
QIIME 2 artifact. We'll do that using a pre-trained Naive Bayes classifier and
the ``q2-feature-classifier`` plugin. This classifier was trained on the
Greengenes 13_8 99% OTUs, where the sequences have been trimmed to only include
250 bases from the region of the 16S that was sequenced in this analysis (the
V4 region, bound by the 515F/806R primer pair). We'll apply this classifier to
our sequences, and we can generate a visualization of the resulting mapping
from sequence to taxonomy.

.. note::
   Taxonomic classifiers perform best when they are trained based on your
   specific sample preparation and sequencing parameters, including the primers
   that were used for amplification and the length of your sequence reads.
   Therefore in general you should follow the instructions in :doc:`Training
   feature classifiers with q2-feature-classifier
   <../tutorials/feature-classifier>` to train your own taxonomic classifiers.
   We provide some common classifiers on our :doc:`data resources page
   <../data-resources>`, including Silva-based 16S classifiers, though in the
   future we may stop providing these in favor of having users train their own
   classifiers which will be most relevant to their sequence data.

.. usage::

   def classifier_factory():
       from urllib import request
       from qiime2 import Artifact
       fp, _ = request.urlretrieve(
           'https://data.qiime2.org/2024.2/common/gg-13-8-99-515-806-nb-classifier.qza',
       )

       return Artifact.load(fp)

   classifier = use.init_artifact('gg-13-8-99-515-806-nb-classifier', classifier_factory)

.. usage::

   taxonomy, = use.action(
        use.UsageAction(plugin_id='feature_classifier', action_id='classify_sklearn'),
        use.UsageInputs(classifier=classifier, reads=rep_seqs_dada2),
        use.UsageOutputNames(classification='taxonomy'),
   )

   taxonomy_as_md = use.view_as_metadata('taxonomy_as_md', taxonomy)

   use.action(
        use.UsageAction(plugin_id='metadata', action_id='tabulate'),
        use.UsageInputs(input=taxonomy_as_md),
        use.UsageOutputNames(visualization='taxonomy'),
   )

.. question::
   Recall that our ``rep-seqs.qzv`` visualization allows you to easily BLAST
   the sequence associated with each feature against the NCBI nt database.
   Using that visualization and the ``taxonomy.qzv`` visualization created
   here, compare the taxonomic assignments with the taxonomy of the best BLAST
   hit for a few features. How similar are the assignments? If they're
   dissimilar, at what *taxonomic level* do they begin to differ (e.g.,
   species, genus, family, ...)?

Next, we can view the taxonomic composition of our samples with interactive bar
plots. Generate those plots with the following command and then open the
visualization.

.. usage::

   use.action(
        use.UsageAction(plugin_id='taxa', action_id='barplot'),
        use.UsageInputs(table=table_dada2, taxonomy=taxonomy,
                         metadata=sample_metadata),
        use.UsageOutputNames(visualization='taxa_bar_plots'),
   )

.. question::
   Visualize the samples at *Level 2* (which corresponds to the phylum level in
   this analysis), and then sort the samples by ``body-site``, then by
   ``subject``, and then by ``days-since-experiment-start``. What are the
   dominant phyla in each in ``body-site``? Do you observe any consistent
   change across the two subjects between ``days-since-experiment-start`` ``0``
   and the later timepoints?

Differential abundance testing with ANCOM-BC
--------------------------------------------

.. usage-selector::

ANCOM-BC can be applied to identify features that are differentially abundant
(i.e. present in different abundances) across sample groups. As with any
bioinformatics method, you should be aware of the assumptions and limitations
of ANCOM-BC before using it. We recommend reviewing the `ANCOM-BC paper`_ before
using this method.

.. note::
   Accurately identifying features that are differentially abundant across sample types in microbiome data is a challenging problem and an open area of research. There is one QIIME 2 plugin that can be used for this: ``q2-composition`` (used in this section). In addition to the methods contained in this plugin, new approaches for differential abundance testing are regularly introduced, and it’s worth assessing the current state of the field when performing differential abundance testing to see if there are new methods that might be useful for your data.

ANCOM-BC is a compositionally-aware linear regression model that allows for testing differentially abundant features across groups while also implementing bias correction, and is currently implemented in the ``q2-composition`` plugin.

Because we expect a lot of features to change in abundance across body sites, in this tutorial we'll filter our full feature table to only contain gut samples. We'll then apply ANCOM-BC to determine which, if any, sequence variants and genera are differentially abundant across the gut samples of our two subjects.

We'll start by creating a feature table that contains only the gut samples. (To
learn more about filtering, see the :doc:`Filtering Data <filtering>`
tutorial.)

.. usage::

   gut_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(table=table_dada2, metadata=sample_metadata,
                        where='[body-site]="gut"'),
        use.UsageOutputNames(filtered_table='gut_table'),
   )

ANCOM-BC operates on a FeatureTable[Frequency] QIIME 2 artifact. We can run ANCOM-BC on the subject column to determine what features differ in abundance across gut samples of the two subjects.

.. usage::

   ancombc_subject, = use.action(
        use.UsageAction(plugin_id='composition', action_id='ancombc'),
        use.UsageInputs(table=gut_table, metadata=sample_metadata, formula='subject'),
        use.UsageOutputNames(differentials='ancombc_subject'),
   )

   use.action(
      use.UsageAction(plugin_id='composition', action_id='da_barplot'),
      use.UsageInputs(data=ancombc_subject, significance_threshold=0.001),
      use.UsageOutputNames(visualization='da_barplot_subject'),
   )

.. question::
   1. Which ASV is most enriched, relative to the reference? Which is most depleted?
   2. What would you expect to change if the ``reference-level`` was changed from ``subject-1`` (the default) to ``subject-2``?

   .. 868528ca947bc57b69ffdf83e6b73bae (enriched), 4b5eeb300368260019c1fbc7a3c718fc (depleted)
   .. The direction of differental abundance (i.e. enriched features would be depleted and vice versa)

We're also often interested in performing a differential abundance test at a
specific taxonomic level. To do this, we can collapse the features in our
``FeatureTable[Frequency]`` at the taxonomic level of interest, and then re-run
the above steps. In this tutorial, we collapse our feature table at the genus
level (i.e. level 6 of the Greengenes taxonomy).

.. usage::

   l6_gut_table, = use.action(
        use.UsageAction(plugin_id='taxa', action_id='collapse'),
        use.UsageInputs(table=gut_table, taxonomy=taxonomy, level=6),
        use.UsageOutputNames(collapsed_table='gut_table_l6'),
   )

   l6_ancombc_subject, = use.action(
        use.UsageAction(plugin_id='composition', action_id='ancombc'),
        use.UsageInputs(table=l6_gut_table, metadata=sample_metadata, formula='subject'),
        use.UsageOutputNames(differentials='l6_ancombc_subject'),
   )

   use.action(
        use.UsageAction(plugin_id='composition', action_id='da_barplot'),
        use.UsageInputs(data=l6_ancombc_subject, significance_threshold=0.001),
        use.UsageOutputNames(visualization='l6_da_barplot_subject'),
   )

.. question::
   1. Which genera is most enriched? Which is most depleted?
   2. Do we see more differentially abundant features in the ``da-barplot-subject.qzv`` visualization, or in the ``l6-da-barplot-subject.qzv`` visualization? Why might you expect this?

.. g__Parabacteroides (enriched), g__Paraprevotella (depleted)
.. We see more differentially abundant features in the original compared to the collapsed table, which is reasonable since we are collapsing at the genus level and thus losing some resolution. However, collapsing at level 6 may allow us to investigate patterns that aren't present when looking at ASVs.

.. _sample metadata: https://data.qiime2.org/2024.2/tutorials/moving-pictures/sample_metadata
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
.. _ANCOM-BC paper: https://pubmed.ncbi.nlm.nih.gov/32665548/
