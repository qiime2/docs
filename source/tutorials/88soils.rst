"88 soils" tutorial
===================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>`.

This tutorial is designed to be a self-guided exercise that could be run after :doc:`the moving pictures tutorial <moving-pictures>` and :doc:`the fecal microbiota transplant tutorial <fmt>` to gain more experience with QIIME 2.

In this tutorial you'll use QIIME 2 to perform an analysis of soil samples from around the globe. A study based on these samples was originally published in `Lauber et al. (2009)`_. In that study, these samples had the hypervariable region 2 (V2) of the 16S rRNA sequenced on a Roche 454 instrument. The data used in this tutorial are based on a re-sequencing of those same samples on an Illumina HiSeq as part of the `Earth Microbiome Project`_. In this instance, the hypervariable region 4 (V4) of the 16S rRNA was sequenced.

Prepare for the analysis
------------------------

You should first look through the sample metadata to familiarize yourself with the samples used in this study. The `sample metadata`_ is available as a Google Spreadsheet. You should download this file as tab-separated text by selecting ``File`` > ``Download as`` > ``Tab-separated values``. Save the file as ``sample-metadata.tsv``.

You can next download the *demultiplexed sequences* that we'll use in this analysis. In this tutorial we'll work with a small subset (1%) of the complete sequence data so that the commands will run quickly.

.. command-block::

   curl -sLO https://data.qiime2.org/2.0.6/tutorials/88soils/88soils-tutorial-demux-1p.qza

Sequence processing and diversity analyses
------------------------------------------

Use the following questions to guide your analyses of the data. (Note: if you're new to QIIME 2, you should work through the :doc:`the moving pictures tutorial <moving-pictures>` and then :doc:`the fecal microbiota transplant tutorial <fmt>`, which will guide you through answering similar questions.)

#. What value would you choose to pass for ``--p-sampling-depth``? How many samples will be excluded from your analysis based on this choice? Approximately how many total sequences will you be analyzing in the ``core-metrics`` command?

#. What sample metadata or combinations of sample metadata are most strongly associated with the differences in microbial composition of the samples? Are these associations stronger with unweighted UniFrac or with Bray-Curtis? Based on what you know about these metrics, what does that difference suggest?

#. What do you conclude about the associations between continuous sample metadata and the richness and evenness of these samples? How does this compare to the results presented in `Lauber et al. (2009)`_? (Hint: Our findings here differ from what was present in `Lauber et al. (2009)`_. Start thinking about why that might be.)

#. Are the associations between biomes and differences in microbial composition statistically significant? How about pH groups? What biomes appear to be most different from each other? What pH groups appear to be most different from each other?

#. What discrete sample metadata categories are most strongly associated with the differences in microbial community richness or evenness? Are these differences statistically significant?

#. What differences do you observe between the unweighted UniFrac and Bray-Curtis PCoA plots?

#. In taxonomic composition bar plots, sort the samples by their pH, and visualize them at the phylum level. What are the dominant phyla in these samples? Which phyla increase and which decrease with increasing pH?

#. Compare the taxonomic composition bar plots of these samples with those in Figure 2 of `Lauber et al. (2009)`_. Are the changes you noted in response to the last question consistent with what you see in this plot? There is one major difference between the plots in Figure 2 of `Lauber et al. (2009)`_ and those generated here. What is it? (Hint: After spending some time to answer that question, take a look at `Bergmann et al. (2011)`_. How do the findings presented there relate to the analysis we're performing?)

#. One sample in this analysis is primarily dominated by the bacterial phylum ``Actinobacteria``. Why do you think this is? (Hint: Refer to the summary of the ``FeatureTable[Frequency]`` artifact.)

#. What features differ in abundance across pH groups? What groups are they most and least abundant in? What are some the taxonomies of some of these features?

.. _sample metadata: https://docs.google.com/spreadsheets/d/1CTOCiyKWLlZiTFkmHjJcTkhHW0OkpEniNoSpscuZapk/edit?usp=sharing
.. _DADA2: https://www.ncbi.nlm.nih.gov/pubmed/27214047
.. _Lauber et al. (2009): https://www.ncbi.nlm.nih.gov/pubmed/19502440
.. _Earth Microbiome Project: http://earthmicrobiome.org
.. _Bergmann et al. (2011): https://www.ncbi.nlm.nih.gov/pubmed/22267877
