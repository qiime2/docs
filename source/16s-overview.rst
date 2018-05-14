16S processing overview
=======================

In this document, we'll go over the basic steps involved in 16S data
processing and analysis. This tutorial is intended for experienced
microbiome researchers who are looking for the **QIIME 2 commands
pertaining to specific steps in 16S processing**, as well as for
early-stage microbiome scientists who want a broad overview of the steps
involved in 16S data processing.

For an overview of the theoreticaly motivations for many of the steps
involve, we recommend Scott Olesen's `16S
primer <link%20to%20leanpub>`__.

Overview
--------

You can think of 16S data as taking a few distinct forms:

1. **Data straight off of the sequencer**. This data is usually
   converted to some formats like ``.bam``, ``.sff``, or ``.fastq`` by
   your sequencing center. We won't cover this here.
2. **Raw data.** By raw data, we mean raw ``.fastq`` or ``.fasta``
   files. These files contain sequences and (sometimes) quality scores,
   but nothing has been done to them yet.
3. **Feature table and "taxa".** This form of data is the output of raw
   data processing, when your raw sequences have been turned into
   individual sequences of interest (e.g. OTUs, sequence variants, etc)
   and sometimes assigned taxonomy. By "feature table," we mean a file
   with samples, sequences, and observed counts for each sequence in
   each sample.
4. **Analysis and insight.** After processing your data into a feature
   table, you can use QIIME 2 to perform some basic analysis and
   (hopefully) gain insights.

In this overview, we'll discuss the potential steps involved in going
from **raw data to feature tables** and some basic analyses to take you
from **feature table to insights.**

Raw data processing
-------------------

The steps you take to process your raw data into a feature table depend
on the form of the raw data that you have and on the choices you make
about processing methods. Briefly, the steps involved here are:

1. Figure out what form your raw data is in.
2. Import data into qiime
3. Map sequences to samples (i.e. demultiplex)
4. Remove non-biological parts of the sequences (i.e. remove primers)
5. Perform quality control and denoise and/or cluster sequences

   -  Denoise sequences with DADA2 or deblur, and/or
   -  Quality filter, length trim, and cluster with VSEARCH or dbOTU

6. If you want, assign taxonomy

Note that not every step has to be done in the order presented here. For
example, if you're using DADA2 to call sequence variants, you don't need
to merge your paired-end reads before denoising. Also, removing primers
and demultiplexing can be done in different orders.

*Pro-tip: qiime artifacts are simply zip files, so if at any point you
want to look at what data files are in the ``.qza`` artifact, you can
unzip your artifact directly (``unzip -k file.qza``) and look through
the files in the ``data/`` folder.*

Figure out what form your raw data is in
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you start, you need to figure out what processing steps your data
will need. This means that you need to figure out what sort of data you
have.

-  Do you have FASTQ or FASTA data?
-  Are your sequences already de-multiplexed with one file per sample,
   or will you need to split sequences by barcodes (i.e. demultiplex)?
-  If you need to demultiplex your reads, where are the barcodes? In the
   sequences, in the header of sequences, or in a separate file?
-  Do you have unmerged paired-end reads (i.e. forward and reverse)?
-  Are the primers still in the sequences?
-  What length of reads do you have? Are they already all trimmed to a
   certain length?

Every sequencing center provides a different kind of “raw data”, so the
answers to these questions will vary across experiments. There are two
ways to find the answers to these questions:

1. **Look at your data**. You can use command-line tools like ``less``
   and ``grep`` or other programming languages like python to look at
   the data files, find barcodes and primers, and count the length of
   reads.
2. **Ask your sequencing center**. If you've looked at your data and
   you're still not sure about some answers, you can ask whoever gave
   you the data - they should know what has been done to the data
   already.

Import data into qiime
~~~~~~~~~~~~~~~~~~~~~~

If you're using qiime to process your data, the first thing you need to
do is get that data into a format that qiime can understand.

```qiime tools import`` <link%20to%20qiime%20tools%20import>`__ will get
you there.

Demultiplex sequences
~~~~~~~~~~~~~~~~~~~~~

If the reads for all of your samples are in the same file, you'll need
to demultiplex your sequences.

**Method**. This method looks for exact matches to barcode sequences
that are specified either in the sequences, in the sequence headers, or
in a separate file. It returns demultiplexed fasta or fastq files, with
all of the sequences corresponding to each sample in separate files. You
don't necessarily need to do this step first, but it helps to have each
sample in a separate file for downstream steps which leverage this to
parallelize their processing code.

```qiime something something`` <link>`__ does this

VSEARCH
^^^^^^^

VSEARCH performs merging with a few different commands...?

Some other tool?
^^^^^^^^^^^^^^^^

Remove primers
~~~~~~~~~~~~~~

If the primers that you used to amplify your sequences are still in the
reads, you may want to trim these prior to clustering or denoising.

cutadapt?
'''''''''

vsearch?
''''''''

Quality control and denoise/cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two main types of ways to group similar reads together:
denoising and clustering. Denoising is the newer approach, and attempts
to identify the exact sequences present in your dataset. DADA2 and
deblur do this by learning error models from your data and
probabilistically determining whether variance between sequences is a
result of sequencing error or is truly a biological variant. These
methods only work with fastq data, as they require quality scores to
build error profiles from your data. "Exact sequence variants,"
"amplicon sequence variants," or "ASVs" are the outputs of this method.
Clustering is a way to group "similar" sequences together, usually based
on the genetic distance between sequences but in some cases
incorporating additional information (e.g. distribution-based
clustering). Clustering methods return "operational taxonomic units," or
"OTUs". If you want, you can first denoise your data and then pass your
exact sequence variants through a clustering algorithm.

All of these methods will output:

1. A list of representative sequences for each of your OTUs and/or ASVs
   (qiime data format ``Something[something]``), and
2. a feature table which indicates how many reads of each OTU/ASV were
   observed in each sample. (qiime data format
   ``FeatureTable[Frequency]``)

Denoising
^^^^^^^^^

Denoising requires little data preparation. There are two main methods
to perform denoising: DADA2 and deblur. By definition, denoising also
performs quality filtering and so you do not need to discard low-quality
sequences before running these methods.

DADA2
'''''

To denoise with DADA2, you can pass in unmerged reads. Note that DADA2
may be slow on very large datasets.

qiime command

deblur
''''''

As of May 2018, deblur can only handle forward reads (even though it can
take unmerged reads as input - it just won't do anything with the
reverse reads). deblur is faster for larger datasets, because it ...

Any other data processing needed?

qiime command

Clustering
^^^^^^^^^^

To cluster your sequences, you need to prepare your data.

Merged paired-end reads
'''''''''''''''''''''''

If you have unmerged forward and reverse reads, you need to merge these
together.

qiime command

Trim sequences
''''''''''''''

Because many clustering algorithms rely on very basic measures of
genetic distance, you may want to ensure that all of your sequences are
trimmed to the same length before clustering.

qiime command

Quality control
'''''''''''''''

You should discard low-quality sequences before clustering. There are
two ways to do this: either by truncating your reads after the first
time a certain low quality is encountered or by discarding whole
sequences based on their expected number of errors (i.e. bases called
incorrectly). Because of the way that sequencing generates errors, it is
generally more advisable to discard merged reads based on the expected
number of errors, and to truncate

Note that which quality filtering method you choose informs when you
should trim the length of your sequences. If you discard reads based on
expected errors, you should trim them *before* quality filtering. If you
truncate reads after a certain quality is encountered, you may want to
trim them *after* quality filtering.

You can learn more about these approaches two by reading the USEARCH
documentation: http://www.drive5.com/usearch/manual/readqualfiltering.

Note that many of these methods also automatically discard reads with
ambiguous base calls (i.e. bases that are called as something other than
A, T, C, or G).

Quality filtering
                 

qiime commands

Quality truncation
                  

Clustering
''''''''''

There are many ways to cluster sequences, which fall into three main
categories:

1. de novo clustering, in which sequences are grouped together based
   solely on the dataset itself
2. closed reference clustering, in which sequences are grouped together
   based on their matches to an external reference database
3. open reference clustering, which first performs closed reference
   clustering and then de novo clustering on any reads which did not map
   to the reference. This method is ill-advised and will not be covered
   here. `link to edgar's scathing paper about qiime open
   reference <link>`__

de novo clustering
                  

Sequences can be clustered *de novo* based on their genetic similarity
alone (i.e. with VSEARCH) or based on a combination of their genetic
similarity and abundance distributions (i.e. with distribution-based
clustering).

VSEARCH
       

qiime command

Distribution-based clustering
                             

Distribution-based clustering incorporates the similarity between
sequences and their abundance distribution to identify ecologically
meaningful populations. You can learn more about this method in the
documentation and paper `link to docs <dbotu.com>`__

qiime command

closed reference clustering
                           

Closed reference clustering groups sequences together which match the
same reference sequence in a database with a certain similarity. Note
that closed reference clustering may produce groupings that are not what
you expect `link to scott's blog <link>`__.

