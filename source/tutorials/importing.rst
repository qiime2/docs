Importing data
==============

.. contents:: Importing data
   :depth: 2

.. note:: This tutorial assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

In order to use QIIME 2, your input data must be stored in *QIIME 2 artifacts* (i.e. ``.qza`` files). This is what enables distributed and automatic provenance tracking, as well as semantic type validation and transformations between data formats (see the :doc:`core concepts <../concepts>` page for more details about QIIME 2 artifacts). This tutorial demonstrates how to import various data formats into QIIME 2 artifacts for use with QIIME 2.

.. note:: This tutorial does not describe all data formats that are currently supported in QIIME 2. It is a work-in-progress that describes some of the most commonly used data formats that are available. We are also actively working on supporting additional data formats. If you need to import data in a format that is not covered here, please post to the `QIIME 2 Forum`_ for help.

Importing will typically happen with your initial data (e.g. sequences obtained from a sequencing facility), but importing can be performed at any step in your analysis pipeline. For example, if a collaborator provides you with a feature table in ``.biom`` format, you can import it into a QIIME 2 artifact to perform "downstream" statistical analyses that operate on a feature table.

Importing can be accomplished using any of the QIIME 2 :doc:`interfaces <../interfaces/index>`. This tutorial will focus on using the QIIME 2 command-line interface (``q2cli``) to import data with the ``qiime tools import`` method. Each section below briefly describes a data format, provides commands to download example data, and illustrates how to import the data into a QIIME 2 artifact.

You may want to begin by creating a directory to work in.

.. command-block::
   :no-exec:

   mkdir qiime2-importing-tutorial
   cd qiime2-importing-tutorial


.. _`importing seqs`:

Sequence data with sequence quality information (i.e. FASTQ)
------------------------------------------------------------

With QIIME 2, there are functions to import different types of FASTQ data:

1. FASTQ data with the EMP Protocol format
2. FASTQ data with the Casava 1.8 demultiplexed format
3. Any other kind of FASTQ data

.. _`emp import`:

"EMP protocol" multiplexed single-end fastq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format description
******************

If your FASTQ files follow the "`Earth Microbiome Project (EMP) protocol`_"  format for `single-end` reads, you should have two ``fastq.gz`` files total:

1. one ``fastq.gz`` file that contains the single-end reads,
2. and another that contains the associated barcode reads

