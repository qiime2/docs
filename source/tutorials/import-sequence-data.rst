Importing sequence data
=======================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and have read :doc:`Importing Data <./import>`.

To begin a QIIME 2 analysis with sequence data, for example as generated on an Illumina MiSeq instrument, it must be imported into a QIIME 2 artifact (``.qza``) file. This document illustrates how to import data in various starting formats, and will be expanded as additional relevant formats are identified. Each section below briefly describes a format of sequence data, provides commands to download example data files, and illustrates how to import data in that format.

.. note:: QIIME 2 is not designed for use with any specific sequence data format, but rather is intended to be general to many different data formats. If you need to import data in a format that is not covered here, please post to the `QIIME 2 Forum`_ for help.

"EMP protocol" multiplexed fastq
--------------------------------

Format description
~~~~~~~~~~~~~~~~~~

In the "Earth Microbiome Project (EMP) protocol" format, there are two ``fastq.gz`` files, one containing sequence reads and one containing the associated barcode reads, and the data are still multiplexed. The order of the records in the two ``fastq.gz`` files defines the association between a sequence read and its barcode read. These can be imported as follows.

Obtaining example data
~~~~~~~~~~~~~~~~~~~~~~

.. command-block::

   mkdir raw-sequences

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/moving-pictures/raw-sequences/barcodes.fastq.gz
   :rename: raw-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/moving-pictures/raw-sequences/sequences.fastq.gz
   :rename: raw-sequences/sequences.fastq.gz

Importing data
~~~~~~~~~~~~~~

.. command-block::

   qiime tools import \
     --type RawSequences \
     --input-path raw-sequences/ \
     --output-path raw-sequences.qza

Casava 1.8 single-end demultiplexed fastq
-----------------------------------------

Format description
~~~~~~~~~~~~~~~~~~

In this format, there is one ``fastq.gz`` file for each sample in the study, and the file name includes the sample identifier. The file name for a single sample might look like ``L2S357_15_L001_R1_001.fastq.gz``. The underscore-separated fields in this file name are the sample identifier, the barcode sequence or a barcode identifier, the lane number, the read number, and the set number.

Obtaining example data
~~~~~~~~~~~~~~~~~~~~~~

.. download::
    :url: https://data.qiime2.org/2.0.6/tutorials/importing-sequence-data/casava-18-single-end-demultiplexed.zip
    :rename: casava-18-single-end-demultiplexed.zip

.. command-block::

    unzip -q casava-18-single-end-demultiplexed.zip

Importing data
~~~~~~~~~~~~~~

.. command-block::
    qiime tools import \
      --type 'SampleData[SequencesWithQuality]' \
      --input-path casava-18-single-end-demultiplexed \
      --source-format CasavaOneEightSingleLanePerSampleDirFmt \
      --output-path demux.qza

.. _QIIME 2 Forum: https://forum.qiime2.org