VSEARCH can do closed reference clustering. You can decide which
reference database to cluster against. Most people use Green Genes or
SILVA, but others curate their own databases or use other standard
references (e.g. UNITE for ...).

qiime command

Assign taxonomy
~~~~~~~~~~~~~~~

If you clustered OTUs with closed-reference clustering, your OTUs will
have the name of the reference sequence they matched to, and you don't
need to do anything else to get taxonomy. For all other *de novo*
methods, you can assign taxonomy with different probabilistic
classifiers.

You have two choices to make here: which type of classifier you want to
use (e.g. RDP, which is a naive Bayesian thing, or something else?) and
which database you want to train your classifier on. Qiime provides
options to do both of these things.

You can also download pre-trained taxonomy classifiers `here <page>`__.

Train a classifier
^^^^^^^^^^^^^^^^^^

qiime commands

Classify sequences
^^^^^^^^^^^^^^^^^^

qiime commands

Analyze feature table and gain insight
--------------------------------------

While the exact analyses you perform depend on your dataset,
experimental design, and questions of interest, there are some basic
analyses that many microbiome analyses have in common.

Export the data
~~~~~~~~~~~~~~~

If you're a veteran microbiome scientist and don't want to use qiime 2
for your analyses, you can extract your feature table and sequences from
the artifact.

