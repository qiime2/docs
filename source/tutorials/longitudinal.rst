Performing longitudinal and paired sample comparisons with q2-longitudinal
==========================================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial will demonstrate the various features of ``q2-longitudinal``, a plugin that supports statistical and visual comparisons of longitudinal study designs and paired samples, to determine if/how samples change between observational "states". "States" will most commonly be related to time or an environmental gradient, and for paired analyses (`pairwise-distances` and `pairwise-differences`) the sample pairs should typically consist of the same individual subject observed at two different time points. For example, patients in a clinical study whose stool samples are collected before and after receiving treatment.

"States" can also commonly be methodological, in which case sample pairs will usually be the same individual at the same time with two different methods. For example, q2-longitudinal could compare the effects of different collection methods, storage methods, DNA extraction methods, or any bioinformatic processing steps on the feature composition of individual samples.

In the examples below, we use data from the `ECAM study`_, a longitudinal study of infants' and mothers' microbiota from birth through 2 years of life. First let's create a new directory and download the relevant tutorial data.

.. command-block::
   :no-exec:

   mkdir longitudinal-tutorial
   cd longitudinal-tutorial

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/sample_metadata.tsv
   :saveas: ecam-sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/ecam_table_maturity.qza
   :saveas: ecam-table.qza

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/ecam_shannon.qza
   :saveas: shannon.qza

.. download::
   :url: https://data.qiime2.org/2017.9/tutorials/longitudinal/unweighted_unifrac_distance_matrix.qza
   :saveas: unweighted_unifrac_distance_matrix.qza


Pairwise difference comparisons
-------------------------------

Pairwise difference tests determine whether the value of a specific metric changed significantly between pairs of paired samples (e.g., pre- and post-treatment).

This visualizer currently supports comparison of feature abundance (e.g., microbial sequence variants or taxa) in a feature table, or of metadata values in a sample metadata file. Alpha diversity values (e.g., observed sequence variants) and beta diversity values (e.g., principal coordinates) are useful metrics for comparison with these tests, and should be contained in one of the metadata files given as input. In the example below, we will test whether alpha diversity (Shannon diversity index) changed significantly between two different time points in the ECAM data according to delivery mode.

.. command-block::

   qiime longitudinal pairwise-differences \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-file shannon.qza \
     --p-metric shannon \
     --p-group-column delivery \
     --p-state-column month \
     --p-state-1 0 \
     --p-state-2 12 \
     --p-individual-id-column studyid \
     --p-replicate-handling random \
     --o-visualization pairwise-differences.qzv

We can also use this method to measure changes in the abundances of specific features of interest. In this example, we test whether the abundance of genus Bacteroides changed significantly between 6 and 18 months of life in vaginally born and Cesarean-delivered infants, and whether the magnitude of change differed between these groups. Note that `pairwise-differences` accepts a feature table as optional input to extract taxon abundance data.

.. command-block::

   qiime longitudinal pairwise-differences \
     --i-table ecam-table.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --p-metric 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides;s__' \
     --p-group-column delivery \
     --p-state-column month \
     --p-state-1 6 \
     --p-state-2 18 \
     --p-individual-id-column studyid \
     --p-replicate-handling random \
     --o-visualization taxa-differences.qzv


Pairwise distance comparisons
-----------------------------

The ``pairwise-distances`` visualizer also assesses changes between paired samples from two different "states", but instead of taking a metadata column or artifact as input, it operates on a distance matrix to assess the distance between "pre" and "post" sample pairs, and tests whether these paired differences are significantly different between different groups, as specified by the ``group-column`` parameter. Here we use this action to compare the stability of the microbiota compositions of vaginally born and cesarean-delivered infants over a 12-month time frame in the ECAM data set.

.. command-block::

   qiime longitudinal pairwise-distances \
     --i-distance-matrix unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --p-group-column delivery \
     --p-state-column month \
     --p-state-1 0 \
     --p-state-2 12 \
     --p-individual-id-column studyid \
     --p-replicate-handling random \
     --o-visualization pairwise-distances.qzv


Linear mixed effect models
--------------------------

Linear mixed effects (LME) models test the relationship between a single response variable and one or more independent variables, where observations are made across dependent samples, e.g., in repeated-measures sampling experiments. This implementation takes at least one numeric "state_column" (e.g., Time) and one or more comma-separated group_categories (which may be categorical or numeric) as independent variables in a LME model, and plots regression plots of the response variable ("metric") as a function of the state caregory and each group column. The response variable may either be a sample metadata mapping file column or a feature ID in the feature table. Here we use LME to test whether alpha diversity (Shannon diversity index) changed over time and in response to delivery mode, diet, and sex in the ECAM data set.

.. command-block::

   qiime longitudinal linear-mixed-effects \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-file shannon.qza \
     --p-metric shannon \
     --p-group-categories delivery,diet,sex \
     --p-state-column month \
     --p-individual-id-column studyid \
     --o-visualization linear-mixed-effects.qzv

