Alternative methods of read-joining in QIIME 2
==============================================

.. note:: This tutorial does not cover read-joining and denoising with
   DADA2. Instead, this tutorial focuses on alternative approaches to analyzing
   paired-end reads in QIIME 2. If you are interested in joining and denoising
   reads with DADA2, the :doc:`Atacama soil microbiome tutorial
   <atacama-soils>` illustrates how to use ``qiime dada2 denoise-paired`` for
   this purpose.  If you plan to use DADA2 to join and denoise your paired end
   data, **do not join your reads prior to denoising with DADA2;** DADA2
   expects reads that have not yet been joined, and will join the reads for you
   during the denoising process.

In QIIME 2, we use the term *single-end reads* to refer to forward or reverse
reads in isolation; we use the term *paired-end reads* to refer to forward and
reverse reads that have not yet been joined; and we use the term *joined reads*
to refer to forward and reverse reads that have already been joined (or
merged). **It is important to understand which of these terms apply to your
data, as this will determine what steps are necessary to analyze your
paired-end data.**

It is currently possible to join paired-end reads in QIIME 2 using the
``q2-vsearch`` plugin, or to import reads that have been joined outside of
QIIME 2 (for example, with `fastq-join`_, see `Importing pre-joined reads`_ for
more details).  This tutorial will cover both of these processes.

Obtain the data
~~~~~~~~~~~~~~~

Start by creating a directory to work in.

.. command-block::
  :no-exec:

  mkdir qiime2-read-joining-tutorial
  cd qiime2-read-joining-tutorial

Next, download the following ``SampleData[PairedEndSequencesWithQuality]``
artifact, which contains the demultiplexed reads from the :doc:`Atacama soil
microbiome tutorial <atacama-soils>`.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/read-joining/atacama-seqs.qza
   :saveas: demux.qza

Joining reads
~~~~~~~~~~~~~

Next, use the ``join-pairs`` method in the ``q2-vsearch`` plugin to join the
reads:

.. command-block::

   qiime vsearch join-pairs \
     --i-demultiplexed-seqs demux.qza \
     --o-joined-sequences demux-joined.qza

Viewing a summary of joined data with read quality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can next generate a summary of the ``demux-joined.qza`` artifact.

.. command-block::

   qiime demux summarize \
     --i-data demux-joined.qza \
     --o-visualization demux-joined.qzv

This summary is particularly useful for determining approximately how long your
joined reads are (we’ll come back to this when we denoise with Deblur). When
looking at the quality plots in this visualization, if you hover over a
specific position you’ll see how many reads are at least that long (of the
reads that were sampled for computing sequence quality). Make note of the
highest sequence position where most (say, > 99%) of your reads are at least
that long.

For example, when hovering over a black box in this visualization (which is
generated from a larger data set than the one used in this tutorial), I see
that 10000 out of the 40126 sequences were used to estimate the quality score
distribution at this position.

When I hover over position 250, which is illustrated with a red box, I see that
some sequences are not this long because only 9994 sequences were used for
estimating the quality score distribution at this position. The red box and the
red text below tell me that some sequences were not at least this long.

When I hover over position 254, which is also illustrated with a red box, I see
that many sequences are not this long because only 845 sequences were used for
estimating the quality score distribution at this position.

**Based on a comparison of these plots, I will note that most of my sequences
are at least 250 bases long.** We plan to simplify this process in `the near
future`_.

Sequence quality control
~~~~~~~~~~~~~~~~~~~~~~~~

Next we’ll apply quality control to our sequences using ``quality-filter
q-score-joined``. This method is identical to ``quality-filter q-score``,
except that it operated on joined reads. The parameters to this method have not
been extensively benchmarked on joined read data, so we recommend experimenting
with different parameter settings.

.. command-block::

   qiime quality-filter q-score-joined \
     --i-demux demux-joined.qza \
     --o-filtered-sequences demux-joined-filtered.qza \
     --o-filter-stats demux-joined-filter-stats.qza

