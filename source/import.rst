Importing data
==============

.. note:: This guide assumes you have performed the steps in the :doc:`install guide <install>`.

In order to use QIIME 2, we require input data to be stored in *artifacts* (i.e. ``.qza`` files). This is what enables distributed and automatic provenance tracking, as well as semantic type validation and transformations between data formats. This guide will demonstrate how to import data into an artifact. This will typically happen with your initial data (e.g. raw sequences obtained from a sequencing facility), but importing can be performed at any step in your analysis pipeline. For example, if a collaborator provides you with a ``.biom`` file, you can import it into an artifact to perform "downstream" statistical analyses.

Importing can be accomplished using any of the QIIME 2 :doc:`interfaces <interfaces/index>`. This guide will focus on using the QIIME 2 command-line interface (``q2cli``) to import data.

First, let's download an example ``.biom`` file:

.. command-block::

   curl -sLO https://data.qiime2.org/2.0.6/tutorials/examples/feature-table.biom

Next we will use the ``qiime tools import`` command, providing a semantic type of ``FeatureTable[Frequency]`` for the ``.biom`` file because this is a feature table of counts (i.e. frequencies):

.. command-block::

   qiime tools import --input-path feature-table.biom --output-path feature-table --type "FeatureTable[Frequency]" --source-format BIOMV100Format

.. note:: We didn't specify a file extension for the output file (``--output-path feature-table``). The command-line interface will automatically append the ``.qza`` file extension (if it isn't present) to output artifacts, and the ``.qzv`` file extension to visualizations.

We now have a QIIME 2 artifact called ``feature-table.qza`` that we can start using in QIIME 2 analyses! For example, we can create a summary of the feature table as follows:

.. command-block::

   qiime feature-table summarize --i-table feature-table.qza --o-visualization table-summary

To see what semantic types are available in QIIME 2 and to learn more about them, see the :doc:`semantic types <semantic-types>` section of our documentation.
