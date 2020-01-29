Exporting data
==============

.. note:: This tutorial assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

In order to use QIIME 2, your input data must be stored in *QIIME 2 artifacts* (i.e. ``.qza`` files). This is what enables distributed and automatic provenance tracking, as well as semantic type validation and transformations between data formats (see the :doc:`core concepts <../concepts>` page for more details about QIIME 2 artifacts).

Sometimes you'll want to export data from a QIIME 2 artifact, for example to analyze data with a different microbiome analysis program, or to do statistical analysis in R. This can be achieved used the ``qiime tools export`` command, which takes a QIIME 2 artifact (``.qza``) file and an output directory as input. The data in the artifact will exported to one or more files depending on the specific artifact.

.. warning:: When exporting data from a QIIME 2 artifact, there will no longer be provenance associated with the data. If you subsequently re-import the exported data, the provenance associated with the new artifact will begin with the import step and all existing provenance will be lost. It's therefore best to only export data from artifacts when you are done with all processing steps that can be achieved with QIIME 2 to maximize the value of each artifact's provenance.

The following sections provide examples of exporting data from QIIME 2 artifacts. It is possible to export data from any QIIME 2 artifact or visualization; the process is the same as what is described below.

Exporting a feature table
-------------------------

A ``FeatureTable[Frequency]`` artifact will be exported as a `BIOM v2.1.0 formatted file`_.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/exporting/feature-table.qza
   :saveas: feature-table.qza

.. command-block::

   qiime tools export \
     --input-path feature-table.qza \
     --output-path exported-feature-table

Exporting a phylogenetic tree
-----------------------------

A ``Phylogeny[Unrooted]`` artifact will be exported as a `newick formatted file`_.

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/exporting/unrooted-tree.qza
   :saveas: unrooted-tree.qza

.. command-block::

   qiime tools export \
     --input-path unrooted-tree.qza \
     --output-path exported-tree

.. _`export vs extract`:

Exporting versus extracting
---------------------------

QIIME 2 artifacts can be extracted using ``qiime tools extract``. Extracting an artifact differs from exporting an artifact. When exporting an artifact, only the data files will be placed in the output directory. Extracting will additionally provide QIIME 2's metadata about an artifact, including for example the artifact's provenance, in the output directory in plain-text formats. An artifact can be extracted as follows. The directory that you're extracting to must already exist.

.. command-block::

   mkdir extracted-feature-table
   qiime tools extract \
     --input-path feature-table.qza \
     --output-path extracted-feature-table

The output directory will contain a new directory whose name is the artifact's UUID. All artifact data and metadata will be stored in that directory.

.. note:: While it is possible to view an artifact's provenance from its extracted metadata text files, the graphical provenance viewer at https://view.qiime2.org is the recommended way to view an artifact's provenance.

.. _BIOM v2.1.0 formatted file: http://biom-format.org/documentation/format_versions/biom-2.1.html

.. _newick formatted file: http://scikit-bio.org/docs/latest/generated/skbio.io.format.newick.html
