# 16S processing overview

In this document, we'll go over the basic steps involved in 16S data processing and analysis.
This tutorial is intended for experienced microbiome researchers who are looking for the **QIIME 2 commands pertaining to specific steps in 16S processing**, as well as for early-stage microbiome scientists who want a broad overview of the steps involved in 16S data processing.
This tutorial is similar to the [QIIME 2 tutorial doc](link to the new tutorial) (**TO DO**).

For an overview of the theoretical motivations for many of the steps involved in 16S processing, we recommend Scott Olesen's [16S primer](link to leanpub)  (**TO DO**).

## Overview

You can think of 16S data as taking a few distinct forms:

1. **Data straight off of the sequencer**. This data is usually converted to some formats like `.bam`, `.sff`, or `.fastq` by your sequencing center. We won't cover this here.     
1. **Raw data.** By raw data, we mean raw `.fastq` or `.fasta` files. These files contain sequences and (sometimes) quality scores, but nothing has been done to them yet.     
1. **Feature table and "taxa".** This form of data is the output of raw data processing, when your raw sequences have been turned into individual sequences of interest (e.g. OTUs, amplicon sequence variants (ASVs), sub-OTUs etc) and sometimes assigned taxonomy. By "feature table," we mean a file with samples, sequences (or OTUs, ASVs, etc), and observed counts for each sequence in each sample.        
1. **Analysis and insight.** After processing your data into a feature table, you can use QIIME 2 to perform some basic analysis and (hopefully) gain insights.    

In this overview, we'll discuss the potential steps involved in going from **raw data to feature tables** and some basic analyses to take you from **feature table to insights.**

## Raw data processing

The steps you take to process your raw data into a feature table depend on the type of raw data that you have and on you: there are many choices to make about processing methods! Briefly, the steps involved here are:

1. Figure out what form your raw data is in.     
1. Import data into qiime    
1. Map each sequence to the sample it came from (i.e. demultiplex)      
1. Remove non-biological parts of the sequences (i.e. remove primers)         
1. Perform quality control and:     
    - denoise sequences with DADA2 or deblur, and/or      
    - quality filter, length trim, and cluster with VSEARCH or dbOTU      
1. If you want, assign taxonomy      

Note that not every step has to be done in the order presented here.
For example, if you're using DADA2 to call ASVs, you shouldn't merge your paired-end reads before denoising.
But if you're using VSEARCH to cluster OTUs based on sequence similarities, you probably do want to merge your reads and trim them to the same lengths.
Also, removing primers and demultiplexing can be done in different orders than presented here.

*Pro-tip #1: QIIME 2 artifacts are simply zip files, so if at any point you want to look at what data files are in the `.qza` artifact, you can unzip your artifact directly (`unzip -k file.qza`) and look through the files in the `data/` folder. Alternatively, you can also use [`qiime tools export`](https://docs.qiime2.org/2018.6/tutorials/exporting/?highlight=extract#exporting-data) to extract the data file directly.*

*Pro-tip #2: the QIIME 2 command line interface tools are slow because they have to unzip and re-zip the data contained in the artifacts each time you call them. If you need to process your data more interactively, you might want to use the Python API - it is much faster since objects can be simply stored in memory.*


### Figure out what form your raw data is in

Before you start, you need to figure out what processing steps your data will need.
This means that you need to figure out what sort of data you have.

* Do you have FASTQ or FASTA data?      
* Are your sequences already de-multiplexed, with each file containing sequences belonging to only one sample, or will you need to assign sequences to samples via their barcodes (i.e. demultiplex)?       
* If you need to demultiplex your reads, where are the barcodes? In the sequences, in the header of sequences, or in a separate file?       
* Do you have unmerged paired-end reads (i.e. forward and reverse), or single-end reads?       
* Are the primers still in the sequences?        
* What length of reads do you have? Are they already all trimmed to a certain length? What length of reads do you expect (considering both the 16S region you amplified and the sequencing read length)?      

Every sequencing center provides a different kind of “raw data”, so the answers to these questions will vary across labs.
There are two ways to find the answers to these questions:

