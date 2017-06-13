Metadata in QIIME 2
===================

.. command-block::
   :no-exec:

   mkdir qiime2-metadata-tutorial
   cd qiime2-metadata-tutorial

Metadata from a mapping file
----------------------------

.. TODO: Update this link
.. download::
   :url: https://data.qiime2.org/2017.5/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

.. TODO: Talk about the file format or something

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv
     --o-visualization tabulated-sample-md.qzv


Metadata from a QIIME 2 artifact
--------------------------------

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/core-metrics-results/faith_pd_vector.qza
   :saveas: faith_pd_vector.qza

.. command-block::
   qiime metadata tabulate \
     --m-input-file faith_pd_vector.qza
     --o-visualization tabulated-faith-pd-md.qzv

Combining metadata
------------------

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv
     --m-input-file faith_pd_vector.qza
     --o-visualization tabulated-combined-md.qzv

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/core-metrics-results/unweighted_unifrac_pcoa_results.qza
   :saveas: unweighted_unifrac_pcoa_results.qza

.. command-block::
   qiime emperor plot \
     --i-pcoa unweighted_unifrac_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-file faith_pd_vector.qza \
     --o-visualization unweighted-unifrac-emperor-with-alpha.qzv

Exploring feature metadata
--------------------------

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/rep-seqs.qza
   :saveas: rep-seqs.qza

.. TODO: update this link
.. download::
   :url: https://docs.qiime2.org/2017.5/data/tutorials/moving-pictures/taxonomy.qza
   :saveas: taxonomy.qza

.. command-block::
   qiime metadata tabulate \
     --m-input-file rep-seqs.qza
     --m-input-file taxonomy.qza
     --o-visualization tabulated-feature-assignments.qzv
