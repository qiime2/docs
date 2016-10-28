Semantic types
==============

All QIIME 2 *artifacts* have defined semantic types. This document is a placeholder for full documentation of how to use these types and how to define new semantic types in QIIME 2 plugins.

Why define semantic types?
--------------------------

Defining semantic types allows us to ensure that the data that is passed to an *action* is meaningful for the operation that will be performed. For example, a ``biom.Table`` object could contain presence/absence data (i.e., a 1 to indicate that an OTU was observed at least one time in a given sample, and a 0 to indicate than an OTU was not observed at least one time in a given sample). However, if that were provided to a function computing a quantitative diversity metric where OTU abundances are included in the calculation (e.g., weighted UniFrac), the function would complete successfully, but the result would not be meaningful.

QIIME 2 defines semantic types to help users avoid using functionality incorrectly, and to allow the system to reason about what *artifacts* can be used with which *methods* and *visualizers*.

Common semantic types
---------------------

The following semantic types are defined by, and importable from, the `q2-types`_ plugin. It is also possible to define semantic types in any plugin, so the available semantic types are not limited to those defined in `q2-types`_. Instructions will be added soon for how to accomplish this. In the meantime, you can refer to the `q2-dummy-types`_ repository for annotated examples.

``FeatureTable[Frequency]``: A feature table (e.g., samples by OTUs) where each value indicates the frequency of an OTU in the corresponding sample expressed as raw counts.

``FeatureTable[RelativeFrequency]``: A feature table (e.g., samples by OTUs) where each value indicates the relative abundance of an OTU in the corresponding sample such that the values for each sample will sum to 1.0.

``FeatureTable[PresenceAbsence]``: a feature table (e.g., samples by OTUs) where each value indicates whether an OTU is present or absent in the corresponding sample.

``Phylogeny[Rooted]``: A rooted phylogenetic tree.

``Phylogeny[Unrooted]``: An unrooted phylogenetic tree.

``DistanceMatrix``: A distance matrix.

``PCoAResults``: The results of running principal coordinate analysis (PCoA).

``SampleData[AlphaDiversity]``: Alpha diversity values, each associated with a single sample identifier.

``SampleData[SequencesWithQuality]``: Sequences with quality scores, where each set of sequences is associated with a sample identifier (i.e. demultiplexed sequences).

``SampleData[PairedEndSequencesWithQuality]``: Paired-end sequences (forward and reverse) with quality scores, where each set of paired-end sequences is associated with a sample identifier (i.e. demultiplexed paired-end sequences).

``FeatureData[Taxonomy]``: Taxonomic information associated with a feature identifier.

``FeatureData[Sequence]``: A single unaligned sequence associated with a feature identifier (e.g. a representative sequence).

``FeatureData[AlignedSequence]``: A single aligned sequence associated with a feature identifier, where the alignment is with respect to the aligned sequences associated with all of the other feature identifiers (i.e., when more than one feature identifier is present this represents a multiple sequence alignment).

``FeatureData[PairedEndSequence]``: Paired-end sequences (forward and reverse) associated with a feature identifier.

``ReferenceFeatures[SSU]``: A collection of reference features for small subunit rRNA data. This will include aligned and unaligned sequences, taxonomic annotations, and a phylogenetic tree. (Subtypes for other types of references will be added in the future, possibly including ``ReferenceFeatures[Genome]`` for shotgun analysis, and ``ReferenceFeatures[ITS]`` for fungal ITS analysis.)

.. _q2-types: https://github.com/qiime2/q2-types

.. _q2-dummy-types: https://github.com/qiime2/q2-dummy-types
