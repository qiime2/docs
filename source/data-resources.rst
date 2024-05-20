Data resources
==============

Taxonomy classifiers for use with q2-feature-classifier
-------------------------------------------------------

Taxonomy classifiers have been moved to the external page https://resources.qiime2.org.

.. _`marker gene db`:

Marker gene reference databases
-------------------------------

These marker gene reference databases are formatted for use with QIIME 1 and QIIME 2. If you're using these databases with QIIME 2, you'll need to :doc:`import them into artifacts <./tutorials/importing>` before using them.

Greengenes (16S rRNA)
`````````````````````

- `2022.10 <http://ftp.microbio.me/greengenes_release/2022.10/>`_ (most recent)
- `13_8 <https://data.qiime2.org/classifiers/greengenes/gg_13_8_otus.tar.gz>`_
- `13_5 <https://data.qiime2.org/classifiers/greengenes/gg_13_5_otus.tar.gz>`_
- `12_10 <https://data.qiime2.org/classifiers/greengenes/gg_12_10_otus.tar.gz>`_
- `February 4th, 2011 <http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz>`_

Find more information about Greengenes in the `DeSantis (2006) <http://aem.asm.org/content/72/7/5069.full>`_, `McDonald (2012) <https://www.nature.com/articles/ismej2011139>`_, and `McDonald (2023) <https://www.nature.com/articles/s41587-023-01845-1>`_ papers.

**License Information** can be found on the `Greengenes website <https://greengenes.secondgenome.com/>`_ (prior to 2022) or on the Greengenes2 `FTP <http://ftp.microbio.me/greengenes_release/current/>`_. Greengenes data (prior to 2022) are released under a `Creative Commons Attribution-ShareAlike 3.0 License <https://creativecommons.org/licenses/by-sa/3.0/deed.en_US>`_. Greengenes2 data (2022-) are released under a `BSD-3 license <http://ftp.microbio.me/greengenes_release/current/00LICENSE>`_.

Silva (16S/18S rRNA)
````````````````````

QIIME-compatible SILVA releases (up to release 132), as well as the licensing information for commercial and non-commercial use, are available at https://www.arb-silva.de/download/archive/qiime.

We also provide pre-formatted SILVA reference sequence and taxonomy files here that were processed using `RESCRIPt <https://github.com/bokulich-lab/RESCRIPt>`_. See licensing information below if you use these files.

- `Silva 138 SSURef NR99 full-length sequences <https://data.qiime2.org/2024.2/common/silva-138-99-seqs.qza>`_ (MD5: ``de8886bb2c059b1e8752255d271f3010``)
- `Silva 138 SSURef NR99 full-length taxonomy <https://data.qiime2.org/2024.2/common/silva-138-99-tax.qza>`_ (MD5: ``f12d5b78bf4b1519721fe52803581c3d``)
- `Silva 138 SSURef NR99 515F/806R region sequences <https://data.qiime2.org/2024.2/common/silva-138-99-seqs-515-806.qza>`_ (MD5: ``a914837bc3f8964b156a9653e2420d22``)
- `Silva 138 SSURef NR99 515F/806R region taxonomy <https://data.qiime2.org/2024.2/common/silva-138-99-tax-515-806.qza>`_ (MD5: ``e2c40ae4c60cbf75e24312bb24652f2c``)


Please cite the following references if you use any of these pre-formatted files:

- Michael S Robeson II, Devon R O'Rourke, Benjamin D Kaehler, Michal Ziemski, Matthew R Dillon, Jeffrey T Foster, Nicholas A Bokulich. RESCRIPt: Reproducible sequence taxonomy reference database management for the masses. bioRxiv 2020.10.05.326504; doi: https://doi.org/10.1101/2020.10.05.326504
- See the `SILVA website <https://www.arb-silva.de/>`_ for the latest citation information for SILVA.

.. note:: The Silva reference files provided here include species-level taxonomy. While Silva annotations do include species, Silva does not curate the species-level taxonomy so this information may be unreliable. In a future version of QIIME 2 we will no longer include species-level information in our Silva reference files. This is discussed on the QIIME 2 Forum `here <https://forum.qiime2.org/t/processing-filtering-and-evaluating-the-silva-database-and-other-reference-sequence-data-with-rescript/15494#heading--second-header>`_ (see *Species-labels: caveat emptor!*).

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

- `Silva 128 SEPP reference database <https://data.qiime2.org/2024.2/common/sepp-refs-silva-128.qza>`_ (MD5: ``7879792a6f42c5325531de9866f5c4de``)
- `Greengenes 13_8 SEPP reference database <https://data.qiime2.org/2024.2/common/sepp-refs-gg-13-8.qza>`_ (MD5: ``9ed215415b52c362e25cb0a8a46e1076``)
