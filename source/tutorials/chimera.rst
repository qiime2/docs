Identifying and filtering chimeric feature sequences with q2-vsearch
====================================================================

Chimera checking in QIIME 2 is performed on a pair of ``FeatureTable[Frequency]`` and ``FeatureData[Sequences]`` artifacts. QIIME 2 wraps the Uchime *de novo* and reference pipelines from vsearch. For details on how these work, see the original `Uchime paper`_, and the `vsearch`_ documentation.

In this tutorial, we'll use the table and sequences from the :doc:`Atacama soils tutorial <atacama-soils>`.

Obtain the data
---------------

Start by creating a directory to work in.

.. command-block::
  :no-exec:

  mkdir qiime2-chimera-filtering-tutorial
  cd qiime2-chimera-filtering-tutorial

Next, download the necessary files:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/chimera/atacama-table.qza
   :saveas: atacama-table.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/chimera/atacama-rep-seqs.qza
   :saveas: atacama-rep-seqs.qza

Run *de novo* chimera checking
------------------------------

.. command-block::

   qiime vsearch uchime-denovo \
     --i-table atacama-table.qza \
     --i-sequences atacama-rep-seqs.qza \
     --output-dir uchime-dn-out

.. note::
   Reference-based chimera checking is also available - see :doc:`vsearch uchime-ref <../plugins/available/vsearch/uchime-ref/>` for more details.

Visualize summary stats
-----------------------

To learn more about the sequences that were identified as chimeric, we can ``tabulate`` the stats output from the previous step:

.. command-block::

   qiime metadata tabulate \
     --m-input-file uchime-dn-out/stats.qza \
     --o-visualization uchime-dn-out/stats.qzv


Filter input tables and sequences
---------------------------------

Exclude chimeras and "borderline chimeras"
..........................................

.. command-block::

   qiime feature-table filter-features \
     --i-table atacama-table.qza \
     --m-metadata-file uchime-dn-out/nonchimeras.qza \
     --o-filtered-table uchime-dn-out/table-nonchimeric-wo-borderline.qza
   qiime feature-table filter-seqs \
     --i-data atacama-rep-seqs.qza \
     --m-metadata-file uchime-dn-out/nonchimeras.qza \
     --o-filtered-data uchime-dn-out/rep-seqs-nonchimeric-wo-borderline.qza
   qiime feature-table summarize \
     --i-table uchime-dn-out/table-nonchimeric-wo-borderline.qza \
     --o-visualization uchime-dn-out/table-nonchimeric-wo-borderline.qzv

Exclude chimeras but retain "borderline chimeras"
.................................................

.. command-block::

   qiime feature-table filter-features \
     --i-table atacama-table.qza \
     --m-metadata-file uchime-dn-out/chimeras.qza \
     --p-exclude-ids \
     --o-filtered-table uchime-dn-out/table-nonchimeric-w-borderline.qza
   qiime feature-table filter-seqs \
     --i-data atacama-rep-seqs.qza \
     --m-metadata-file uchime-dn-out/chimeras.qza \
     --p-exclude-ids \
     --o-filtered-data uchime-dn-out/rep-seqs-nonchimeric-w-borderline.qza
   qiime feature-table summarize \
     --i-table uchime-dn-out/table-nonchimeric-w-borderline.qza \
     --o-visualization uchime-dn-out/table-nonchimeric-w-borderline.qzv

.. _Uchime paper: http://dx.doi.org/10.1093/bioinformatics/btr381
.. _vsearch: https://github.com/torognes/vsearch
