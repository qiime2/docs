Sequence alignment and phylogenetic inference with q2-phylogeny
===============================================================

..note:: This tutorial assumes, you've read through the `QIIME 2 Overview`_ documentation and have at least worked through some of the other `Tutorials`_..

Inferring phylogenies
---------------------
Several downstream diversity metrics, available within QIIME, require that a
phylogenetic tree be constructed using the Operational Taxonomic Units (`OTUs`_) or
Exact Sequence Variants (`ESVs`_) being investigated.

*But how do we proceed to construct a phylogeny from our sequence data?*
 Well, there are two phylogeny-based approaches we can use. Deciding upon which to use is largely dependent on your study questions:
1)  A reference-based `fragment insertion`_ approach. Which, is likely the ideal choice. Especially, if your reference phylogeny (and associated representative sequences) encompass neighboring relatives of which your sequences can be reliably inserted. Any sequences that do not match well enough to the reference are not inserted. This may or may not have implications for your study questions. For more information, check out these great `fragment insertion examples`_.
2) A *de novo* approach. Marker genes that can be globally aligned across divergent taxa, are usually amenable to sequence alignment and phylogenetic investigation through this approach. This community tutorial will focus on the *de novo* approaches.


**Here, you will learn how to make use of _de novo_ phylogenetic approaches to**:
	1) generate a sequence alignment within QIIME
	2) mask the alignment if needed
	3) construct a phylogenetic tree
	4) root the phylogenetic tree

If you would like to substitute any of the steps outlined here by making use of tools external to QIIME 2, please see the `import`_, `export`_, and `filtering`_ documentation where appropriate.


Sequence Alignment
..................
Prior to constructing a `phylogeny`_ we must generate a multiple sequence alignment (`MSA`_). When constructing a MSA we are making a statement about the `putative homology`_ of the aligned residues (columns of the MSA) by virtue of their `sequence similarity`_.

The number of algorithms to construct a MSA are legion. We will make use of `MAFFT`_ (Multiple Alignment using Fast Fourier Transform)) via the `q2-alignment`_ plugin. For more information checkout the `MAFFT paper`_.

**Input: unaligned representative sequences from the [Atacama soil microbiome tutorial](https://docs.qiime2.org/2019.7/tutorials/atacama-soils/):**
.. download::
   :no-exec: 
   :url: https://docs.qiime2.org/2019.7/data/tutorials/atacama-soils/rep-seqs.qza
   :saveas: rep-seqs.qza

**Run MAFFT**

.. command-block::
   qiime alignment mafft \
      --i-sequences rep-seqs.qza \
      --o-alignment aligned-rep-seqs.qza

Reducing alignment ambiguity: masking and reference alignments.
...............................................................
*Why mask an alignment?*
Masking helps to eliminate alignment columns that are phylogenetically uninformative or misleading before phylogenetic analysis. Much of the time alignment errors can introduce noise and confound phylogenetic inference. It is common practice to mask (remove) these ambiguously aligned regions prior to performing phylogenetic inference. In particular, `David Lane's (1991)`_ chapter `16S/23S rRNA sequencing`_ proposed masking SSU data prior to phylogenetic analysis.  However, knowing how to deal with ambiguously aligned regions and when to apply masks largely depends on the marker genes being analyzed and the question being asked of the data.

.. note:: Keep in mind that this is still an active area of discussion, as highlighted by the following non-exhaustive list of articles: `Wu *et al*. 2012`_, `Ashkenazy *et al*. 2018`_, `Schloss 2010`_, `Tan *et al*. 2015`_, `Rajan 2015`_.


*How to mask alignment.*
For our purposes, we'll assume that we have ambiguously aligned columns in the MAFFT alignment we produced above. The default settings for the ``--p-min-conservation`` of the `alignment mask plugin`_ approximates the Lane mask filtering of QIIME 1. Keep an eye out for updates to the alignment plugin.

.. command-block::
   qiime alignment mask \
   --i-alignment aligned-rep-seqs.qza \
   --o-masked-alignment masked-aligned-rep-seqs.qza

*Reference based alignments*
There are a variety of tools such as `PyNAST`_) (using `NAST`_), `Infernal`_, and `SINA`_, etc., that attempt to reduce the amount of ambiguously aligned regions by using curated reference alignments (e.g. `SILVA`_. Reference alignments are particularly powerful for rRNA gene sequence data, as knowledge of secondary structure is incorporated into the curation process, thus increasing alignment quality. For a more in-depth and eloquent overview of reference-based alignment approaches, check out the great `SINA community tutorial`_).