The visualizer produced by this command contains several results. First, the input parameters are shown at the top of the visualization for convenience (e.g., when flipping through multiple visualizations it is useful to have a summary). Scatter plots categorized by each "group column" are shown, with linear regression lines (plus 95% confidence interval in grey) for each group. If ``--p-lowess`` is enabled, instead locally weighted averages are shown for each group. Next, the "model summary" shows some descriptive information about the LME model that was trained. This just shows descriptive information about the "groups"; in this case, groups will be individuals (as set by the ``--p-individual-id-column``). The main results to examine will be the "model results" at the bottom of the visualization. These results summarize the effects of each fixed effect (and their interactions) on the dependent variable (shannon diversity). This table shows parameter estimates, estimate standard errors, Wald Z test statistics, P values (P>|z|), and 95% confidence intervals upper and lower bounds for each parameter. We see in this table that shannon diversity is significantly impacted by month of life and by diet, as well as several interacting factors. More information about LME models and the interpretation of these data can be found on the `statsmodels LME description page`_, which provides a number of useful technical references for further reading.


Volatility analysis
-------------------

Volatility analysis is a method for assessing how volatile a dependent variable is over time (or a gradient) in one or more groups. Whereas LME tests how different factors (e.g., treatment, subject characteristics) impact the trajectory of change in a dependent variable across time (or a gradient), `volatility` examines how variance changes over time (or a gradient), and compares variances between groups at each state, between baseline and each state, and between groups across all states globally. Any metadata (including alpha and beta diversity artifacts) or `FeatureTable[RelativeFrequency]` feature can be used as the dependent variable ("metric"). *Note that volatility analysis currently works best for comparing groups that are sampled fairly evenly at each state in the dataset. Datasets that contain groups sampled at different states are not supported, and users should either filter out those samples or "bin" them with other groups prior to using this visualizer.*

Here we examine how variance in Shannon diversity changes across time in the ECAM cohort.

.. command-block::

   qiime longitudinal volatility \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-file shannon.qza \
     --p-metric shannon \
     --p-group-categories delivery \
     --p-state-column month \
     --p-individual-id-column studyid \
     --o-visualization volatility.qzv


The resulting visualization contains several resuls. First, the "Volatility test parameters" summarizes some key parameters, as well as global mean and standard deviation — these are measured across all samples, regardless of which group they are in.

Second, control charts display the mean value of "metric" at each "state". The first plot shown contains all samples, categorized by group (as defined by `group-column`); the following plots show each individual group, in order to show their individual control characteristics as described in the rest of this paragraph. The mean for all samples in each plot is shown as a black line. The "control limits", 3 standard deviations above and below the mean, are shown as dashed lines. The "warning limits", 2 standard deviations above and below the mean, are shown as dotted lines. The idea behind this plot is to show how a variable is changing over time (or a gradient) in relation to the mean. Large departures from the mean values can cross the warning/control limits, indicating a major disruption at that state; for example, antibiotic use or other disturbances impacting diversity could be tracked with these plots.

Finally, we are interested in seeing how variance changes over time (or a gradient). For example, we may be interested in testing whether a group of patients becomes more variable with time, following a treatment, or in relation to a control group. This pairs well with LME tests, which evaluate the impact of independent variables on the trajectory of change in a dependent variable, but here we are interested in how a single factor impacts the spread of the data. We assess this using variance tests (users have the choice of Bartlett's, `Levene`_, or Fligner-Killeen tests), with the null hypothesis that all distributions being compared have equal variance. Equality of variances is tested between 1) all groups, regardless of state (time point), 2) all groups at each individual state (time point), and 3) between baseline and each state for each group. The row "All states: compare groups" contains the results of test 1. Rows labeled "State s: compare groups" contain the results of test type 2, where "s" indicates the state (e.g., time point) at which groups are compared. Rows labeled "group: baseline vs. state" contain the results of test type 3, where "group" indicates the individual group being tested, "baseline" indicates the baseline state (this defaults to "0", but any value in `state_column` can be used as `baseline`), and "state" indicates the state being compared to baseline. In this example, we see that vaginally delivered and cesarean-delivery infants exhibit significantly different variances across all time (vaginally born infants are more variable but only because they accrue higher species diversity, so this result is not necessarily interesting); that vaginally and cesarean-born infants typically do not exhibit significantly different variances at isolated time points (indicating similar degrees of volatility over time; this is a more important statistic, given the developmental trajectory expected during early life); and that both groups' variances differ significantly from baseline at many times (probably not an important or interesting finding, given the developmental trajectory espected during early life; this particular test is more interesting when assessing, e.g., how a stable system responds to perturbation at a particular time point).


.. _ECAM study: https://doi.org/10.1126/scitranslmed.aad7121
.. _statsmodels LME description page: http://www.statsmodels.org/dev/mixed_linear.html
.. _Levene: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.levene.html
