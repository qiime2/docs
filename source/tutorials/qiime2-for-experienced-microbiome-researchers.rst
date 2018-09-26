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
Furthermore, by wrapping tools into a common framework, **data processing pipelines are streamlined**: with QIIME 2, you'll be able to re-write what was once a collection of scripts in different coding languages, calling different executables and re-formatting data inputs and outputs in most intermediate steps, into one (or a few) simple bash scripts.

Finally, QIIME 2 is **open-sourced and specifically designed for experienced researchers to contribute and expand the reach of their work.**
QIIME 2 is really just a collection of wrappers called :doc:`plugins <../plugins/index>`, which can be written for any software, package, or other installable executables.
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

**Pro-tip #3: to enable tab-complete in QIIME 2**, run ``source tab-qiime``.

Data processing steps
---------------------

The processing steps we'll cover in this tutorial include:

1. Importing data into QIIME 2
2. Demultiplexing data (i.e. mapping each sequence to the sample it came from)
3. Removing non-biological parts of the sequences (i.e. primers)
4. Performing quality control and:

   -  denoising sequences with DADA2 or deblur, and/or
   -  quality filtering, length trimming, and clustering with VSEARCH or dbOTU

5. Assigning taxonomy

Importing data into QIIME 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're using QIIME 2 to process your data, the first thing you need to do is get that data into a format that QIIME 2 can understand.
Various importing methods currently available in QIIME 2 are highlighted in the :doc:`QIIME 2 importing
tutorial <importing>`.

This step has the potential to be the most confusing part of the QIIME 2 pipeline as there are dozens of import and format types to choose from.
To see a full list of available import/format types use: ``qiime tools import --show-importable-formats`` and ``qiime tools import --show-importable-types``

If you're importing data that you've generated, you'll likely need to generate a :ref:`manifest file <manifest file>`, which is just a text file that  maps each FASTQ or FASTA file to its sample ID and direction (if applicable).

If you have sequencing data with one of two very specific formats (:ref:`EMP <emp import>` or :ref:`Casava <casava import>`), you can directly import the folder containing your sequencing files with
the ``--type EMPSingleEndSequences`` or ``--type 'SampleData[PairedEndSequencesWithQuality]'`` flags (or their respective paired-end types).
Otherwise if you don't have one of these two very specific formats, you'll need to make the manifest file to give ``import`` instructions on what and how to import your files.

Demultiplexing sequences
~~~~~~~~~~~~~~~~~~~~~~~~

If you have reads from multiple samples in the same file, you'll need to demultiplex your sequences.

If your barcodes have already been removed from the reads and are in a separate file, you can use `q2-demux <https://docs.qiime2.org/2018.6/plugins/available/demux/>`__ to demultiplex these.