.. note:: Alignments constructed using reference based alignment approaches can be masked too, just like the above MAFFT example. Also, the reference alignment approach we are discussing here is distinct from the reference phylogeny approach (i.e. `q2-fragment-insertion`_) we mentioned earlier. That is, we are not inserting our data into an existing tree, but simply trying to create a more robust alignment for making a better *de novo* phylogeny.


Construct a phylogeny
---------------------
As with MSA algorithms, phylogenetic inference tools are also legion. Fortunately, there are many great resources to learn about phylogentics. Below are just a few introductory resources to get you started:

1. `Phylogeny for the faint of heart - a tutorial`_
2. `Molecular phylogenetics - principles and practice`_
3. `Phylogenetics - An Introduction`_

Via the `q2-phylogeny`_ plugin of :qiime2:, there are several methods for phylogenetic inference based on the following tools: 
 1. `FastTree`_
 2. `RAxML`_
 3. `IQ-TREE`_
and this plugin pipeline:
 1. `align-to-tree-mafft-fasttree`_

Methods 
=======

fasttree
------------
FastTree is able to construct phylogenies from large sequence alignments quite rapidly. It does this by using the using a `CAT-like`_ rate category  approximation, which is also available through RAxML (discussed below). Check out the `FastTree online manual`_ for more information.

.. code-block::
   qiime phylogeny fasttree \
      --i-alignment masked-aligned-rep-seqs.qza \
      --o-tree fasttree-tree.qza --verbose

.. tip:: For an easy and direct way to view your ``tree.qza`` files, upload them to `iTOL`_. Here, you caninteractively view and manipulate your phylogeny. Even better, while viewing the tree topology in "Normal mode", you can drag and drop your associated ``alignment.qza`` (the one you used to build the phylogeny) or a relevent ``taxonomy.qza`` file onto the iTOL tree visualization. This will allow you to directly view the sequence alignment or taxonomy alongside the phylogeny. :sunglasses:


raxml
-----
Like ``fasttree``,  ``raxml`` will perform a single phylogentic inference and return a tree. Note, the default model for ``raxml`` is ``--p-substitution-model GTRGAMMA``. If you'd like to construct a tree using the CAT model like ``fasttree``, simply replace ``GTRGAMMA`` with ``GTRCAT`` as shown below:

.. code-block::
   qiime phylogeny raxml \
      --p-substitution-model GTRCAT \
      --i-alignment masked-aligned-rep-seqs.qza \
      --o-tree raxml-cat-tree.qza

Perform multiple searches using raxml
.....................................
If you'd like to perform a more thorough search of "tree space" you can instruct ``raxml`` to perform multiple independent searches on the full alignment by using ``--p-n-searches 5``. Once these 5 independent searches are completed, only the single best scoring tree will be returned. *Note, we are not bootstrapping here, we'll do that in a later example.* Let's set ``--p-substitution-model GTRCAT``. Finally, let's also manually set a seed via ``--p-seed``. By setting our seed, we allow other users the ability to reproduce our phylogeny. That is, anyone using the same sequence alignment and substitution model, will generate the same tree as long as they set the same seed value. Although, ``--p-seed`` is not a required argument, it is generally a good idea to set this value.

