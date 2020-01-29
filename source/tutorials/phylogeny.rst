Phylogenetic inference with q2-phylogeny
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents:: Phylogenetic inference with q2-phylogeny
   :depth: 4

.. note:: This tutorial assumes, you've read through the :doc:`QIIME 2 Overview
   <overview>` documentation and have at least worked through some of the other
   :doc:`Tutorials <index>`.

Inferring phylogenies
=====================
Several downstream diversity metrics, available within QIIME 2, require that a
phylogenetic tree be constructed using the Operational Taxonomic Units
(`OTUs`_) or Exact Sequence Variants (`ESVs`_) being investigated.

*But how do we proceed to construct a phylogeny from our sequence data?*

Well, there are two phylogeny-based approaches we can use. Deciding upon which
to use is largely dependent on your study questions:

1. A reference-based `fragment insertion`_ approach. Which, is likely the
ideal choice. Especially, if your reference phylogeny (and associated
representative sequences) encompass neighboring relatives of which your
sequences can be reliably inserted. Any sequences that do not match well enough
to the reference are not inserted. For example, this approach may not work well
if your data contain sequences that are not well represented within your
reference phylogeny (e.g. missing clades, etc.). For more information, check
out these great `fragment insertion examples`_.

2. A *de novo* approach. Marker genes that can be globally aligned across
divergent taxa, are usually amenable to sequence alignment and phylogenetic
investigation through this approach. Be mindful of the length of your
sequences when constructing a *de novo* phylogeny, short reads many not have
enough phylogenetic information to capture a meaningful phylogeny. This
community tutorial will focus on the *de novo* approaches.

Here, you will learn how to make use of *de novo* phylogenetic approaches
to:

1. generate a sequence alignment within QIIME 2
2. mask the alignment if needed
3. construct a phylogenetic tree
4. root the phylogenetic tree

If you would like to substitute any of the steps outlined here by making use of
tools external to QIIME 2, please see the :doc:`import <importing>`,
:doc:`export <exporting>`, and :doc:`filtering <filtering>` documentation
where appropriate.

Sequence Alignment
------------------

Prior to constructing a `phylogeny`_ we must generate a multiple sequence
alignment (`MSA`_). When constructing a MSA we are making a statement about the
`putative homology`_ of the aligned residues (columns of the MSA) by virtue of
their `sequence similarity`_.

The number of algorithms to construct a MSA are legion. We will make use of
`MAFFT`_ (Multiple Alignment using Fast Fourier Transform)) via the
:doc:`q2-alignment <../plugins/available/alignment/index>` plugin. For more
information checkout the `MAFFT paper`_.

Let's start by creating a directory to work in:

.. command-block::

   mkdir qiime2-phylogeny-tutorial
   cd qiime2-phylogeny-tutorial

Next, download the data:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/phylogeny/rep-seqs.qza
   :saveas: rep-seqs.qza

**Run MAFFT**

.. command-block::

   qiime alignment mafft \
     --i-sequences rep-seqs.qza \
     --o-alignment aligned-rep-seqs.qza

Reducing alignment ambiguity: masking and reference alignments
--------------------------------------------------------------

*Why mask an alignment?*

Masking helps to eliminate alignment columns that are phylogenetically
uninformative or misleading before phylogenetic analysis. Much of the time
alignment errors can introduce noise and confound phylogenetic inference. It is
common practice to mask (remove) these ambiguously aligned regions prior to
performing phylogenetic inference. In particular, `David Lane's (1991)`_
chapter `16S/23S rRNA sequencing`_ proposed masking SSU data prior to
phylogenetic analysis. However, knowing how to deal with ambiguously aligned
regions and when to apply masks largely depends on the marker genes being
analyzed and the question being asked of the data.

.. note:: Keep in mind that this is still an active area of discussion, as
   highlighted by the following non-exhaustive list of articles: |Wu et al.
   2012|_, |Ashkenazy et al. 2018|_, `Schloss 2010`_, |Tan et al. 2015|_,
   `Rajan 2015`_.

*How to mask alignment.*

