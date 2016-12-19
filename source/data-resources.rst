Data resources
==============

Taxonomy classifiers for use with q2-feature-classifier
-------------------------------------------------------

.. note:: Pre-trained classifiers that can be used with ``q2-feature-classifier`` currently present a security risk. If using a pre-trained classifier such as the ones provided here, you should trust the person who trained the classifier and the person who provided you with the qza file. This security risk will be addressed in a future version of ``q2-feature-classifier``.

.. note:: Taxonomic classifiers perform best when they are trained based on your specific sample preparation and sequencing parameters, including the primers that were used for amplification and the length of your sequence reads. Therefore in general you should follow the instructions in :doc:`Training feature classifiers with q2-feature-classifier <../tutorials/feature-classifier>` to train your own taxonomic classifiers (for example, from the marker gene reference databases below). We provided some common classifiers as this step can require a large amount of memory. For example, the Silva classifier linked here required approximately 30 GB of RAM to train.

These classifiers were trained using scikit-learn 0.18.1, and therefore can only be used with scikit-learn 0.18.1. If you are using a native installation of QIIME, before using these classifiers you should run the following to ensure that you are using the correct version of scikit-learn. If you are using a QIIME 2.0.6 virtual machine, scikit-learn 0.18.1 will be installed and you do not need to run this command. The scikit-learn version restriction will be relaxed in a future version of ``q2-feature-classifier``.

.. command-block::
   :no-exec:

    conda install scikit-learn=0.18.1

Naive Bayes classifiers trained on:

- `Silva 119 99% OTUs full-length sequences <https://data.qiime2.org/2.0.6/common/silva-119-99-full-length-nb-classifier.qza>`_ (MD5: ``bb15be94fcfa2270d57e05b8630233af``)
- `Silva 119 99% OTUs 250 base forward reads from 515F/806R region of sequences <https://data.qiime2.org/2.0.6/common/silva-119-99-515-806-nb-classifier.qza>`_ (MD5: ``d0f7f85c03fa1def6d3d98252094762f``)
- `Greengenes 13_8 99% OTUs full-length sequences <https://data.qiime2.org/2.0.6/common/gg-13-8-99-full-length-nb-classifier.qza>`_ (MD5: ``ccc41644e053f18c4aa9f6fcfe01dbc4``)
- `Greengenes 13_8 99% OTUs 250 base forward reads from 515F/806R region of sequences <https://data.qiime2.org/2.0.6/common/gg-13-8-99-515-806-nb-classifier.qza>`_ (MD5: ``4c2e010fcc44687dd3a2915a30d5d9c8``)

Marker gene reference databases
-------------------------------

Greengenes (16S rRNA)
`````````````````````

- `13_8 <ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz>`_ (most recent)
- `13_5 <ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_5_otus.tar.gz>`_
- `12_10 <ftp://greengenes.microbio.me/greengenes_release/gg_12_10/gg_12_10_otus.tar.gz>`_
- `February 4th, 2011 <http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz>`_

Find more information about Greengenes at http://greengenes.secondgenome.com.

Silva (16S/18S rRNA)
````````````````````

QIIME-compatible SILVA releases, as well as the licensing information for commercial and non-commercial use, are available at http://www.arb-silva.de/download/archive/qiime.

UNITE (fungal ITS)
``````````````````

All releases are available for download at http://unite.ut.ee/repository.php.

Find more information about UNITE at http://unite.ut.ee.

Microbiome bioinformatics benchmarking
--------------------------------------

Many microbiome bioinformatics benchmarking studies use *mock communities* (artificial communities constructed by pooling isolated microorganisms together in known abundances). For example, see `Bokulich et al., (2013) <http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3531572/>`_ and `Caporaso et al., (2011) <http://www.pnas.org/content/108/Supplement_1/4516.full>`_. Public mock community data can be downloaded from `mockrobiota <http://caporaso-lab.github.io/mockrobiota/>`_, which is described in `Bokulich et al., (2016) <http://msystems.asm.org/content/1/5/e00062-16>`_.

Public microbiome data
----------------------

`Qiita <http://qiita.microbio.me>`_ provides access to many public microbiome datasets. If you're looking for microbiome data for testing or for meta-analyses, Qiita is a good place to start.
