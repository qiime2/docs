Predicting sample metadata categories with q2-sample-classifier
===============================================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial will demonstrate how to use ``q2-sample-classifier`` to predict sample metadata values. Supervised learning methods predict sample data (e.g., metadata values) as a function of other sample data (e.g., microbiota composition). The predicted targets may be discrete sample classes (for classification problems) or continuous values (for regression problems). Any other data may be used as predictive features, but for the purposes of q2-sample-classifier this will most commonly be microbial sequence variant, operational taxonomic unit (OTU), or taxonomic composition. However, any features contained in a feature table may be used — for non-microbial data, just `convert your observation tables to biom format`_ and `import to qiime2`_.

We will download and create several files, so first create a working directory.

.. command-block::
   :no-exec:

   mkdir sample-classifier-tutorial
   cd sample-classifier-tutorial

Predicting categorical sample data
----------------------------------

Supervised learning classifiers predict the categorical metadata classes of unlabled samples by learning the composition of labeled training samples. For example, we may use a classifier to diagnose or predict disease susceptibility based on stool microbiome composition, or predict sample type as a function of the sequence variants, microbial taxa, or metabolites detected in a sample. In this tutorial, we will use the `moving pictures tutorial data`_ to train a classifier that predicts the body site from which a sample was collected. Download the feature table and sample metadata with the following links:

.. download::
   :url: https://data.qiime2.org/2017.7/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: moving-pictures-sample-metadata.tsv

.. download::
   :url: https://docs.qiime2.org/2017.7/data/tutorials/moving-pictures/table.qza
   :saveas: moving-pictures-table.qza

Next, we will attempt to predict which body site each sample originated from based on its microbial composition.

.. command-block::

   qiime sample-classifier classify-samples \
    --i-table moving-pictures-table.qza \
    --m-metadata-file moving-pictures-sample-metadata.tsv \
    --m-metadata-category BodySite \
    --o-visualization moving-pictures-BodySite \
    --p-optimize-feature-selection \
    --p-parameter-tuning \
    --p-estimator RandomForestClassifier \
    --p-n-estimators 100

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
   Sequence variants are not the only feature data that can be used to train a classifier or regressor. Taxonomic composition is another feature type that can be easily created using the tutorial data provided in QIIME2. Try to figure out how this works (hint: you will need to `assign taxonomy`_ and `collapse taxonomy`_ to create a new feature table). Try using feature tables collapsed to different taxonomic levels. How does taxonomic specificity (e.g., species-level is more specific than phylum-level) impact classifier performance?

.. question::
   The ``--p-n-estimators`` parameter adjusts the number of trees grown by ensemble estimators, such as random forest classifiers (this parameter will have no effect on non-ensemble methods), which increases classifier accuracy up to a certain point, but at the cost of increased computation time. Try the same command above with different numbers of estimators, e.g., 10, 50, 100, 250, and 500 estimators. How does this impact the overall accuracy of predictions? Are more trees worth the time?


Predicting continuous sample data
---------------------------------

Supervised learning regressors predict continuous metadata values of unlabled samples by learning the composition of labeled training samples. For example, we may use a regressor to predict the abundance of a metabolite that will be producted by a microbial community, or a sample's pH,  temperature, or altitude as a function of the sequence variants, microbial taxa, or metabolites detected in a sample. In this tutorial, we will use the `Atacama soils tutorial data`_ to train a regressor to predict the percent relative humidity in a soil sample. Download the feature table and sample metadata with the following links:

.. download::
   :url: https://data.qiime2.org/2017.7/tutorials/atacama-soils/sample_metadata.tsv
   :saveas: atacama-soils-sample-metadata.tsv

.. download::
   :url: https://docs.qiime2.org/2017.7/data/tutorials/atacama-soils/table.qza
   :saveas: atacama-soils-table.qza

Next, we will attempt to predict soil relative humidity as a function of microbial composition.

.. command-block::

   qiime sample-classifier regress-samples \
    --i-table atacama-soils-table.qza \
    --m-metadata-file atacama-soils-sample-metadata.tsv \
    --m-metadata-category PercentRelativeHumiditySoil_100 \
    --o-visualization atacama-soils-PercentRelativeHumiditySoil_100 \
    --p-optimize-feature-selection \
    --p-parameter-tuning \
    --p-estimator RandomForestRegressor \
    --p-n-estimators 100

The visualization produced by this command presents classification accuracy results in the form of a scatter plot showing predicted vs. true values for each test sample, accompanied by a linear regression line fitted to the data with 95% confidence intervals (grey shading). The true 1:1 ratio between predicted and true values is represented by a dotted line for comparison. Below this model accuracy is quantified in a table displaying mean square error and the R value, P value, standard error of the estimated gradient, slope, and intercept of the linear regression fit. The remainder of the visualization shows optional feature selection data, as described above for ``classify-samples``.

.. question::
   What other metadata can we predict with ``regress-samples``? Take a look at the metadata categories in the ``sample-metadata`` and try some other values. Not all metadata can be easily learned by the regressor! 

.. question::
   Many different regressors can be trained via the ``--p-estimator`` parameter in ``regress-samples``. Try some of the other regressors. How do these methods compare?



.. _convert your observation tables to biom format: http://biom-format.org/documentation/biom_conversion.html
.. _import to qiime2: https://docs.qiime2.org/2017.7/tutorials/importing/#feature-table-data
.. _moving pictures tutorial data: https://docs.qiime2.org/2017.7/tutorials/moving-pictures/
.. _assign taxonomy: https://docs.qiime2.org/2017.7/tutorials/moving-pictures/#taxonomic-analysis
.. _collapse taxonomy: https://docs.qiime2.org/2017.7/plugins/available/taxa/collapse/
.. _Atacama soils tutorial data: https://docs.qiime2.org/2017.7/tutorials/atacama-soils/