1. **Look at your data**. You can use command-line tools like `less` and `grep` or other programming languages like python to look at the data files, find barcodes and primers, and count the length of reads.       
2. **Ask your sequencing center**. If you've looked at your data and you're still not sure about some answers, you can ask whoever gave you the data - they should know what has been done to the data already.    

### Import data into qiime

If you're using qiime to process your data, the first thing you need to do is get that data into a format that qiime can understand.
Various importing methods currently available in qiime are highlighted [in the QIIME 2 importing tutorial](https://docs.qiime2.org/2018.6/tutorials/importing/).

A note that if you're importing data that you've generated, you'll likely need to generate a _manifest file_ (**TO DO**: link to a qiime doc page?) which maps each file to its sample ID.
Make sure to read the tutorial carefully, and don't get discouraged if you get stuck - this step is often the most tedious (and the QIIME developers agree!)
If you have questions, try searching the [QIIME 2 forum](https://forum.qiime2.org/) or posting your own question.

<Link to a tutorial. Bod: Hopefully I'll have a visualizer/wizard done soon that we can link to for now we can just cite the importing tutorial>

<Something about seeing all the available types of importable data>

### Demultiplex sequences

If you have reads from multiple samples in the same file, you'll need to demultiplex your sequences.

If your barcodes have already been removed from the reads and are in a separate file, you can use [q2-demux](https://docs.qiime2.org/2018.6/plugins/available/demux/) to demultiplex these.
<**TO DO**: q2-demux calls the underlying function/package XX to read barcodes from index file (or is it in-house code? just need a brief sentence here)>

If your barcodes are still in your sequences, you can use functions from the  [cutadapt plugin](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/).
The `cutadapt ` **XXXX function TO DO** looks for barcode sequences at the beginning of your reads (5' end) with a certain error tolerance, removes them, and returns sequence data separated by each sample.
The QIIME 2 forum has a [tutorial on various functions available in cutadapt](https://forum.qiime2.org/t/demultiplexing-and-trimming-adapters-from-reads-with-q2-cutadapt/2313), including demultiplexing.
You can learn more about how `cutadapt` works under the hood by reading their [documentation](https://cutadapt.readthedocs.io/en/stable/index.html).

<Think we might want to remove this code snippet, especially if nothing else gets code snippets...>

For single-end data, demultiplexing with cutadapt in QIIME 2 looks something like this:

```
$ qiime cutadapt demux-single \
  --i-seqs multiplexed-seqs.qza \
  --m-barcodes-file metadata.tsv \
  --m-barcodes-column Barcode \
  --p-error-rate 0 \
  --o-per-sample-sequences demultiplexed-seqs.qza \
  --o-untrimmed-sequences untrimmed.qza \
  --verbose
```

You don't necessarily need to do the demultiplexing step first in your data processing, but it helps to have each sample in a separate file for downstream steps which leverage this to parallelize their processing code.

<_The actual commands that qiime2 is calling can be found in the [source repo](https://github.com/qiime2/q2-cutadapt). As of June 2018, the main command is defined in the [`_build_demux_command()`](https://github.com/qiime2/q2-cutadapt/blob/master/q2_cutadapt/_demux.py#L36) in `_demux.py`._>

Note: Currently `q2 demux` and `q2-cutadapt` do not support demultiplexing dual-barcoded paired-end sequences, but only can demultiplex with barcodes in the forward reads. So for the time being for this type of demultiplexing needs to be done outside of qiime using other tools, for example [bcl2fastq](https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software.html).

<Maybe we can suggest an alternative tool for now outside of R, any thoughts?>
<Nope, have no thoughts on this - not sure I even know what this is lol XD>

### Merge reads

Whether or not you need to merge reads depends on how you plan to cluster or denoise your sequences into OTUs/ASVs.

#### Deciding to merge

If you'll be using DADA2 to call ASVs, you shouldn't merge your reads beforehand because DADA2 does it for you.
Instead, you'll need to ensure that your forward and reverse reads have at least 20 bp overlap after any quality filtering and trimming you do.
You may even want to leave for more to account for natural amplicon length variation.
Failure to do so will lead to failed or poor merging and loss of many reads.

With deblur you have to make a choice. Deblur only works on the forward reads, so feeding it unmerged paired-end data will produce the same results as if you were to only feed it the forward reads. If you want to use the full length of your paired-end reads you'll want to merge these prior to deblur using VSEARCH (see below).

If you'll be calling OTUs based on sequence similarity (e.g. 97% OTUs) or with distribution-based clustering, you probably want to merge your reads before clustering.
Merging forward and reverse reads increases the total length of each read, and thus the information that it contains.
However, if something went wrong with sequencing and merging throws out a lot of your data, you may want to proceed instead with the shorter (but more abundant) forward reads only.

#### Merging reads with VSEARCH

You can use the QIIME 2 [VSEARCH plugin](link to plugin) (**TO DO**: link to plugin) to merge paired-end reads with the  [join-pairs](https://docs.qiime2.org/2018.6/plugins/available/vsearch/join-pairs/) function.

### Remove non-biological sequences

Prior to clustering or denoising, it's very important to remove all nonbiological sequences in your reads.
These include barcodes, primers, sequencing adapters, PCR spacers etc.
Failure to remove these sequences will introduce clustering artifacts and make your results mostly useless.

The q2-cutadapt plugin has comprehensive functions for removing non-biological sequences from [paired-end](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-paired/) or [single-end](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-single/) data.  

DADA2 has a built-in `trim` option which allows you to trim a specified number of nucleotides off the 3' end. Deblur does not have this functionality yet.

(**TO DO**: link to the DADA2 trim function (in the plugin, I'm assuming?))

### Identifying and grouping similar sequences

There are two main types of ways to group similar reads together: denoising and clustering.
Denoising is the newer approach, and attempts to identify the exact sequences present in your dataset.
Denoising methods do this by probabilistically determining whether differences between sequences are a result of sequencing error or are truly reflective of biological differences.
These methods return exact sequence variants, sometimes called "amplicon sequence variants" (ASVs) or "sub-OTUs" (sOTUs).

Clustering groups "similar" sequences together, usually based on the genetic distance between sequences but in some cases incorporating additional information (e.g. distribution-based clustering).
Clustering methods return "operational taxonomic units" (OTUs).

If you want, you can first denoise your data and then pass your exact sequence variants through a clustering algorithm.

Regardless of how you group your sequences, the methods will output:

1. A list of representative sequences for each of your OTUs and/or sequence variants (qiime data format `FeatureData[Sequence]`), and     
1. a feature table which indicates how many reads of each OTU/sequence variants were observed in each sample. (qiime data format `FeatureTable[Frequency]`)     

#### Denoising

DADA2 and deblur are currently the two denoising methods available in QIIME 2.
Both learn an error model to then probabilistically determine whether variance between sequences is a result of sequencing error or is truly a biological variant.
DADA2 learns the error model based on a portion of your data, while deblur uses a pre-packaged model based on Illumina machines.
Because deblur uses a pre-packaged model, the error model estimation step is much faster than in DADA2, especially on larger datasets.

Both methods are completely parallelizable, as they process one sequence at a time. <question: are they completely parallelized in the qiime 2 code? If so, should change "parallelizable" to "parallelized")
These methods only work with fastq data, as they require quality scores to build error profiles from your data.

The creators of these denoising methods have different terminology for the resulting exact sequence variants; DADA2 creators call these "amplicon sequence variants" or "ASVs" while creators of deblur call theirs "sub-OTU"  or "sOTU". They both represent denoised sequence variants and under comparable parameters they produce very similar results.
For a benchmarked comparison between these methods, see the following [pre-print](https://peerj.com/preprints/26566/).

Denoising requires little data preparation.
Both DADA2 and deblur perform quality filtering, denoising, and chimera removal, so you shouldn't need to perform any quality screening prior to running them.
That said, the official qiime2 tutorial does recommend doing an initial [quality-filter](https://docs.qiime2.org/2018.6/tutorials/moving-pictures/#option-2-deblur) with default settings prior to using deblur.
In our experience, DADA2 performs better without this step.

Both methods have an option to truncate your reads to a constant length (**TO DO**: clarify - do they truncate reads prior to denoising, or after denoising?).
DADA2 can handle variable lengths but deblur needs all the reads to be of equal length (**TO DO**: clarify - does this mean the input data to deblur needs to already be pre-trimmed, or does it mean that the trim length parameter is required?).
An appropriate truncating value is important thus we strongly recommend using [summary quality plots](https://docs.qiime2.org/2018.6/plugins/available/demux/summarize/) to determine the appropriate parameters.

##### DADA2

The [denoise paired-end](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-paired/) function in DADA2 requires unmerged reads.
The [denoising single-end](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-single/) method accepts unmerged paired-end data, but will only use the forward reads.
(It also accepts single-end data.)

Note that DADA2 may be slow on very large datasets.
You can increase the number of threads to use with the `--p-n-threads` parameter.

<Something about the truncating length parameter, and/or any other parameters>

DADA2 can handle pyrosequencing and ion torrent data using the [denoise-pyro](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-pyro/) tool.

##### deblur

Deblur tends to be faster than DADA2, especially on larger datasets, but comes with other limitations.

It is faster than DADA2 because it uses a pre-packaged error model based on Illumina MiSeq and HiSeq machines instead of training one from scratch.
It also reduces processing time with an initial positive filtering step based on the GreenGenes database (**TO DO**: what does this mean? It only processes sequences that match to GG at a certain % identity??)


Because it uses the pre-packaged model, you can only use deblur to denoise Illumina data.
Deblur's [denoise-16S]((https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-16S/) method can also currently only denoise single-end reads.
It will accept unmerged paired-end reads as input, it just won't do anything with the reverse reads.
As discussed above, deblur can however take in merged reads and treat them as single-end reads.

If you don't want to do the default positive filtering to GreenGenes step, you can use a different positive filter with the [denoise-other](https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-other/) tool.

#### Clustering

##### Preparing your data

To cluster your sequences, you need to prepare your data.

Specifically, you need to make sure that:

- paired-end reads are merged
- non-biological sequences are removed
- reads are all trimmed to the same length
- low-quality reads are discarded

We discussed merging paired-end reads and removing non-biological sequences above.

###### Length trimming

Because many clustering algorithms rely on very basic measures of genetic distance, you want to ensure that all of your sequences are trimmed to the same length before clustering.
You can use the [method name](link) method from the [cutadapt](to do) plugin to trim reads to the same length. (**TO DO**: fill in method name and links.)

###### Quality filtering

You should also filter out low-quality sequences before clustering.
There are two ways to do this:

1. by truncating reads after the first time a certain low quality is encountered, or
2. by discarding whole sequences based on their expected number of errors (i.e. expected number bases called incorrectly).

Because sequencers generate more errors toward the end of reads, it is generally more advisable to discard merged reads based on the expected number of errors (since the "worst" reads will be in the middle), and to truncate single-end reads after a low quality (since the "worst" reads are at the end, and can get quite bad).

Note that which quality filtering method you choose informs when you should _length trim_ sequences.
If you discard reads based on expected errors, you should trim them *before* quality filtering.
If you truncate reads after a certain quality is encountered, you may want to trim them *after* quality filtering.

You can learn more about
these approaches two by reading the USEARCH documentation:
http://www.drive5.com/usearch/manual/readqualfiltering. (**TO DO**: maybe we should link to an equivalent page for the VSEARCH documentation...?)

Note that many of VSEARCH methods also automatically discard reads with ambiguous base calls (i.e. bases that are called as something other than A, T, C, or G).
(**TO DO**: is this true of the VSEARCH functions, do you know? I've only used USEARCH)

##### Clustering

There are many ways to cluster sequences, which fall into three main categories:

1. [de novo clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-de-novo/), in which sequences are grouped together based solely on the reads in the dataset itself. Can take a long time.     
1. [closed reference clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-closed-reference/), in which sequences are grouped together based on their matches to an external reference database. Takes much less time.     
1. [open reference clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-open-reference/), which first performs closed reference clustering and then de novo clustering on any reads which did not map to the reference. This method is ill-advised and will not be covered here. [link to edgar's scathing paper about qiime open reference](link)

###### de novo clustering

Sequences can be clustered *de novo* based on their genetic similarity alone (i.e. with VSEARCH) or based on a combination of their genetic similarity and abundance distributions (i.e. with distribution-based clustering).

- **Similarity-based clustering.** The QIIME 2 VSEARCH plugin method **XX** clusters OTUs. You can change the genetic similarity threshold with the **XXXX** parameter.     
- **Distribution-based clustering** incorporates the similarity between sequences and their abundance distribution to identify ecologically meaningful populations. You can learn more about this method in the documentation and paper [link to docs](dbotu.com). The call-otus function in the q2-dbotu plugin performs distribution-based clustering on input data. **TO DO**: fill in all these right details.

###### closed reference clustering

Closed reference clustering groups sequences together which match the same reference sequence in a database with a certain similarity.
Note that closed reference clustering may produce groupings that are not what you expect [link to scott's blog](link). (**TO DO** add links)

VSEARCH can do closed reference clustering.
You can decide which reference database to cluster against.
Most people use Green Genes or SILVA, but others curate their own databases or use other standard references (e.g. UNITE for ITS data).

**TO DO**: flesh this out. Include links to download the databases (unless they're built-in?)

### Assign taxonomy

If you clustered OTUs with closed-reference clustering, your OTUs will have the name of the reference sequence they matched to, and you don't need to do anything else to get taxonomy.
For all other *de novo* methods, you can assign taxonomy with different probabilistic classifiers.

In qiime2, two ways of assigning taxonomy are available and covered in the [taxonomy classification tutorial](https://docs.qiime2.org/2018.6/tutorials/overview/#taxonomy-classification-and-taxonomic-analyses).
The first way aligns reads to reference databases directly, and can be used with the [`classify-consensus-blast`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-blast/) or [`classify-consensus-vsearch`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-vsearch/) methods.
These two methods differ in the type of alignment method that they use (**TO DO**: is that correct?)
The second way uses trained machine learning classifiers to assign likely taxonomies to reads, and can be used through the  [`fit-classifier-sklearn`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-sklearn/) or [`fit-classifier-naive-bayes`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-naive-bayes/) functions.
These two functions differ in the type of machine learning model that they use (**TO DO**: is that correct?)

The machine learning-based methods require training a classifier for your data's 16S region and sequencing primers.
This training step is particularly computationally heavy, but in most cases you can simply download some pre-trained taxonomy classifiers [on the QIIME 2 data resources page](https://docs.qiime2.org/2018.6/data-resources/).
The [machine learning classifier overview tutorial](link) (**TO DO**: add link) covers how to train a classifier and classify sequences.

## Analyze feature table and gain insight

At this point, you should be ready to analyze your feature table to answer your scientific questions!
While the exact analyses you perform depend on your dataset, experimental design, and questions of interest, there are some basic analyses that many microbiome analyses have in common.

### Export the data

If you're a veteran microbiome scientist and don't want to use QIIME 2 for your analyses, you can extract your feature table and sequences from the artifact using the [export](https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-data) tool.
While `export` only outputs the data, the [extract](https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-versus-extracting) tool allows you to also extract other metadata such as the citations, provenance etc.

Note that this places generically named files (e.g. `feature-table.txt`) into the output directory, so you may want to immediately rename the files to something more information (or somehow ensure that they stay in their original directory)!

You can also use the handy [qiime2R](https://github.com/jbisanz/qiime2R) package to import qiime2 artifacts directly within R.

### Look at the data

The first thing you might want to do is simply to look at your data: what phyla are represented? Genera?

QIIME 2 provides easy ways to visualize your data using the [taxa barplot visualizers](https://docs.qiime2.org/2018.6/plugins/available/taxa/barplot/?highlight=barplots#barplot-visualize-taxonomy-with-an-interactive-bar-plot).

You can also export your data to Phinch for some beautiful and interactive visualizations (plugin coming soon!).

### Phylogenetic tree

Some downstream analyses need to know the phylogenetic relationships between your sequences.
You can build an unrooted phylogenetic tree using a variety of methods in the QIIME 2 phylogeny plugin:
- [fasttree](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/fasttree/)
- [raxml](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/raxml/)
- [raxml-rapid-bootstrap](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/raxml-rapid-bootstrap/)

With the same phylogeny plugin, cou can then [midpoint-root](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/midpoint-root/) your tree or [filter](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/filter-table/) your feature table based on a tree.

<@Bod - is there a visualizer for phylogenetic trees?? This would be awesome if there were! If there's not, we can recommend using ITOL or ... your favorite tool of choice? I've only ever done basic stuff and used ITOL just fine...>

### Alpha diversity

Alpha diversity tells you something about the diversity of the communities *within* each sample.
There are many ways to calculate alpha diversity, which are wonderfully explained in a [community contribution](https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282) on the QIIME 2 forum.
You can access them all through the `diversity` plugin, through the [qiime diversity alpha](https://docs.qiime2.org/2018.6/plugins/available/diversity/alpha/) and [alpha-phylogenetic](https://docs.qiime2.org/2018.6/plugins/available/diversity/alpha-phylogenetic/) groups of commands.
The `alpha-phylogenetic` methods require a phylogenetic tree.


### Beta diversity

Beta diversity tells you something about the diversity or difference of the communities *between* samples.
Again, there are many metrics to choose from in the `diversity` plugin, through the [qiime diversity beta](https://docs.qiime2.org/2018.6/plugins/available/diversity/beta/) and [beta-phylogenetic](https://docs.qiime2.org/2018.6/plugins/available/diversity/beta-phylogenetic/) groups of commands.

#### PCoA

Once you've calculated distances between all pairwise samples in your data, you can project your samples onto a PCoA plot using the [emperor](https://docs.qiime2.org/2018.6/plugins/available/emperor/plot/) plot tool which can also create [procrustes](https://docs.qiime2.org/2018.6/plugins/available/emperor/procrustes-plot/) plots.
Currently biplots and triplots are not supported in QIIME 2, so if you are interested in identifying important taxa and/or environmental variables in your plots, you'll need to do this outside of qiime for example with vegan package in R.
<@Bod - could you add a one-phrase description of what each of these things do? e.g. You can also make a procustes plot with the emperor tool, which tells you whether two distance matrices calculated from the same samples (e.g. between 16S or metabolomics data) are the same. [is that what those are? i can never remember]>

#### PERMANOVA/ANOSIM/etc

If you have multiple groups and want to know whether their communities as a whole are different from each other, you can use a statistical methods that calculate whether the distances between samples in different groups is different than the distance between samples in the same group.

In QIIME 2, there are currently two different methods to approach this: PERMANOVA and ANOSIM which are performed using the [beta-group-significance](https://docs.qiime2.org/2018.6/plugins/available/diversity/beta-group-significance/) plugin.
For a nice overview of these tests see: [PERMANOVA](https://mb3is.megx.net/gustame/hypothesis-tests/manova/npmanova) and [ANOSIM](https://mb3is.megx.net/gustame/hypothesis-tests/anosim).

### Differential abundance testing

If you are comparing two groups of samples, you can ask if any taxa in your data are differentially abundant in the two groups.
There are many ways to measure differential abundance.
You should understand what assumptions are being made by each method and ensure that your data meets these assumptions.

#### Analysis of Composition of Microbiomes (ANCOM)



The [ANCOM plugin](https://docs.qiime2.org/2018.6/plugins/available/composition/ancom/) is a very useful tool based on [this paper](https://www.ncbi.nlm.nih.gov/pubmed/26028277) for differential abundance testing which uses log-ratios of relative abundance data so does not require normalization or rarefaction and does not make distributional assumptions. According to this [benchmark paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5335496/) it also appears to be more sensitive than some other tests such as DESEQ2 and MetagenomeSeq and has better control of false discovery rate. ANCOM does make some assumptions which are detailed [here](http://mortonjt.blogspot.com/2016/06/ancom-explained.html). In brief, ANCOM assumes that few taxa are changing across groups as there is a drop in power if >25% of the taxa are changing across groups. ANCOM also does not perform well when there are large number of low abundance features or features that only occur across a few samples. It is therefore strongly recommended to remove low abundance features (i.e. less than 10) and those that are present in only a few samples (i.e occuring in less than 25-50% of samples). The qiime2 plugin currently does not support pairwise comparison if you have more than 2 groups but [ANCOM2](https://sites.google.com/site/siddharthamandal1985/research) (available as an R package) can handle linear model frameworks such as repeated measures, covariates, and longtiduinal analysis. ANCOM2 will likely make its way to Qiime2 in the future.

#### Gneiss

Gneiss builds on the method used by ANCOM by employing [balance trees](https://github.com/biocore/gneiss/blob/master/ipynb/balance_trees.ipynb) to infer properties of subcommunities, rather than individual species ([original paper](http://msystems.asm.org/content/2/1/e00162-16)). Gneiss shares many of the same assumptions and filtering recommendations as ANCOM. The q2-gneiss plugin allows for building of common linear regression models using balances as well as dealing with mixed effects models with covariates. The [gneiss tutorial](https://docs.qiime2.org/2018.6/tutorials/gneiss/) shows a nice example of performing differential abundance testing in microbial communities with pH as a gradient covariable.

<DESEQ2 and MetagenomeSeq are currently not supported in qiime2. I personally doubt the q2 developers with implemented these since ANCOM and gneiss appear to outperform these. Perhaps someone will develop a plugin for them later)>

### Normalization methods for unequal sampling depth

Currently only [rarefying](https://docs.qiime2.org/2018.6/plugins/available/feature-table/rarefy/) is supported in QIIME 2.
Other methods that were previously available in QIIME 1 such as cumulative sum scaling (CSS) or DESeq2 have not been implemented in QIIME 2 yet.
However, the existing methods of differential abundance testing in QIIME 2 do not require normalization, but low feature samples should still be removed prior to these tests as they introduce noise and weaken the integrity of the outcome. [Filtering samples](https://docs.qiime2.org/2018.6/plugins/available/feature-table/filter-samples/) with less than 1000 features is a good start though you'll want to make sure your choice matches the needs of your project.

**TO DO**: also add fitlering features for low read counts

#### Analyzing longitudinal data

Alpha and beta diversity measures can be analysed using either a paired or longitduinal approach using [q2-longitudinal](https://docs.qiime2.org/2018.6/plugins/available/longitudinal/) which utilizes linear mixed effect models or non-parametric microbial interdependence test (NMIT). See this [great tutorial](https://docs.qiime2.org/2018.6/tutorials/longitudinal/) for more details.


#### Machine learning classifiers

Machine learning can be used to build complex models that can predict a sample's metadata trait, identify features that are predictive of sample characteristics, and predict outliers. The [q-2sample-classifier](https://docs.qiime2.org/2018.6/plugins/available/sample-classifier/) has several actions for these classifiers. Also see this great [tutorial](https://docs.qiime2.org/2018.6/tutorials/sample-classifier/) for mroe details on machine learning in q2.
You should familiarize yourself with the underlying methods called by qiime - the scikit-learn user guide is a fantastic resource.
Also, make sure that you are using appropriate cross-validation or holdout data to prevent overfitting.


### And much much more!

You can explore qiime's ever-growing list of [plugins](https://docs.qiime2.org/2018.6/plugins/) to find other methods to apply to your data.
And remember that you're not limited to what qiime can do: you can export your data at any point and do more complicated or unique analyses on your own computer. 
