"Atacama soil microbiome" tutorial
==================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

This tutorial is designed to serve two purposes. First, it illustrates the initial processing steps of paired-end read analysis, up to the point where the analysis steps are identical to single-end read analysis. This includes the importing, demultiplexing, and denoising steps, and results in a feature table and the associated feature sequences. Second, this is intended to be a self-guided exercise that could be run after :doc:`the moving pictures tutorial <moving-pictures>` to gain more experience with QIIME 2. For this exercise, we provide some questions that can be used to guide your analysis, but do not provide commands that will allow you to address each. Instead, you should apply the commands that you learned in :doc:`the moving pictures tutorial <moving-pictures>`.

In this tutorial you'll use QIIME 2 to perform an analysis of soil samples from the Atacama Desert in northern Chile. The Atacama Desert is one of the most arid locations on Earth, with some areas receiving less than a millimeter of rain per decade. Despite this extreme aridity, there are microbes living in the soil. The soil microbiomes profiled in this study follow two east-west transects, *Baquedano* and *Yungay*, across which average soil relative humidity is positively correlated with elevation (higher elevations are less arid and thus have higher average soil relative humidity). Along these transects, pits were dug at each site and soil samples were collected from three depths in each pit.

Obtain the data
---------------

Start by creating a directory to work in.

.. command-block::
   :no-exec:

   mkdir qiime2-atacama-tutorial
   cd qiime2-atacama-tutorial

Before starting the analysis, explore the sample metadata to familiarize yourself with the samples used in this study. The `sample metadata`_ is available as a Google Sheet. This ``sample-metadata.tsv`` file is used throughout the rest of the tutorial.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/sample_metadata.tsv
   :saveas: sample-metadata.tsv


Next, you'll download the multiplexed reads. You will download three ``fastq.gz`` files, corresponding to the forward, reverse, and barcode (i.e., index) reads. These files contain a subset of the reads in the full data set generated for this study, which allows for the following commands to be run relatively quickly. If you are only planning to run through the commands presented here to get experience with the first steps of paired-end read analysis, you can use the 1% subsample data set so that the commands will run quickly. If you're planning to work through the questions presented at the end of this document to gain more experience with QIIME analysis and data interpretation, you should use the 10% subsample data set so that the analysis results will be supported by more sequence data.

1% subsample data
~~~~~~~~~~~~~~~~~

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

10% subsample data
~~~~~~~~~~~~~~~~~~

.. command-block::
   :no-exec:

   mkdir emp-paired-end-sequences

.. download::
   :no-exec:
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/10p/forward.fastq.gz
   :saveas: emp-paired-end-sequences/forward.fastq.gz

.. download::
   :no-exec:
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/10p/reverse.fastq.gz
   :saveas: emp-paired-end-sequences/reverse.fastq.gz

.. download::
   :no-exec:
   :url: https://data.qiime2.org/2020.2/tutorials/atacama-soils/10p/barcodes.fastq.gz
   :saveas: emp-paired-end-sequences/barcodes.fastq.gz


.. _`atacama demux`:

Paired-end read analysis commands
---------------------------------

To analyze these data, the sequences that you just downloaded must first be imported into an artifact of type ``EMPPairedEndSequences``.

.. command-block::

   qiime tools import \
      --type EMPPairedEndSequences \
      --input-path emp-paired-end-sequences \
      --output-path emp-paired-end-sequences.qza

You next can demultiplex the sequence reads. This requires the sample metadata file, and you must indicate which column in that file contains the per-sample barcodes. In this case, that column name is ``barcode-sequence``. In this data set, the barcode reads are the reverse complement of those included in the sample metadata file, so we additionally include the ``--p-rev-comp-mapping-barcodes`` parameter. After demultiplexing, we can generate and view a summary of how many sequences were obtained per sample.

.. command-block::

   qiime demux emp-paired \
     --m-barcodes-file sample-metadata.tsv \
     --m-barcodes-column barcode-sequence \
     --p-rev-comp-mapping-barcodes \
     --i-seqs emp-paired-end-sequences.qza \
     --o-per-sample-sequences demux.qza \
     --o-error-correction-details demux-details.qza

   qiime demux summarize \
     --i-data demux.qza \
     --o-visualization demux.qzv