At this stage you can choose to proceed using `Deblur`_ for additional quality
control, or you can dereplicate sequences and optionally :doc:`cluster them
<../plugins/available/vsearch/index>` into OTUs with ``q2-vsearch``. Deblur
should give much higher quality results, so we recommend that procedure and
will illustrate that approach in the next steps of this tutorial.

If you are instead interested in experimenting with an analysis workflow that
is more like QIIME 1 processing (for example, to compare your Deblur or DADA2
result with a QIIME 1-like pipeline), you should next dereplicate and cluster
your sequences. If you try this option, we strongly encourage you to call
``qiime quality-filter q-score-joined`` with a higher ``min-quality`` threshold
- possibly ``--p-min-quality 20`` or ``--p-min-quality 30`` (see `Bokulich et
al. 2013`_ for more details). You can then follow the steps in the `OTU
clustering tutorial`_. After clustering, you will likely want to filter
features that are observed in only one sample using ``qiime feature-table
filter-features --p-min-samples``. In addition, removing singletons with an
abundance filter is also advisable (see `Bokulich et al. 2013`_ for more
details), as well as :doc:`filtering chimeric sequences <chimera>`.

Deblur
~~~~~~

You’re now ready to denoise your sequences with Deblur. You should pass
the sequence length value you selected from the quality score plots for
``--p-trim-length``. This will trim all sequences to this length, and
discard any sequences which are not at least this long.

.. note:: We use a trim length of 250 based on the quality score plots
   generated from the tutorial data set. Do not use 250 with your own data set,
   as this value will depend on your data set’s read lengths. Use the quality
   score plots to choose an appropriate trim length for your data.

.. command-block::

   qiime deblur denoise-16S \
     --i-demultiplexed-seqs demux-joined-filtered.qza \
     --p-trim-length 250 \
     --p-sample-stats \
     --o-representative-sequences rep-seqs.qza \
     --o-table table.qza \
     --o-stats deblur-stats.qza

View summary of Deblur feature table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can next summarize the feature table resulting from q2-deblur. This table
and the corresponding representative sequences are now ready to be analyzed
with the same methods and visualizers that would be used on single-end read
data.

.. command-block::

   qiime feature-table summarize \
     --i-table table.qza \
     --o-visualization table.qzv

--------------

Importing pre-joined reads
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have joined your reads outside of QIIME 2, for example with
``fastq-join``, this section will illustrate how to import those reads.
First, download the following demultiplexed and joined read data, which
has been joined on a per-sample basis with ``fastq-join``.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/read-joining/fj-joined.zip
   :saveas: fj-joined.zip

Unzip this file as follows:

.. command-block::

   unzip fj-joined.zip

Import reads
------------

Next, use ``qiime tools import`` to import these data. The format that is
currently used here is ``SingleEndFastqManifestPhred33`` - this will
likely be `updated in the future`_ to a format
that clearly describes this as joined read data, but in the meantime you
should follow the :doc:`formatting guidelines for the single-end "Fastq
Manifest" formats <importing>`.

.. command-block::

   qiime tools import \
     --input-path fj-joined/manifest \
     --output-path fj-joined-demux.qza \
     --type SampleData[JoinedSequencesWithQuality] \
     --input-format SingleEndFastqManifestPhred33

Viewing summary of imported data with read quality
--------------------------------------------------

You can generate a summary of the resulting artifact as follows:

.. command-block::

   qiime demux summarize \
     --i-data fj-joined-demux.qza \
     --o-visualization fj-joined-demux.qzv

You can now continue analyses with your joined reads as described above,
e.g. quality filtering with q2-quality-filter, denoising with q2-deblur, or
dereplicating and picking OTUs with q2-vsearch.

Happy QIIMEing!

.. _fastq-join: https://github.com/brwnj/fastq-join
.. _`the near future`: https://github.com/qiime2/q2-demux/issues/71
.. _Deblur: http://msystems.asm.org/content/2/2/e00191-16
.. _`OTU clustering tutorial`: https://forum.qiime2.org/t/clustering-sequences-into-otus-using-q2-vsearch/1348
.. _`updated in the future`: https://github.com/qiime2/q2-types/issues/162
.. _`Bokulich et al. 2013`: https://doi.org/10.1038/nmeth.2276
