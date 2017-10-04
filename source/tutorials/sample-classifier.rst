Predicting sample metadata values with q2-sample-classifier
===========================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

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
   :url: https://data.qiime2.org/2017.10/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: moving-pictures-sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/sample-classifier/moving-pictures-table.qza
   :saveas: moving-pictures-table.qza

Next, we will attempt to predict which body site each sample originated from based on its microbial composition.

.. command-block::

   qiime sample-classifier classify-samples \
     --i-table moving-pictures-table.qza \
     --m-metadata-file moving-pictures-sample-metadata.tsv \
     --m-metadata-category BodySite \
     --p-optimize-feature-selection \
     --p-parameter-tuning \
     --p-estimator RandomForestClassifier \
     --p-n-estimators 100 \
     --o-visualization moving-pictures-BodySite.qzv

The visualization produced by this command presents classification accuracy results in the form of a confusion matrix. This matrix indicates how frequently a sample is classified with to the correct class vs. all other classes. The confusion matrix is displayed at the top of the visualization in the form of a heatmap, and below that as a table containing overall accuracy (the fraction of times that test samples are assigned the correct class). 

.. question::
   What other metadata can we predict with ``classify-samples``? Take a look at the metadata categories in the ``sample-metadata`` and try some other categories. Not all metadata can be easily learned by the classifier! 


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
   :url: https://data.qiime2.org/2017.10/tutorials/longitudinal/sample_metadata.tsv
   :saveas: ecam-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2017.10/tutorials/longitudinal/ecam_table_maturity.qza
   :saveas: ecam-table.qza

Next, we will train a regressor to predict an infant's age based on its microbiota composition.

.. command-block::

   qiime sample-classifier regress-samples \
     --i-table ecam-table.qza \
     --m-metadata-file ecam-metadata.tsv \
     --m-metadata-category month \
     --p-optimize-feature-selection \
     --p-parameter-tuning \
     --p-estimator RandomForestRegressor \
     --p-n-estimators 100 \
     --o-visualization ecam-month.qzv

The visualization produced by this command presents classification accuracy results in the form of a scatter plot showing predicted vs. true values for each test sample, accompanied by a linear regression line fitted to the data with 95% confidence intervals (grey shading). The true 1:1 ratio between predicted and true values is represented by a dotted line for comparison. Below this, model accuracy is quantified in a table displaying mean square error and the R value, P value, standard error of the estimated gradient, slope, and intercept of the linear regression fit. The remainder of the visualization shows optional feature selection data, as described above for ``classify-samples``.

.. question::
   What other metadata can we predict with ``regress-samples``? Take a look at the metadata categories in the ``sample-metadata`` and try some other values. Not all metadata can be easily learned by the regressor! 

.. question::
   Many different regressors can be trained via the ``--p-estimator`` parameter in ``regress-samples``. Try some of the other regressors. How do these methods compare?


"Maturity Index" prediction
---------------------------

.. note:: This analysis currently works best for comparing groups that are sampled fairly evenly across time (the category used for regression). Datasets that contain groups sampled sporadically at different times are not supported, and users should either filter out those samples or “bin” them with other groups prior to using this visualizer.
.. note:: This analysis will only work on data sets with a large sample size, particularly in the "control" group, and with sufficient biological replication at each time point.

This method calculates a "microbial maturity" index from a regression model trained on feature data to predict a given continuous metadata category, e.g., to predict a subject's age as a function of microbiota composition. This method is different from standard supervised regression because it quantifies the relative rate of change over time in two or more groups. The model is trained on a subset of control group samples, then predicts the category value for all samples. This visualization computes maturity index z-scores (MAZ) to compare relative "maturity" between each group, as described in `Sathish et al. 2014`_. This method was designed to predict between-group differences in intestinal microbiome development by age, so ``category`` should typically be a measure of time. Other types of continuous metadata gradients might be testable, as long as two or more different "treatment" groups are being compared *with a large number of biological replicates* in the "control" group and treatment groups are sampled at the same "states" (time or position on gradient) for comparison. However, we do not necessarily recommend *or offer technical support* for unusual approaches.

Here we will compare microbial maturity between vaginally born and cesarean-delivered infants as a function of age in the ECAM dataset.

.. command-block::

   qiime sample-classifier maturity-index \
     --i-table ecam-table.qza \
     --m-metadata-file ecam-metadata.tsv \
     --p-category month \
     --p-group-by delivery \
     --p-control Vaginal \
     --p-test-size 0.4 \
     --o-visualization maturity.qzv

The visualizer produces a linear regression plot of predicted vs. expected values on the control test samples (as described above for regression models). Predicted vs. expected values are also shown for all samples in both control and test sets.

MAZ scores are calculated based on these predictions, statistically compared across each value "bin" (e.g., month of life) using ANOVA and paired t-tests, and shown as boxplots of MAZ distributions for each group in each value "bin". A link within the visualizers allows download of the MAZ scores for each sample, facilitating customized follow-up testing, e.g., in R, or use as metadata, e.g., for constructing PCoA plots. Want to take this analysis to the next level? Download the raw MAZ scores from within the visualization and feed these scores into :doc:`linear mixed effects models <longitudinal>`

The average abundances of features used for training maturity models are viewed as heatmaps within the visualization. Feature abundance is averaged across all samples within each value bin (e.g., month of life) and within each individual sample group (e.g., vaginal controls vs. cesarean), demonstrating how different patterns of feature abundance (e.g., trajectories of development in the case of age or time-based models) may affect model predictions and MAZ scores.



.. _convert your observation tables to biom format: http://biom-format.org/documentation/biom_conversion.html
.. _ECAM study: https://doi.org/10.1126/scitranslmed.aad7121
.. _Sathish et al. 2014: https://doi.org/10.1038/nature13421