.. code-block::
   qiime phylogeny raxml \
      --p-substitution-model GTRCAT \
      --p-seed 1723 \
      --p-n-searches 5 \
      --i-alignment masked-aligned-rep-seqs.qza \
      --o-tree raxml-cat-searches-tree.qza \
      --verbose

raxml-rapid-bootstrap
.....................
In phylogenetics, it is good practice to check how well the `splits / bipartitions`_ in your phylogeny are supported. Often one is interested in which clades are robustly separated from other clades in the phylogeny. One way, of doing this is via bootstrapping (See the *Bootstrapping* section of the first introductory link above). In QIIME 2, we've provided access to the RAxML `rapid bootsrap`_ feature. The only difference between this command and the previous are the additional flags ``--p-bootstrap-replicates`` and ``--p-rapid-bootstrap-seed``. It is quite common to perform anywhere from 100 - 1000 bootstrap replicates. The ``--p-rapid-bootstrap-seed`` works very much like the ``--p-seed`` argument from above except that it allows anyone to reproduce the bootstrapping process and the associated supports for your splits.

As per the `RAxML online documentation`_ and the `RAxML manual`_, the rapid bootstrapping command that we will execute below will do the following:

1. Bootstrap the input alignment 100 times and perform a Maximum Likelihood (ML) search on each. 
2. Find best scoring ML tree through multiple independent searches using the original input alignment. The number of independent searches is determined by the number of bootstrap replicates set in the 1st step. That is, your search becomes more thorough with increasing bootstrap replicates. The ML optimization of RAxML uses every 5th bootstrap tree as the starting tree for an ML search on the original alignment.
3. Map the bipartitions (bootstrap supports, 1st step) onto the best scoring ML tree (2nd step).

.. code-block::
   qiime phylogeny raxml-rapid-bootstrap \
      --p-seed 1723 \
      --p-rapid-bootstrap-seed 9384 \
      --p-bootstrap-replicates 100 \
      --p-substitution-model GTRCAT \
      --i-alignment masked-aligned-rep-seqs.qza \
      --o-tree raxml-cat-bootstrap-tree.qza \
      --verbose

.. tip:: RAxML Run Time.
You may gave noticed that we've added the flag ``--p-raxml-version`` to both RAxML methods. Here, we are providing a means to simply access versions of RAxML that have optimized vector instructions for various modern x86 processor architectures. Paraphrased from the RAxML manual and help documentation:

1. Most recent processors will support SSE3 vector instructions (i.e. will likely support the faster AVX2 vector instructions). 
2. These instructions will substantially accelerate the likelihood and parsimony computations. SSE3 versions will run approximately 40% faster than the standard version. The AVX2 version will run 10-30% faster than the SSE3 version.

.. tip:: Larger sequence alignments.
 1. Make use of multiple cores / threads as outlined earlier. Keep in mind that using more cores / threads is `not necessarily always better`_. Additionally, the RAxML manual suggests 1 core per ~500 DNA alignment patterns. This is usually visible on screen, when the ``--verbose`` option is used.
 2. Try using a rate category (CAT model; via ``--p-substitution-model``), which results in equally good trees as the GAMMA models and is approximately 4 times faster. See the `CAT paper`_. The CAT approximation is also Ideal for alignments containing `10,000 or more taxa`_, and is very much similar the `CAT-like model of FastTree2`_.

iqtree
------