If your barcodes are still in your sequences, you can use functions from the `cutadapt
plugin <https://docs.qiime2.org/2018.6/plugins/available/cutadapt/>`__.
The ``cutadapt demux-single`` method looks for barcode sequences at the beginning of your reads (5' end) with a certain error tolerance, removes them, and returns sequence data separated by each sample.
The QIIME 2 forum has a `tutorial on various functions available in cutadapt <https://forum.qiime2.org/t/demultiplexing-and-trimming-adapters-from-reads-with-q2-cutadapt/2313>`__, including demultiplexing.
You can learn more about how ``cutadapt`` works under the hood by reading their `documentation <https://cutadapt.readthedocs.io/en/stable/index.html>`__.

Note: Currently ``q2-demux`` and ``q2-cutadapt`` do not support demultiplexing dual-barcoded paired-end sequences, but only can demultiplex with barcodes in the forward reads.
So for the time being for this type of demultiplexing needs to be done outside of QIIME 2 using other tools, for example
`bcl2fastq <https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software.html>`__.

.. _`merge reads`:

Merging reads
~~~~~~~~~~~~~~

Whether or not you need to merge reads depends on how you plan to cluster or denoise your sequences into amplicon sequence variants (ASVs) or operational taxonomic units (OTUs).
**TODO: link to the part of the overview tutorial where we'll put the "deciding to merge" section**

If you do need to merge your reads, you can use the QIIME 2 `VSEARCH plugin <https://docs.qiime2.org/2018.6/plugins/available/vsearch/>`__  with the `join-pairs <https://docs.qiime2.org/2018.6/plugins/available/vsearch/join-pairs/>`__ method.

.. _`Remove non-biological sequences`:

Removing non-biological sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your data contains any non-biological sequences (e.g. primers, sequencing adapters, PCR spacers, etc), you should remove these.

The `q2-cutadapt <https://docs.qiime2.org/2018.6/plugins/available/cutadapt>`__ plugin has comprehensive methods for removing non-biological sequences from `paired-end <https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-paired/>`__ or `single-end <https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-single/>`__ data.

If you're going to use DADA2 to denoise your sequences, you can remove biological sequences at the same time as you call the denoising function.
All of DADA2's ``denoise`` fuctions have some sort of ``--p-trim`` parameter you can specify to remove base pairs from the end(s) of your reads.
(Deblur does not have this functionality yet.)

Grouping similar sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two main approaches for grouping similar sequences together: denoising and clustering.
The overview tutorial provides more in-depth discussion of these approaches (**TODO: link to where this will be**).

Regardless of how you group your sequences, the grouping methods will output:

1. A list of representative sequences for each of your OTUs and/or ASVs (QIIME 2 data format ``FeatureData[Sequence]``), and
2. A feature table which indicates how many reads of each OTU/sequence variants were observed in each sample. (QIIME 2 data format ``FeatureTable[Frequency]``)

DADA2 and deblur will also produce a stats summary file with useful information regarding the filtering and denoising.

Denoising
~~~~~~~~~

DADA2 and deblur are currently the two denoising methods available in QIIME 2.
You can read more about the methods in the overview tutorial (**TO DO** link to this section when it's done).

DADA2 and deblur both output exact sequence variants, which supposedly represent the true biological sequences present in your data.
Their creators have different terminology for these sequences (DADA2 calls them "amplicon sequence variants" (ASVs) and deblur calls them "sub-OTUs").
We'll be using the ASV terminology throughout this tutorial to refer to both outputs.

Preparing data for denoising
''''''''''''''''''''''''''''

Denoising requires little data preparation.
Both DADA2 and deblur perform quality filtering, denoising, and chimera removal, so you shouldn't need to perform any quality screening prior to running them.
That said, the official QIIME 2 tutorial recommends doing an initial `quality-filter <https://docs.qiime2.org/2018.6/tutorials/moving-pictures/#option-2-deblur>`__ with default settings prior to using deblur (as recommended by the deblur developers).
In our experience, DADA2 performs better without this step.

Both methods have an option to truncate your reads to a constant length (which occurs prior to denoising).
The truncating parameter is required for deblur and optional for DADA2.
Reads shorter than the truncation length are discarded and reads longer are truncated at that position.
The overview tutorial has more discussion on deciding what length you should truncate to. (**TODO: link to it**)

Denoising with DADA2
''''''''''''''''''''

The `DADA2 plugin <https://docs.qiime2.org/2018.6/plugins/available/dada2/>`__ has multiple methods to denoise reads:

* `denoise paired-end <https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-paired/>`__ requires unmerged, paired-end reads (i.e. both forward and reverse).
* `denoise single-end <https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-single/>`__ accepts either single-end or unmerged paired-end data. If you give it unmerged paired-end data, it will only use the forward reads (and do nothing with the reverse reads).
* `denoise-pyro <https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-pyro/>`__ accepts ion torrent data.

Note that DADA2 may be slow on very large datasets. You can increase the number of threads to use with the ``--p-n-threads`` parameter.

Denoising with deblur
''''''''''''''''''''''

The `deblur <https://docs.qiime2.org/2018.6/plugins/available/deblur/>`__ plugin has two methods to denoise sequences:

* `denoise-16S <https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-16S/>`__ denoises 16S sequences.
* `denoise-other <https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-other/>`__ denoises other types of sequences.

If you use `denoise-16S`, deblur performs an initial positive filtering step where it discards any reads which do not have a minimum 60% identity similarity to sequences from the 85% OTU GreenGenes database.
If you don't want to do this step, use the `denoise-other` method.

deblur can currently only denoise single-end reads.
It will accept unmerged paired-end reads as input, it just won't do anything with the reverse reads.
Note that deblur _can_ take in *merged* reads and treat them as single-end reads.

OTU Clustering
~~~~~~~~~~~~~~

In this tutorial, we'll cover QIIME 2 methods that perform `de novo  <https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-de-novo/>`__ and `closed reference <https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-closed-reference/>`__ clustering.
**TODO: link overview tutorial with more discussion about these types of clustering**

To cluster your sequences, you need to make sure that:

-  paired-end reads are merged
-  non-biological sequences are removed
-  reads are all trimmed to the same length
-  low-quality reads are discarded

We discussed merging paired-end reads and removing non-biological sequences above (Sections `Merge reads`_ and `Remove non-biological sequences`_).

Once your data is ready, you need to dereplicate your reads before clustering.

Length trimming
'''''''''''''''

If for some reason your raw reads are not already all the same length, you'll need to trim them to the same length before doing OTU clustering.
There isn't currently a QIIME 2 function to trim reads to the same length without doing anything else, though you may be able to use functions from the ``cutadapt`` plugin to do something like that.
(The reason for this is that the `QIIME 2 workflow <https://docs.qiime2.org/2018.6/tutorials/overview/#denoising-and-clustering>`__ recommends first denoising reads - which involves a length trimming step - and then optionally passing the ASVs through a clustering algorithm.)

Quality filtering
'''''''''''''''''

You can perform different types of quality filtering with the `quality filter <https://docs.qiime2.org/2018.6/plugins/available/quality-filter/>`__ plugin.
**TODO: what's the difference between the q-score and q-score-joined? Why are there two separate functions?**
The option descriptions for each method cover the different types of available quality filtering.

Dereplicating sequences
'''''''''''''''''''''''

No matter which type of clustering you do, you first need to dereplicate your sequences. The `q2-vsearch <https://docs.qiime2.org/2018.6/plugins/available/vsearch/>`__ plugin's method `dereplicate-sequences  <https://docs.qiime2.org/2018.6/plugins/available/vsearch/dereplicate-sequences/>`__ performs this step.

de novo clustering
''''''''''''''''''

Sequences can be clustered *de novo* based on their genetic similarity alone (i.e. with VSEARCH) or based on a combination of their genetic similarity and abundance distributions (i.e. with distribution-based clustering).

-  **Similarity-based clustering.** The QIIME 2 VSEARCH plugin method `cluster-features-de-novo <https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-de-novo/>`__ clusters OTUs. You can change the genetic similarity threshold with the ``--p-perc-identity`` parameter. The plugin wraps the VSEARCH ``--cluster_size`` function.
-  **Distribution-based clustering** incorporates the similarity between sequences and their abundance distribution to identify ecologically meaningful populations. You can learn more about this method in the `plugin documentation <https://github.com/cduvallet/q2-dbotu>`__, `original paper <http://dx.doi.org/10.1128/AEM.00342-13>`__, and the `re-implementation update paper <https://doi.org/10.1371/journal.pone.0176335>`__. The ``call-otus`` function in the `q2-dbotu <https://github.com/cduvallet/q2-dbotu>`__ plugin performs distribution-based clustering on input data.

Both of these functions take as input the output of ``q2-vsearch dereplicate-sequences``, which are dereplicated sequences with QIIME 2 data type ``'FeatureData[Sequence]'``, and a table of counts with QIIME 2 data type ``'FeatureTable[Frequency]'``.

closed reference clustering
'''''''''''''''''''''''''''

Closed reference clustering groups sequences together which match the same reference sequence in a database with a certain similarity.

VSEARCH can do closed reference clustering with the `cluster-features-closed-reference <https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-closed-reference/>`__ method.
This method wraps the ``--usearch_global`` VSEARCH function.
You can decide which reference database to cluster against with the ``--i-reference-sequences`` flag.
The input file to this flag should be a ``.qza`` file containing a fasta file with the sequences to use as references, with QIIME 2 data type ``FeatureData[Sequence]``.
Most people use GreenGenes or SILVA, but others curate their own databases or use other standard references (e.g. UNITE for ITS data).
You can download the references from the links on the `QIIME 2 data resources page <https://docs.qiime2.org/2018.6/data-resources/#marker-gene-reference-databases>`__.
You'll need to unzip/untar and import them as ``FeatureData[Sequence]`` artifacts, since they're provided as raw data files.

Assigning taxonomy
~~~~~~~~~~~~~~~~~~

Assigning taxonomy to ASV or OTU representative sequences is covered in the `taxonomy classification
tutorial <https://docs.qiime2.org/2018.6/tutorials/overview/#taxonomy-classification-and-taxonomic-analyses>`__.
All taxonomy assignment methods are in the `feature-classifier plugin <https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/>`__.

There are two main approaches for assigning taxonomy, each with multiple methods available.

The first involves aligning reads to reference databases directly:

- `classify-consensus-blast <https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-blast/>`__: BLAST+ local alignment
- `classify-consensus-vsearch <https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-vsearch/>`__:  VSEARCH global alignment

Both use the *consensus* approach of taxonomy assignment, which you can learn more about in the overview (**TODO link**) and tweak with the ``maxaccepts``, ``perc-identity``, and ``min-consensus`` parameters.

The second approach uses machine learning classifiers to assign likely taxonomies to reads:

- `fit-classifier-sklearn <https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-sklearn/>`__
- `fit-classifier-naive-bayes <https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-naive-bayes/>`__

These two functions differ in the type of machine learning model that they use.
(**TODO: maybe link to the paper here?**)
These methods need a pre-trained model as one of the inputs: you can either download one of the pre-trained taxonomy classifiers from the `data resources page <https://docs.qiime2.org/2018.6/data-resources/>`__, or train one yourself (following the steps outlined in the :doc:`feature classifier tutorial <feature-classifier>`).

Analyze feature table and gain insight
--------------------------------------

At this point, you should be ready to analyze your feature table to answer your scientific questions!
QIIME 2 offers multiple built-in functions to analyze your data, and you can also `export <Export the data>`_ it to do downstream analyses in your preferred coding language.

Some general things you can do with QIIME 2 are:

-  **Look at the data:** QIIME 2 has some a nice `taxa barplot visualizer <https://docs.qiime2.org/2018.6/plugins/available/taxa/barplot/?highlight=barplots#barplot-visualize-taxonomy-with-an-interactive-bar-plot>`__ to make visually exploring your data easy. You can also visualize your data on a PCoA plot with the `emperor <https://docs.qiime2.org/2018.6/plugins/available/emperor/plot/>`__ plugin (after calculating beta diversity between samples).
-  **Build a phylogenetic tree:** QIIME 2 has a `phylogeny <https://docs.qiime2.org/2018.6/plugins/available/phylogeny/>`__ plugin with different tree-building methods.
-  **Calculate alpha diversity of your samples:** the `diversity plugin <https://docs.qiime2.org/2018.6/plugins/available/diversity/>`__ has many `alpha diversity metrics <https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282>`__ available through the ``alpha`` and ``alpha-phylogenetic`` methods.
-  **Calculate beta diversity between samples:** the `diversity plugin <https://docs.qiime2.org/2018.6/plugins/available/diversity/>`__ also has these metrics available in the ``beta``, ``beta-phylogenetic``, and ``beta-phylogenetic-alt`` methods.
-  **Test for differences between samples**, through differential abundance or distribution testing: PERMANOVA, ANOSIM, ANCOM, and Gneiss are some of the relevant methods which are available in QIIME 2. PERMANOVA and ANOSIM can be done with the `beta-group-significance <https://docs.qiime2.org/2018.6/plugins/available/diversity/beta-group-significance/>`__ method in the ``diversity`` plugin. ANCOM is available in the `composition <https://docs.qiime2.org/2018.6/plugins/available/composition/>`__ plugin. Gneiss is available in the `gneiss <https://docs.qiime2.org/2018.6/plugins/available/gneiss/>`__ plugin, and has an associated tutorial, `"Differential abundance  analysis with gneiss" <https://docs.qiime2.org/2018.6/tutorials/gneiss/>`__.
-  **Build machine learning classifiers to make predictions:** the `q2-sample-classifier <https://docs.qiime2.org/2018.6/plugins/available/sample-classifier/>`__ plugin has several actions for these classifiers, and the associated `"Predicting sample metadata values with q2-sample-classifier" tutorial <https://docs.qiime2.org/2018.6/tutorials/sample-classifier/>`__ provides more details.

Export the data
~~~~~~~~~~~~~~~

If you're a veteran microbiome scientist and don't want to use QIIME 2 for your analyses, you can extract your feature table and sequences from the artifact using the `export <https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-data>`__ tool.
While ``export`` only outputs the data, the `extract <https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-versus-extracting>`__ tool allows you to also extract other metadata such as the citations, provenance etc.

Note that this places generically named files (e.g. ``feature-table.txt``) into the output directory, so you may want to immediately rename the files to something more information (or somehow ensure that they stay in their original directory)!
(**TODO: update this if the new 2018.8/whatever version lets you rename files**)

You can also use the handy `qiime2R <https://github.com/jbisanz/qiime2R>`__ package to import QIIME 2 artifacts directly into R.

New plugins
------------

You can explore QIIME 2's ever-growing list of
`plugins <https://docs.qiime2.org/2018.6/plugins/>`__ to find other methods to apply to your data.

And remember that you can also :doc:`make your own QIIME 2 plugins <../plugins/developing/>` to add functionality to QIIME 2 and share it with the community!
