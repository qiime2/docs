# 16S processing overview

In this document, we'll go over the basic steps involved in 16S data processing and analysis.
This tutorial is intended for experienced microbiome researchers who are looking for the **QIIME 2 commands pertaining to specific steps in 16S processing**, as well as for early-stage microbiome scientists who want a broad overview of the steps involved in 16S data processing.
This tutorial is similar to the [QIIME 2 "Overview of QIIME 2 Plugin Workflows" tutorial](https://docs.qiime2.org/2018.6/tutorials/overview/).

For an overview of the theoretical motivations for many of the steps involved in 16S processing, we recommend Scott Olesen's [16S primer](https://leanpub.com/primer16s).

## Overview

You can think of 16S data as taking a few distinct forms:

1. **Data straight off of the sequencer**. This data is usually converted to some formats like `.bam`, `.sff`, or `.fastq` by your sequencing center. We won't cover this here.     
1. **Raw data.** By raw data, we mean raw `.fastq` or `.fasta` files. These files contain sequences and (sometimes) quality scores, but nothing has been done to them yet.     
1. **Feature table and "taxa".** This form of data is the output of raw data processing, when your raw sequences have been turned into individual sequences of interest (e.g. OTUs, amplicon sequence variants (ASVs), sub-OTUs etc) and sometimes assigned taxonomy. By "feature table," we mean a file with samples, sequences (or OTUs, ASVs, etc), and observed counts for each sequence in each sample.        
1. **Analysis and insight.** After processing your data into a feature table, you can use QIIME 2 to perform some basic analysis and (hopefully) gain insights.    

In this overview, we'll discuss the potential steps involved in going from **raw data to feature tables** and some basic analyses to take you from **feature table to insights.**

## Pro-tips for power users

Transitioning to QIIME 2 can be difficult for users who are used to processing data with their own tools and scripts, and who want fine control over every step in the process.
We understand the frustrating learning curve for experienced microbiome researchers, but believe that the community, open-sourced nature, and commitment to reproducible science make switching to QIIME 2 worth the initial frustration.
Also, since most QIIME 2 plugins are just wrappers around existing tools, we encourage you to add any functionalities or parameter settings that you find are missing!
Reach out to the [developers on the QIIME 2 forum](https://forum.qiime2.org/c/dev-discussion) - they'll be excited to have your contributions!

That said, here are a few tips we've learned that should substantially improve your experience in transitioning your workflows to QIIME 2:

**Pro-tip #1: QIIME 2 artifacts are just zip files**, so if at any point you want to look at what data files are in the `.qza` artifact, you can unzip your artifact directly (`unzip -k file.qza`) and look through the files in the `data/` folder. Alternatively, you can also use [`qiime tools export`](https://docs.qiime2.org/2018.6/tutorials/exporting/?highlight=extract#exporting-data) to extract the data file directly (which also basically just calls `unzip`).

**Pro-tip #2: the QIIME 2 command line interface tools are slow because they have to unzip and re-zip the data contained in the artifacts each time you call them.** If you need to process your data more interactively, you might want to use the Python API - it is much faster since objects can be simply stored in memory.

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

1. **Look at your data**. You can use bash commands like `less` and `grep` or other programming languages like python to look at the data files, find barcodes and primers, and count the length of reads.       
2. **Ask your sequencing center**. If you've looked at your data and you're still not sure about some answers, you can ask whoever gave you the data - they should know what has been done to the data already.    

### Import data into qiime

If you're using qiime to process your data, the first thing you need to do is get that data into a format that qiime can understand.
Various importing methods currently available in qiime are highlighted [in the QIIME 2 importing tutorial](https://docs.qiime2.org/2018.6/tutorials/importing/). This step has the potential to be the most confusing part of the qiime2 pipeline as there are dozens of import and format types to choose frome and only one will be appropriate for a given file.
To see a full list of available import/format types use: `qiime tools import --show-importable-formats` & `qiime tools import --show-importable-types`

If you're importing data that you've generated, you'll likely need to generate a [_manifest file_](https://docs.qiime2.org/2018.6/tutorials/importing/#fastq-manifest-formats) which maps each file to its sample ID.
Make sure to read the [importing tutorial](https://docs.qiime2.org/2018.6/tutorials/importing/) carefully, and don't get discouraged if you get stuck - this step is often the most tedious (and the QIIME developers agree!)
If you have questions, try searching the [QIIME 2 forum](https://forum.qiime2.org/) or posting your own question.

*Clarifying note: If you have sequencing data with one of two very specific formats (*[EMP](https://docs.qiime2.org/2018.6/tutorials/importing/#emp-protocol-multiplexed-paired-end-fastq) *or* [Casava](https://docs.qiime2.org/2018.6/tutorials/importing/#casava-1-8-single-end-demultiplexed-fastq)*), you can directly import the folder containing your sequencing files with the `--type EMPSingleEndSequences` or `--type 'SampleData[PairedEndSequencesWithQuality]'` flags (or their respective paired-end types). If you don't have one of these two very specific formats, you'll need to make the manifest file to give `import` instructions on what and how to import your files.*


@Bod - <Something about seeing all the available types of importable data>

### Demultiplex sequences

If you have reads from multiple samples in the same file, you'll need to demultiplex your sequences.

If your barcodes have already been removed from the reads and are in a separate file, you can use [q2-demux](https://docs.qiime2.org/2018.6/plugins/available/demux/) to demultiplex these.

**@Bod - TO DO: does q2-demux call an underlying function/package XX to read barcodes from index file or is it in-house code? just need a brief sentence here making it clear to power-users whether this is relying on another tool, or a simple script matching files.**

<@CD I do believe this is in-house, the code certainly doesn't look like its calling any specifi package anyways. https://github.com/qiime2/q2-demux/blob/master/q2_demux/_demux.py> 

If your barcodes are still in your sequences, you can use functions from the  [cutadapt plugin](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/).
The `cutadapt demux-single` looks for barcode sequences at the beginning of your reads (5' end) with a certain error tolerance, removes them, and returns sequence data separated by each sample.
The QIIME 2 forum has a [tutorial on various functions available in cutadapt](https://forum.qiime2.org/t/demultiplexing-and-trimming-adapters-from-reads-with-q2-cutadapt/2313), including demultiplexing.
You can learn more about how `cutadapt` works under the hood by reading their [documentation](https://cutadapt.readthedocs.io/en/stable/index.html).

**@Bod - what's the difference between demux-single and trim-single? Is it the same method under the hood, just that demux-single converts one file into multiple files (corresponding to each sample with barcodes removed), whereas trim-single converts multiple files to multiple files with adapters/primers removed? If so, let's clarify this for power users!**
<@CD, you're correct, they do fundementally different things since demux-single actually demultiplexes which means the input must be multiplexed sequences and does, whereas trim-single is only there for searching and trimming and doesn't do any demultiplexing, i.e takes in demultiplexed sequences. So usually you would demux-single to demux and get rid of barcodes, then do trim-single to get rid of anything after barcodes, i.e the overhang adapters or pads etc. It has a lot of options for searching and trimming which is very useful.>

If your barcodes and primers are within your sequences a typical workflow would be to use `demux-single/paired` to demultiplex your sequences based on a given metadata file which also removes the barcodes, and run the output from this through `trim-single/paired` to remove any furhter non-biological sequences such as overhang adaptors or heterogenity pads etc. 
You don't necessarily need to do the demultiplexing step first in your data processing, but it helps to have each sample in a separate file for downstream steps which leverage this to parallelize their processing code.
<@CD, this is actually not true for the denoisers, they do need everything to be demultiplexed going on. Might be ok with OTU picking...never even though about not doing it in that order> 

Note: Currently `q2-demux` and `q2-cutadapt` do not support demultiplexing dual-barcoded paired-end sequences, but only can demultiplex with barcodes in the forward reads. So for the time being for this type of demultiplexing needs to be done outside of qiime using other tools, for example [bcl2fastq](https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software.html).

@Bod - is this still the case? The cutadapt plugin has `demux-paired` and `trim-paired` functions
<@CD, Yup! still the case, crazy eh? see my explanation above for what the differences between trim and demux are> 

@Bod - yes, let's suggest alternative tools outside of R. Maybe something in USEARCH/VSEARCH? I don't actually know what these tools are though, so if you know of others feel free to add them otherwise this is as good as it'll be!
<@CD - The bcl2fastq tool I linked above is that, its a python tool not an R package , I don't know any other tool that specifically deals with this, at least not that I've used. So let's just stick with bcl2fastq which comes with basespace and 0is the default for Illumina runs going through basespace.>

### Merge reads

Whether or not you need to merge reads depends on how you plan to cluster or denoise your sequences into amplicon sequence variants (ASVs) or operational taxonomic units (OTUs). (See below for more information on these distinctions: (TO DO: link to "### Identifying and grouping similar sequences" section in the rst file)).
<@CD, sorry not sure what link/info you are referring to here> 

#### Deciding to merge

If you'll be using [DADA2](https://docs.qiime2.org/2018.6/plugins/available/dada2/) to call ASVs, you shouldn't merge your reads beforehand because DADA2 does it for you.
Instead, you'll need to ensure that your forward and reverse reads have at least 20 bp overlap after any quality filtering and trimming you do.
You may even want to leave for more to account for natural amplicon length variation.
Failure to do so will lead to failed or poor merging (during the call to DADA2) and loss of many reads.

With [deblur](https://docs.qiime2.org/2018.6/plugins/available/deblur/) you have to make a choice.
Deblur only works on the forward reads, so feeding it unmerged paired-end data will produce the same results as if you were to only feed it the forward reads.
If you want to use the full length of your paired-end reads you'll want to merge these prior to deblur using VSEARCH (see section below).

If you'll be calling OTUs based on sequence similarity (e.g. 97% OTUs) or with distribution-based clustering, you probably want to merge your reads before clustering.
Merging forward and reverse reads increases the total length of each read, and thus the information that each one contains.
However, if something went wrong with sequencing and merging throws out a lot of your data, you may want to proceed instead with the shorter (but more abundant) forward reads only.

#### Merging reads with VSEARCH

You can use the QIIME 2 [VSEARCH plugin](https://docs.qiime2.org/2018.6/plugins/available/vsearch/) to merge paired-end reads with the  [join-pairs](https://docs.qiime2.org/2018.6/plugins/available/vsearch/join-pairs/) function.

### Remove non-biological sequences

Prior to clustering or denoising, it's very important to remove all nonbiological sequences in your reads.
These include barcodes, overhang region of primers, sequencing adapters, PCR spacers etc.
Failure to remove these sequences will introduce clustering artifacts and make your results mostly useless.

If you're using DADA2 to denoise your sequences, you can remove biological sequences at the same time as you call the denoising function.
All of DADA2's `denoise` fuctions have some sort of `--p-trim` parameter you can specify to remove base pairs from the end(s) of your reads.   

Note that deblur does not have this functionality yet, so you should remove non-biological sequences before denoising with deblur.
You should also remove non-biological sequences before clustering reads into OTUs.

The [q2-cutadapt](https://docs.qiime2.org/2018.6/plugins/available/cutadapt) plugin has comprehensive functions for removing non-biological sequences from [paired-end](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-paired/) or [single-end](https://docs.qiime2.org/2018.6/plugins/available/cutadapt/trim-single/) data.  

### Identifying and grouping similar sequences

There are two main types of ways to group similar reads together: denoising and clustering.
Denoising is the newer approach, and attempts to identify the exact sequences present in your dataset.
Denoising methods do this by probabilistically determining whether differences between sequences are a result of sequencing error or are truly reflective of biological differences.
These methods return exact sequence variants, sometimes called "amplicon sequence variants" (ASVs) or "sub-OTUs" (sOTUs).

Clustering is a way to group "similar" sequences together, usually based on the genetic distance between sequences but in some cases incorporating additional information (e.g. [distribution-based clustering](http://doi.org/10.1128/AEM.00342-13)).
Clustering methods return "operational taxonomic units" (OTUs).

If you want, you can first denoise your data and then pass your exact sequence variants through a clustering algorithm.

Regardless of how you group your sequences, the grouping methods will output:

1. A list of representative sequences for each of your OTUs and/or sequence variants (qiime data format `FeatureData[Sequence]`), and     
1. A feature table which indicates how many reads of each OTU/sequence variants were observed in each sample. (qiime data format `FeatureTable[Frequency]`)     
    
1. Dada2 and Deblur will also produce a stats summary file with useful information regarding the filtering and denoising.     


#### Denoising

DADA2 and deblur are currently the two denoising methods available in QIIME 2.
Both learn an error model to then probabilistically determine whether variance between sequences is a result of sequencing error or is truly a biological variant.
DADA2 learns the error model based on a portion of your data, while deblur uses a pre-packaged model based on Illumina machines.
Because deblur uses a pre-packaged model, the error model estimation step is much faster than in DADA2, especially on larger datasets.

Both methods are completely parallelized, as they process one sequence at a time.
These methods only work with fastq data, as they require quality scores to build error profiles from your data.

The creators of these denoising methods have different terminology for the resulting exact sequence variants; DADA2 creators call these "amplicon sequence variants" or "ASVs" while creators of deblur call theirs "sub-OTU"  or "sOTU". They both represent denoised sequence variants and under comparable parameters they produce very similar results.
For a benchmarked comparison between these methods, see the following [pre-print](https://peerj.com/preprints/26566/).
We'll be using the ASV terminology throughout this tutorial.

Denoising requires little data preparation.
Both DADA2 and deblur perform quality filtering, denoising, and chimera removal, so you shouldn't need to perform any quality screening prior to running them.
That said, the official qiime2 tutorial does recommend doing an initial [quality-filter](https://docs.qiime2.org/2018.6/tutorials/moving-pictures/#option-2-deblur) with default settings prior to using deblur.
In our experience, DADA2 performs better without this step.

Both methods have an option to truncate your reads to a constant length (**TO DO**: clarify - do they truncate reads prior to denoising, or after denoising?).
<Good question! I don't know tbh..I'll ask. I'm guessing DADA2 does after so it can build a more accurate error model based on the whole thing and Deblur would do before since the error model is pre-packaged> 
DADA2 can handle variable lengths but deblur needs all the reads to be of equal length. As so a truncating parameter in deblur is required, meaning reads shorter than `--p-trim-length` are discarded and reads longer are truncated at that position.
An appropriate truncating value is important thus we strongly recommend using [summary quality plots](https://docs.qiime2.org/2018.6/plugins/available/demux/summarize/) to determine the appropriate parameters. Deciding how to choose these values is one of the most commonly asked questions on the qiime2 forum and unfortunately there is no one size fit all answer. If your truncating parameters are including the poor quality tail (3') of your reads with too many consecutive low scores, the reads might get discarded all together and you will end up with very few reads. If the truncating parameter is too conservative and you're trimming too much of your reads then an inadequate overlap region may lead to improper or failed merging, again leading to a loss of reads. Shorter reads also tend to have lower resolution for taxonomic assignments. One common starting point is to truncate at a position where the medial quality score dips below 20. Generally, you want to discard as much as low quality sequences as you can without sacrificing adequate overlap region. Single-end reads do not require this consideration. Ultimately, ne might have to try a few values and find the 'sweet spot' between quality vs. quantity that most satisfactorily services their data. 

@Bod - can you clarify both of the TO DO's in the paragraph above?
@CD - waiting to hear about the first one

##### DADA2

The [denoise paired-end](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-paired/) function in DADA2 requires unmerged reads.
The [denoising single-end](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-single/) method accepts unmerged paired-end data, but will only use the forward reads.
(It also accepts single-end data.)
DADA2 can also handle pyrosequencing and ion torrent data using the [denoise-pyro](https://docs.qiime2.org/2018.6/plugins/available/dada2/denoise-pyro/) tool.

Note that DADA2 may be slow on very large datasets.
You can increase the number of threads to use with the `--p-n-threads` parameter.

@Bod - do you think we should include something about the truncating length parameter, and/or any other parameters? If so, mind throwing that in here?
@DC - I added a bit there, this a loaded topic and I could write a whole document on the topic...and maybe I will later, but for now this sould suffice I think.

##### deblur

Deblur tends to be faster than DADA2, especially on larger datasets, but comes with other limitations.

It is faster than DADA2 because it uses a pre-packaged error model based on Illumina MiSeq and HiSeq machines instead of training one from scratch.
It also reduces unnecessary denoising with an initial positive filtering step which requires the reads to have a minimum 60% idenditiy similarity to sequences from the 85% OTU GreenGenes database. 
If you don't want to do the default positive filtering to GreenGenes step, you can use a different positive filter with the [denoise-other](https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-other/) tool.

@Bod - can you clarify the GG filtering stuff? Also happy to discuss offline if my confusion is confusing XD
@CD - Is my clarification ok?

Because it uses the pre-packaged model, you can only use deblur to denoise Illumina data.
Deblur's [denoise-16S](https://docs.qiime2.org/2018.6/plugins/available/deblur/denoise-16S/) method can also currently only denoise single-end reads.
It will accept unmerged paired-end reads as input, it just won't do anything with the reverse reads.
As discussed above, deblur can however take in _merged_ reads and treat them as single-end reads. Note that deblur's expected mean error rate increases as read lengths increase so it tends to become more conservative with longer reads, whereas dada2's error model is learnt from the data itself.

#### OTU Clustering

##### Preparing your data

To cluster your sequences, you need to prepare your data.

Specifically, you need to make sure that:

- paired-end reads are merged
- non-biological sequences are removed
- reads are all trimmed to the same length
- low-quality reads are discarded

We discussed merging paired-end reads and removing non-biological sequences above. (to do in rst: add links to these sections)

###### Length trimming

Because many clustering algorithms rely on very basic measures of genetic distance, you want to ensure that all of your sequences are trimmed to the same length before clustering.
You can use the [method name](link) method from the [plugin name](to do) plugin to trim reads to the same length. (**TO DO**: fill in method name and links.)

@Bod - is there a function in qiime2 to truncate read lengths??! I can't seem to find one!! Also a note that the [overview tutorial](https://docs.qiime2.org/2018.6/tutorials/overview/) tells people to denoise --> dereplicate --> cluster. We're presenting a slightly different philosophy here - do you think it's worth highlighting the similarities/differences in the intro to this section (Identifying and grouping similar sequences)?
@CD - If you're referring to just trimming without anything else, I actually don't think so...might be able to hack a way with cutadapt but I haven't actually thought about that. As for the denoise--> cluster approach, what is the different philosophy you are referring to? I tend to agree with that approach, OTU clustering can still benefit from having gone through denoising first, clustering after. not sure about db-otu if that is what you are referring to but for common vsearch approach I would recommend denoise -> cluster.

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
http://www.drive5.com/usearch/manual/readqualfiltering.

Note that many of VSEARCH methods also automatically discard reads with ambiguous base calls (i.e. bases that are called as something other than A, T, C, or G).

@Bod - **TO DO**: is this true of the VSEARCH functions, do you know? I've only used USEARCH
@CD - VSEARCH is very similar to USEARCH but I'm not sure, it's been a while since I've looked at the VSEARCH paper, might be worth referring to that [paper](https://peerj.com/articles/2584/) instead or perhaps link the default settings of [q2-vsearch](https://github.com/qiime2/q2-vsearch/blob/master/q2_vsearch/_cluster_features.py) 

##### Clustering

There are many ways to cluster sequences, which fall into three main categories:

1. [de novo clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-de-novo/), in which sequences are grouped together based solely on the reads in the dataset itself. Can take a long time.     
1. [closed reference clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-closed-reference/), in which sequences are grouped together based on their matches to an external reference database. Takes much less time.     
1. [open reference clustering](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-open-reference/), which first performs closed reference clustering and then de novo clustering on any reads which did not map to the reference. This method is ill-advised and will not be covered here ([Edgar 2017, doi: 10.7717/peerj.3889](http://doi.org/10.7717/peerj.3889)).

###### Dereplicating sequences

No matter which method you use, you first need to dereplicate your sequences.
Note that "dereplicating" sequences is the same thing as "clustering at 100%" - you're essentially just finding all of the _unique_ sequences before passing those into the clustering algorithm.

The [q2-vsearch](https://docs.qiime2.org/2018.6/plugins/available/vsearch/) plugin has a function to [dereplicate sequences](https://docs.qiime2.org/2018.6/plugins/available/vsearch/dereplicate-sequences/).

###### de novo clustering

Sequences can be clustered *de novo* based on their genetic similarity alone (i.e. with VSEARCH) or based on a combination of their genetic similarity and abundance distributions (i.e. with distribution-based clustering).

- **Similarity-based clustering.** The QIIME 2 VSEARCH plugin method [`cluster-features-de-novo`](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-de-novo/) clusters OTUs. You can change the genetic similarity threshold with the `--p-perc-identity` parameter.     
- **Distribution-based clustering** incorporates the similarity between sequences and their abundance distribution to identify ecologically meaningful populations. You can learn more about this method in the [plugin documentation](https://github.com/cduvallet/q2-dbotu), [original paper](http://dx.doi.org/10.1128/AEM.00342-13), and the [re-implementation update paper](https://doi.org/10.1371/journal.pone.0176335). The `call-otus` function in the [q2-dbotu](https://github.com/cduvallet/q2-dbotu) plugin performs distribution-based clustering on input data.

Both of these functions take as input the output of the q2-vsearch `dereplicate-sequences`: dereplicated sequences with qiime data type `'FeatureData[Sequence]'` and a table of counts with qiime data type `'FeatureTable[Frequency]'`.

###### closed reference clustering

Closed reference clustering groups sequences together which match the same reference sequence in a database with a certain similarity. Unlike the de novo method, closed reference clustering is completely parallelizable.
Note that closed reference clustering may produce groupings that are not what you expect [link to scott's blog](link). (**TO DO** add links)

VSEARCH can do closed reference clustering with the [`cluster-features-closed-reference`](https://docs.qiime2.org/2018.6/plugins/available/vsearch/cluster-features-closed-reference/) function.
You can decide which reference database to cluster against with the `--i-reference-sequences` flag.
The input file to this flag should be a `.qza` file containing a fasta file with the sequences to use as references, with qiime data type `FeatureData[Sequence]`.
Most people use Green Genes or SILVA, but others curate their own databases or use other standard references (e.g. UNITE for ITS data).
You can download the references from the links on the [QIIME 2 data resources page](https://docs.qiime2.org/2018.6/data-resources/#marker-gene-reference-databases).
You'll need to unzip/untar and import them as `FeatureData[Sequence]` artifacts, since they're provided as raw data files.

@Bod - can you double-check this for accuracy?
@CD - You're good!

### Assign taxonomy

If you clustered OTUs with closed-reference clustering, your OTUs will have the name of the reference sequence they matched to, and you don't need to do anything else to get taxonomy.
For all other *de novo* methods (including denoising reads with DADA2/deblur), you can assign taxonomy with different probabilistic classifiers.

In qiime2, two general ways of assigning taxonomy are available and covered in the [taxonomy classification tutorial](https://docs.qiime2.org/2018.6/tutorials/overview/#taxonomy-classification-and-taxonomic-analyses).
Taxonomy assignment functions are in the [`feature-classifier` plugin](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/).

The first way to assign taxonomy _aligns reads to reference databases directly_. It can be used with the [`classify-consensus-blast`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-blast/) or [`classify-consensus-vsearch`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/classify-consensus-vsearch/) methods.
These two methods differ in the type of alignment method that they use but both use the _consensus_ approach of taxonomy assignment which searches the database for matches to a query sequence (can be any database as long as it included an accompanying taxonomy with greengenes format). The top `maxaccepts` hits in the database are retained if they have `≥ perc-identity` to the query. The taxonomy is assigned based on `min-consensus` agreement between the two starting at the Kingdom and continue until assignments no longer agree.

The second way uses trained _machine learning classifiers to assign likely taxonomies to reads_, and can be used through the  [`fit-classifier-sklearn`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-sklearn/) or [`fit-classifier-naive-bayes`](https://docs.qiime2.org/2018.6/plugins/available/feature-classifier/fit-classifier-naive-bayes/) functions.
These two functions differ in the type of machine learning model that they use.

@Bod - are my two "these two functions differ in..." statements correct?
@CD - Yes, but I added a bit more. Might be good to get Nic to give it a final glance incase I missed something here too.

The machine learning-based methods require training a classifier for your data's 16S region and sequencing primers.
This training step is particularly computationally heavy, but in most cases you can simply download some pre-trained taxonomy classifiers [on the QIIME 2 data resources page](https://docs.qiime2.org/2018.6/data-resources/).
The ["Training feature classifiers with q2-feature-classifier"](https://docs.qiime2.org/2018.6/tutorials/feature-classifier/) covers how to train a classifier and use it to classify sequences (i.e. assign them a taxonomy).

## Analyze feature table and gain insight

At this point, you should be ready to analyze your feature table to answer your scientific questions!
While the exact analyses you perform depend on your dataset, experimental design, and questions of interest, there are some basic analyses that many microbiome analyses have in common.

### Export the data

If you're a veteran microbiome scientist and don't want to use QIIME 2 for your analyses, you can extract your feature table and sequences from the artifact using the [export](https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-data) tool.
While `export` only outputs the data, the [extract](https://docs.qiime2.org/2018.6/tutorials/exporting/#exporting-versus-extracting) tool allows you to also extract other metadata such as the citations, provenance etc.

Note that this places generically named files (e.g. `feature-table.txt`) into the output directory, so you may want to immediately rename the files to something more information (or somehow ensure that they stay in their original directory)!

You can also use the handy [qiime2R](https://github.com/jbisanz/qiime2R) package to import qiime2 artifacts directly within R.

### After that...

After that, the rest is up to you!
We'll cover some basic QIIME 2 methods to analyze data in an upcoming tutorial, but some general things you can do are:

- **Look at the data:** just see who's there, and if any patterns in abundance jump out at you. QIIME 2 has some really nice visualization functionalities (taxa barplot visualizers](https://docs.qiime2.org/2018.6/plugins/available/taxa/barplot/?highlight=barplots#barplot-visualize-taxonomy-with-an-interactive-bar-plot)) to make this easy. You can also visualize your data on a PCoA plot with the [emperor](https://docs.qiime2.org/2018.6/plugins/available/emperor/plot/) plugin (after calculating beta diversity between samples).
- **Build a phylogenetic tree:** this is required for many downstream analyses/calculations, and is also just a good thing to do to see how related the sequences in your data are. QIIME 2 has a [phylogeny](https://docs.qiime2.org/2018.6/plugins/available/phylogeny/) plugin with different tree-building methods.
- **Calculate alpha diversity of your samples:** usually a first go-to to learn something about the diversity of the communities *within* each sample. The [`diversity` plugin](https://docs.qiime2.org/2018.6/plugins/available/diversity/) has many [alpha diversity metrics](https://forum.qiime2.org/t/alpha-and-beta-diversity-explanations-and-commands/2282) available through the `alpha` and `alpha-phylogenetic` methods.
- **Calculate beta diversity between samples:** this calculation can help you answer questions about difference in communities *between* samples. The [`diversity` plugin](https://docs.qiime2.org/2018.6/plugins/available/diversity/) also has these metrics available in the `beta`, `beta-phylogenetic`, and `beta-phylogenetic-alt` methods.
- **Test for differences between samples**, through differential abundance or distribution testing: there are many ways to test for "differences" between samples. PERMANOVA, ANOSIM, ANCOM, and Gneiss are just some of the relevant methods which are available in QIIME 2. PERMANOVA and ANOSIM can be done with the [`beta-group-significance`](https://docs.qiime2.org/2018.6/plugins/available/diversity/beta-group-significance/) method in the `diversity` plugin. ANCOM is available in the [`composition`](https://docs.qiime2.org/2018.6/plugins/available/composition/) plugin. Gneiss is available in the [`gneiss`](https://docs.qiime2.org/2018.6/plugins/available/gneiss/) plugin, and has an associated [tutorial, "Differential abundance analysis with gneiss"](https://docs.qiime2.org/2018.6/tutorials/gneiss/)
- **Build machine learning classifiers to make predictions:** you can try to learn patterns from your samples and make predictions about new data by building machine learning classifiers. The [q-2sample-classifier](https://docs.qiime2.org/2018.6/plugins/available/sample-classifier/) plugin has several actions for these classifiers, and the associated ["Predicting sample metadata values with q2-sample-classifier" tutorial](https://docs.qiime2.org/2018.6/tutorials/sample-classifier/) provides more details.

### And much much more!

You can explore qiime's ever-growing list of [plugins](https://docs.qiime2.org/2018.6/plugins/) to find other methods to apply to your data.
And remember that you're not limited to what qiime can do: you can export your data at any point and do more complicated or unique analyses on your own computer.