For our purposes, we'll assume that we have ambiguously aligned columns in the
MAFFT alignment we produced above. The default settings for the
``--p-min-conservation`` of the
:doc:`alignment mask <../plugins/available/alignment/mask/>` approximates the
Lane mask filtering of QIIME 1. Keep an eye out for updates to the alignment
plugin.

.. command-block::

   qiime alignment mask \
     --i-alignment aligned-rep-seqs.qza \
     --o-masked-alignment masked-aligned-rep-seqs.qza

*Reference based alignments*

There are a variety of tools such as `PyNAST`_) (using `NAST`_), `Infernal`_,
and `SINA`_, etc., that attempt to reduce the amount of ambiguously aligned
regions by using curated reference alignments (e.g. `SILVA`_. Reference
alignments are particularly powerful for rRNA gene sequence data, as knowledge
of secondary structure is incorporated into the curation process, thus
increasing alignment quality. For a more in-depth and eloquent overview of
reference-based alignment approaches, check out the great `SINA community
tutorial`_).

.. note:: Alignments constructed using reference based alignment approaches can
   be masked too, just like the above MAFFT example. Also, the reference
   alignment approach we are discussing here is distinct from the reference
   phylogeny approach (i.e.
   :doc:`q2-fragment-insertion <../plugins/available/fragment-insertion/index>`)
   we mentioned earlier. That is, we are not inserting our data into an
   existing tree, but simply trying to create a more robust alignment for
   making a better *de novo* phylogeny.

Construct a phylogeny
---------------------

As with MSA algorithms, phylogenetic inference tools are also legion.
Fortunately, there are many great resources to learn about phylogentics. Below
are just a few introductory resources to get you started:

1. `Phylogeny for the faint of heart - a tutorial`_
2. `Molecular phylogenetics - principles and practice`_
3. `Phylogenetics - An Introduction`_

There are several methods / pipelines available through the
:doc:`q2-phylogeny <../plugins/available/phylogeny/index>` plugin of :qiime2:.
These are based on the following tools:

1. `FastTree`_
2. `RAxML`_
3. `IQ-TREE`_

Methods
=======

fasttree
--------

FastTree is able to construct phylogenies from large sequence alignments quite
rapidly. It does this by using the using a `CAT-like`_ rate category
approximation, which is also available through RAxML (discussed below). Check
out the `FastTree online manual`_ for more information.

.. command-block::

   qiime phylogeny fasttree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --o-tree fasttree-tree.qza

.. tip:: For an easy and direct way to view your ``tree.qza`` files, upload
   them to `iTOL`_. Here, you can interactively view and manipulate your
   phylogeny. Even better, while viewing the tree topology in "Normal mode",
   you can drag and drop your associated ``alignment.qza`` (the one you used to
   build the phylogeny) or a relevent ``taxonomy.qza`` file onto the iTOL tree
   visualization. This will allow you to directly view the sequence alignment
   or taxonomy alongside the phylogeny. 🕶️

raxml
-----

Like ``fasttree``, ``raxml`` will perform a single phylogentic inference and
return a tree. Note, the default model for ``raxml`` is
``--p-substitution-model GTRGAMMA``. If you'd like to construct a tree using
the CAT model like ``fasttree``, simply replace ``GTRGAMMA`` with ``GTRCAT`` as
shown below:

.. command-block::
   :stdout:

   qiime phylogeny raxml \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-substitution-model GTRCAT \
     --o-tree raxml-cat-tree.qza \
     --verbose

Perform multiple searches using raxml
.....................................

If you'd like to perform a more thorough search of "tree space" you can
instruct ``raxml`` to perform multiple independent searches on the full
alignment by using ``--p-n-searches 5``. Once these 5 independent searches are
completed, only the single best scoring tree will be returned. *Note, we are
not bootstrapping here, we'll do that in a later example.* Let's set
``--p-substitution-model GTRCAT``. Finally, let's also manually set a seed via
``--p-seed``. By setting our seed, we allow other users the ability to
reproduce our phylogeny. That is, anyone using the same sequence alignment and
substitution model, will generate the same tree as long as they set the same
seed value. Although, ``--p-seed`` is not a required argument, it is generally
a good idea to set this value.

