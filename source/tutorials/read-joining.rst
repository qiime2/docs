Alternative methods of read-joining in QIIME 2
==============================================

.. include:: ../_old_docs_warning.rst

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
   :url: https://data.qiime2.org/2024.10/tutorials/read-joining/atacama-seqs.qza
   :saveas: demux.qza

Joining reads
~~~~~~~~~~~~~

Next, use the ``merge-pairs`` method in the ``q2-vsearch`` plugin to join the
reads:

.. command-block::

   qiime vsearch merge-pairs \
     --i-demultiplexed-seqs demux.qza \
     --o-merged-sequences demux-joined.qza \
     --o-unmerged-sequences demux-unjoined.qza

Viewing a summary of joined data with read quality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can next generate a summary of the ``demux-joined.qza`` artifact.

.. command-block::

   qiime demux summarize \
     --i-data demux-joined.qza \
     --o-visualization demux-joined.qzv

This summary is particularly useful for estimating joined read length as well as the
quality scores at each sequence base position. If you hover over a specific position
on the interactive quality plot you will see the table below the plot updates itself
to display the parametric seven-number summary for that sequence base position.
This table corresponds to what is visually represented by the box plot at that position.
Between the plot and the table you can see that 10,000 out of the 40,126 sequences
were used to estimate the quality scores at each position.

Hovering over positions towards the other end of the plot and examining their
respective seven-number summary shows the gradual decline in quality scores that is
frequently observed towards the 3' end.

Based on the demultiplexed sequence length summary table at the bottom of this
visualization, we can see that most of our sequences are at least 250 bases long.
**This information along with what we've noted about the quality scores above will
help us to determine the trim length that we'll use in the denoising step below.**

Sequence quality control
~~~~~~~~~~~~~~~~~~~~~~~~

Next we’ll apply quality control to our sequences using ``quality-filter
q-score``. The parameters to this method have not been extensively benchmarked
on joined read data, so we recommend experimenting with different parameter
settings.

.. command-block::

   qiime quality-filter q-score \
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
``qiime quality-filter q-score`` with a higher ``min-quality`` threshold
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
   :url: https://data.qiime2.org/2024.10/tutorials/read-joining/fj-joined.zip
   :saveas: fj-joined.zip

Unzip this file as follows:

.. command-block::

   unzip fj-joined.zip

Import reads
------------

Next, use ``qiime tools import`` to import these data. The format that is
currently used here is ``SingleEndFastqManifestPhred33V2`` - this will
likely be `updated in the future`_ to a format
that clearly describes this as joined read data, but in the meantime you
should follow the :doc:`formatting guidelines for the single-end "Fastq
Manifest" formats <importing>`.

.. command-block::

   qiime tools import \
     --input-path fj-joined/manifest \
     --output-path fj-joined-demux.qza \
     --type SampleData[JoinedSequencesWithQuality] \
     --input-format SingleEndFastqManifestPhred33V2

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
