Data resources
==============

Taxonomy classifiers for use with q2-feature-classifier
-------------------------------------------------------

.. danger:: Pre-trained classifiers that can be used with ``q2-feature-classifier`` currently present a security risk. If using a pre-trained classifier such as the ones provided here, you should trust the person who trained the classifier and the person who provided you with the qza file. This security risk will be addressed in a future version of ``q2-feature-classifier``.

.. note:: Taxonomic classifiers perform best when they are trained based on your specific sample preparation and sequencing parameters, including the primers that were used for amplification and the length of your sequence reads. Therefore in general you should follow the instructions in :doc:`Training feature classifiers with q2-feature-classifier <../tutorials/feature-classifier>` to train your own taxonomic classifiers (for example, from the marker gene reference databases below).

Naive Bayes classifiers trained on:

- `Silva 138 99% OTUs full-length sequences <https://data.qiime2.org/2020.8/common/silva-138-99-nb-classifier.qza>`_ (MD5: ``fddefff8bfa2bbfa08b9cad36bcdf709``)
- `Silva 138 99% OTUs from 515F/806R region of sequences <https://data.qiime2.org/2020.8/common/silva-138-99-515-806-nb-classifier.qza>`_ (MD5: ``28105eb0f1256bf38b9bb310c701dc4e``)
- `Greengenes 13_8 99% OTUs full-length sequences <https://data.qiime2.org/2020.8/common/gg-13-8-99-nb-classifier.qza>`_ (MD5: ``03078d15b265f3d2d73ce97661e370b1``)
- `Greengenes 13_8 99% OTUs from 515F/806R region of sequences <https://data.qiime2.org/2020.8/common/gg-13-8-99-515-806-nb-classifier.qza>`_ (MD5: ``682be39339ef36a622b363b8ee2ff88b``)


Please cite the following references if you use any of these pre-trained classifiers:

- Bokulich, N.A., Robeson, M., Dillon, M.R. bokulich-lab/RESCRIPt. Zenodo. http://doi.org/10.5281/zenodo.3891931
- Bokulich, N.A., Kaehler, B.D., Rideout, J.R. et al. Optimizing taxonomic classification of marker-gene amplicon sequences with QIIME 2’s q2-feature-classifier plugin. Microbiome 6, 90 (2018). https://doi.org/10.1186/s40168-018-0470-z
- See the `SILVA website <https://www.arb-silva.de/>`_ and the latest `Greengenes publication <https://www.nature.com/articles/ismej2011139>`_ for the latest citation information for these reference databases.

Please note, these classifiers were trained using scikit-learn 0.23.1, and therefore can only be used with scikit-learn 0.23.1. If you observe errors related to scikit-learn version mismatches, please ensure you are using the pretrained-classifiers that were published with the release of QIIME 2 you are using.


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

**License Information** can be found on the `Greengenes website <https://greengenes.secondgenome.com/>`_. Greengenes data are released under a `Creative Commons Attribution-ShareAlike 3.0 License <https://creativecommons.org/licenses/by-sa/3.0/deed.en_US>`_.



Silva (16S/18S rRNA)
````````````````````

QIIME-compatible SILVA releases (up to release 132), as well as the licensing information for commercial and non-commercial use, are available at https://www.arb-silva.de/download/archive/qiime.

We also provide pre-formatted SILVA reference sequence and taxonomy files here that were processed using `RESCRIPt <https://github.com/bokulich-lab/RESCRIPt>`_. See licensing information below if you use these files.

- `Silva 138 SSURef NR99 full-length sequences <https://data.qiime2.org/2020.8/common/silva-138-99-seqs.qza>`_ (MD5: ``de8886bb2c059b1e8752255d271f3010``)
- `Silva 138 SSURef NR99 full-length taxonomy <https://data.qiime2.org/2020.8/common/silva-138-99-tax.qza>`_ (MD5: ``f12d5b78bf4b1519721fe52803581c3d``)
- `Silva 138 SSURef NR99 515F/806R region sequences <https://data.qiime2.org/2020.8/common/silva-138-99-seqs-515-806.qza>`_ (MD5: ``a914837bc3f8964b156a9653e2420d22``)
- `Silva 138 SSURef NR99 515F/806R region taxonomy <https://data.qiime2.org/2020.8/common/silva-138-99-tax-515-806.qza>`_ (MD5: ``e2c40ae4c60cbf75e24312bb24652f2c``)


Please cite the following references if you use any of these pre-formatted files:

- Bokulich, N.A., Robeson, M., Dillon, M.R. bokulich-lab/RESCRIPt. Zenodo. http://doi.org/10.5281/zenodo.3891931
- See the `SILVA website <https://www.arb-silva.de/>`_ for the latest citation information for SILVA.

License Information:
^^^^^^^^^^^^^^^^^^^^

The pre-formatted SILVA reference sequence and taxonomy files above are available under a `Creative Commons Attribution 4.0 License <https://creativecommons.org/licenses/by/4.0/>`_ (CC-BY 4.0). See the `SILVA license <https://www.arb-silva.de/silva-license-information/>`_ for more information.

The files above were downloaded and processed from the SILVA 138 release data using the `RESCRIPt plugin <https://github.com/bokulich-lab/RESCRIPt>`_ and `q2-feature-classifier <https://github.com/qiime2/q2-feature-classifier/>`_. Sequences were downloaded, reverse-transcribed, and filtered to remove sequences based on length, presence of ambiguous nucleotides and/or homopolymer. Taxonomy was parsed to generate even 7-level rank taxonomic labels, including species labels. Sequences and taxonomies were dereplicated using RESCRIPt. Sequences and taxonomies representing the 515F/806R region of the 16S SSU rRNA gene were extracted with q2-feature-classifier, followed by dereplication with RESCRIPt.



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

- `Silva 128 SEPP reference database <https://data.qiime2.org/2020.8/common/sepp-refs-silva-128.qza>`_ (MD5: ``7879792a6f42c5325531de9866f5c4de``)
- `Greengenes 13_8 SEPP reference database <https://data.qiime2.org/2020.8/common/sepp-refs-gg-13-8.qza>`_ (MD5: ``9ed215415b52c362e25cb0a8a46e1076``)
