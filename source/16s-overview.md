# 16S processing overview

In this document, we'll go over the basic steps involved in 16S data processing and analysis.
This tutorial is intended for experienced microbiome researchers who are looking for the **QIIME 2 commands pertaining to specific steps in 16S processing**, as well as for early-stage microbiome scientists who want a broad overview of the steps involved in 16S data processing.

For an overview of the theoreticaly motivations for many of the steps involve, we recommend Scott Olesen's [16S primer](link to leanpub).

## Overview

You can think of 16S data as taking a few distinct forms:

1. **Data straight off of the sequencer**. This data is usually converted to some formats like `.bam`, `.sff`, or `.fastq` by your sequencing center. We won't cover this here.     
1. **Raw data.** By raw data, we mean raw `.fastq` or `.fasta` files. These files contain sequences and (sometimes) quality scores, but nothing has been done to them yet.     
1. **Feature table and "taxa".** This form of data is the output of raw data processing, when your raw sequences have been turned into individual sequences of interest (e.g. OTUs, amplicon sequence variants (ASV), sOTUs etc) and sometimes assigned taxonomy. By "feature table," we mean a file with samples, sequences, and observed counts for each sequence in each sample.       
1. **Analysis and insight.** After processing your data into a feature table, you can use QIIME 2 to perform some basic analysis and (hopefully) gain insights.    

In this overview, we'll discuss the potential steps involved in going from **raw data to feature tables** and some basic analyses to take you from **feature table to insights.**

## Raw data processing

The steps you take to process your raw data into a feature table depend on the form of the raw data that you have and on the choices you make about processing methods. Briefly, the steps involved here are:

1. Figure out what form your raw data is in.     
1. Import data into qiime    
1. Map sequences to samples (i.e. demultiplex)      
1. Remove non-biological parts of the sequences (i.e. remove primers)         
1. Perform quality control and denoise and/or cluster sequences     
    - Denoise sequences with DADA2 or deblur, and/or      
    - Quality filter, length trim, and cluster with VSEARCH or dbOTU      
1. If you want, assign taxonomy      

Note that not every step has to be done in the order presented here.
For example, if you're using DADA2 to call ASV, you shouldn't merge your paired-end reads before denoising.
Also, removing primers and demultiplexing can be done in different orders.
<though these should be removed prior to DADA2...>

