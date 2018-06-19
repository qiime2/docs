Performing longitudinal and paired sample comparisons with q2-longitudinal
==========================================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial will demonstrate the various features of ``q2-longitudinal``, a plugin that supports statistical and visual comparisons of longitudinal study designs and paired samples, to determine if/how samples change between observational "states". "States" will most commonly be related to time or an environmental gradient, and for paired analyses (``pairwise-distances`` and ``pairwise-differences``) the sample pairs should typically consist of the same individual subject observed at two different time points. For example, patients in a clinical study whose stool samples are collected before and after receiving treatment.

"States" can also commonly be methodological, in which case sample pairs will usually be the same individual at the same time with two different methods. For example, q2-longitudinal could compare the effects of different collection methods, storage methods, DNA extraction methods, or any bioinformatic processing steps on the feature composition of individual samples.

.. note:: Many of the actions in q2-longitudinal take a ``metric`` value as input, which is usually a column name in a metadata file or a metadata-transformable artifact (including alpha diversity vectors, PCoA results, and many other QIIME 2 artifacts), or a feature ID in a feature table. The names of valid ``metric`` values in metadata files and metadata-transformable artifacts can be checked with the :doc:`metadata tabulate <metadata>` command. Valid feature names (to use as ``metric`` values associated with a feature table) can be checked with the ``feature-data summarize`` command.

In the examples below, we use data from the `ECAM study`_, a longitudinal study of infants' and mothers' microbiota from birth through 2 years of life. First let's create a new directory and download the relevant tutorial data.

.. command-block::
   :no-exec:

   mkdir longitudinal-tutorial
   cd longitudinal-tutorial

.. download::
   :url: https://data.qiime2.org/2018.6/tutorials/longitudinal/sample_metadata.tsv
   :saveas: ecam-sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2018.6/tutorials/longitudinal/ecam_shannon.qza
   :saveas: shannon.qza

.. download::
   :url: https://data.qiime2.org/2018.6/tutorials/longitudinal/unweighted_unifrac_distance_matrix.qza
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

Linear mixed effects (LME) models test the relationship between a single response variable and one or more independent variables, where observations are made across dependent samples, e.g., in repeated-measures sampling experiments. This implementation takes at least one numeric ``state-column`` (e.g., Time) and one or more comma-separated ``group-columns`` (which may be categorical or numeric metadata columns; these are the fixed effects) as independent variables in a LME model, and plots regression plots of the response variable ("metric") as a function of the state column and each group column. Additionally, the ``individual-id-column`` parameter should be a metadata column that indicates the individual subject/site that was sampled repeatedly. The response variable may either be a sample metadata mapping file column or a feature ID in the feature table. A comma-separated list of random effects can also be input to this action; a random intercept for each individual is included by default, but another common random effect that users may wish to use is a random slope for each individual, which can be set by using the ``state-column`` value as input to the ``random-effects`` parameter. Here we use LME to test whether alpha diversity (Shannon diversity index) changed over time and in response to delivery mode, diet, and sex in the ECAM data set.

.. note:: Deciding whether a factor is a fixed effect or a random effect can be complicated. In general, a factor should be a fixed effect if the different factor levels (metadata column values) represent (more or less) all possible discrete values. For example, ``delivery mode``, ``sex``, and ``diet`` (dominantly breast-fed or formula-fed) are designated as fixed effects in the example below. Conversely, a factor should be a random effect if its values represent random samples from a population. For example, we could imagine having metadata variables like ``body-weight``, ``daily-kcal-from-breastmilk``, ``number-of-peanuts-eaten-per-day``, or ``mg-of-penicillin-administered-daily``; such values would represent random samples from within a population, and are unlikely to capture all possible values representative of the whole population. Not sure about the factors in your experiment? 🤔 Consult a statistician or reputable statistical tome for guidance. 📚

.. command-block::

   qiime longitudinal linear-mixed-effects \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-file shannon.qza \
     --p-metric shannon \
     --p-group-columns delivery,diet,sex \
     --p-state-column month \
     --p-individual-id-column studyid \
     --o-visualization linear-mixed-effects.qzv

