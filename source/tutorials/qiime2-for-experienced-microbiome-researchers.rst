QIIME 2 for Experienced Microbiome Researchers
##############################################


.. contents:: QIIME 2 for Experienced Microbiome Researchers
   :depth: 3

In this document, we'll go over how to use QIIME 2 to process microbiome data.
This tutorial is intended for experienced microbiome researchers who already know how to process data and need to know the **QIIME 2 commands pertaining to specific steps in 16S processing**.

The :doc:`QIIME 2 overview tutorial <overview>` contains a more theoretical overview of microbiome data processing.

Why switch to QIIME 2?
----------------------

Transitioning to QIIME 2 can be difficult for users who are used to processing data with their own tools and scripts, and who want fine control over every step in the process.
We understand the frustrating learning curve for experienced microbiome researchers, but believe that
the community, open-sourced nature, and commitment to reproducible science make switching to QIIME 2 worth any initial frustrations.

By providing a common framework for microbiome data analysis, QIIME 2 brings together a **vibrant and inclusive community**.
By joining the QIIME 2 community as an established microbiome researcher, you will automatically be connected to other leaders in this field and can more easily work together to propel the development and implementation of best practices in microbiome research for broad use.
The QIIME 2 community includes both established leaders in microbiome research as well as newcomers: all are encouraged to participate and learn from each other.
The `QIIME 2 forum <https://forum.qiime2.org/>`__ contains a wealth of information on how to perform microbiome data processing and analysis, as well as fruitful discussion on best practices in this space.

QIIME 2 also encourages making **microbiome research more reproducible**.
QIIME 2 reduces inappropriate analyses by defining specific data types and restricting methods only to their appropriate data type inputs.
It also keeps track of everything that's been done to a given data file in the :doc:`provenance <../concepts>` metadata associated with each QIIME 2 artifact.

Furthermore, by wrapping tools into a common framework, **data processing pipelines are streamlined**.
With QIIME 2, most data processing workflows can be consolidated into one (or a few) bash scripts, reducing the number of different programs or executables you need to call and the number of re-formatting data steps that are necessary.

Finally, QIIME 2 is **open-sourced and specifically designed for experienced researchers to contribute and expand the reach of their work.**
Any tool can be added to QIIME 2 as a :doc:`plugin <../plugins/index>`, which can be written for any software, package, or other installable executables.
Writing a QIIME 2 plugin for a method that you develop instantly makes it accessible and usable by thousands of users.

Pro-tips for power users
~~~~~~~~~~~~~~~~~~~~~~~~

That said, here are a few tips we've learned that should substantially improve your experience in transitioning your workflows to QIIME 2:

**Pro-tip #1: QIIME 2 artifacts are just zip files**.
If at any point you want to look at what actual files are in the ``.qza`` artifact, you can use :doc:`qiime tools export <exporting>` to extract the data file directly (which is basically just a wrapper for ``unzip``).
Alternatively, you can also unzip your artifact directly (``unzip -k file.qza``) and look through the files in the ``data/`` folder.

**Pro-tip #2: the QIIME 2 command line interface tools are slow because they have to unzip and re-zip the data contained in the artifacts each time you call them.**
If you need to process your data more interactively, you might want to use the Python API - it is much faster since objects can be simply stored in memory.
You can learn more about the different `QIIME 2 interfaces <https://docs.qiime2.org/2018.6/interfaces/>`__.

Data processing steps
---------------------

The processing steps we'll cover in this tutorial include:

1. Importing raw sequence (FASTQ) data into QIIME 2
2. Demultiplexing data (i.e. mapping each sequence to the sample it came from)
3. Removing non-biological parts of the sequences (i.e. primers)
4. Performing quality control and:

   -  denoising sequences with DADA2 or deblur, and/or
   -  quality filtering, length trimming, and clustering with VSEARCH or dbOTU

5. Assigning taxonomy
6. Analyze data and gain insight!

The :doc:`overview tutorial <overview>` and :doc:`list of available plugins <../plugins/available/index>` can give you ideas for additional possible processing and analysis steps.

Importing data into QIIME 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Relevant plugin**: ``qiime tools import``

If you're using QIIME 2 to process your data, the first thing you need to do is get that data into a format that QIIME 2 can understand.
Various importing methods currently available in QIIME 2 are highlighted in the :doc:`QIIME 2 importing tutorial <importing>`.

This step has the potential to be the most confusing part of the QIIME 2 pipeline as there are dozens of import and format types to choose from.
To see a full list of available import/format types use: ``qiime tools import --show-importable-formats`` and ``qiime tools import --show-importable-types``