*Pro-tip: qiime artifacts are simply zip files, so if at any point you want to look at what data files are in the `.qza` artifact, you can unzip your artifact directly (`unzip -k file.qza`) and look through the files in the `data/` folder. Alternatively, you can also use [qiime tools export](https://docs.qiime2.org/2018.6/tutorials/exporting/?highlight=extract#exporting-data) to extract the data file directly.*


### Figure out what form your raw data is in

Before you start, you need to figure out what processing steps your data will need.
This means that you need to figure out what sort of data you have.

* Do you have FASTQ or FASTA data?      
* Are your sequences already de-multiplexed with one file per sample, or will you need to split sequences by barcodes (i.e. demultiplex)?       
* If you need to demultiplex your reads, where are the barcodes? In the sequences, in the header of sequences, or in a separate file?       
* Do you have unmerged paired-end reads (i.e. forward and reverse)?       
* Are the primers still in the sequences?        
* What length of reads do you have? Are they already all trimmed to a certain length?       

Every sequencing center provides a different kind of “raw data”, so the answers to these questions will vary across experiments.
There are two ways to find the answers to these questions:

1. **Look at your data**. You can use command-line tools like `less` and `grep` or other programming languages like python to look at the data files, find barcodes and primers, and count the length of reads.       
2. **Ask your sequencing center**. If you've looked at your data and you're still not sure about some answers, you can ask whoever gave you the data - they should know what has been done to the data already.    

### Import data into qiime

If you're using qiime to process your data, the first thing you need to do is get that data into a format that qiime can understand.
Various importing methods currently available in qiime are highlighted [here](https://docs.qiime2.org/2018.6/tutorials/importing/).

<Link to a tutorial. Bod: Hopefully I'll have a visualizer/wizard done soon that we can link to for now we can just cite the importing tutorial>

<Something about seeing all the available types of importable data>

### Demultiplex sequences

If the reads for all of your samples are in the same file, you'll need to demultiplex your sequences.
If your barcodes have already been removed from the reads and are in a separate file, you can use [q2-demux](https://docs.qiime2.org/2018.6/plugins/available/demux/) to demultiplex these.
The [cutadapt plugin](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/) on the other hand provides functions to demultiplex sequence data with barcodes still in the sequences.
It looks for barcode sequences at the beginning of your reads (5' end) with a certain error tolerance, removes them, and returns sequence data separated by each sample.

The QIIME 2 forum has a tutorial on various functions available in cutadapt, including demultiplexing: https://forum.qiime2.org/t/demultiplexing-and-trimming-adapters-from-reads-with-q2-cutadapt/2313


You can learn more about how `cutadapt` works by reading their [documentation](https://cutadapt.readthedocs.io/en/stable/index.html).

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

You don't necessarily need to do the demultiplexing step first, but it helps to have each sample in a separate file for downstream steps which leverage this to parallelize their processing code.

_The actual commands that qiime2 is calling can be found in the [source repo](https://github.com/qiime2/q2-cutadapt). As of June 2018, the main command is defined in the [`_build_demux_command()`](https://github.com/qiime2/q2-cutadapt/blob/master/q2_cutadapt/_demux.py#L36) in `_demux.py`._

Note: Currently `q2 demux` and `q2-cutadapt` do not support demultiplexing dual-barcoded paired-end sequences, but only can demultiplex with barcodes in the forward reads.
<Maybe we can suggest an alternative tool for now outside of R, any thoughts?> 
### Merge reads
If you're using DADA2, you shouldn't merge your reads beforehand as the script does this for you. Instead you need to ensure that your truncating parameters allow for a minimum of 20 nt overlap. You may even want to leave for more to account for natural amplicon length variation. Failure to do so will lead to failed or poor merging and loss of many reads. 

With deblur you have to make a choice. Deblur only works on the forward reads, so feeding it unmerged paired-end data will produce the same results as if you were to only feed it the forward reads. If you want to use the full length of your paired-end reads you'll want to merge these prior to deblur using VSEARCH (see below).

Tip: Very important that prior to DADA2 and deblur your barcodes and primers/adaptors are removed.
#### VSEARCH

Prior to deblur or OTU picking you can use VSEARCH's [join-pairs](https://docs.qiime2.org/2018.6/plugins/available/vsearch/join-pairs/) to merge paired-end reads. 

### Remove non-biological sequences

Prior to clustering or denoising, it's very important to remove all nonbiological sequences such as your barcodes, primers, adapters, spacers etc. Failure to do will render the results useless. 

DADA2 has a built-in 'trim' option which allows you to trim a specified amount of nt off the 3' end. Deblur doesn't have this functionality yet. The q2 cutadapt plugin for [paired-end](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-paired/) or [single-end](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-single/) have much more comprehensive options for removing non-biological sequences.  


### Quality control and denoise/cluster

There are two main types of ways to group similar reads together: denoising and clustering.
Denoising is the newer approach, and attempts to identify the exact sequences present in your dataset.
DADA2 does this by learning an error model based on a portion of your data while deblur usesa a pre-packaged model based on Illumina machines which makes this step much faster, especially on larger datasets. Both methods probabilistically determine whether variance between sequences is a result of sequencing error or is truly a biological variant. Both methods are completely parallelizable as they denoise one sequence at a time. These methods only work with fastq data, as they require quality scores to build error profiles from your data.
The creators of these denoising methods have different terminology for the resuling exact sequence variants; DADA2 creators call these "amplicon sequence variants" or "ASVs" while creators of deblur call theirs "sub-OTU"  or "sOTU". They both represent denoised sequence variants and under comparable parameters they produce very similar results. For a benchmarked comparison between these methods, see the following [pre-print](https://peerj.com/preprints/26566/). 

Clustering is a way to group "similar" sequences together, usually based on the genetic distance between sequences but in some cases incorporating additional information (e.g. distribution-based clustering).
Clustering methods return "operational taxonomic units," or "OTUs".
If you want, you can first denoise your data and then pass your exact sequence variants through a clustering algorithm.

All of these methods will output:

1. A list of representative sequences for each of your OTUs and/or sequence variants (qiime data format `FeatureData[Sequence]`), and     
1. a feature table which indicates how many reads of each OTU/sequence variants were observed in each sample. (qiime data format `FeatureTable[Frequency]`)     

#### Denoising

Denoising requires little data preparation.
There are two main methods to perform denoising: DADA2 and deblur.
Both these methods performs quality filtering, denoising, and chimera removal and so you shouldn't perform any quality screening prior. That being said the official qiime2 tutorial does recommend doing an initial [quality-filter](https://docs.qiime2.org/2018.6/tutorials/moving-pictures/#option-2-deblur) with default settings prior to using deblur. Dada2 performs better without this step.
Both methods have an option to truncate your reads to a constant length. Dada2 can handle variable lengths but deblur does need all the reads to be of equal length. An appropriate truncating value is important thus we strongly recommend using [summary quality plots](https://docs.qiime2.org/2018.6/plugins/available/demux/summarize/) to determine the appropriate parameters.

##### DADA2

To [denoise paired-end](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-paired/) data with DADA2, you should pass in unmerged reads. For [denoising single-end](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-single/) method you can still use paired-end data, but only the forward reads will be used.
Note that DADA2 may be slow on very large datasets but with the `--p-n-threads` parameters you can increase number of threads to use.
DADA2 can also handle pyrosequencing and ion torrent data using the [denoise-pyro](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-pyro/) tool. 

##### deblur

Deblur's [denoise-16S]((https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-16S/)) tool is designed to only denoise single-end reads (even though it can take unmerged reads as input - it just won't do anything with the reverse reads). It can however take in merged data and treat them as single-ends reads.
Deblur is faster for larger datasets because it uses a pre-packaged error model based on Illumina MiSeq and HiSeq machines instead of training one from scratch. That also means that only Illumina data is fit for denoising with deblur. By default deblur also uses an initial positive filtering step based on the GreenGenese database which significantly reduces processing time. The user can choose to use a different positive filter of their choice with the [denoise-other](https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-other/) tool.


#### Clustering
<much of the below section is already covered by now in the above. We probably don't need to include these again, but just say 'as per above'.. I left them untouched in case you think we should keep them.>

To cluster your sequences, you need to prepare your data.

##### Merged paired-end reads

If you have unmerged forward and reverse reads, you need to merge these together.

qiime command

##### Trim sequences

Because many clustering algorithms rely on very basic measures of genetic distance, you may want to ensure that all of your sequences are trimmed to the same length before clustering.

qiime command

##### Quality control

You should discard low-quality sequences before clustering.
There are two ways to do this: either by truncating your reads after the first time a certain low quality is encountered or by discarding whole sequences based on their expected number of errors (i.e. bases called incorrectly).
Because of the way that sequencing generates errors, it is generally more advisable to discard merged reads based on the expected number of errors, and to truncate

Note that which quality filtering method you choose informs when you should trim the length of your sequences.
If you discard reads based on expected errors, you should trim them *before* quality filtering.
If you truncate reads after a certain quality is encountered, you may want to trim them *after* quality filtering.

You can learn more about
these approaches two by reading the USEARCH documentation:
http://www.drive5.com/usearch/manual/readqualfiltering.

Note that many of these methods also automatically discard reads with ambiguous base calls (i.e. bases that are called as something other than A, T, C, or G).

###### Quality filtering

qiime commands

###### Quality truncation

##### Clustering

There are many ways to cluster sequences, which fall into three main categories:

1. [de novo clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-de-novo/), in which sequences are grouped together based solely on the dataset itself. Can take a long time.     
1. [closed reference clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-closed-reference/), in which sequences are grouped together based on their matches to an external reference database. Takes much less time.     
1. [open reference clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-open-reference/), which first performs closed reference clustering and then de novo clustering on any reads which did not map to the reference. This method is ill-advised and will not be covered here. [link to edgar's scathing paper about qiime open reference](link)

###### de novo clustering

Sequences can be clustered *de novo* based on their genetic similarity alone (i.e. with VSEARCH) or based on a combination of their genetic similarity and abundance distributions (i.e. with distribution-based clustering).

####### VSEARCH
<I've linked these above, do we want to actually provide example commands or just links to the right page? I was thinking this starts to be too long and resemeble the tutorials if we are providing example commands>
qiime command

####### Distribution-based clustering

Distribution-based clustering incorporates the similarity between sequences and their abundance distribution to identify ecologically meaningful populations. You can learn more about this method in the documentation and paper [link to docs](dbotu.com)

qiime command

###### closed reference clustering

Closed reference clustering groups sequences together which match the same reference sequence in a database with a certain similarity.
Note that closed reference clustering may produce groupings that are not what you expect [link to scott's blog](link).

VSEARCH can do closed reference clustering.
You can decide which reference database to cluster against.
Most people use Green Genes or SILVA, but others curate their own databases or use other standard references (e.g. UNITE for ITS data).


qiime command

### Assign taxonomy

If you clustered OTUs with closed-reference clustering, your OTUs will have the name of the reference sequence they matched to, and you don't need to do anything else to get taxonomy.
For all other *de novo* methods, you can assign taxonomy with different probabilistic classifiers.

In qiime2, two methods of assigning taxonomy is available and they are nicely covered in this [tutorial](https://docs.qiime2.org/2018.6/tutorials/overview/#taxonomy-classification-and-taxonomic-analyses). Briefly, the first is an alignment based method found in [`classify-consensus-blast`[(https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-blast/) and [`classify-consensus-vsearch`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-vsearch/) which use reference databases directly and second is using machine-learning classification through [`fit-classifier-sklearn`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-sklearn/) and [`fit-classifier-naive-bayes`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-naive-bayes/). These require training a classifier based on your specific region and primers. This training step is particularly computationly heavy. 

You can also download some pre-trained taxonomy classifiers [here](https://docs.qiime2.org/2018.6/data-resources/).

#### Train a classifier
<I think between the tutorials and Nick's new overview tutorial we can skip these command examples, thoughts?>
qiime commands

#### Classify sequences

qiime commands

## Analyze feature table and gain insight

While the exact analyses you perform depend on your dataset, experimental design, and questions of interest, there are some basic analyses that many microbiome analyses have in common.

### Export the data

If you're a veteran microbiome scientist and don't want to use qiime 2 for your analyses, you can extract your feature table and sequences from the artifact using the [export](https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-data) tool. While export only outputs the data, the [extract](https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-versus-extracting) tool allows you to also extract other metadata such as the citations, provenance etc.

Note that this places generically named files (e.g. `feature-table.txt`) into the output directory, so you may want to immediately rename the files to something more information (or somehow ensure that they stay in their original directory)!

You can also use the handy [qiime2R](https://github.com/jbisanz/qiime2R) package to import qiime2 artifacts within R. 
### Look at the data

The first thing you might want to do is simply to look at your data: what phyla are represented? Genera?

Qiime 2 provides easy ways to visualize your data using the [taxa barplots](https://docs.qiime2.org/2018.6/plugins/available/taxa/barplot/?highlight=barplots#barplot-visualize-taxonomy-with-an-interactive-bar-plot).


You can also export your data to Phinch for some beautiful and interactive visualizations (plugin coming soon!).

### Phylogenetic tree

Some downstream analyses need to know the phylogenetic relationship between your sequences.
You can build an unrooted phylogenetic tree using a variety of methods using: [fasttree](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/fasttree/), [raxml](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/raxml/), and [raxml-rapid-bootstrap](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/raxml-rapid-bootstrap/). You can then [midpoint-root](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/midpoint-root/) your tree or [filter](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/filter-table/) your feature table based on a tree.

### Alpha diversity

Alpha diversity tells you something about the *diversity* of the community in each sample.
There are many ways to calculate alpha diversity, which are wonderfully explained in a [community contribution](https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282) on the qiime 2 forum.
You can see them all within [qiime diversity alpha](https://docs.qiime2.org/2018.6/plugins/available/diversity/alpha/). The following metrics are currently supported in qiime2:
`[mcintosh_d|chao1_ci|berger_parker_d|strong|robbins|mcintosh_e|michaelis_menten_fit|menhinick|doubles|pielou_e|shannon|gini_index|ace|observed_otus|kempton_taylor_q|chao1|esty_ci|dominance|lladser_pe|simpson_e|heip_e|goods_coverage|singles|osd|lladser_ci|margalef|fisher_alpha|simpson|brillouin_d|enspie]`



### Beta diversity

You can also calculate the "distance" or "difference" between communities across samples.
Again, there are many metrics to choose from using [beta diversity](https://docs.qiime2.org/2018.6/plugins/available/diversity/beta/).
The following distance metrics are currently supported in qiime2.
`[correlation|sokalmichener|russellrao|hamming|rogerstanimoto|chebyshev|cityblock|kulsinski|sqeuclidean|braycurtis|yule|matching|jaccard|canberra|euclidean|seuclidean|sokalsneath|wminkowski|dice|mahalanobis|cosine]`


#### PCoA

Once you've calculated distances between all pairwise samples in your data, you can project your samples onto a PCoA plot.

qiime command

#### PERMANOVA/ANOSIM/etc

If you have multiple groups and want to know whether they are meanginfully different, you can use a statistical methods that calculates whether the distances between samples in different groups is different than the distance between samples in the same group.

There are a few different ways to do this, learn more about it somewhere...?

qiime commands...

### Differential abundance testing

If you are comparing two groups of samples, you can ask if any taxa in your data are differentially abundant in the two groups.
There are many ways to measure differential abundance.
You should understand what assumptions are being made by each method and ensure that your data meets these assumptions.

#### Non-parametric tests

qiime command for wilcoxon, etc

#### DESEQ2

#### MetagenomeSeq

#### Others?

### Machine learning and multivariate models

Beyond testing for differentially abundant taxa, you can also compare groups with multi-variate approaches like regression models and machine learning classifiers.

#### Machine learning classifiers

Machine learning can be used to build complex models that distinguish groups of samples well.
You should familiarize yourself with the underlying methods called by qiime - the scikit-learn user guide is a fantastic resource.
Also, make sure that you are using appropriate cross-validation or holdout data to prevent overfitting.

qiime commands

#### Regression models

You can also build more complicated models to identify differences between groups of samples...

### And much much more!

You can explore qiime's ever-growing list of plugins to find other methods to apply to your data.
And remember that you're not limited to what qiime can do: you can export your data at any point and do more complicated or unique analyses on your own computer.