The visualizer produced by this command contains several results. First, the input parameters are shown at the top of the visualization for convenience (e.g., when flipping through multiple visualizations it is useful to have a summary). Next, the "model summary" shows some descriptive information about the LME model that was trained. This just shows descriptive information about the "groups"; in this case, groups will be individuals (as set by the ``--p-individual-id-column``). The main results to examine will be the "model results" below the "model summary". These results summarize the effects of each fixed effect (and their interactions) on the dependent variable (shannon diversity). This table shows parameter estimates, estimate standard errors, z scores, P values (P>|z|), and 95% confidence interval upper and lower bounds for each parameter. We see in this table that shannon diversity is significantly impacted by month of life and by diet, as well as several interacting factors. More information about LME models and the interpretation of these data can be found on the `statsmodels LME description page`_, which provides a number of useful technical references for further reading.

Finally, scatter plots categorized by each "group column" are shown at the bottom of the visualization, with linear regression lines (plus 95% confidence interval in grey) for each group. If ``--p-lowess`` is enabled, instead locally weighted averages are shown for each group. Two different groups of scatter plots are shown. First, regression scatterplots show the relationship between ``state_column`` (x-axis) and ``metric`` (y-axis) for each sample. These plots are just used as a quick summary for reference; users are recommended to use the ``volatility`` visualizer for interactive plotting of their longitudinal data. Volatility plots can be used to qualitatively identify outliers that disproportionately drive the variance within individuals and groups, including by inspecting residuals in relation to control limits (see note below and the section on "Volatility analysis" for more details).

The second set of scatterplots are fit vs. residual plots, which show the relationship between metric predictions for each sample (on the x-axis), and the residual or observation error (prediction - actual value) for each sample (on the y-axis). Residuals should be roughly zero-centered and normal across the range of measured values. Uncentered, systematically high or low, and autocorrelated values could indicate a poor model. If your residual plots look like an ugly mess without any apparent relationship between values, you are doing a good job. If you see a U-shaped curve or other non-random distribution, either your predictor variables (``group_columns`` and/or ``random_effects``) are failing to capture all explanatory information, causing information to leak into your residuals, or else you are not using an appropriate model for your data 🙁. Check your predictor variables and available metadata columns to make sure you aren't missing anything.

.. note:: If you want to dot your i's and cross your t's, residual and predicted values for each sample can be obtained in the "Download raw data as tsv" link below the regression scatterplots. This file can be input as metadata to the ``volatility`` visualizer to check whether residuals are correlated with other metadata columns. If they are, those columns should probably be used as prediction variables in your model! Control limits (± 2 and 3 standard deviations) can be toggled on/off to easily identify outliers, which can be particularly useful for re-examining fit vs. residual plots with this visualizer. 🍝


Volatility analysis
-------------------

The volatility visualizer generates interactive line plots that allow us to assess how volatile a dependent variable is over a continuous, independent variable (e.g., time) in one or more groups. Multiple metadata files (including alpha and beta diversity artifacts) and ``FeatureTable[RelativeFrequency]`` tables can be used as input, and in the interactive visualization we can select different dependent variables to plot on the y-axis.

Here we examine how variance in Shannon diversity and other metadata changes across time (set with the ``state-column`` parameter) in the ECAM cohort, both in groups of samples (interactively selected as described below) and in individual subjects (set with the ``individual-id-column`` parameter).

.. command-block::

   qiime longitudinal volatility \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-file shannon.qza \
     --p-default-metric shannon \
     --p-default-group-column delivery \
     --p-state-column month \
     --p-individual-id-column studyid \
     --o-visualization volatility.qzv


In the resulting visualization, a line plot appears on the left-hand side of the plot and a panel of "Plot Controls" appears to the right. These "Plot Controls" interactively adjust several variables and parameters. This allows us to determine how groups' and individuals' values change across a single independent variable, ``state-column``. Interective features in this visualization include:

