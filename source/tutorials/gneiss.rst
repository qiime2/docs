Differential abundance analysis with gneiss
===========================================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.


In this tutorial you will learn how to perform differential abundance analysis using balances in gneiss.  The main problem that we will focus on is how to identify differentially abundant taxa in a compositionally coherent way.

Compositionality refers to the issue of dealing with proportions.  To account for differences in sequencing depth, microbial abundances are typically interpreted as proportions (e.g. relative abundance).  Because of this, it becomes challenging to infer exactly which microbes are changing -- since proportions add to one, the change of a single microbe will also change the proportions of the remaining microbes.

Consider the following example:

.. image:: images/gneiss-bars.jpg

On the left, we have the true abundances of ten species, and the first species doubles between Time point 1 and Time point 2.  When we normalize these to proportions, it appears as if all of the species have changed between the two time points.  Looking at proportions alone, we would never realize this problem, and we actually cannot exactly determine which species are changing based on proportions alone.

While we cannot exactly solve the problem of identifying differentially abundant species, we can relax this problem and ask which partitions of microbes are changing.  In the case above, if we compute the ratio between the first species and the second species, that ratio will be 1:1 at Time point 1, and 2:1 at Time point 2 for both the original abundances and the proportions.  This is the type of question that balances try to solve.
Rather than focusing on individual taxa, we can focus on the ratio between taxa (or groups of taxa), since these ratios are consist between the true abundances and the observed proportions of the species observed. We typically log transform these ratios for improved visualization ('log ratios'). The concept of calculating balances (or ratios) for multiple species can be extended to trees as shown in the following example.

.. image:: images/gneiss-balances.jpg

On the left, we define a tree, where each of the tips corresponds to a taxon, and underneath are the proportions of each taxon in the first sample.  The internal nodes (i.e. balances) define the log ratio between the taxa underneath.  On the right is the same tree, and underneath are the proportions of each taxa in a different sample. Only one of the taxa abundances changes.  As we have observed before, the proportions of all of the taxa will change, but looking at the balances, only the balances containing the purple taxa will change.  In this case, balance :math:`b_3` won't change, since it only considers the ratio between the red and taxa.  By looking at balances instead proportions, we can eliminate some of the variance by restricting observations to only focus on the taxa within a given balance.

The outstanding question here is, how do we construct a balance tree to control for the variation, and identify interesting differentially abundant partitions of taxa?  In gneiss, there are three main ways that this can be done:

1. Correlation clustering.  If we don't have relevant prior information about how to cluster together organisms, we can group together organisms based on how often they co-occur with each other. This is available in the ``correlation-clustering`` command and creates tree input for ``ilr-hierarchical``.
2. Gradient clustering.  Use a metadata category to cluster taxa found in similar sample types. For example, if we want to evaluate if pH is a driving factor, we can cluster according to the pH that the taxa are observed in, and observe whether the ratios of low-pH organisms to high-pH organisms change as the pH changes.  This is available in the ``gradient-clustering`` command and creates tree input for ``ilr-hierarchical``.
3. Phylogenetic analysis. A phylogenetic tree (e.g. ``rooted-tree.qza``) created outside of gneiss can also be used. In this case you can use your phylogenetic tree as input for ``ilr-phylogenetic``.

Once we have a tree, we can calculate balances using the following equation:

.. math::

   b_i = \sqrt{\frac{rs}{r+s}} \log \frac{g(x_r)}{g(x_s)}

where :math:`i` represents the :math:`i^{th}` internal node in the tree, :math:`g(x)` represents the geometric mean within set :math:`x`, and :math:`x_r` represents the set of taxa abundances in the numerator of the balance, :math:`x_s` represents the set of taxa abundances in the denominator of the balance, and :math:`r` and :math:`s` represents the number of taxa within :math:`x_r` and :math:`x_s` respectively.

After the balances are calculated, standard statistical procedures such as ANOVA and linear regression can be performed.  We will demonstrate running these procedures using the Chronic Fatigue Syndrome dataset.

Creating balances
---------------------------------------------------------------
In the Chronic Fatigue Syndrome dataset published in `Giloteaux et al (2016)`_, there are 87 individuals with 48 diseased patients and 39 healthy controls. The data used in this tutorial were sequenced on an Illumina MiSeq using the `Earth Microbiome Project`_ hypervariable region 4 (V4) 16S rRNA sequencing protocol.

Before beginning this tutorial, create a new directory and change to that directory.

.. command-block::
   :no-exec:

   mkdir qiime2-chronic-fatigue-syndrome-tutorial
   cd qiime2-chronic-fatigue-syndrome-tutorial