If you're importing FASTQ data that you've generated, you'll likely need to generate a :ref:`manifest file <manifest file>`, which is just a text file that  maps each FASTQ file to its sample ID and direction (if applicable).

If you have sequencing data with one of two very specific formats (:ref:`EMP <emp import>` or :ref:`Casava <casava import>`), you can directly import the folder containing your sequencing files with
the ``--type EMPSingleEndSequences`` or ``--type 'SampleData[PairedEndSequencesWithQuality]'`` flags (or their respective paired-end types).
Otherwise if you don't have one of these two very specific formats, you'll need to make the manifest file to give ``import`` instructions on what and how to import your files.

If you want to import FASTA files or a feature table directly, you can also do that by using a different ``--type`` flag for ``qiime tools import``.
The :doc:`importing tutorial <importing>` goes through all these options in detail.

Demultiplexing sequences
~~~~~~~~~~~~~~~~~~~~~~~~

**Relevant plugins**

- :doc:`q2-demux <../plugins/available/demux/index>`
- :doc:`cutadapt <../plugins/available/cutadapt/index>`

If you have reads from multiple samples in the same file, you'll need to demultiplex your sequences.

If your barcodes have already been removed from the reads and are in a separate file, you can use :doc:`q2-demux <../plugins/available/demux/emp-paired/>` to demultiplex these.

