Data resources
==============

Taxonomy classifiers for use with q2-feature-classifier
-------------------------------------------------------

.. danger:: Pre-trained classifiers that can be used with ``q2-feature-classifier`` currently present a security risk. If using a pre-trained classifier such as the ones provided here, you should trust the person who trained the classifier and the person who provided you with the qza file. This security risk will be addressed in a future version of ``q2-feature-classifier``.

.. warning:: These classifiers were trained using scikit-learn 0.19.1, and therefore can only be used with scikit-learn 0.19.1. If you are using a native installation of QIIME, before using these classifiers you should run the following to ensure that you are using the correct version of scikit-learn. If you are using a QIIME 2018.6 virtual machine, scikit-learn 0.19.1 will be installed and you do not need to run this command. The scikit-learn version restriction will be relaxed in a future version of ``q2-feature-classifier``.

   .. command-block::
      :no-exec:

      conda install --override-channels -c defaults scikit-learn=0.19.1

.. note:: Taxonomic classifiers perform best when they are trained based on your specific sample preparation and sequencing parameters, including the primers that were used for amplification and the length of your sequence reads. Therefore in general you should follow the instructions in :doc:`Training feature classifiers with q2-feature-classifier <../tutorials/feature-classifier>` to train your own taxonomic classifiers (for example, from the marker gene reference databases below).

Naive Bayes classifiers trained on:

- `Silva 119 99% OTUs full-length sequences <https://data.qiime2.org/2018.6/common/silva-119-99-nb-classifier.qza>`_ (MD5: ``ea31f08bd07ff510f179fa7e8af8014e``)
- `Silva 119 99% OTUs from 515F/806R region of sequences <https://data.qiime2.org/2018.6/common/silva-119-99-515-806-nb-classifier.qza>`_ (MD5: ``aeb2f3144ba8b64b118167d3b7c8c52c``)
- `Greengenes 13_8 99% OTUs full-length sequences <https://data.qiime2.org/2018.6/common/gg-13-8-99-nb-classifier.qza>`_ (MD5: ``bb72a9e3f1a4c810dd50bceef3508105``)
- `Greengenes 13_8 99% OTUs from 515F/806R region of sequences <https://data.qiime2.org/2018.6/common/gg-13-8-99-515-806-nb-classifier.qza>`_ (MD5: ``919f2a946433b4ff2f9b554d3a99f6ac``)

Marker gene reference databases
-------------------------------

These marker gene reference databases are formatted for use with QIIME 1 and QIIME 2. If you're using these databases with QIIME 2, you'll need to :doc:`import them into artifacts <./tutorials/importing>` before using them.

Greengenes (16S rRNA)
`````````````````````

- `13_8 <ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz>`_ (most recent)
- `13_5 <ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_5_otus.tar.gz>`_
- `12_10 <ftp://greengenes.microbio.me/greengenes_release/gg_12_10/gg_12_10_otus.tar.gz>`_
- `February 4th, 2011 <http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz>`_

Find more information about Greengenes in the `DeSantis (2006) <http://aem.asm.org/content/72/7/5069.full>`_ and `McDonald (2012) <https://www.nature.com/articles/ismej2011139>`_ papers.

Silva (16S/18S rRNA)
````````````````````

QIIME-compatible SILVA releases, as well as the licensing information for commercial and non-commercial use, are available at https://www.arb-silva.de/download/archive/qiime.

UNITE (fungal ITS)
``````````````````

All releases are available for download at https://unite.ut.ee/repository.php.

Find more information about UNITE at https://unite.ut.ee.

Microbiome bioinformatics benchmarking
--------------------------------------

Many microbiome bioinformatics benchmarking studies use *mock communities* (artificial communities constructed by pooling isolated microorganisms together in known abundances). For example, see `Bokulich et al., (2013) <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3531572/>`_ and `Caporaso et al., (2011) <http://www.pnas.org/content/108/Supplement_1/4516.full>`_. Public mock community data can be downloaded from `mockrobiota <http://mockrobiota.caporasolab.us>`_, which is described in `Bokulich et al., (2016) <http://msystems.asm.org/content/1/5/e00062-16>`_.

Public microbiome data
----------------------

`Qiita <https://qiita.ucsd.edu/>`_ provides access to many public microbiome datasets. If you're looking for microbiome data for testing or for meta-analyses, Qiita is a good place to start.