.. _QIIME 2 Overview: https://docs.qiime2.org/2019.7/tutorials/overview
.. _Tutorials: https://docs.qiime2.org/2019.7/tutorials
.. _OTUs: https://en.wikipedia.org/wiki/Operational_taxonomic_unit
.. _ESVs: https://doi.org/10.1038/ismej.2019.119
.. _fragment insertion: https://doi.org/10.1128/mSystems.00021-18
.. _fragment insertion examples: https://github.com/biocore/q2-fragment-insertion
.. _import: https://docs.qiime2.org/2019.7/tutorials/importing/
.. _export: https://docs.qiime2.org/2019.7/tutorials/exporting/
.. _filtering: https://docs.qiime2.org/2019.7/tutorials/filtering/
.. _phylogeny: https://simple.wikipedia.org/wiki/Phylogeny
.. _MSA: https://en.wikipedia.org/wiki/Multiple_sequence_alignment
.. _putative homology: http://doi.org/10.1006/mpev.2000.0785
.. _sequence similarity: http://doi.org/10.1002/0471250953.bi0301s42
.. _MAFFT: https://en.wikipedia.org/wiki/MAFFT
.. _q2-alignment: https://docs.qiime2.org/2018.11/plugins/available/alignment/
.. _MAFFT paper: http://doi.org/10.1093/molbev/mst010
.. _David Lane's (1991): http://www.worldcat.org/title/nucleic-acid-techniques-in-bacterial-systematics/oclc/22310197
.. _16S/23S rRNA sequencing: http://catdir.loc.gov/catdir/toc/onix05/90012998.html
.. _Wu *et al*. 2012: https://doi.org/10.1371/journal.pone.0030288
.. _Ashkenazy *et al*. 2018: https://doi.org/10.1093/sysbio/syy036
.. _Schloss 2010: https://doi.org/10.1371/journal.pcbi.1000844
.. _Tan *et al*. 2015: https://doi.org/10.1093/sysbio/syv033
.. _Rajan 2015: https://doi.org/10.1093/molbev/mss264
.. _alignment mask plugin: https://docs.qiime2.org/2019.7/plugins/available/alignment/mask/
.. _PyNAST: https://doi.org/10.1093/bioinformatics/btp636
.. _NAST: https://doi.org/10.1093/nar/gkl244
.. _Infernal: https://doi.org/10.1093/bioinformatics/btt509
.. _SINA: https://doi.org/10.1093/bioinformatics/bts252
.. _SILVA: https://www.arb-silva.de/
.. _SILVA community tutorial: https://forum.qiime2.org/t/q2-alignment-reference-based-alignment-using-sina/6220
.. _q2-fragment-insertion: https://github.com/biocore/q2-fragment-insertion
.. _Phylogeny for the faint of heart - a tutorial: http://doi.org/10.1016/S0168-9525(03)00112-4
.. _Molecular phylogenetics - principles and practice: http://dx.doi.org/10.1038/nrg3186
.. _Phylogenetics - An Introduction: https://www.ebi.ac.uk/training/online/course/introduction-phylogenetics
.. _q2-phylogeny: https://docs.qiime2.org/2019.7/plugins/available/phylogeny/
.. _FastTree: https://doi.org/10.1371/journal.pone.0009490
.. _RAxML: https://doi.org/10.1093/bioinformatics/btu033
.. _IQ-TREE: https://doi.org/10.1093/molbev/msu300
.. _align-to-tree-mafft-fasttree: https://docs.qiime2.org/2019.11/plugins/available/phylogeny/align-to-tree-mafft-fasttree/
.. _CAT-like: https://doi.org/10.1109/IPDPS.2006.1639535
.. _FastTree online manual: http://www.microbesonline.org/fasttree/
.. _iTOL: https://itol.embl.de/
.. _splits / bipartitions: https://en.wikipedia.org/wiki/Split_(phylogenetics)
.. _rapid bootstrap: http://dx.doi.org/10.1080/10635150802429642
.. _RAxML online documentation: https://sco.h-its.org/exelixis/web/software/raxml/hands_on.html
.. _Raxml manual: https://sco.h-its.org/exelixis/resource/download/NewManual.pdf
.. _not necessarily always better: https://groups.google.com/d/msg/raxml/v5k3usO_p38/_9A11D5_QAwJ
.. _CAT paper: https://doi.org/10.1109/IPDPS.2006.1639535
.. _10,000 or more taxa: https://doi.org/10.1186/1471-2105-12-470
.. _CAT-like model of FastTree2: https://doi.org/10.1371/journal.pone.0009490