After demultiplexing reads, we'll look at the sequence quality based on ten-thousand randomly selected reads, and then denoise the data. When you view the quality plots, note that in contrast to the corresponding plots in :doc:`the moving pictures tutorial <moving-pictures>`, there are now two interactive plots to be considered together. The plot on the left presents the quality scores for the forward reads, and the plot on the right presents the quality scores for the reverse reads. We'll use these plots to determine what trimming parameters we want to use for denoising with DADA2, and then denoise the reads using ``dada2 denoise-paired``.

In this example we have 150-base forward and reverse reads. Since we need the reads to be long enough to overlap when joining paired ends, the first thirteen bases of the forward and reverse reads are being trimmed, but no trimming is being applied to the ends of the sequences to avoid reducing the read length by too much. In this example, the same values are being provided for ``--p-trim-left-f`` and ``--p-trim-left-r`` and for ``--p-trunc-len-f`` and ``--p-trunc-len-r``, but that is not a requirement.

.. command-block::

   qiime dada2 denoise-paired \
     --i-demultiplexed-seqs demux.qza \
     --p-trim-left-f 13 \
     --p-trim-left-r 13 \
     --p-trunc-len-f 150 \
     --p-trunc-len-r 150 \
     --o-table table.qza \
     --o-representative-sequences rep-seqs.qza \
     --o-denoising-stats denoising-stats.qza

At this stage, you will have artifacts containing the feature table and corresponding feature sequences. You can generate summaries of those as follows.

.. command-block::

   qiime feature-table summarize \
     --i-table table.qza \
     --o-visualization table.qzv \
     --m-sample-metadata-file sample-metadata.tsv

   qiime feature-table tabulate-seqs \
     --i-data rep-seqs.qza \
     --o-visualization rep-seqs.qzv

As well, you can visualize the denoising stats by running:

.. command-block::

   qiime metadata tabulate \
     --m-input-file denoising-stats.qza \
     --o-visualization denoising-stats.qzv

From this point, analysis of paired-end read data progresses in the same way as analysis of single-end read data. You can therefore continue your analyses of these data following the steps that you ran in :doc:`the moving pictures tutorial <moving-pictures>`.

Questions to guide data analysis
--------------------------------

Use the following questions to guide your further analyses of these data data.

#. What value would you choose to pass for ``--p-sampling-depth``? How many samples will be excluded from your analysis based on this choice? Approximately how many total sequences will you be analyzing in the ``core-metrics-phylogenetic`` command?

#. What sample metadata or combinations of sample metadata are most strongly associated with the differences in microbial composition of the samples? Are these associations stronger with unweighted UniFrac or with Bray-Curtis? Based on what you know about these metrics, what does that difference suggest? For exploring associations between continuous metadata and sample composition, the commands ``qiime metadata distance-matrix`` in combination with ``qiime diversity mantel`` and ``qiime diversity bioenv`` will be useful. These were not covered in the Moving Pictures tutorial, but you can learn about them by running them with the ``--help`` parameter.

#. What do you conclude about the associations between continuous sample metadata and the richness and evenness of these samples? For exploring associations between continuous metadata and richness or evenness, the command ``qiime diversity alpha-correlation`` will be useful. This was not covered in the Moving Pictures tutorial, but you can learn about it by running it with the ``--help`` parameter.

#. Which categorical sample metadata columns are most strongly associated with the differences in microbial community richness or evenness? Are these differences statistically significant?

#. In taxonomic composition bar plots, sort the samples by their average soil relative humidity, and visualize them at the phylum level. What are the dominant phyla in these samples? Which phyla increase and which decrease with increasing average soil relative humidity?

#. What phyla differ in abundance across vegetated and unvegetated sites?

Acknowledgements
----------------

The data used in this tutorial is presented in: *Significant Impacts of Increasing Aridity on the Arid Soil Microbiome.* Julia W. Neilson, Katy Califf, Cesar Cardona, Audrey Copeland, Will van Treuren, Karen L. Josephson, Rob Knight, Jack A. Gilbert, Jay Quade, J. Gregory Caporaso, and Raina M. Maier. mSystems May 2017, 2 (3) e00195-16; DOI: 10.1128/mSystems.00195-16.

.. _sample metadata: https://data.qiime2.org/2020.2/tutorials/atacama-soils/sample_metadata
