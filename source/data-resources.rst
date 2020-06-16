Data resources
==============

Taxonomy classifiers for use with q2-feature-classifier
-------------------------------------------------------

.. danger:: Pre-trained classifiers that can be used with ``q2-feature-classifier`` currently present a security risk. If using a pre-trained classifier such as the ones provided here, you should trust the person who trained the classifier and the person who provided you with the qza file. This security risk will be addressed in a future version of ``q2-feature-classifier``.

.. warning:: These classifiers were trained using scikit-learn 0.23.1, and therefore can only be used with scikit-learn 0.23.1. If you are using a native installation of QIIME 2, before using these classifiers you should run the following to ensure that you are using the correct version of scikit-learn. If you are using a QIIME 2020.6 virtual machine, scikit-learn 0.23.1 will be installed and you do not need to run this command. The scikit-learn version restriction will be relaxed in a future version of ``q2-feature-classifier``.

   .. command-block::
      :no-exec:

      conda install --override-channels -c defaults scikit-learn=0.23.1

.. note:: Taxonomic classifiers perform best when they are trained based on your specific sample preparation and sequencing parameters, including the primers that were used for amplification and the length of your sequence reads. Therefore in general you should follow the instructions in :doc:`Training feature classifiers with q2-feature-classifier <../tutorials/feature-classifier>` to train your own taxonomic classifiers (for example, from the marker gene reference databases below).

Naive Bayes classifiers trained on:

- `Silva 138 99% OTUs full-length sequences <https://data.qiime2.org/2020.6/common/silva-138-99-nb-classifier.qza>`_ (MD5: ``ded341b2a9220f1c473072bc85f221f0``)
- `Silva 138 99% OTUs from 515F/806R region of sequences <https://data.qiime2.org/2020.6/common/silva-138-99-515-806-nb-classifier.qza>`_ (MD5: ``37d890e5860b23246181ea9d50c14555``)
- `Greengenes 13_8 99% OTUs full-length sequences <https://data.qiime2.org/2020.6/common/gg-13-8-99-nb-classifier.qza>`_ (MD5: ``57cfea6fa6c6bd7ca27cbd9ccd5038f7``)
- `Greengenes 13_8 99% OTUs from 515F/806R region of sequences <https://data.qiime2.org/2020.6/common/gg-13-8-99-515-806-nb-classifier.qza>`_ (MD5: ``28bf2739f48b4da34a326498126c456b``)


Please cite the following references if you use any of these pre-trained classifiers:

- Bokulich, N.A., Robeson, M., Dillon, M.R. bokulich-lab/RESCRIPt. Zenodo. http://doi.org/10.5281/zenodo.3891931
- Bokulich, N.A., Kaehler, B.D., Rideout, J.R. et al. Optimizing taxonomic classification of marker-gene amplicon sequences with QIIME 2’s q2-feature-classifier plugin. Microbiome 6, 90 (2018). https://doi.org/10.1186/s40168-018-0470-z
- See the `SILVA website <https://www.arb-silva.de/>`_ and the latest `Greengenes publication <https://www.nature.com/articles/ismej2011139>`_ for the latest citation information for these reference databases.


.. warning:: If using any of the pre-trained classifiers above, consult the  `Greengenes <https://greengenes.secondgenome.com/>`_ or `SILVA <https://www.arb-silva.de/silva-license-information/>`_ websites for licensing information.


.. _`marker gene db`:

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

QIIME-compatible SILVA releases (up to release 132), as well as the licensing information for commercial and non-commercial use, are available at https://www.arb-silva.de/download/archive/qiime.

We also provide pre-formatted SILVA reference sequence and taxonomy files here.

- `Silva 138 SSURef NR99 full-length sequences <https://data.qiime2.org/2020.6/common/silva-138-99-seqs.qza>`_ (MD5: ``7f3ec37359911f7d7d1a745dfe9c5ffe``)
- `Silva 138 SSURef NR99 full-length taxonomy <https://data.qiime2.org/2020.6/common/silva-138-99-tax.qza>`_ (MD5: ``d9d2ec745f25eca522a6fa32f56a2982``)
- `Silva 138 SSURef NR99 515F/806R region sequences <https://data.qiime2.org/2020.6/common/silva-138-99-seqs-515-806.qza>`_ (MD5: ``98ffd2cec2840df3c2211fc999887bb9``)
- `Silva 138 SSURef NR99 515F/806R region taxonomy <https://data.qiime2.org/2020.6/common/silva-138-99-tax-515-806.qza>`_ (MD5: ``6c261dbb93d022b69da2dd3361744fcc``)


Please cite the following references if you use any of these pre-formatted files:

- Bokulich, N.A., Robeson, M., Dillon, M.R. bokulich-lab/RESCRIPt. Zenodo. http://doi.org/10.5281/zenodo.3891931
- See the `SILVA website <https://www.arb-silva.de/>`_ for the latest citation information for SILVA.


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

SEPP reference databases
------------------------

The following databases are intended for use with q2-fragment-insertion, and
are constructed directly from the
`SEPP-Refs project <https://github.com/smirarab/sepp-refs/>`_.

- `Silva 128 SEPP reference database <https://data.qiime2.org/2020.6/common/sepp-refs-silva-128.qza>`_ (MD5: ``7879792a6f42c5325531de9866f5c4de``)
- `Greengenes 13_8 SEPP reference database <https://data.qiime2.org/2020.6/common/sepp-refs-gg-13-8.qza>`_ (MD5: ``9ed215415b52c362e25cb0a8a46e1076``)
