Predicting sample metadata values with q2-sample-classifier
===========================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

.. warning:: Just as with any statistical method, the actions described in this plugin require adequate sample sizes to achieve meaningful results. As a rule of thumb, a minimum of approximately 50 samples should be provided. Categorical metadata columns that are used as classifier targets should have a minimum of 10 samples per unique value, and continuous metadata columns that are used as regressor targets should not contain many outliers or grossly uneven distributions. Smaller counts will result in inaccurate models, and may result in errors.

This tutorial will demonstrate how to use ``q2-sample-classifier`` to predict sample metadata values. Supervised learning methods predict sample data (e.g., metadata values) as a function of other sample data (e.g., microbiota composition). The predicted targets may be discrete sample classes (for classification problems) or continuous values (for regression problems). Any other data may be used as predictive features, but for the purposes of q2-sample-classifier this will most commonly be microbial sequence variant, operational taxonomic unit (OTU), or taxonomic composition data. However, any features contained in a feature table may be used — for non-microbial data, just `convert your observation tables to biom format`_ and :doc:`import the feature table data into qiime2 <importing>`.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir sample-classifier-tutorial
   cd sample-classifier-tutorial

Predicting categorical sample data
----------------------------------

Supervised learning classifiers predict the categorical metadata classes of unlabeled samples by learning the composition of labeled training samples. For example, we may use a classifier to diagnose or predict disease susceptibility based on stool microbiome composition, or predict sample type as a function of the sequence variants, microbial taxa, or metabolites detected in a sample. In this tutorial, we will use the :doc:`moving pictures tutorial data <moving-pictures>` to train a classifier that predicts the body site from which a sample was collected. Download the feature table and sample metadata with the following links:

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: moving-pictures-sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/sample-classifier/moving-pictures-table.qza
   :saveas: moving-pictures-table.qza

Next, we will attempt to predict which body site each sample originated from based on its microbial composition.

.. command-block::

   qiime sample-classifier classify-samples \
     --i-table moving-pictures-table.qza \
     --m-metadata-file moving-pictures-sample-metadata.tsv \
     --m-metadata-column BodySite \
     --p-optimize-feature-selection \
     --p-parameter-tuning \
     --p-estimator RandomForestClassifier \
     --p-n-estimators 100 \
     --output-dir moving-pictures-classifier

The visualization produced by this command presents classification accuracy results in the form of a confusion matrix. This matrix indicates how frequently a sample is classified with to the correct class vs. all other classes. The confusion matrix is displayed at the top of the visualization in the form of a heatmap, and below that as a table containing overall accuracy (the fraction of times that test samples are assigned the correct class).

.. question::
   What other metadata can we predict with ``classify-samples``? Take a look at the metadata columns in the ``sample-metadata`` and try some other categorical columns. Not all metadata can be easily learned by the classifier!


If ``--p-optimize-feature-selection`` is enabled, the visualization will also display a recursive feature extraction plot, which illustrates how model accuracy changes as a function of feature count. The combination of features that maximize accuracy are automatically selected for the final model, which is used for sample prediction results that are displayed in the visualization. A list of the features chosen, and their relative importances, will be displayed at the bottom of the visualization. Features with higher importance scores are more important for distinguishing each class.

.. question::
   What happens when feature optimization is disabled with the option ``--p-no-optimize-feature-selection``? How does this impact classification accuracy?

K-fold cross-validation is performed during automatic feature selection and parameter optimization steps. Five-fold cross-validation is performed by default, and this value can be adjusted using the ``--p-cv`` parameter. A separate portion of samples is removed from the data set prior to model training and optimization, and used as a test set to determine model accuracy. The fraction of test samples to remove is adjusted with the ``--p-test-size`` parameter.

.. question::
   Try to figure out what the ``--p-parameter-tuning`` parameter does. What happens when it is disabled with the option ``--p-no-parameter-tuning``? How does this impact classification accuracy?

.. question::
   Many different classifiers can be trained via the ``--p-estimator`` parameter in ``classify-samples``. Try some of the other classifiers. How do these methods compare?