1. The "Metric column" tab lets us select which continuous metadata values to plot on the y-axis. All continuous numeric columns found in metadata/artifacts input to this action will appear as options in this drop-down tab. In this example, the initial variable plotted in the visualization is shannon diversity because this column was designated by the optional ``default-metric`` parameter.
2. The "Group column" tab lets us select which categorical metadata values to use for calculating mean values. All categorical metadata columns found in metadata/artifacts input to this action will appear as options in this drop-down tab. These mean values are plotted on the line plot, and the thickness and opacity of these mean lines can be modified using the slider bars in the "Plot Controls" on the right-hand side of the visualization. Error bars (standard deviation) can be toggled on and off with a button in the "Plot Controls".
3. Longitudinal values for each individual subject are plotted as "spaghetti" lines (so-called because this tangled mass of individual vectors looks like a ball of spaghetti). The thickness and opacity of spaghetti can be modified using the slider bars in the "Plot Controls" on the right-hand side of the visualization.
4. Color scheme can be adjusted using the "Color scheme" tab.
5. Global mean and warning/control limits (2X and 3X standard deviations from global mean) can be toggled on/off with the buttons in the "Plot Controls". The goal of plotting these values is to show how a variable is changing over time (or a gradient) in relation to the mean. Large departures from the mean values can cross the warning/control limits, indicating a major disruption at that state; for example, antibiotic use or other disturbances impacting diversity could be tracked with these plots.
6. Group mean lines and spaghetti can also be modified with the "scatter size" and "scatter opacity" slider bars in the "Plot Controls". These adjust the size and opacity of individual points. Maximize scatter opacity and minimize line opacity to transform these into longitudinal scatter plots!
7. Relevant sample metadata at individual points can be viewed by hovering the mouse over a point of interest.

If the interactive features of this visualization don't quite scratch your itch, click on the "Open in Vega Editor" button at the top of the "Plot Controls" and customize to your heart's content. This opens a window for manually editing plot characteristics in `Vega Editor`_, a visualization tool external to QIIME2.

Buon appetito! 🍝


First differencing to track rate of change
------------------------------------------
Another way to view time series data is by assessing how the rate of change differs over time. We can do this through calculating first differences, which is the magnitude of change between successive time points. If :math:`Y_\text{t}` is the value of metric :math:`Y` at time :math:`t`, the first difference at time :math:`t`, :math:`{\Delta}Y_\text{t} = Y_\text{t} - Y_\text{t-1}`. This transformation is performed in the ``first-differences`` method in ``q2-longitudinal``.

.. command-block::

   qiime longitudinal first-differences \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-file shannon.qza \
     --p-state-column month \
     --p-metric shannon \
     --p-individual-id-column studyid \
     --p-replicate-handling random \
     --o-first-differences shannon-first-differences.qza

This outputs a ``SampleData[FirstDifferences]`` artifact, which can then be viewed, e.g., with the ``volatility`` visualizer or analyzed with ``linear-mixed-effects`` or other methods.

A similar method is ``first-distances``, which instead identifies the beta diversity distances between successive samples from the same subject. The pairwise distance between all samples can already be calculated by the ``beta`` or ``core-metrics`` methods in ``q2-diversity``, so this method simply identifies the distances between successive samples collected from the same subject and outputs this series of values as metadata that can be consumed by other methods.

.. command-block::

   qiime longitudinal first-distances \
     --i-distance-matrix unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --p-state-column month \
     --p-individual-id-column studyid \
     --p-replicate-handling random \
     --o-first-distances first-distances.qza

This output can be used in the same way as the output of ``first-differences``. The output of ``first-distances`` is particularly empowering, though, because it allows us to analyze longitudinal changes in beta diversity using actions that cannot operate directly on a distance matrix, such as ``linear-mixed-effects``.

.. command-block::

   qiime longitudinal linear-mixed-effects \
     --m-metadata-file first-distances.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --p-metric Distance \
     --p-state-column month \
     --p-individual-id-column studyid \
     --p-group-columns delivery,diet \
     --o-visualization first-distances-LME.qzv


Tracking rate of change from static timepoints
----------------------------------------------
The ``first-differences`` and ``first-distances`` methods both have an optional "baseline" parameter to instead calculate differences from a static point (e.g., baseline or a time point when a treatment is administered: :math:`{\Delta}Y_\text{t} = Y_\text{t} - Y_\text{0}`). Calculating baseline differences can help tease apart noisy longitudinal data to reveal underlying trends in individual subjects or highlight significant experimental factors related to changes in diversity or other dependent variables.


.. command-block::

   qiime longitudinal first-distances \
     --i-distance-matrix unweighted_unifrac_distance_matrix.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --p-state-column month \
     --p-individual-id-column studyid \
     --p-replicate-handling random \
     --p-baseline 0 \
     --o-first-distances first-distances-baseline-0.qza

.. note:: **Fun fact!** We can also use the ``first-distances`` method to track longitudinal change in the proportion of features that are shared between an individual’s samples. This can be performed by calculating pairwise Jaccard distance (proportion of features that are not shared) between each pair of samples and using this as input to ``first-distances``. This is particularly useful for pairing with the ``baseline`` parameter, e.g., to determine how unique features are lost/gained over the course of an experiment.