In this format, sequence data is still multiplexed (i.e. you have only one ``fastq.gz`` file containing raw data for all of your samples.

The order of the records in the two ``fastq.gz`` files defines the association between a sequence read and its barcode read (i.e. the first barcode read corresponds to the first sequence read, the second barcode to the second read, and so on.)

Obtaining example data
```````````````````````

.. command-block::

   mkdir emp-single-end-sequences

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/moving-pictures/emp-single-end-sequences/barcodes.fastq.gz
   :saveas: emp-single-end-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/moving-pictures/emp-single-end-sequences/sequences.fastq.gz
   :saveas: emp-single-end-sequences/sequences.fastq.gz

Importing data
**************

.. command-block::

   qiime tools import \
     --type EMPSingleEndSequences \
     --input-path emp-single-end-sequences \
     --output-path emp-single-end-sequences.qza

"EMP protocol" multiplexed paired-end fastq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format description
******************

If your FASTQ files follow the "`Earth Microbiome Project (EMP) protocol`_" format for `paired-end` reads, you should have three ``fastq.gz`` files total:

1. one ``fastq.gz`` file that contains the forward sequence reads,
2. one ``fastq.gz`` file that contains the reverse sequence reads,
3. and a third that contains the associated barcode reads

In this format, sequence data is still multiplexed (i.e. you have only one forward and one reverse ``fastq.gz`` file containing raw data for all of your samples).

The order of the records in the ``fastq.gz`` files defines the association between a sequence read and its barcode read (i.e. the first barcode read corresponds to the first sequence read, the second barcode to the second read, and so on.)

Obtaining example data
``````````````````````

.. command-block::

   mkdir emp-paired-end-sequences

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/atacama-soils/1p/forward.fastq.gz
   :saveas: emp-paired-end-sequences/forward.fastq.gz

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/atacama-soils/1p/reverse.fastq.gz
   :saveas: emp-paired-end-sequences/reverse.fastq.gz

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/atacama-soils/1p/barcodes.fastq.gz
   :saveas: emp-paired-end-sequences/barcodes.fastq.gz

Importing data
**************

.. command-block::

   qiime tools import \
     --type EMPPairedEndSequences \
     --input-path emp-paired-end-sequences \
     --output-path emp-paired-end-sequences.qza

Casava 1.8 single-end demultiplexed fastq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format description
******************

In the `Casava 1.8 demultiplexed`_ (single-end) format, there is one ``fastq.gz`` file for each sample in the study which contains the `single-end` reads for that sample. The file name includes the sample identifier and should look like ``L2S357_15_L001_R1_001.fastq.gz``. The underscore-separated fields in this file name are:

1. the sample identifier,
2. the barcode sequence or a barcode identifier,
3. the lane number,
4. the direction of the read (i.e. only R1, because these are single-end reads), and
5. the set number.

Obtaining example data
``````````````````````

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/importing/casava-18-single-end-demultiplexed.zip
   :saveas: casava-18-single-end-demultiplexed.zip

.. command-block::

   unzip -q casava-18-single-end-demultiplexed.zip

Importing data
**************

.. command-block::

   qiime tools import \
     --type 'SampleData[SequencesWithQuality]' \
     --input-path casava-18-single-end-demultiplexed \
     --input-format CasavaOneEightSingleLanePerSampleDirFmt \
     --output-path demux-single-end.qza

Casava 1.8 paired-end demultiplexed fastq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format description
******************

In `Casava 1.8 demultiplexed`_ (paired-end) format, there are two ``fastq.gz`` files for each sample in the study, each containing the forward or reverse reads for that sample. The file name includes the sample identifier. The forward and reverse read file names for a single sample might look like ``L2S357_15_L001_R1_001.fastq.gz`` and ``L2S357_15_L001_R2_001.fastq.gz``, respectively.
The underscore-separated fields in this file name are:

1. the sample identifier,
2. the barcode sequence or a barcode identifier,
3. the lane number,
4. the direction of the read (i.e. R1 or R2), and
5. the set number.

Obtaining example data
``````````````````````

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/importing/casava-18-paired-end-demultiplexed.zip
   :saveas: casava-18-paired-end-demultiplexed.zip

.. command-block::

   unzip -q casava-18-paired-end-demultiplexed.zip

Importing data
**************

.. command-block::
   qiime tools import \
     --type 'SampleData[PairedEndSequencesWithQuality]' \
     --input-path casava-18-paired-end-demultiplexed \
     --input-format CasavaOneEightSingleLanePerSampleDirFmt \
     --output-path demux-paired-end.qza

.. _`manifest file`:

"Fastq manifest" formats
~~~~~~~~~~~~~~~~~~~~~~~~

If you don't have either EMP or Casava format, you need to import your data into QIIME 2 manually.

Format description
******************

First, you'll create a text file called a "manifest file", which maps sample identifiers to ``fastq.gz`` or ``fastq`` `absolute filepaths`_ that contain sequence and quality data for the sample (i.e. these are FASTQ files).
The manifest file also indicates the direction of the reads in each ``fastq.gz`` or ``fastq`` file. The manifest file will generally be created by you, and it is designed to be a simple format that doesn't put restrictions on the naming of the demultiplexed ``fastq.gz`` / ``fastq`` files, since there is no broadly used naming convention for these files. You can call the manifest file whatever you want.

The manifest file is a comma-separated (i.e., ``.csv``) text file. The first field on each line is the sample identifier that should be used by QIIME, the second field is the absolute filepath, and the third field is the read direction. Lines beginning with ``#`` and blank lines are ignored. The first line in the file that does not begin with a ``#`` and is not blank must be the header line: ``sample-id,absolute-filepath,direction``. With the exception of the header line, the order of lines in this file is not important.

For single-end reads, there must be exactly one line per sample id corresponding to the forward reads (or reverse, if you're processing these separately as single-end reads). For paired-end reads there must be exactly two lines per sample id, corresponding to the forward and the reverse reads. The direction field on each line can only contain the text ``forward`` or ``reverse``.

The ``fastq.gz`` absolute filepaths may contain environment variables (e.g., ``$HOME`` or ``$PWD``). The following example illustrates a simple fastq manifest file for paired-end read data for two samples.

::

  sample-id,absolute-filepath,direction
  # Lines starting with '#' are ignored and can be used to create
  # "comments" or even "comment out" entries
  sample-1,$PWD/some/filepath/sample1_R1.fastq.gz,forward
  sample-2,$PWD/some/filepath/sample2_R1.fastq.gz,forward
  sample-1,$PWD/some/filepath/sample1_R2.fastq.gz,reverse
  sample-2,$PWD/some/filepath/sample2_R2.fastq.gz,reverse

Just like with ``fastq.gz``, the absolute filepaths in the manifest for any ``fastq`` files must be accurate. The following example illustrates a simple fastq manifest file for ``fastq`` single-end read data for one sample.

::

  sample-id,absolute-filepath,direction
  sample-1,$PWD/some/filepath/sample1_R1.fastq,forward

There are four variants of FASTQ data which you must specific to QIIME 2 when importing, and which are defined in the following sections.

SingleEndFastqManifestPhred33
*****************************

In this variant of the fastq manifest format, the read directions must all either be forward or reverse. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 33.

SingleEndFastqManifestPhred64
*****************************

In this variant of the fastq manifest format, the read directions must all either be forward or reverse. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 64. During import, QIIME 2 will convert the PHRED 64 encoded quality scores to PHRED 33 encoded quality scores. This conversion will be slow, but will only happen one time.

PairedEndFastqManifestPhred33
*****************************

In this variant of the fastq manifest format, there must be forward and reverse read ``fastq.gz`` / ``fastq`` files for each sample id. As a result, each sample id is represented twice in the manifest file: once for its forward reads, and once for its reverse reads. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 33.

PairedEndFastqManifestPhred64
*****************************

In this variant of the fastq manifest format, there must be forward and reverse read ``fastq.gz`` / ``fastq`` files for each sample id. As a result, each sample id is represented twice in the manifest file: once for its forward reads, and once for its reverse reads. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 64. During import, QIIME 2 will convert the PHRED 64 encoded quality scores to PHRED 33 encoded quality scores. This conversion will be slow, but will only happen one time.

Obtaining example data
```````````````````````

Since importing data in these four formats is very similar, we'll only provide examples for two of the variants: ``SingleEndFastqManifestPhred33`` and ``PairedEndFastqManifestPhred64``.

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/se-33.zip
   :saveas: se-33.zip

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/se-33-manifest
   :saveas: se-33-manifest

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/pe-64.zip
   :saveas: pe-64.zip

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/pe-64-manifest
   :saveas: pe-64-manifest

.. command-block::

   unzip -q se-33.zip
   unzip -q pe-64.zip


Importing Data
**************

.. command-block::

   qiime tools import \
     --type 'SampleData[SequencesWithQuality]' \
     --input-path se-33-manifest \
     --output-path single-end-demux.qza \
     --input-format SingleEndFastqManifestPhred33

.. command-block::

   qiime tools import \
     --type 'SampleData[PairedEndSequencesWithQuality]' \
     --input-path pe-64-manifest \
     --output-path paired-end-demux.qza \
     --input-format PairedEndFastqManifestPhred64

Sequences without quality information (i.e. FASTA)
--------------------------------------------------------

.. _`casava import`:

Unfortunately, there is currently no way to import data files which contain quality-filtered FASTA sequences associated with sample IDs.
If you have this sort of data, you might consider dereplicating your sequences externally, and then importing the representative sequences (described in the section below) and the respective feature table of counts into QIIME 2.

Per-feature unaligned sequence data (i.e., representative FASTA sequences)
--------------------------------------------------------------------------

Format description
~~~~~~~~~~~~~~~~~~

Unaligned sequence data is imported from a fasta formatted file containing DNA sequences that are not aligned (i.e., do not contain `-` or `.` characters). The sequences may contain degenerate nucleotide characters, such as ``N``, but some QIIME 2 actions may not support these characters. See the `scikit-bio fasta format description`_ for more information about the fasta format.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/importing/sequences.fna
   :saveas: sequences.fna

Importing data
~~~~~~~~~~~~~~

.. command-block::

   qiime tools import \
     --input-path sequences.fna \
     --output-path sequences.qza \
     --type 'FeatureData[Sequence]'

Per-feature aligned sequence data (i.e., aligned representative FASTA sequences)
--------------------------------------------------------------------------------

Format description
~~~~~~~~~~~~~~~~~~

Aligned sequence data is imported from a fasta formatted file containing DNA sequences that are aligned to one another. All aligned sequences must be exactly the same length. The sequences may contain degenerate nucleotide characters, such as ``N``, but some QIIME 2 actions may not support these characters. See the `scikit-bio fasta format description`_ for more information about the fasta format.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/importing/aligned-sequences.fna
   :saveas: aligned-sequences.fna

Importing data
~~~~~~~~~~~~~~

.. command-block::

   qiime tools import \
     --input-path aligned-sequences.fna \
     --output-path aligned-sequences.qza \
     --type 'FeatureData[AlignedSequence]'

.. _`importing feature tables`:

Feature table data
------------------

You can also import pre-processed feature tables into QIIME 2.

BIOM v1.0.0
~~~~~~~~~~~

Format description
******************

See the `BIOM v1.0.0 format specification`_ for details.

Obtaining example data
``````````````````````

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/feature-table-v100.biom
   :saveas: feature-table-v100.biom

Importing data
**************

.. command-block::

   qiime tools import \
     --input-path feature-table-v100.biom \
     --type 'FeatureTable[Frequency]' \
     --input-format BIOMV100Format \
     --output-path feature-table-1.qza

BIOM v2.1.0
~~~~~~~~~~~

Format description
******************

See the `BIOM v2.1.0 format specification`_ for details.

Obtaining example data
``````````````````````

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/feature-table-v210.biom
   :saveas: feature-table-v210.biom

Importing data
**************

.. command-block::

   qiime tools import \
     --input-path feature-table-v210.biom \
     --type 'FeatureTable[Frequency]' \
     --input-format BIOMV210Format \
     --output-path feature-table-2.qza

Phylogenetic trees
------------------

Format description
~~~~~~~~~~~~~~~~~~

Phylogenetic trees are imported from newick formatted files. See the `scikit-bio newick format description`_ for more information about the newick format.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/importing/unrooted-tree.tre
   :saveas: unrooted-tree.tre

Importing data
~~~~~~~~~~~~~~

.. command-block::

   qiime tools import \
     --input-path unrooted-tree.tre \
     --output-path unrooted-tree.qza \
     --type 'Phylogeny[Unrooted]'

If you have a rooted tree, you can use ``--type 'Phylogeny[Rooted]'`` instead.

Other data types
----------------

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/aligned-sequences.fna
   :saveas: aligned-sequences.fna

QIIME 2 can import many other data types not covered in this tutorial.
You can see which formats of input data are importable with the following command:

.. command-block::

   qiime tools import \
     --show-importable-formats

And which QIIME 2 types you can import these formats as:

.. command-block::

   qiime tools import \
     --show-importable-types

.. download::
   :url: https://data.qiime2.org/2018.11/tutorials/importing/unrooted-tree.tre
   :saveas: unrooted-tree.tre

Unfortunately, there isn't currently documentation detailing which data formats can be imported as which QIIME 2 data types, but hopefully the names of these formats and types should be self-explanatory enough to figure it out.
If you have any questions, please post to the `QIIME 2 Forum`_ for help!

.. _Earth Microbiome Project (EMP) protocol: http://www.earthmicrobiome.org/protocols-and-standards/

.. _Casava 1.8 demultiplexed:  http://illumina.bioinfo.ucr.edu/ht/documentation/data-analysis-docs/CASAVA-FASTQ.pdf/view

.. _QIIME 2 Forum: https://forum.qiime2.org

.. _BIOM v1.0.0 format specification: http://biom-format.org/documentation/format_versions/biom-1.0.html

.. _BIOM v2.1.0 format specification: http://biom-format.org/documentation/format_versions/biom-2.1.html

.. _scikit-bio fasta format description: http://scikit-bio.org/docs/latest/generated/skbio.io.format.fasta.html#fasta-format

.. _scikit-bio newick format description: http://scikit-bio.org/docs/latest/generated/skbio.io.format.newick.html

.. _absolute filepaths: https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths

.. _PHRED offset: http://scikit-bio.org/docs/latest/generated/skbio.io.format.fastq.html#quality-score-variants
