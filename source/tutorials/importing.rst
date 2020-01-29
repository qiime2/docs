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

Single-end "`Earth Microbiome Project (EMP) protocol`_"  formatted reads should have two ``fastq.gz`` files total:

1. one ``fastq.gz`` file that contains the single-end reads,
2. and another that contains the associated barcode reads

In this format, sequence data is still multiplexed (i.e. you have only one ``fastq.gz`` file containing raw data for all of your samples).

The order of the records in the two ``fastq.gz`` files defines the association between a sequence read and its barcode read (i.e. the first barcode read corresponds to the first sequence read, the second barcode to the second read, and so on).

Obtaining example data
```````````````````````

.. command-block::

   mkdir emp-single-end-sequences

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/emp-single-end-sequences/barcodes.fastq.gz
   :saveas: emp-single-end-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/emp-single-end-sequences/sequences.fastq.gz
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

Paired-end "`Earth Microbiome Project (EMP) protocol`_" formatted reads should have three ``fastq.gz`` files total:

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
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/1p/forward.fastq.gz
   :saveas: emp-paired-end-sequences/forward.fastq.gz

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/1p/reverse.fastq.gz
   :saveas: emp-paired-end-sequences/reverse.fastq.gz

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/1p/barcodes.fastq.gz
   :saveas: emp-paired-end-sequences/barcodes.fastq.gz

Importing data
**************

.. command-block::

   qiime tools import \
     --type EMPPairedEndSequences \
     --input-path emp-paired-end-sequences \
     --output-path emp-paired-end-sequences.qza

.. _`casava import`:

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
   :url: https://data.qiime2.org/2020.2/tutorials/importing/casava-18-single-end-demultiplexed.zip
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
   :url: https://data.qiime2.org/2020.2/tutorials/importing/casava-18-paired-end-demultiplexed.zip
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

If you don't have either EMP or Casava format, you need to import your data into QIIME 2 manually by first creating a "manifest file" and then using the ``qiime tools import`` command with different specifications than in the EMP or Casava import commands.

Format description
******************

First, you'll create a text file called a "manifest file", which maps sample identifiers to ``fastq.gz`` or ``fastq`` `absolute filepaths`_ that contain sequence and quality data for the sample (i.e. these are FASTQ files).
The manifest file also indicates the direction of the reads in each ``fastq.gz`` or ``fastq`` file. The manifest file will generally be created by you, and it is designed to be a simple format that doesn't put restrictions on the naming of the demultiplexed ``fastq.gz`` / ``fastq`` files, since there is no broadly used naming convention for these files. You can call the manifest file whatever you want. As well, the manifest format is Metadata-compatible, so you can re-use the manifest file to bootstrap your :doc:`Sample Metadata <metadata>`, too.

The manifest file is a tab-seperated (i.e., ``.tsv``) text file. The first column defines the Sample ID, while the second (and optional third) column defines the absolute filepath to the forward (and optional reverse) reads. All of the rules and behavior of this format are inherited from the :doc:`QIIME 2 Metadata format <metadata>`.

The ``fastq.gz`` absolute filepaths may contain environment variables (e.g., ``$HOME`` or ``$PWD``). The following example illustrates a simple fastq manifest file for paired-end read data for four samples.

::

  sample-id	forward-absolute-filepath	reverse-absolute-filepath
  sample-1	$PWD/some/filepath/sample0_R1.fastq.gz	$PWD/some/filepath/sample1_R2.fastq.gz
  sample-2	$PWD/some/filepath/sample2_R1.fastq.gz	$PWD/some/filepath/sample2_R2.fastq.gz
  sample-3	$PWD/some/filepath/sample3_R1.fastq.gz	$PWD/some/filepath/sample3_R2.fastq.gz
  sample-4	$PWD/some/filepath/sample4_R1.fastq.gz	$PWD/some/filepath/sample4_R2.fastq.gz

Just like with ``fastq.gz``, the absolute filepaths in the manifest for any ``fastq`` files must be accurate. The following example illustrates a simple fastq manifest file for ``fastq`` single-end read data for two samples.

::

  sample-id	absolute-filepath
  sample-1	$PWD/some/filepath/sample1_R1.fastq
  sample-2	$PWD/some/filepath/sample2_R1.fastq

There are four variants of FASTQ data which you must specify to QIIME 2 when importing, and which are defined in the following sections. Since importing data in these four formats is very similar, we'll only provide examples for two of the variants: ``SingleEndFastqManifestPhred33V2`` and ``PairedEndFastqManifestPhred64V2``.

SingleEndFastqManifestPhred33V2
*******************************

In this variant of the fastq manifest format, the read directions must all either be forward or reverse. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 33.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/importing/se-33.zip
   :saveas: se-33.zip

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/importing/se-33-manifest
   :saveas: se-33-manifest

.. command-block::

   unzip -q se-33.zip

   qiime tools import \
     --type 'SampleData[SequencesWithQuality]' \
     --input-path se-33-manifest \
     --output-path single-end-demux.qza \
     --input-format SingleEndFastqManifestPhred33V2


SingleEndFastqManifestPhred64V2
*******************************

In this variant of the fastq manifest format, the read directions must all either be forward or reverse. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 64. During import, QIIME 2 will convert the PHRED 64 encoded quality scores to PHRED 33 encoded quality scores. This conversion will be slow, but will only happen one time.

PairedEndFastqManifestPhred33V2
*******************************

In this variant of the fastq manifest format, there must be forward and reverse read ``fastq.gz`` / ``fastq`` files for each sample ID. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 33.

PairedEndFastqManifestPhred64V2
*******************************

In this variant of the fastq manifest format, there must be forward and reverse read ``fastq.gz`` / ``fastq`` files for each sample ID. This format assumes that the `PHRED offset`_ used for the positional quality scores in all of the ``fastq.gz`` / ``fastq`` files is 64. During import, QIIME 2 will convert the PHRED 64 encoded quality scores to PHRED 33 encoded quality scores. This conversion will be slow, but will only happen one time.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/importing/pe-64.zip
   :saveas: pe-64.zip

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/importing/pe-64-manifest
   :saveas: pe-64-manifest

.. command-block::

   unzip -q pe-64.zip

   qiime tools import \
     --type 'SampleData[PairedEndSequencesWithQuality]' \
     --input-path pe-64-manifest \
     --output-path paired-end-demux.qza \
     --input-format PairedEndFastqManifestPhred64V2

Sequences without quality information (i.e. FASTA)
--------------------------------------------------------

QIIME 2 currently supports importing the |QIIME1_file|_ format, which consists of a single FASTA file with exactly two lines per record: header and sequence. Each sequence must span exactly one line and cannot be split across multiple lines. The ID in each header must follow the format ``<sample-id>_<seq-id>``. ``<sample-id>`` is the identifier of the sample the sequence belongs to, and ``<seq-id>`` is an identifier for the sequence *within* its sample.

An example of importing and dereplicating this kind of data can be found in the :doc:`OTU Clustering tutorial <otu-clustering>`.

Other FASTA formats like FASTA files with differently formatted sequence headers or per-sample demultiplexed FASTA files (i.e. one FASTA file per sample) are not currently supported.

Per-feature unaligned sequence data (i.e., representative FASTA sequences)
--------------------------------------------------------------------------

Format description
~~~~~~~~~~~~~~~~~~

Unaligned sequence data is imported from a FASTA formatted file containing DNA sequences that are not aligned (i.e., do not contain `-` or `.` characters). The sequences may contain degenerate nucleotide characters, such as ``N``, but some QIIME 2 actions may not support these characters. See the `scikit-bio FASTA format description`_ for more information about the FASTA format.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/importing/sequences.fna
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

Aligned sequence data is imported from a FASTA formatted file containing DNA sequences that are aligned to one another. All aligned sequences must be exactly the same length. The sequences may contain degenerate nucleotide characters, such as ``N``, but some QIIME 2 actions may not support these characters. See the `scikit-bio FASTA format description`_ for more information about the FASTA format.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/importing/aligned-sequences.fna
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
   :url: https://data.qiime2.org/2020.2/tutorials/importing/feature-table-v100.biom
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
   :url: https://data.qiime2.org/2020.2/tutorials/importing/feature-table-v210.biom
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
   :url: https://data.qiime2.org/2020.2/tutorials/importing/unrooted-tree.tre
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

QIIME 2 can import many other data types not covered in this tutorial.
You can see which formats of input data are importable with the following command:

.. command-block::

   qiime tools import \
     --show-importable-formats

And which QIIME 2 types you can import these formats as:

.. command-block::

   qiime tools import \
     --show-importable-types

Unfortunately, there isn't currently documentation detailing which data formats can be imported as which QIIME 2 data types, but hopefully the names of these formats and types should be self-explanatory enough to figure it out.
If you have any questions, please post to the `QIIME 2 Forum`_ for help!

.. _Earth Microbiome Project (EMP) protocol: http://www.earthmicrobiome.org/protocols-and-standards/

.. _Casava 1.8 demultiplexed:  http://illumina.bioinfo.ucr.edu/ht/documentation/data-analysis-docs/CASAVA-FASTQ.pdf/view

.. _QIIME 2 Forum: https://forum.qiime2.org

.. _BIOM v1.0.0 format specification: http://biom-format.org/documentation/format_versions/biom-1.0.html

.. _BIOM v2.1.0 format specification: http://biom-format.org/documentation/format_versions/biom-2.1.html

.. _scikit-bio FASTA format description: http://scikit-bio.org/docs/latest/generated/skbio.io.format.fasta.html#fasta-format

.. _scikit-bio newick format description: http://scikit-bio.org/docs/latest/generated/skbio.io.format.newick.html

.. _absolute filepaths: https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths

.. _PHRED offset: http://scikit-bio.org/docs/latest/generated/skbio.io.format.fastq.html#quality-score-variants

.. |QIIME1_file| replace:: QIIME 1 ``seqs.fna`` file
.. _`QIIME1_file`: http://qiime.org/documentation/file_formats.html#post-split-libraries-fasta-file-overview