qiime tools export

Note that this places generically named files (e.g.
``feature-table.txt``) into the output directory, so you may want to
immediately rename the files to something more information (or somehow
ensure that they stay in their original directory)!

Look at the data
~~~~~~~~~~~~~~~~

The first thing you might want to do is simply to look at your data:
what phyla are represented? Genera?

Qiime 2 provides easy ways to visualize your data in taxonomy barplots:

qiime command

You can also export your data to Phinch for some beautiful and
interactive visualizations (plugin coming soon!).

Phylogenetic tree
~~~~~~~~~~~~~~~~~

Some downstream analyses need to know the phylogenetic relationship
between your sequences. You can build a phylogenetic tree using a
variety of methods:

qiime commands

Alpha diversity
~~~~~~~~~~~~~~~

Alpha diversity tells you something about the *diversity* of the
community in each sample. There are many ways to calculate alpha
diversity, which are wonderfully explained in a `community
contribution <link>`__ on the qiime 2 forum. You can call them all with
the ``q2-diversity`` plugin:

qiime command to list all available diversity

qiime command to call one

Beta diversity
~~~~~~~~~~~~~~

You can also calculate the "distance" or "difference" between
communities across samples. Again, there are many ways (metrics) to
calculate this distance (beta diversity). scikit-bio is a good place to
learn more about these?

qiime command to show all the methods

qiime command to do one

PCoA
^^^^

Once you've calculated distances between all pairwise samples in your
data, you can project your samples onto a PCoA plot.

qiime command

PERMANOVA/ANOSIM/etc
^^^^^^^^^^^^^^^^^^^^

If you have multiple groups and want to know whether they are
meanginfully different, you can use a statistical methods that
calculates whether the distances between samples in different groups is
different than the distance between samples in the same group.

There are a few different ways to do this, learn more about it
somewhere...?

qiime commands...

Differential abundance testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are comparing two groups of samples, you can ask if any taxa in
your data are differentially abundant in the two groups. There are many
ways to measure differential abundance. You should understand what
assumptions are being made by each method and ensure that your data
meets these assumptions.

Non-parametric tests
^^^^^^^^^^^^^^^^^^^^

qiime command for wilcoxon, etc

DESEQ2
^^^^^^

MetagenomeSeq
^^^^^^^^^^^^^

Others?
^^^^^^^

Machine learning and multivariate models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Beyond testing for differentially abundant taxa, you can also compare
groups with multi-variate approaches like regression models and machine
learning classifiers.

Machine learning classifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Machine learning can be used to build complex models that distinguish
groups of samples well. You should familiarize yourself with the
underlying methods called by qiime - the scikit-learn user guide is a
fantastic resource. Also, make sure that you are using appropriate
cross-validation or holdout data to prevent overfitting.

qiime commands

Regression models
^^^^^^^^^^^^^^^^^

You can also build more complicated models to identify differences
between groups of samples...

And much much more!
~~~~~~~~~~~~~~~~~~~

You can explore qiime's ever-growing list of plugins to find other
methods to apply to your data. And remember that you're not limited to
what qiime can do: you can export your data at any point and do more
complicated or unique analyses on your own computer.