Non-parametric microbial interdependence test (NMIT)
----------------------------------------------------
Within microbial communities, microbial populations do not exist in isolation but instead form complex ecological interaction webs. Whether these interdependence networks display the same temporal characteristics within subjects from the same group may indicate divergent temporal trajectories. NMIT evaluates how interdependencies of features (e.g., microbial taxa, sequence variants, or OTUs) within a community might differ over time between sample groups. NMIT performs a nonparametric microbial interdependence test to determine longitudinal sample similarity as a function of temporal microbial composition. For each subject, NMIT computes pairwise correlations between each pair of features. Between-subject distances are then computed based on a distance norm between each subject's microbial interdependence correlation matrix. For more details and citation, please see `Zhang et al., 2017`_.

.. note:: NMIT, as with most longitudinal methods, largely depends on the quality of the input data. This method will only work for longitudinal data (i.e., the same subjects are sampled repeatedly over time). To make the method robust, we suggest a minimum of 5-6 samples (time points) per subject, but the more the merrier. NMIT does not require that samples are collected at identical time points (and hence is robust to missing samples) but this may impact data quality if highly undersampled subjects are included, or if subjects' sampling times do not overlap in biologically meaningful ways. It is up to the users to ensure that their data are high quality and the methods are used in a biologically relevant fashion.

.. note:: NMIT can take a long time to run on very large feature tables. Removing low-abundance features and collapsing feature tables on taxonomy (e.g., to genus level) will improve runtime.

First let's download a feature table to test. Here we will test genus-level taxa that exhibit a relative abundance > 0.1% in more than 15% of the total samples.

.. download::
   :url: https://data.qiime2.org/2018.6/tutorials/longitudinal/ecam_table_taxa.qza
   :saveas: ecam-table-taxa.qza

Now we are ready run NMIT. The output of this command is a distance matrix that we can pass to other QIIME2 commands for significance testing and visualization.

.. command-block::

   qiime longitudinal nmit \
     --i-table ecam-table-taxa.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --p-individual-id-column studyid \
     --p-corr-method pearson \
     --o-distance-matrix nmit-dm.qza


Now let's put that distance matrix to work. First we will perform PERMANOVA tests to evaluate whether between-group distances are larger than within-group distance.

.. note:: NMIT computes between-subject distances across all time points, so each subject (as defined the ``--p-individual-id-column`` parameter used above) gets compressed into a single "sample" representing that subject's longitudinal microbial interdependence. This new "sample" will be labeled with the ``SampleID`` of one of the subjects with a matching ``individual-id``; this is done for the convenience of passing this distance matrix to downstream steps without needing to generate a new sample metadata file but it means that you must **pay attention**. **For significance testing and visualization, only use group columns that are uniform across each** ``individual-id``. **DO NOT ATTEMPT TO USE METADATA COLUMNS THAT VARY OVER TIME OR BAD THINGS WILL HAPPEN.** For example, in the tutorial metadata a patient is labeled ``antiexposedall==y`` only after antibiotics have been used; this is a column that you should not use, as it varies over time. Now have fun and be responsible.

.. command-block::

   qiime diversity beta-group-significance \
     --i-distance-matrix nmit-dm.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --m-metadata-column delivery \
     --o-visualization nmit.qzv

Finally, we can compute principal coordinates and use Emperor to visualize similarities among **subjects** (not individual samples; see the note above).

.. command-block::

   qiime diversity pcoa \
     --i-distance-matrix nmit-dm.qza \
     --o-pcoa nmit-pc.qza

.. command-block::

   qiime emperor plot \
     --i-pcoa nmit-pc.qza \
     --m-metadata-file ecam-sample-metadata.tsv \
     --o-visualization nmit-emperor.qzv

So there it is. We can use PERMANOVA test or other distance-based statistical tests to determine whether groups exhibit different longitudinal microbial interdependence relationships, and PCoA/emperor to visualize the relationships among groups of subjects. **Don't forget the caveats mentioned above about using and interpreting NMIT**. Now be safe and have fun.

.. _ECAM study: https://doi.org/10.1126/scitranslmed.aad7121
.. _statsmodels LME description page: http://www.statsmodels.org/dev/mixed_linear.html
.. _Vega Editor: https://vega.github.io/vega/docs/
.. _Zhang et al., 2017: https://doi.org/10.1002/gepi.22065