.. command-block::
   :stdout:

   qiime phylogeny raxml \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-substitution-model GTRCAT \
     --p-seed 1723 \
     --p-n-searches 5 \
     --o-tree raxml-cat-searches-tree.qza \
     --verbose

raxml-rapid-bootstrap
---------------------

In phylogenetics, it is good practice to check how well the `splits /
bipartitions`_ in your phylogeny are supported. Often one is interested in
which clades are robustly separated from other clades in the phylogeny. One
way, of doing this is via bootstrapping (See the *Bootstrapping* section of the
first introductory link above). In QIIME 2, we've provided access to the RAxML
`rapid bootstrap`_ feature. The only difference between this command and the
previous are the additional flags ``--p-bootstrap-replicates`` and
``--p-rapid-bootstrap-seed``. It is quite common to perform anywhere from 100 -
1000 bootstrap replicates. The ``--p-rapid-bootstrap-seed`` works very much
like the ``--p-seed`` argument from above except that it allows anyone to
reproduce the bootstrapping process and the associated supports for your
splits.

As per the `RAxML online documentation`_ and the `RAxML manual`_, the rapid
bootstrapping command that we will execute below will do the following:

1. Bootstrap the input alignment 100 times and perform a Maximum Likelihood
   (ML) search on each.
2. Find best scoring ML tree through multiple independent searches using the
   original input alignment. The number of independent searches is determined
   by the number of bootstrap replicates set in the 1st step. That is, your
   search becomes more thorough with increasing bootstrap replicates. The ML
   optimization of RAxML uses every 5th bootstrap tree as the starting tree for
   an ML search on the original alignment.
3. Map the bipartitions (bootstrap supports, 1st step) onto the best scoring ML
   tree (2nd step).

.. command-block::
   :stdout:

   qiime phylogeny raxml-rapid-bootstrap \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-seed 1723 \
     --p-rapid-bootstrap-seed 9384 \
     --p-bootstrap-replicates 100 \
     --p-substitution-model GTRCAT \
     --o-tree raxml-cat-bootstrap-tree.qza \
     --verbose


.. tip:: **Optimizing RAxML Run Time.**
   You may gave noticed that we haven't added the flag ``--p-raxml-version`` to
   the RAxML methods. This parameter provides a means to access versions of
   RAxML that have optimized vector instructions for various modern x86
   processor architectures. Paraphrased from the RAxML manual and help
   documentation: Firstly, most recent processors will support SSE3 vector
   instructions (i.e. will likely support the faster AVX2 vector instructions).
   Secondly, these instructions will substantially accelerate the likelihood
   and parsimony computations. In general, SSE3 versions will run approximately
   40% faster than the standard version. The AVX2 version will run 10-30%
   faster than the SSE3 version. Additionally, keep in mind that using more
   cores / threads will not necessarily decrease run time. The RAxML manual
   suggests using 1 core per ~500 DNA alignment patterns. Alignment pattern
   information is usually visible on screen, when the ``--verbose`` option is
   used. Additionally, try using a rate category (CAT model; via
   ``--p-substitution-model``), which results in equally good trees as the
   GAMMA models and is approximately 4 times faster. See the `CAT paper`_. The
   CAT approximation is also Ideal for alignments containing `10,000 or more
   taxa`_, and is very much similar the `CAT-like model of FastTree2`_.

iqtree
------