The datasets required for this tutorial can be found below (to learn how these would be generated, see the :doc:`moving pictures tutorial <moving-pictures>`).


.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/gneiss/sample-metadata.tsv
   :saveas: sample-metadata.tsv

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/gneiss/table.qza
   :saveas: table.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/gneiss/taxa.qza
   :saveas: taxa.qza


First, we will define partitions of microbes for which we want to construct balances. Again, there are multiple possible ways to construct a tree (i.e. hierarchy) which defines the partition of microbes (balances) for which we want to construct balances. We will show examples of both ``correlation-clustering`` and ``gradient-clustering`` on this dataset.

Note that the differential abundance techniques that we will be running will utilize log ratio transforms. Since it is not possible to take the logarithm of zero, both clustering methods below include a default pseudocount parameter. This replaces all zeroes in the table with a 1, so that we can apply logarithms on this transformed table.

The input table is the raw count table (FeatureTable[Frequency]).

Option 1: Correlation-clustering
---------------------------------------------------------------
This option should be your default option. We will employ unsupervised clustering via Ward's hierarchical clustering to obtain Principal Balances. In essence, this will define the partitions of microbes that commonly co-occur with each other using Ward hierarchical clustering, which is defined by the following metric.

.. math::

   d(x, y) = V [ \ln \frac{x}{y} ]

Where :math:`x` and :math:`y` represent the proportions of two microbes across all of the samples.   If two microbes are highly correlated, then this quantity will shrink close to zero.  Ward hierarchical cluster will then use this distance metric to iteratively cluster together groups of microbes that are correlated with each other.  In the end, the tree that we obtain will highlight the high level structure and identify any blocks within in the data.

.. command-block::

   qiime gneiss correlation-clustering \
     --i-table table.qza \
     --o-clustering hierarchy.qza


Option 2: Gradient-clustering
---------------------------------------------------------------
An alternative to ``correlation-clustering`` is to create a tree based on a numeric metadata category. With ``gradient-clustering``, we can group taxa that occur in similar ranges of a metadata category. In this example, we will create a tree (hierarchy) using the metadata category Age. Note that the metadata category can have no missing variables, and must be numeric.

.. command-block::

   qiime gneiss gradient-clustering \
     --i-table table.qza \
     --m-gradient-file sample-metadata.tsv \
     --m-gradient-column Age \
     --o-clustering gradient-hierarchy.qza

An important consideration for downstream analyses is the problem of overfitting. When using ``gradient-clustering``, you are creating a tree to best highlight compositional differences along the metadata category of your choice, and it is possible to get false positives. Use ``gradient-clustering`` with caution.

We will visualize the hierarchy (Option 1, above) on a heatmap to see which groups of taxa they represent.  By default, the values within the feature table are log-scaled, with the sample means centered around zero.

.. command-block::

   qiime gneiss dendrogram-heatmap \
     --i-table table.qza \
     --i-tree hierarchy.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-column Subject \
     --p-color-map seismic \
     --o-visualization heatmap.qzv

As noted in the legend, the numerators for each balance are highlighted in light red, while the denominators are highlighted in dark red. From here, we can see that the denominator of :math:`y0` has few OTUs compared to the numerator of :math:`y0`.  These taxa in the denominator could be interesting, so let's investigate the taxonomies making up this balance with ``balance_taxonomy``.

Conclusion
----------

Remember, based on the toy examples given in the beginning of this tutorial, it is not possible to infer absolute changes of microbes in a given sample.  Balances will not be able to provide this sort of answer, but it can limit the number of possible scenarios.  Specifically, one of the five following scenarios could have happened.

1) The taxa in the :math:`y0_{numerator}` on average have increased between patient group and the healthy control.

2) The taxa in the :math:`y0_{denominator}` on average have decreased between patient group and the healthy control.

3) A combination of the above occurred

4) Taxa abundances in both :math:`y0_{numerator}` and :math:`y0_{denominator}` both increased, but taxa abundances in :math:`y0_{numerator}` increased more compared to :math:`y0_{denominator}`

5) Taxa abundances in both :math:`y0_{numerator}` and :math:`y0_{denominator}` both decreased, but taxa abundances in :math:`y0_{denominator}` increased more compared to :math:`y0_{numerator}`

To further narrow down these hypothesis,  biological prior knowledge or experimental validation will be required.


.. _Giloteaux et al (2016): https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-016-0171-4
.. _Earth Microbiome Project: http://earthmicrobiome.org/
.. _multivariate response linear regression: http://www.public.iastate.edu/~maitra/stat501/lectures/MultivariateRegression.pdf
.. _this post: https://stats.stackexchange.com/a/76292/79569
