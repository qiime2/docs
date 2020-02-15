Citing QIIME 2
==============

Please note that almost all QIIME 2 plugins implement methods that were developed independently of the QIIME 2 framework, which should be cited in addition to the QIIME 2 framework itself. This information can be extracted as described below.

If you use QIIME 2 in your research, please cite the following `preprint`_:

    Bolyen E, Rideout JR, Dillon MR, Bokulich NA, Abnet CC, Al-Ghalith GA, Alexander H, Alm EJ, Arumugam M, Asnicar F, Bai Y, Bisanz JE, Bittinger K, Brejnrod A, Brislawn CJ, Brown CT, Callahan BJ, Caraballo-Rodríguez AM, Chase J, Cope EK, Da Silva R, Diener C, Dorrestein PC, Douglas GM, Durall DM, Duvallet C, Edwardson CF, Ernst M, Estaki M, Fouquier J, Gauglitz JM, Gibbons SM, Gibson DL, Gonzalez A, Gorlick K, Guo J, Hillmann B, Holmes S, Holste H, Huttenhower C, Huttley GA, Janssen S, Jarmusch AK, Jiang L, Kaehler BD, Kang KB, Keefe CR, Keim P, Kelley ST, Knights D, Koester I, Kosciolek T, Kreps J, Langille MGI, Lee J, Ley R, Liu YX, Loftfield E, Lozupone C, Maher M, Marotz C, Martin BD, McDonald D, McIver LJ, Melnik AV, Metcalf JL, Morgan SC, Morton JT, Naimey AT, Navas-Molina JA, Nothias LF, Orchanian SB, Pearson T, Peoples SL, Petras D, Preuss ML, Pruesse E, Rasmussen LB, Rivers A, Robeson MS, Rosenthal P, Segata N, Shaffer M, Shiffer A, Sinha R, Song SJ, Spear JR, Swafford AD, Thompson LR, Torres PJ, Trinh P, Tripathi A, Turnbaugh PJ, Ul-Hasan S, van der Hooft JJJ, Vargas F, Vázquez-Baeza Y, Vogtmann E, von Hippel M, Walters W, Wan Y, Wang M, Warren J, Weber KC, Williamson CHD, Willis AD, Xu ZZ, Zaneveld JR, Zhang Y, Zhu Q, Knight R, and Caporaso JG. 2019. Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2. Nature Biotechnology 37: 852–857. https://doi.org/10.1038/s41587-019-0209-9


Citing QIIME 2 Plugins
-----------------------
Most QIIME 2 plugins are the products of independent development work. This includes software, methods, algorithms, and metrics that were devised independently of QIIME 2, frequently by independent research teams who have no affiliation with QIIME 2 or its developers. Please practice due diligence: be aware of the plugins, methods, metrics, and software that QIIME 2 is using under the hood, and cite these as is appropriate, in addition to citing QIIME 2 itself.

For example, external software like `VSEARCH`_ is used under the hood in some QIIME 2 plugins, such as ``q2-vsearch`` and in the ``classify-consensus-vsearch`` method in ``q2-feature-classifier``. If we use ``classify-consensus-vsearch``, we should cite `VSEARCH`_ (which provides the alignment algorithm used by this method), we should cite `q2-feature-classifier`_ (which provides the LCA taxonomy classification performed by this method), and we should cite QIIME 2 (which brings truth to the world and meaning to our existence).

Citation information can be retrieved in two different ways: for specific plugins/actions, or using the provenance contained in an artifact or visualization to list citations for each method used to generate that file. In either case it may be appropriate to add additional citations not listed there. For example, the q2-diversity plugin lists citations for UniFrac, but if you use other beta or alpha diversity methods in a publication, you should cite the original source of those method(s).

Both citation retrieval methods will list citations in BibTeX format, which should be importable by most citation management software.

.. _plugin-specific-citations:

Retrieving plugin-specific citations
````````````````````````````````````
You can retrieve citation information for any QIIME 2 plugin by using the command ``qiime <plugin-name> --citations``, though that command will only list citations that are directly related to the plugin, and not the individual actions contained therein. The command ``qiime <plugin-name> <action-name> --citations`` can retrieve action-specific citations, if any are listed. Ultimately, provenance will be more useful for retroactively tracing appropriate citations for any given QIIME 2 results file.


Using provenance to list citations.
```````````````````````````````````
.. note:: Citation tracking was added to QIIME 2 provenance starting in release 2018.4, so if your data were analyzed with older versions of QIIME 2 at any point citation information will not be available for those actions.

Each time any action is performed in QIIME 2, that information is logged in the provenance of artifacts and visualizations that are generated, along with any citations associated with that action. This provenance information is inherited by other artifacts or visualizations generated from that file, and hence citation (and other provenance) information is stored in a persistent record that can be used to trace all actions (and citations) that were used to generate any given QIIME 2 artifact or visualization. This information can be viewed and compiled using QIIME 2 view:

1. Open https://view.qiime2.org/ in a browser window and drop your artifact/visualization of interest into the browser window. OR use the ```qiime tools view`` command to view an artifact or visualization in QIIME 2 view.
2. Click on the "Provenance" tab in the upper right-hand corner of the browser window.
3. Click on the "Citations" tab that appears in the window below to view a list of citations.
4. Click "Download" to download the list in BibTeX format.
5. Review the citations list and use common sense to make sure that you are citing all software and methods appropriately. If you notice any discrepancies in the citations that are listed by any QIIME 2 plugin, please verify which plugin/action is missing citations or mis-citing, using the directions above for retrieving plugin-specific citation information. Then get in touch on the `QIIME 2 forum`_ to let us know!