If your barcodes are still in your sequences, you can use functions from the :doc:`cutadapt
plugin <../plugins/available/cutadapt/index>`.
The ``cutadapt demux-single`` method looks for barcode sequences at the beginning of your reads (5' end) with a certain error tolerance, removes them, and returns sequence data separated by each sample.
The QIIME 2 forum has a `tutorial on various functions available in cutadapt <https://forum.qiime2.org/t/demultiplexing-and-trimming-adapters-from-reads-with-q2-cutadapt/2313>`__, including demultiplexing.
You can learn more about how ``cutadapt`` works under the hood by reading their `documentation <https://cutadapt.readthedocs.io/en/stable/index.html>`__.

Note: Currently ``q2-demux`` and ``q2-cutadapt`` do not support demultiplexing dual-barcoded paired-end sequences, but only can demultiplex with barcodes in the forward reads.
So for the time being, this type of demultiplexing needs to be done outside of QIIME 2 using other tools, for example
`bcl2fastq <https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software.html>`__.

.. _`merge reads`:

Merging reads
~~~~~~~~~~~~~~

**Relevant plugin**: :doc:`q2-vsearch <../plugins/available/vsearch/index>`

Whether or not you need to merge reads depends on how you plan to cluster or denoise your sequences into amplicon sequence variants (ASVs) or operational taxonomic units (OTUs).
If you plan to use deblur or OTU clustering methods next, join your sequences now.
If you plan to use dada2 to denoise your sequences, do not merge — dada2 performs read merging automatically after denoising each sequence.

If you need to merge your reads, you can use the QIIME 2 :doc:`q2-vsearch plugin <../plugins/available/vsearch/index>`  with the :doc:`join-pairs <../plugins/available/vsearch/join-pairs/>` method.

.. _`Remove non-biological sequences`:

Removing non-biological sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Relevant plugins**

- :doc:`q2-cutadapt <../plugins/available/cutadapt/index>`
- :doc:`dada2 </plugins/available/dada2/index>`

If your data contains any non-biological sequences (e.g. primers, sequencing adapters, PCR spacers, etc), you should remove these.

The :doc:`q2-cutadapt <../plugins/available/cutadapt/index>` plugin has comprehensive methods for removing non-biological sequences from :doc:`paired-end <../plugins/available/cutadapt/trim-paired/>` or :doc:`single-end <../plugins/available/cutadapt/trim-single/>` data.

If you're going to use DADA2 to denoise your sequences, you can remove biological sequences at the same time as you call the denoising function.
All of DADA2's ``denoise`` fuctions have some sort of ``--p-trim`` parameter you can specify to remove base pairs from the 5' end of your reads.
(Deblur does not have this functionality yet.)

Grouping similar sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two main approaches for grouping similar sequences together: denoising and clustering.
The :ref:`overview tutorial <Denoising>` provides more in-depth discussion of these approaches.

Regardless of how you group your sequences, the grouping methods will output:

1. A list of representative sequences for each of your OTUs and/or ASVs (QIIME 2 data format ``FeatureData[Sequence]``), and
2. A feature table which indicates how many reads of each OTU/sequence variants were observed in each sample. (QIIME 2 data format ``FeatureTable[Frequency]``)

DADA2 and deblur will also produce a stats summary file with useful information regarding the filtering and denoising.

Denoising
~~~~~~~~~

**Relevant plugins**:

- :doc:`dada2 </plugins/available/dada2/index>`
- :doc:`deblur <../plugins/available/deblur/index>`

DADA2 and deblur are currently the two denoising methods available in QIIME 2.
You can read more about the methods in the :ref:`overview tutorial <Denoising>`.

DADA2 and deblur both output exact sequence variants, which supposedly represent the true biological sequences present in your data.
Their creators have different terminology for these sequences (DADA2 calls them "amplicon sequence variants" (ASVs) and deblur calls them "sub-OTUs").
We'll be using the ASV terminology throughout this tutorial to refer to both outputs.

Preparing data for denoising
''''''''''''''''''''''''''''

Denoising requires little data preparation.
Both DADA2 and deblur perform quality filtering, denoising, and chimera removal, so you shouldn't need to perform any quality screening prior to running them.
That said, the deblur developers recommend doing an initial :ref:`quality-filter <moving pictures deblur>` with default settings prior to using deblur (as illustrated in the :ref:`"Moving Pictures" tutorial <moving pictures deblur>`).
Q-score based filtering is built in to DADA2, so doing this `quality-filter` step prior to denoising with DADA2 is unnecessary.

Both methods have an option to truncate your reads to a constant length (which occurs prior to denoising).
In DADA2, this is the `--p-trunc-len` parameter; in deblur it's `--p-trim-length`.
The truncating parameter is optional for both DADA2 and deblur (though if you're using deblur you'll need to specify `--p-trim-length -1` to disable truncation).
Reads shorter than the truncation length are discarded and reads longer are truncated at that position.
The overview tutorial has more discussion on deciding what length you should truncate to.

Denoising with DADA2
''''''''''''''''''''

The :doc:`DADA2 plugin </plugins/available/dada2/index>` has multiple methods to denoise reads:

* :doc:`denoise paired-end <../plugins/available/dada2/denoise-paired/>` requires unmerged, paired-end reads (i.e. both forward and reverse).
* :doc:`denoise single-end <../plugins/available/dada2/denoise-single/>` accepts either single-end or unmerged paired-end data. If you give it unmerged paired-end data, it will only use the forward reads (and do nothing with the reverse reads).
* :doc:`denoise-pyro <../plugins/available/dada2/denoise-pyro/>` accepts ion torrent data.

Note that DADA2 may be slow on very large datasets. You can increase the number of threads to use with the ``--p-n-threads`` parameter.

Denoising with deblur
''''''''''''''''''''''

The :doc:`deblur <../plugins/available/deblur/index>` plugin has two methods to denoise sequences:

* :doc:`denoise-16S <../plugins/available/deblur/denoise-16S/>` denoises 16S sequences.
* :doc:`denoise-other <../plugins/available/deblur/denoise-other/>` denoises other types of sequences.

If you use ``denoise-16S``, deblur performs an initial positive filtering step where it discards any reads which do not have a minimum 60% identity similarity to sequences from the 85% OTU GreenGenes database.
If you don't want to do this step, use the ``denoise-other`` method.

deblur can currently only denoise single-end reads.
It will accept unmerged paired-end reads as input, it just won't do anything with the reverse reads.
Note that deblur *can* take in *merged* reads and treat them as single-end reads, so you might want to merge your reads first if you're denoising with deblur.

OTU Clustering
~~~~~~~~~~~~~~

In this tutorial, we'll cover QIIME 2 methods that perform :doc:`de novo  <../plugins/available/vsearch/cluster-features-de-novo/>` and :doc:`closed reference <../plugins/available/vsearch/cluster-features-closed-reference/>` clustering.
The QIIME :doc:`OTU clustering tutorial <otu-clustering>` also covers these in more detail.

To cluster your sequences, you need to make sure that:

-  paired-end reads are merged
-  non-biological sequences are removed
-  reads are all trimmed to the same length
-  low-quality reads are discarded

We discussed merging paired-end reads and removing non-biological sequences above (Sections `Merge reads`_ and `Remove non-biological sequences`_).

Once your data are ready, you'll also need to dereplicate your reads before clustering.

Length trimming
'''''''''''''''

If for some reason your raw reads are not already all the same length, you'll need to trim them to the same length before doing OTU clustering.
There isn't currently a QIIME 2 function to trim reads to the same length without doing anything else, though you may be able to use functions from the ``cutadapt`` plugin to do something like that.
(The reason for this is that the :ref:`QIIME 2 workflow <Denoising>` recommends first denoising reads - which involves a length trimming step - and then optionally passing the ASVs through a clustering algorithm.)

Quality filtering
'''''''''''''''''

**Relevant plugin**: :doc:`quality-filter <../plugins/available/quality-filter/index>`

You can perform different types of quality filtering with the :doc:`quality filter <../plugins/available/quality-filter/index>` plugin.
The `q-score` method is for single- or paired-end sequences (i.e. `SampleData[PairedEndSequencesWithQuality | SequencesWithQuality]`) while `q-score-joined` is for joined reads (i.e. `SampleData[JoinedSequencesWithQuality]` after merging).
The option descriptions for each method cover the different types of available quality filtering.

Dereplicating sequences
'''''''''''''''''''''''

**Relevant plugin**: :doc:`q2-vsearch <../plugins/available/vsearch/index>`

No matter which type of clustering you do, you first need to dereplicate your sequences. The :doc:`q2-vsearch <../plugins/available/vsearch/index>` plugin's method :doc:`dereplicate-sequences  <../plugins/available/vsearch/dereplicate-sequences/>` performs this step.

de novo clustering
''''''''''''''''''

**Relevant plugins**:

- :doc:`q2-vsearch <../plugins/available/vsearch/index>`
- `q2-dbotu <https://library.qiime2.org/plugins/q2-dbotu/>`__

Sequences can be clustered *de novo* based on their genetic similarity alone (i.e. with VSEARCH) or based on a combination of their genetic similarity and abundance distributions (i.e. with distribution-based clustering).

-  **Similarity-based clustering.** The `q2-vsearch` plugin method :doc:`cluster-features-de-novo <../plugins/available/vsearch/cluster-features-de-novo/>` clusters OTUs. You can change the genetic similarity threshold with the ``--p-perc-identity`` parameter. The plugin wraps the VSEARCH ``--cluster_size`` function.
-  **Distribution-based clustering** incorporates the similarity between sequences and their abundance distribution to identify ecologically meaningful populations. You can learn more about this method in the `plugin documentation <https://github.com/cduvallet/q2-dbotu>`__, `original paper <http://dx.doi.org/10.1128/AEM.00342-13>`__, and the `re-implementation update paper <https://doi.org/10.1371/journal.pone.0176335>`__. The ``call-otus`` function in the `q2-dbotu <https://github.com/cduvallet/q2-dbotu>`__ plugin performs distribution-based clustering on input data.

Both of these functions take as input the output of ``q2-vsearch dereplicate-sequences``, which are dereplicated sequences with QIIME 2 data type ``'FeatureData[Sequence]'``, and a table of counts with QIIME 2 data type ``'FeatureTable[Frequency]'``.

closed reference clustering
'''''''''''''''''''''''''''

**Relevant plugin**: :doc:`q2-vsearch <../plugins/available/vsearch/index>`

Closed reference clustering groups sequences together which match the same reference sequence in a database with a certain similarity.

VSEARCH can do closed reference clustering with the :doc:`cluster-features-closed-reference <../plugins/available/vsearch/cluster-features-closed-reference/>` method.
This method wraps the ``--usearch_global`` VSEARCH function.
You can decide which reference database to cluster against with the ``--i-reference-sequences`` flag.
The input file to this flag should be a ``.qza`` file containing a fasta file with the sequences to use as references, with QIIME 2 data type ``FeatureData[Sequence]``.
Most people use GreenGenes or SILVA for 16S rRNA gene sequences, but others curate their own databases or use other standard references (e.g. UNITE for ITS data).
You can download the references from the links on the :ref:`QIIME 2 data resources page <marker gene db>`.
You'll need to unzip/untar and import them as ``FeatureData[Sequence]`` artifacts, since they're provided as raw data files.

Assigning taxonomy
~~~~~~~~~~~~~~~~~~

**Relevant plugin**: :doc:`feature-classifier <../plugins/available/feature-classifier/index>`

Assigning taxonomy to ASV or OTU representative sequences is covered in the :ref:`taxonomy classification
tutorial <Taxonomy>`.
All taxonomy assignment methods are in the :doc:`feature-classifier plugin <../plugins/available/feature-classifier/index>`.

There are two main approaches for assigning taxonomy, each with multiple methods available.

The first involves aligning reads to reference databases directly:

- :doc:`classify-consensus-blast <../plugins/available/feature-classifier/classify-consensus-blast/>`: BLAST+ local alignment
- :doc:`classify-consensus-vsearch <../plugins/available/feature-classifier/classify-consensus-vsearch/>`:  VSEARCH global alignment

Both use the *consensus* approach of taxonomy assignment, which you can learn more about in the :ref:`overview <Taxonomy>` and tweak with the ``maxaccepts``, ``perc-identity``, and ``min-consensus`` parameters.

The second approach uses a machine learning classifier to assign likely taxonomies to reads, and can be used through the :doc:`classify-sklearn <../plugins/available/feature-classifier/classify-sklearn/>` method.

This method needs a pre-trained model to classify the sequences: you can either download one of the pre-trained taxonomy classifiers from the :doc:`data resources page <../data-resources/>`, or train one yourself (following the steps outlined in the :doc:`feature classifier tutorial <feature-classifier>`).
(You can also learn a lot more about the specific models implemented in `the plugin's associated paper <https://doi.org/10.1186/s40168-018-0470-z>`__.)

Analyze feature table and gain insight
--------------------------------------

**Relevant plugins**: :doc:`Many! <../plugins/available/index>`

At this point, you should be ready to analyze your feature table to answer your scientific questions!
QIIME 2 offers multiple built-in functions to analyze your data, and you can also `export <Export the data>`_ it to do downstream analyses in your preferred coding language or software package.

Some general things you can do with QIIME 2 are:

-  **Look at the data:** QIIME 2 has a nice :doc:`taxa barplot visualizer <../plugins/available/taxa/barplot/>` to make visually exploring your data easy. You can also visualize your data on a PCoA plot with the :doc:`emperor <../plugins/available/emperor/plot/>` plugin (after calculating beta diversity between samples).
-  **Build a phylogenetic tree:** QIIME 2 has a :doc:`phylogeny <../plugins/available/phylogeny/index>` plugin with different tree-building methods.
-  **Calculate alpha diversity of your samples:** the :doc:`diversity plugin <../plugins/available/diversity/index>` has many `alpha diversity metrics <https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282>`__ available through the ``alpha`` and ``alpha-phylogenetic`` methods.
-  **Calculate beta diversity between samples:** the :doc:`diversity plugin <../plugins/available/diversity/index>` also has these metrics available in the ``beta``, ``beta-phylogenetic``, and ``beta-phylogenetic-alt`` methods. Note that the ``diversity core-metrics`` and ``diversity core-metrics-phylogenetic`` pipelines are a handy wrapper for alpha and beta diversity analyses. These are described in the :ref:`overview tutorial <Diversity>`.
-  **Test for differences between samples**, through differential abundance or distribution testing: PERMANOVA, ANOSIM, ANCOM, and Gneiss are some of the relevant methods which are available in QIIME 2. PERMANOVA and ANOSIM can be done with the :doc:`beta-group-significance <../plugins/available/diversity/beta-group-significance/>` method in the ``diversity`` plugin. ANCOM is available in the :doc:`composition <../plugins/available/composition/index>` plugin. Gneiss is available in the :doc:`gneiss <../plugins/available/gneiss/index>` plugin, and has an associated tutorial, :doc:`"Differential abundance  analysis with gneiss" <gneiss/>`.
-  **Build machine learning classifiers and regressors to make predictions:** the :doc:`q2-sample-classifier <../plugins/available/sample-classifier/index>` plugin has several actions for building classifiers and regressors, and the associated :doc:`"Predicting sample metadata values with q2-sample-classifier" tutorial <sample-classifier>` provides more details.

Export the data
~~~~~~~~~~~~~~~

**Relevant plugin**: ``qiime tools export``

If you're a veteran microbiome scientist and don't want to use QIIME 2 for your analyses, you can extract your feature table and sequences from the artifact using the :doc:`export <exporting>` tool.
While ``export`` only outputs the data, the :ref:`extract <export vs extract>` tool allows you to also extract other metadata such as the citations, provenance etc.

Note that this places generically named files (e.g. ``feature-table.txt``) into the output directory, so you may want to immediately rename the files to something more information (or somehow ensure that they stay in their original directory)!

You can also use the handy `qiime2R <https://github.com/jbisanz/qiime2R>`__ package to import QIIME 2 artifacts directly into R.

New plugins
------------

You can explore QIIME 2's ever-growing list of
:doc:`plugins <../plugins/available/index>` to find other methods to apply to your data.

And remember that you can also :doc:`make your own QIIME 2 plugins <../plugins/developing>` to add functionality to QIIME 2 and share it with the community!
