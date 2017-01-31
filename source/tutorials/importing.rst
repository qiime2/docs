Importing data
==============

.. note:: This tutorial assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

In order to use QIIME 2, we require input data to be stored in *artifacts* (i.e. ``.qza`` files). This is what enables distributed and automatic provenance tracking, as well as semantic type validation and transformations between data formats (see the :doc:`core concepts <../concepts>` page for more details about artifacts). This tutorial demonstrates how to import various data formats into artifacts for use with QIIME 2.

.. note:: This tutorial does not describe all data formats that are currently supported in QIIME 2. It is a work-in-progress that describes some of the most commonly used data formats available in QIIME 2. We are also actively working on supporting additional data formats. If you need to import data in a format that is not covered here, please post to the `QIIME 2 Forum`_ for help.

Importing will typically happen with your initial data (e.g. raw sequences obtained from a sequencing facility), but importing can be performed at any step in your analysis pipeline. For example, if a collaborator provides you with a ``.biom`` file, you can import it into an artifact to perform "downstream" statistical analyses that operate on a feature table.

Importing can be accomplished using any of the QIIME 2 :doc:`interfaces <../interfaces/index>`. This tutorial will focus on using the QIIME 2 command-line interface (``q2cli``) to import data. Each section below briefly describes a data format, provides commands to download example data, and illustrates how to import the data into an artifact.

Sequence data
-------------

"EMP protocol" multiplexed fastq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format description
******************

In the "Earth Microbiome Project (EMP) protocol" format, there are two ``fastq.gz`` files, one containing sequence reads and one containing the associated barcode reads, with the sequence data still multiplexed. The order of the records in the two ``fastq.gz`` files defines the association between a sequence read and its barcode read.

Obtaining example data
**********************

.. command-block::

   mkdir raw-sequences

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/moving-pictures/raw-sequences/barcodes.fastq.gz
   :saveas: raw-sequences/barcodes.fastq.gz

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/moving-pictures/raw-sequences/sequences.fastq.gz
   :saveas: raw-sequences/sequences.fastq.gz

Importing data
**************

.. command-block::

   qiime tools import \
     --type EMPSingleEndSequences \
     --input-path raw-sequences \
     --output-path raw-sequences.qza

Casava 1.8 single-end demultiplexed fastq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format description
******************

In this format, there is one ``fastq.gz`` file for each sample in the study, and the file name includes the sample identifier. The file name for a single sample might look like ``L2S357_15_L001_R1_001.fastq.gz``. The underscore-separated fields in this file name are the sample identifier, the barcode sequence or a barcode identifier, the lane number, the read number, and the set number.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/importing-sequence-data/casava-18-single-end-demultiplexed.zip
   :saveas: casava-18-single-end-demultiplexed.zip

.. command-block::

   unzip -q casava-18-single-end-demultiplexed.zip

Importing data
**************

.. command-block::
   qiime tools import \
     --type 'SampleData[SequencesWithQuality]' \
     --input-path casava-18-single-end-demultiplexed \
     --source-format CasavaOneEightSingleLanePerSampleDirFmt \
     --output-path demux.qza

Feature table data
------------------

BIOM v1.0.0
~~~~~~~~~~~

Format description
******************

See the `BIOM v1.0.0 format specification`_ for details.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2.0.6/tutorials/examples/feature-table.biom
   :saveas: feature-table.biom

Importing data
**************

.. command-block::

   qiime tools import \
     --input-path feature-table.biom \
     --type "FeatureTable[Frequency]" \
     --source-format BIOMV100Format \
     --output-path feature-table.qza

BIOM v2.1.0
~~~~~~~~~~~

Format description
******************

See the `BIOM v2.1.0 format specification`_ for details.

Obtaining example data
**********************

.. download::
   :url: https://data.qiime2.org/2017.2/tutorials/importing/feature-table-v210.biom
   :saveas: feature-table-v210.biom

Importing data
**************

.. command-block::

   qiime tools import \
     --input-path feature-table-v210.biom \
     --type "FeatureTable[Frequency]" \
     --source-format BIOMV210Format \
     --output-path feature-table-v210.qza

.. _QIIME 2 Forum: https://forum.qiime2.org

.. _BIOM v1.0.0 format specification: http://biom-format.org/documentation/format_versions/biom-1.0.html

.. _BIOM v2.1.0 format specification: http://biom-format.org/documentation/format_versions/biom-2.1.html