.. question::
   Sequence variants are not the only feature data that can be used to train a classifier or regressor. Taxonomic composition is another feature type that can be easily created using the tutorial data provided in QIIME2. Try to figure out how this works (hint: you will need to assign taxonomy, as described in the :doc:`moving pictures tutorial <moving-pictures>`, and :doc:`collapse taxonomy <../plugins/available/taxa/collapse/>` to create a new feature table). Try using feature tables collapsed to different taxonomic levels. How does taxonomic specificity (e.g., species-level is more specific than phylum-level) impact classifier performance?

.. question::
   The ``--p-n-estimators`` parameter adjusts the number of trees grown by ensemble estimators, such as random forest classifiers (this parameter will have no effect on non-ensemble methods), which increases classifier accuracy up to a certain point, but at the cost of increased computation time. Try the same command above with different numbers of estimators, e.g., 10, 50, 100, 250, and 500 estimators. How does this impact the overall accuracy of predictions? Are more trees worth the time?


Predicting continuous (i.e., numerical) sample data
---------------------------------------------------

Supervised learning regressors predict continuous metadata values of unlabeled samples by learning the composition of labeled training samples. For example, we may use a regressor to predict the abundance of a metabolite that will be producted by a microbial community, or a sample's pH,  temperature, or altitude as a function of the sequence variants, microbial taxa, or metabolites detected in a sample. In this tutorial, we will use the `ECAM study`_, a longitudinal cohort study of microbiome development in U.S. infants. Download the feature table and sample metadata with the following links:

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/longitudinal/sample_metadata.tsv
   :saveas: ecam-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2018.8/tutorials/longitudinal/ecam_table_maturity.qza
   :saveas: ecam-table.qza

Next, we will train a regressor to predict an infant's age based on its microbiota composition.

.. command-block::

   qiime sample-classifier regress-samples \
     --i-table ecam-table.qza \
     --m-metadata-file ecam-metadata.tsv \
     --m-metadata-column month \
     --p-optimize-feature-selection \
     --p-parameter-tuning \
     --p-estimator RandomForestRegressor \
     --p-n-estimators 100 \
     --output-dir ecam-regressor

The visualization produced by this command presents classification accuracy results in the form of a scatter plot showing predicted vs. true values for each test sample, accompanied by a linear regression line fitted to the data with 95% confidence intervals (grey shading). The true 1:1 ratio between predicted and true values is represented by a dotted line for comparison. Below this, model accuracy is quantified in a table displaying mean square error and the R value, P value, standard error of the estimated gradient, slope, and intercept of the linear regression fit. The remainder of the visualization shows optional feature selection data, as described above for ``classify-samples``.

.. question::
   What other metadata can we predict with ``regress-samples``? Take a look at the metadata columns in the ``sample-metadata`` and try some other values. Not all metadata can be easily learned by the regressor!

.. question::
   Many different regressors can be trained via the ``--p-estimator`` parameter in ``regress-samples``. Try some of the other regressors. How do these methods compare?


"Maturity Index" prediction
---------------------------

.. note:: This analysis currently works best for comparing groups that are sampled fairly evenly across time (the column used for regression). Datasets that contain groups sampled sporadically at different times are not supported, and users should either filter out those samples or “bin” them with other groups prior to using this visualizer.
.. note:: This analysis will only work on data sets with a large sample size, particularly in the "control" group, and with sufficient biological replication at each time point.

This method calculates a "microbial maturity" index from a regression model trained on feature data to predict a given continuous metadata column ("state_column"), e.g., to predict a subject's age as a function of microbiota composition. This method is different from standard supervised regression because it quantifies the relative rate of change over time in two or more groups. The model is trained on a subset of control group samples, then predicts the column value for all samples. This visualization computes maturity index z-scores (MAZ) to compare relative "maturity" between each group, as described in `Sathish et al. 2014`_. This method was designed to predict between-group differences in intestinal microbiome development by age, so ``state_column`` should typically be a measure of time. Other types of continuous metadata gradients might be testable, as long as two or more different "treatment" groups are being compared *with a large number of biological replicates* in the "control" group and treatment groups are sampled at the same "states" (time or position on gradient) for comparison. However, we do not necessarily recommend *or offer technical support* for unusual approaches.