Similar to the ``raxml`` and ``raxml-rapid-bootstrap`` methods above, we
provide similar functionality for `IQ-TREE`_: ``iqtree`` and
``iqtree-ultrafast-bootstrap``. IQ-TREE is unique compared to the ``fastree``
and ``raxml`` options, in that it provides access to 286 `models of nucleotide
substitution`_! IQ-TREE can also determine which of these models best fits your
dataset prior to constructing your tree via its built-in `ModelFinder`_
algorithm. This is the default in QIIME 2, but do not worry, you can set any
one of the 286 models of nucleotide substitution via the
``--p-substitution-model`` flag, e.g. you can set the model as ``HKY+I+G``
instead of the default ``MFP`` (a basic short-hand for: "build a phylogeny
after determining the best fit model as determined by ModelFinder"). Keep in
mind the additional computational time required for model testing via
ModelFinder.

The simplest way to run the
:doc:`iqtree command <../plugins/available/phylogeny/iqtree/>` with default
settings and automatic model selection (``MFP``) is like so:

.. command-block::
   :stdout:

   qiime phylogeny iqtree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --o-tree iqt-tree.qza \
     --verbose

Specifying a substitution model
...............................

We can also set a substitution model of our choosing. You may have noticed
while watching the onscreen output of the previous command that the best
fitting model selected by ModelFinder is noted. For the sake of argument, let's
say the best selected model was shown as ``GTR+F+I+G4``. The ``F`` is only a
notation to let us know that *if* a given model supports *unequal base
frequencies*, then the *empirical base frequencies* will be used by default.
Using empirical base frequencies (``F``), rather than estimating them, greatly
reduces computational time. The ``iqtree`` plugin will not accept ``F`` within
the model notation supplied at the command line, as this will always be implied
automatically for the appropriate model. Also, the ``iqtree`` plugin only
accepts ``G`` *not* ``G4`` to be specified within the model notation. The ``4``
is simply another explicit notation to remind us that four rate categories are
being assumed by default. The notation approach used by the plugin simply helps
to retain simplicity and familiarity when supplying model notations on the
command line. So, in brief, we only have to type ``GTR+I+G`` as our input
model:

.. command-block::
   :stdout:

   qiime phylogeny iqtree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-substitution-model 'GTR+I+G' \
     --o-tree iqt-gtrig-tree.qza \
     --verbose

Let's rerun the command above and add the ``--p-fast`` option. This option,
only compatible with the ``iqtree`` method, resembles the fast search performed
by ``fasttree``. 🏎️ Secondly, let's also perform multiple tree searches and
keep the best of those trees (as we did earlier with the
``raxml --p-n-searches ...`` command):

.. command-block::
   :stdout:

   qiime phylogeny iqtree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-substitution-model 'GTR+I+G' \
     --p-fast \
     --p-n-runs 10 \
     --o-tree iqt-gtrig-fast-ms-tree.qza \
     --verbose

Single branch tests
...................

IQ-TREE provides access to a few `single branch testing methods`_

1. `SH-aLRT`_ via ``--p-alrt [INT >= 1000]``
2. `aBayes`_ via ``--p-abayes [TRUE | FALSE]``
3. `local bootstrap test`_ via ``--p-lbp [INT >= 1000]``

Single branch tests are commonly used as an alternative to the bootstrapping
approach we've discussed above, as they are substantially faster and `often
recommended`_ when constructing large phylogenies (e.g. >10,000 taxa). All
three of these methods can be applied simultaneously and viewed within `iTOL`_
as separate bootstrap support values. These values are always in listed in the
following order of *alrt / lbp / abayes*. We'll go ahead and apply all of the
branch tests in our next command, while specifying the same substitution model
as above. Feel free to combine this with the ``--p-fast`` option. 😉

.. command-block::
   :stdout:

   qiime phylogeny iqtree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-alrt 1000 \
     --p-abayes \
     --p-lbp 1000 \
     --p-substitution-model 'GTR+I+G' \
     --o-tree iqt-sbt-tree.qza \
     --verbose

.. tip:: **IQ-TREE search settings**.
   There are quite a few adjustable parameters available for ``iqtree`` that
   can be modified improve searches through "tree space" and prevent the search
   algorithms from getting stuck in local optima. One particular `best
   practice`_ to aid in this regard, is to adjust the following parameters:
   ``--p-perturb-nni-strength`` and ``--p-stop-iter`` (each respectively maps
   to the ``-pers`` and ``-nstop`` flags of ``iqtree`` ). In brief, the larger
   the value for NNI (nearest-neighbor interchange) perturbation, the larger
   the jumps in "tree space". This value should be set high enough to allow the
   search algorithm to avoid being trapped in local optima, but not to high
   that the search is haphazardly jumping around "tree space". That is, like
   Goldilocks and the three 🐻s you need to find a setting that is "just
   right", or at least within a set of reasonable bounds. One way of assessing
   this, is to do a few short trial runs using the ``--verbose`` flag. If you
   see that the likelihood values are jumping around to much, then lowering the
   value for ``--p-perturb-nni-strength`` may be warranted. As for the stopping
   criteria, i.e. ``--p-stop-iter``, the higher this value, the more thorough
   your search in "tree space". Be aware, increasing this value may also
   increase the run time. That is, the search will continue until it has
   sampled a number of trees, say 100 (default), without finding a better
   scoring tree. If a better tree is found, then the counter resets, and the
   search continues. These two parameters deserve special consideration when a
   given data set contains many short sequences, quite common for microbiome
   survey data. We can modify our original command to include these extra
   parameters with the recommended modifications for short sequences, i.e. a
   lower value for perturbation strength (shorter reads do not contain as much
   phylogenetic information, thus we should limit how far we jump around in
   "tree space") and a larger number of stop iterations. See the `IQ-TREE
   command reference`_ for more details about default parameter settings.
   Finally, we'll let ``iqtree`` perform the model testing, and automatically
   determine the optimal number of CPU cores to use.

.. command-block::
   :stdout:

   qiime phylogeny iqtree \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-perturb-nni-strength 0.2 \
     --p-stop-iter 200 \
     --p-n-cores 1 \
     --o-tree iqt-nnisi-fast-tree.qza \
     --verbose

iqtree-ultrafast-bootstrap
--------------------------

As per our discussion in the ``raxml-rapid-bootstrap`` section above, we can
also use IQ-TREE to evaluate how well our splits / bipartitions are supported
within our phylogeny via the `ultrafast bootstrap algorithm`_. Below, we'll
apply the plugin's
:doc:`ultrafast bootstrap command <../plugins/available/phylogeny/iqtree-ultrafast-bootstrap/>`:
automatic model selection (``MFP``), perform ``1000`` bootstrap replicates
(minimum required), set the same generally suggested parameters for
constructing a phylogeny from short sequences, and automatically determine the
optimal number of CPU cores to use:

.. command-block::
   :stdout:

   qiime phylogeny iqtree-ultrafast-bootstrap \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-perturb-nni-strength 0.2 \
     --p-stop-iter 200 \
     --p-n-cores 1 \
     --o-tree iqt-nnisi-bootstrap-tree.qza \
     --verbose

Perform single branch tests alongside ufboot
............................................

We can also apply single branch test methods concurrently with ultrafast
bootstrapping. The support values will always be represented in the following
order: *alrt / lbp / abayes / ufboot*. Again, these values can be seen as
separately listed bootstrap values in `iTOL`_. We'll also specify a model as we
did earlier.

.. command-block::
   :stdout:

   qiime phylogeny iqtree-ultrafast-bootstrap \
     --i-alignment masked-aligned-rep-seqs.qza \
     --p-perturb-nni-strength 0.2 \
     --p-stop-iter 200 \
     --p-n-cores 1 \
     --p-alrt 1000 \
     --p-abayes \
     --p-lbp 1000 \
     --p-substitution-model 'GTR+I+G' \
     --o-tree iqt-nnisi-bootstrap-sbt-gtrig-tree.qza \
     --verbose

.. tip:: If there is a need to reduce the impact of `potential model
   violations`_ that occur during a `UFBoot search`_, and / or would simply
   like to be more rigorous, we can add the ``--p-bnni`` option to any of the
   ``iqtree-ultrafast-bootstrap`` commands above.

Root the phylogeny
------------------

In order to make proper use of diversity metrics such as UniFrac, the phylogeny
must be `rooted`_. Typically an `outgroup`_ is chosen when rooting a tree. In
general, phylogenetic inference tools using Maximum Likelihood often return an
unrooted tree by default.

QIIME 2 provides a way to
:doc:`mid-point root <../plugins/available/phylogeny/midpoint-root/>` our
phylogeny. Other rooting options may be available in the future. For now, we'll
root our bootstrap tree from ``iqtree-ultrafast-bootstrap`` like so:

.. command-block::

   qiime phylogeny midpoint-root \
     --i-tree iqt-nnisi-bootstrap-sbt-gtrig-tree.qza \
     --o-rooted-tree iqt-nnisi-bootstrap-sbt-gtrig-tree-rooted.qza

.. tip:: **iTOL viewing Reminder**. We can view our tree and its associated
   alignment via `iTOL`_. All you need to do is upload the
   `iqt-nnisi-bootstrap-sbt-gtrig-tree-rooted.qza` tree file. Display the tree
   in `Normal` mode. Then drag and drop the `masked-aligned-rep-seqs.qza` file
   onto the visualization. Now you can view the phylogeny alongside the
   alignment.

Pipelines
=========

Here we will outline the use of the phylogeny pipeline
:doc:`align-to-tree-mafft-fasttree <../plugins/available/phylogeny/align-to-tree-mafft-fasttree/>`

One advantage of pipelines is that they combine ordered sets of commonly used
commands, into one condensed simple command. To keep these "convenience"
pipelines easy to use, it is quite common to only expose a few options to the
user. That is, most of the commands executed via pipelines are often configured
to use default option settings. However, options that are deemed important
enough for the user to consider setting, are made available. The options
exposed via a given pipeline will largely depend upon what it is doing.
Pipelines are also a great way for new users to get started, as it helps to lay
a foundation of good practices in setting up standard operating procedures.

Rather than run one or more of the following QIIME 2 commands listed below:

1. ``qiime alignment mafft ...``
2. ``qiime alignment mask ...``
3. ``qiime phylogeny fasttree ...``
4. ``qiime phylogeny midpoint-root ...``

We can make use of the pipeline
:doc:`align-to-tree-mafft-fasttree <../plugins/available/phylogeny/align-to-tree-mafft-fasttree>`
to automate the above four steps in one go. Here is the description taken from
the pipeline help doc:

 This pipeline will start by creating a sequence alignment using MAFFT,
 after which any alignment columns that are phylogenetically uninformative
 or ambiguously aligned will be removed (masked). The resulting masked
 alignment will be used to infer a phylogenetic tree and then subsequently
 rooted at its midpoint. Output files from each step of the pipeline will be
 saved. This includes both the unmasked and masked MAFFT alignment from
 q2-alignment methods, and both the rooted and unrooted phylogenies from
 q2-phylogeny methods.

This can all be accomplished by simply running the following:

.. command-block::

   qiime phylogeny align-to-tree-mafft-fasttree \
     --i-sequences rep-seqs.qza \
     --output-dir mafft-fasttree-output

**Congratulations! You now know how to construct a phylogeny in QIIME 2!**

.. _OTUs: https://en.wikipedia.org/wiki/Operational_taxonomic_unit
.. _ESVs: https://doi.org/10.1038/ismej.2019.119
.. _fragment insertion: https://doi.org/10.1128/mSystems.00021-18
.. _fragment insertion examples: https://library.qiime2.org/plugins/q2-fragment-insertion/16/
.. _phylogeny: https://simple.wikipedia.org/wiki/Phylogeny
.. _MSA: https://en.wikipedia.org/wiki/Multiple_sequence_alignment
.. _putative homology: http://doi.org/10.1006/mpev.2000.0785
.. _sequence similarity: http://doi.org/10.1002/0471250953.bi0301s42
.. _MAFFT: https://en.wikipedia.org/wiki/MAFFT
.. _MAFFT paper: http://doi.org/10.1093/molbev/mst010
.. _David Lane's (1991): http://www.worldcat.org/title/nucleic-acid-techniques-in-bacterial-systematics/oclc/22310197
.. _16S/23S rRNA sequencing: http://catdir.loc.gov/catdir/toc/onix05/90012998.html
.. |Wu et al. 2012| replace:: Wu *et al*. 2012
.. _Wu et al. 2012: https://doi.org/10.1371/journal.pone.0030288
.. |Ashkenazy et al. 2018| replace:: Ashkenazy *et al*. 2018
.. _Ashkenazy et al. 2018: https://doi.org/10.1093/sysbio/syy036
.. _Schloss 2010: https://doi.org/10.1371/journal.pcbi.1000844
.. |Tan et al. 2015| replace:: Tan *et al*. 2015
.. _Tan et al. 2015: https://doi.org/10.1093/sysbio/syv033
.. _Rajan 2015: https://doi.org/10.1093/molbev/mss264
.. _PyNAST: https://doi.org/10.1093/bioinformatics/btp636
.. _NAST: https://doi.org/10.1093/nar/gkl244
.. _Infernal: https://doi.org/10.1093/bioinformatics/btt509
.. _SINA: https://doi.org/10.1093/bioinformatics/bts252
.. _SILVA: https://www.arb-silva.de/
.. _SINA community tutorial: https://forum.qiime2.org/t/q2-alignment-reference-based-alignment-using-sina/6220
.. _Phylogeny for the faint of heart - a tutorial: http://doi.org/10.1016/S0168-9525(03)00112-4
.. _Molecular phylogenetics - principles and practice: http://dx.doi.org/10.1038/nrg3186
.. _Phylogenetics - An Introduction: https://www.ebi.ac.uk/training/online/course/introduction-phylogenetics
.. _FastTree: https://doi.org/10.1371/journal.pone.0009490
.. _RAxML: https://doi.org/10.1093/bioinformatics/btu033
.. _IQ-TREE: https://doi.org/10.1093/molbev/msu300
.. _CAT-like: https://doi.org/10.1109/IPDPS.2006.1639535
.. _FastTree online manual: http://www.microbesonline.org/fasttree/
.. _iTOL: https://itol.embl.de/
.. _splits / bipartitions: https://en.wikipedia.org/wiki/Split_(phylogenetics)
.. _rapid bootstrap: http://dx.doi.org/10.1080/10635150802429642
.. _RAxML online documentation: https://sco.h-its.org/exelixis/web/software/raxml/hands_on.html
.. _Raxml manual: https://sco.h-its.org/exelixis/resource/download/NewManual.pdf
.. _CAT paper: https://doi.org/10.1109/IPDPS.2006.1639535
.. _10,000 or more taxa: https://doi.org/10.1186/1471-2105-12-470
.. _CAT-like model of FastTree2: https://doi.org/10.1371/journal.pone.0009490
.. _models of nucleotide substitution : https://doi.org/10.1016/j.dci.2004.07.007
.. _ModelFinder: https://doi.org/10.1038/nmeth.4285
.. _single branch testing methods: http://www.iqtree.org/doc/Tutorial#assessing-branch-supports-with-single-branch-tests
.. _SH-aLRT: https://doi.org/10.1093/sysbio/syq010
.. _aBayes: https://doi.org/10.1093/sysbio/syr041
.. _local bootstrap test: https://doi.org/10.1007/BF0249864
.. _often recommended: http://www.iqtree.org/doc/Command-Reference#single-branch-tests
.. _best practice: https://groups.google.com/forum/#!searchin/iqtree/iterations|sort:date/iqtree/0mwGhDokNns/vlBryIwXHAAJ
.. _IQ-TREE command reference: http://www.iqtree.org/doc/Command-Reference
.. _ultrafast bootstrap algorithm: https://doi.org/10.1093/molbev/msx281
.. _potential model violations: http://www.iqtree.org/doc/Tutorial#reducing-impact-of-severe-model-violations-with-ufboot
.. _UFBoot search: https://doi.org/10.1093/molbev/msx281
.. _rooted: https://www.ebi.ac.uk/training/online/course/introduction-phylogenetics/what-phylogeny/aspects-phylogenies/nodes/root
.. _outgroup: http://phylobotanist.blogspot.com/2015/01/how-to-root-phylogenetic-tree-outgroup.html
