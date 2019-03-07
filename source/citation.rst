Citing QIIME 2
==============

Please note that almost all QIIME™ 2 plugins implement methods that were developed independently of the QIIME™ 2 framework, which should be cited in addition to the QIIME™ 2 framework itself. This information can be extracted as described below.

If you use QIIME™ 2 in your research, please cite the following `preprint`_:

    Bolyen E, Rideout JR, Dillon MR, Bokulich NA, Abnet C, Al-Ghalith GA, Alexander H, Alm EJ, Arumugam M, Asnicar F, Bai Y, Bisanz JE, Bittinger K, Brejnrod A, Brislawn CJ, Brown CT, Callahan BJ, Caraballo-Rodríguez AM, Chase J, Cope E, Da Silva R, Dorrestein PC, Douglas GM, Durall DM, Duvallet C, Edwardson CF, Ernst M, Estaki M, Fouquier J, Gauglitz JM, Gibson DL, Gonzalez A, Gorlick K, Guo J, Hillmann B, Holmes S, Holste H, Huttenhower C, Huttley G, Janssen S, Jarmusch AK, Jiang L, Kaehler B, Kang KB, Keefe CR, Keim P, Kelley ST, Knights D, Koester I, Kosciolek T, Kreps J, Langille MG, Lee J, Ley R, Liu Y, Loftfield E, Lozupone C, Maher M, Marotz C, Martin BD, McDonald D, McIver LJ, Melnik AV, Metcalf JL, Morgan SC, Morton J, Naimey AT, Navas-Molina JA, Nothias LF, Orchanian SB, Pearson T, Peoples SL, Petras D, Preuss ML, Pruesse E, Rasmussen LB, Rivers A, Robeson, II MS, Rosenthal P, Segata N, Shaffer M, Shiffer A, Sinha R, Song SJ, Spear JR, Swafford AD, Thompson LR, Torres PJ, Trinh P, Tripathi A, Turnbaugh PJ, Ul-Hasan S, van der Hooft JJ, Vargas F, Vázquez-Baeza Y, Vogtmann E, von Hippel M, Walters W, Wan Y, Wang M, Warren J, Weber KC, Williamson CH, Willis AD, Xu ZZ, Zaneveld JR, Zhang Y, Zhu Q, Knight R, Caporaso JG. 2018. QIIME 2: Reproducible, interactive, scalable, and extensible microbiome data science. PeerJ Preprints 6:e27295v2 https://doi.org/10.7287/peerj.preprints.27295v2


Citing QIIME™ 2 Plugins
-----------------------
Most QIIME™ 2 plugins are the products of independent development work. This includes software, methods, algorithms, and metrics that were devised independently of QIIME™ 2, frequently by independent research teams who have no affiliation with QIIME™ 2 or its developers. Please practice due diligence: be aware of the plugins, methods, metrics, and software that QIIME™ 2 is using under the hood, and cite these as is appropriate, in addition to citing QIIME™ 2 itself.

For example, external software like `VSEARCH`_ is used under the hood in some QIIME™ 2 plugins, such as ``q2-vsearch`` and in the ``classify-consensus-vsearch`` method in ``q2-feature-classifier``. If we use ``classify-consensus-vsearch``, we should cite `VSEARCH`_ (which provides the alignment algorithm used by this method), we should cite `q2-feature-classifier`_ (which provides the LCA taxonomy classification performed by this method), and we should cite QIIME 2 (which brings truth to the world and meaning to our existence).

Citation information can be retrieved in two different ways: for specific plugins/actions, or using the provenance contained in an artifact or visualization to list citations for each method used to generate that file. In either case it may be appropriate to add additional citations not listed there. For example, the q2-diversity plugin lists citations for UniFrac, but if you use other beta or alpha diversity methods in a publication, you should cite the original source of those method(s).

Both citation retrieval methods will list citations in BibTeX format, which should be importable by most citation management software.


Retrieving plugin-specific citations
````````````````````````````````````
You can retrieve citation information for any QIIME™ 2 plugin by using the command ``qiime <plugin-name> --citations``, though that command will only list citations that are directly related to the plugin, and not the individual actions contained therein. The command ``qiime <plugin-name> <action-name> --citations`` can retrieve action-specific citations, if any are listed. Ultimately, provenance will be more useful for retroactively tracing appropriate citations for any given QIIME™ 2 results file.


Using provenance to list citations.
```````````````````````````````````
.. note:: Citation tracking was added to QIIME 2 provenance starting in release 2018.4, so if your data were analyzed with older versions of QIIME 2 at any point citation information will not be available for those actions.

Each time any action is performed in QIIME™ 2, that information is logged in the provenance of artifacts and visualizations that are generated, along with any citations associated with that action. This provenance information is inherited by other artifacts or visualizations generated from that file, and hence citation (and other provenance) information is stored in a persistent record that can be used to trace all actions (and citations) that were used to generate any given QIIME 2 artifact or visualization. This information can be viewed and compiled using QIIME™ 2 view:

1. Open https://view.qiime2.org/ in a browser window and drop your artifact/visualization of interest into the browser window. OR use the ```qiime tools view`` command to view an artifact or visualization in QIIME™ 2 view.
2. Click on the "Provenance" tab in the upper right-hand corner of the browser window.
3. Click on the "Citations" tab that appears in the window below to view a list of citations.
4. Click "Download" to download the list in BibTeX format.
5. Review the citations list and use common sense to make sure that you are citing all software and methods appropriately. If you notice any discrepancies in the citations that are listed by any QIIME 2 plugin, please verify which plugin/action is missing citations or mis-citing, using the directions above for retrieving plugin-specific citation information. Then get in touch on the `QIIME 2 forum`_ to let us know!



.. _preprint: https://peerj.com/preprints/27295/
.. _VSEARCH: https://github.com/torognes/vsearch
.. _q2-feature-classifier: https://doi.org/10.1186/s40168-018-0470-z
.. _QIIME 2 forum: https://forum.qiime2.org/
