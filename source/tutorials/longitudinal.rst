Performing longitudinal and paired sample comparisons with q2-longitudinal
==========================================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

This tutorial will demonstrate the various features of ``q2-longitudinal``, a plugin that supports statistical and visual comparisons of longitudinal study designs and paired samples, to determine if/how samples change between observational "states". "States" will most commonly be related to time, and the sample pairs should typically consist of the same individual subject  observed at two different time points. For example, patients in a clinical study whose stool samples are collected before and after receiving treatment.

"States" can also commonly be methodological, in which case sample pairs will usually be the same individual at the same time with two different methods. For example, q2-longitudinal could compare the effects of different collection methods, storage methods, DNA extraction methods, or any bioinformatic processing steps on the feature composition of individual samples.

In the examples below, we will use the :doc:`moving pictures tutorial data <moving-pictures>`. First let's create a new directory and download the relevant tutorial data.

.. command-block::
   :no-exec:

   mkdir longitudinal-tutorial
   cd longitudinal-tutorial

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: moving-pictures-sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/table.qza
   :saveas: moving-pictures-table.qza

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/observed_otus_vector.qza
   :saveas: observed_otus_vector.qza

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/unweighted_unifrac_distance_matrix.qza
   :saveas: unweighted_unifrac_distance_matrix.qza


Pairwise difference comparisons
-------------------------------

Pairwise difference tests determine whether the value of a specific metric changed significantly between pairs of paired samples (e.g., pre- and post-treatment).

This visualizer currently supports comparison of feature abundance (e.g., microbial sequence variants or taxa) in a feature table, or of metadata values in a sample metadata file. Alpha diversity values (e.g., observed sequence variants) and beta diversity values (e.g., principal coordinates) are useful metrics for comparison with these tests, and should be contained in one of the metadata files given as input. In the example below, we will test whether alpha diversity (observed OTUs) changed significantly between two different time points in the moving pictures data in each body site.

.. command-block::

   qiime longitudinal pairwise-differences \
     --m-metadata-file moving-pictures-sample-metadata.tsv \
     --m-metadata-file observed_otus_vector.qza \
     --p-metric observed_otus \
     --p-group-column BodySite \
     --p-state-column Month \
     --p-state-1 1 \
     --p-state-2 10 \
     --p-individual-id-column Subject \
     --p-replicate-handling random \
     --o-visualization pairwise-differences.qzv


Pairwise distance comparisons
-----------------------------

The ``pairwise-distances`` visualizer also assesses changes between paired samples from two different "states", but instead of taking a metadata column or artifact as input, it operates on a distance matrix to assess the distance between "pre" and "post" sample pairs, and tests whether these paired differences are significantly different between different groups, as specified by the ``group-column`` parameter. Here we use this action to test whether the microbiota compositions of some body sites are more stable than others over a 9-month time frame in the moving pictures data set.

.. command-block::

   qiime longitudinal pairwise-distances \
     --i-distance-matrix unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file moving-pictures-sample-metadata.tsv \
     --p-group-column BodySite \
     --p-state-column Month \
     --p-state-1 1 \
     --p-state-2 10 \
     --p-individual-id-column Subject \
     --p-replicate-handling random \
     --o-visualization pairwise-distances.qzv


Linear mixed effect models
--------------------------

Linear mixed effects (LME) models test the relationship between a single response variable and one or more independent variables, where observations are made across dependent samples, e.g., in repeated-measures sampling experiments. This implementation takes at least one numeric "state_column" (e.g., Time) and one or more comma-separated group_categories (which may be categorical or numeric) as independent variables in a LME model, and plots regression plots of the response variable ("metric") as a function of the state caregory and each group column. The response variable may either be a sample metadata mapping file column or a feature ID in the feature table. Here we use LME to test whether alpha diversity (observed OTUs) changed over time and in response to body site and antibiotic use in the moving pictures data set.

.. command-block::

   qiime longitudinal linear-mixed-effects \
     --m-metadata-file moving-pictures-sample-metadata.tsv \
     --m-metadata-file observed_otus_vector.qza \
     --p-metric observed_otus \
     --p-group-categories BodySite,ReportedAntibioticUsage \
     --p-state-column Month \
     --p-individual-id-column Subject \
     --o-visualization linear-mixed-effects.qzv

The visualizer produced by this command contains several results. First, the input parameters are shown at the top of the visualization for convenience (e.g., when flipping through multiple visualizations it is useful to have a summary). Scatter plots categorized by each "group column" are shown, with linear regression lines (plus 95% confidence interval in grey) for each group. If ``--p-lowess`` is enabled, instead locally weighted averages are shown for each group. Next, the "model summary" shows some descriptive information about the LME model that was trained. This just shows descriptive information about the "groups"; in this case, groups will be individuals (as set by the ``--p-individual-id-column``). The main results to examine will be the "model results" at the bottom of the visualization. These results summarize the effects of each fixed effect (and their interactions) on the dependent variable (shannon diversity). This table shows parameter estimates, estimate standard errors, Wald Z test statistics, P values (P>|z|), and 95% confidence intervals upper and lower bounds for each parameter. We see in this table that shannon diversity is significantly impacted by month of life and by diet, as well as several interacting factors. More information about LME models and the interpretation of these data can be found on the `statsmodels LME description page`_, which provides a number of useful technical references for further reading.

.. _statsmodels LME description page: http://www.statsmodels.org/dev/mixed_linear.html