Here we will compare microbial maturity between vaginally born and cesarean-delivered infants as a function of age in the ECAM dataset.

.. command-block::

   qiime sample-classifier maturity-index \
     --i-table ecam-table.qza \
     --m-metadata-file ecam-metadata.tsv \
     --p-state-column month \
     --p-group-by delivery \
     --p-individual-id-column studyid \
     --p-control Vaginal \
     --p-test-size 0.4 \
     --output-dir maturity

This pipeline produces several output files:

1. ``accuracy_results.qzv`` contains a linear regression plot of predicted vs. expected values on all control test samples (as described above for regression models). This is a subset of "control" samples that were not used for model training (the fraction defined by the ``test-size`` parameter).

2. ``lineplots.qzv`` contains an interactive volitility chart as described in the :doc:`longitudinal tutorial <longitudinal>`. This visualization can be useful for assessing how MAZ and other metrics change over time in each sample group (by default, the ``group_by`` column is used but other sample metadata may be selected for grouping samples). The default metric displayed on this chart is MAZ scores for the chosen ``state_column``. The "prediction" (predicted "state_column" values) and state_column "maturity" metrics are other metrics calculated by this plugin that can be interesting to explore. See `Sathish et al. 2014`_ for more details on the MAZ and maturity metrics.

3. ``clustermap.qzv`` contains a heatmap showing the frequency of each important feature across time in each group. This plot is useful for visualizing how the frequency of important features changes over time in each group, demonstrating how different patterns of feature abundance (e.g., trajectories of development in the case of age or time-based models) may affect model predictions and MAZ scores. Important features shown along the x-axis; samples grouped and ordered by ``group_by`` and ``state_column`` are shown on the y-axis. See :doc:`heatmap <../plugins/available/feature-table/heatmap/>` for details on how features are clustered along the x-axis (default parameters are used).

4. ``maz_scores.qza`` contains MAZ scores for each sample (excluding training samples). This is useful for downstream testing as described below.

5. ``predictions.qza`` contains "state column" predictions for each sample (excluding training samples). These predictions are used to calculate the MAZ scores, and a subset (control test samples) are used to assess model accuracy. Nonetheless, the predictions are supplied in case they prove useful...

6. ``feature_importance.qza`` contains importance scores for all features included in the final regression model. If the ``optimize-feature-selection`` parameter is used, this will only contain important features; if not, importance scores will be assigned to all features in the original feature table.

7. ``sample_estimator.qza`` contains the trained ``SampleEstimator[Regressor]``. You probably will not want to re-use this estimator for predicting other samples (since it is trained on a subset of samples), but nevertheless it is supplied for the curious and intrepid.

8. ``model_summary.qzv`` contains a summary of the model parameters used by the supervised learning estimator, as described above for the equivalently named outputs from the ``classify-samples`` pipeline.

So what does this all show us? In the ECAM dataset that we are testing here, we see that MAZ scores are suppressed in Cesarean-delivered subjects in the second year of life, compared to vaginally born subjects (See ``lineplots.qzv``). Several important sequence variants exhibit reduced frequency during this time frame, suggesting involvement in delayed maturation of the Cesarean cohort (See ``clustermap.qzv``). (This tutorial example does not have a ``random-state`` set so local results may vary slightly)

Note that none of the results presented so far actually confirm a statistical difference between groups. Want to take this analysis to the next level (with multivariate statistical testing)? Use the MAZ scores (or possibly ``predictions``) as input metrics (dependent variables) in :doc:`linear mixed effects models <longitudinal>`.




.. _convert your observation tables to biom format: http://biom-format.org/documentation/biom_conversion.html
.. _ECAM study: https://doi.org/10.1126/scitranslmed.aad7121
.. _Sathish et al. 2014: https://doi.org/10.1038/nature13421