Example methods descriptions
----------------------------
A good methods description not only gives credit where it is due, it also promotes transparency and reproducibility of the results. A bad methods section will not detail the steps performed in an analysis; will not cite or incompletely cite underlying plugins, methods, or software; and will utterly obfuscate any possibility of reproducing that analysis.

A bad methods section
`````````````````````
  Bacterial 16S rRNA gene sequence data were analyzed with QIIME 2 (Bolyen et al., 2019) to generate principal coordinates analysis plots and assign taxonomy.

.. question:: What steps were performed in this analysis? What distance metric was used for PCoA? Was any type of quality control or normalization applied to the data? What methods and reference databases were used to assign taxonomy?

A good methods section
``````````````````````
This methods section was adapted from `Pearson et al. 2019`_ (and shortened in the interest of brevity; see the original publication for a full methods description). Note that each step of analysis is described, including non-default parameter settings, the plugins performing each operation are mentioned, and individual plugins, underlying software, and methods/metrics are cited as appropriate. This paragraph describes most of the steps that are performed in a basic QIIME 2 analysis (e.g., following the :doc:`moving pictures tutorial <tutorials/moving-pictures>`), plus some additional steps; it may be used as a template methods section for similar workflows.

  Microbiome bioinformatics were performed with QIIME 2 2017.4 (Bolyen et al. 2019). Raw sequence data were demultiplexed and quality filtered using the q2‐demux plugin followed by denoising with DADA2 (Callahan et al. 2016) (via q2‐dada2). All amplicon sequence variants (ASVs) were aligned with mafft (Katoh et al. 2002) (via q2‐alignment) and used to construct a phylogeny with fasttree2 (Price et al. 2010) (via q2‐phylogeny). Alpha‐diversity metrics (observed OTUs and Faith's Phylogenetic Diversity (Faith 1992)), beta diversity metrics (weighted UniFrac (Lozupone et al. 2007), unweighted UniFrac (Lozupone et al. 2005), Jaccard distance, and Bray‐Curtis dissimilarity), and Principle Coordinate Analysis (PCoA) were estimated using q2‐diversity after samples were rarefied (subsampled without replacement) to 900 sequences per sample. Taxonomy was assigned to ASVs using the q2‐feature‐classifier (Bokulich et al. 2018a) classify‐sklearn naïve Bayes taxonomy classifier against the Greengenes 13_8 99% OTUs reference sequences (McDonald et al. 2012). We computed the change in direction and magnitude in the first principal co-ordinate axis (PC1) for each subject between their pretreatment and posttreatment samples using q2‐longitudinal (Bokulich et al. 2018b). The average change in PC1 for each treatment group, overall and stratified by sex, was tested for difference from zero using a one‐sample t test with Benjamini‐Hochberg false discovery rate (FDR) correction (Benjamini and Hochberg 1995).


* Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57:289‐300.
* Bokulich NA, Kaehler BD, Rideout JR, et al. Optimizing taxonomic classification of marker‐gene amplicon sequences with QIIME 2's q2‐feature‐classifier plugin. Microbiome. 2018a;6:90.
* Bokulich NA, Dillon MR, Zhang Y, et al. q2‐longitudinal: Longitudinal and paired‐sample analyses of microbiome data. mSystems. 2018b;3:e00219‐e318.
* Bolyen E, Rideout JR, Dillon MR, et al. 2019. Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2. Nature Biotechnology 37: 852–857. https://doi.org/10.1038/s41587-019-0209-9
* Bray JR, Curtis JT. An ordination of upland forest communities of southern Wisconsin. Ecol Monogr. 1957;27:325-349
* Callahan BJ, McMurdie PJ, Rosen MJ, et al. DADA2: high‐resolution sample inference from Illumina amplicon data. Nat Methods. 2016;13:581‐583.
* Faith DP. Conservation evaluation and phylogenetic diversity. Biol Cons. 1992;61:1‐10.
* Katoh K, Misawa K, Kuma K, et al. MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform. Nucleic Acids Res. 2002;30:3059‐3066.
* Lozupone CA, Hamady M, Kelley ST, et al. Quantitative and qualitative beta diversity measures lead to different insights into factors that structure microbial communities. Appl Environ Microbiol. 2007;73:1576‐1585.
* Lozupone C, Knight R. UniFrac: a new phylogenetic method for comparing microbial communities. Appl Environ Microbiol. 2005;71:8228‐8235.
* McDonald D, Price MN, Goodrich J, et al. An improved Greengenes taxonomy with explicit ranks for ecological and evolutionary analyses of bacteria and archaea. ISME J. 2012;6:610‐ 618.
* Price MN, Dehal PS, Arkin AP. FastTree 2–approximately maximum‐likelihood trees for large alignments. PLoS ONE. 2010;5:e9490.


.. _preprint: https://peerj.com/preprints/27295/
.. _VSEARCH: https://github.com/torognes/vsearch
.. _q2-feature-classifier: https://doi.org/10.1186/s40168-018-0470-z
.. _QIIME 2 forum: https://forum.qiime2.org/
.. _Pearson et al. 2019: https://doi.org/10.1002/cam4.1965
