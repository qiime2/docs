Metadata in QIIME 2
===================

.. note:: This guide assumes you have installed QIIME 2 using one of the procedures in the :doc:`install documents <../install/index>` and completed the :doc:`moving pictures tutorial <moving-pictures>`.

Metadata provides the key to gaining biological insight from your data. In QIIME 2, *sample metadata* may include technical details, such as the DNA barcodes that were used for each sample in a multiplexed sequencing run, or descriptions of the samples, such as which subject, time point, and body site each sample came from in a human microbiome time series. *Feature metadata* is often a feature annotation, such as the taxonomy assigned to a sequence variant or OTU. Sample and feature metadata are used by many plugins in QIIME 2, and examples are provided in this tutorial (and other QIIME 2 tutorials) illustrating how to use metadata in your own microbiome analyses.

Metadata is usually specific to a given microbiome study, and collecting sample metadata is typically one of the first steps you'll take before beginning a QIIME 2 analysis. It is up to the investigator to decide what information is collected and tracked as metadata. QIIME 2 does not place restrictions on what types of metadata are expected to be present; there are no enforced "metadata standards". This is your opportunity to track whatever information you think may be important to your analyses, and unfortunately QIIME 2 is not able to gather that information for you. When in doubt, collect as much metadata as possible, as you may not be able to retroactively collect certain types of information.

.. tip:: While QIIME 2 does not enforce standards for what types of metadata to collect, the MIMARKS_ standard provides recommendations for microbiome studies and may be helpful in determining what information to collect in your study. If you plan to deposit your data in a data archive (e.g. ENA_ or Qiita_), it is also important to determine the types of metadata expected by the archive, as each archive may have its own requirements.

Metadata Formatting Requirements
--------------------------------

QIIME 2 metadata is most commonly stored in a TSV_ (i.e. tab-separated values) file. These files typically have a ``.tsv`` or ``.txt`` file extension, though it doesn't matter to QIIME 2 what file extension is used. TSV files are simple text files used to store tabular data, and the format is supported by many types of software, such as editing, importing, and exporting from spreadsheet programs and databases. Thus, it's usually straightforward to manipulate QIIME 2 metadata using the software of your choosing. If in doubt, we recommend using a spreadsheet program such as Microsoft Excel or Google Sheets to edit and export your metadata files.

.. note:: In addition to TSV files, QIIME 2 Artifacts (i.e. ``.qza`` files) can also be used as metadata. See the section :ref:`artifacts-as-metadata` below for details. QIIME 2 may also support additional file formats in the future.

.. qiime1-users:: In QIIME 1, TSV metadata files were referred to as `mapping files`_. In QIIME 2, we refer to these files as *metadata files*, but they are conceptually the same thing. QIIME 2 metadata files are backwards-compatible with QIIME 1 mapping files, meaning that you can use existing QIIME 1 mapping files in QIIME 2 without needing to make modifications to the file.

The following sections describe formatting requirements for QIIME 2 metadata files, and how to validate your metadata files. Since there is no universal standard for TSV files, it is important to adhere to these requirements and understand how QIIME 2 will interpret the file's contents to get the most out of your (meta)data!

Metadata Validation
*******************

Sample and feature metadata files stored in Google Sheets can be validated using Keemei_. Select *Add-ons > Keemei > Validate QIIME 2 metadata file* to validate metadata stored in Google Sheets.

QIIME 2 will also automatically validate a metadata file anytime it is used by the software. However, using Keemei_ to validate your metadata is recommended because a report of all validation errors and warnings will be presented each time Keemei is run. Loading your metadata in QIIME 2 will typically present only a single error at a time, which can make identifying and resolving validation issues cumbersome, especially if there are many issues with the metadata.

.. note:: In the future, there will be a ``qiime metadata validate`` command to perform Keemei-style validation within QIIME 2 (e.g. if using Google Sheets is not an option for you).

Leading and trailing whitespace characters
******************************************

If **any** cell in the metadata contains leading or trailing whitespace characters (e.g. spaces, tabs), those characters will be ignored when the file is loaded. Thus, leading and trailing whitespace characters are not significant, so cells containing the values ``'gut'`` and ``'  gut  '`` are equivalent. This rule is applied before any other rules described below.

Comments and Empty Rows
***********************

Rows whose first cell begins with the pound sign (``#``) are interpreted as comments and may appear anywhere in the file. Comment rows are ignored by QIIME 2 and are for informational purposes only. Inline comments are not supported.

Empty rows (e.g. blank lines or rows consisting solely of empty cells) may appear anywhere in the file and are ignored.

.. _identifier-column:

Identifier Column
*****************

The first column in the metadata file is the identifier (ID) column. This column defines the sample or feature IDs associated with your study. It is not recommended to mix sample and feature IDs in a single metadata file; keep sample and feature metadata stored in separate files.

The ID column name (i.e. *ID header*) must be one of the following values. The values listed below may not be used to name other IDs or columns in the file.

Case-insensitive:

- ``id``
- ``sampleid``
- ``sample id``
- ``sample-id``
- ``featureid``
- ``feature id``
- ``feature-id``

Case-sensitive (these are mostly for backwards-compatibility with QIIME 1, biom-format, and Qiita files):

- ``#SampleID``
- ``#Sample ID``
- ``#OTUID``
- ``#OTU ID``
- ``sample_name``

The following rules apply to IDs:

- IDs may consist of any Unicode characters, with the exception that IDs must not start with the pound sign (``#``), as those rows would be interpreted as comments and ignored. See the section :ref:`identifier-recommendations` for recommendations on choosing identifiers in your study.
- IDs cannot be empty (i.e. they must consist of at least one character).
- IDs must be unique (exact string matching is performed to detect duplicates).
- At least one ID must be present in the file.
- IDs cannot use any of the reserved ID column names listed above.

.. _identifier-recommendations:

Recommendations for Identifiers
*******************************

Our goal with QIIME 2 is to support arbitrary Unicode characters in all cells of metadata files. However, given that QIIME 2 plugins and interfaces can be developed by anyone, we can't make a guarantee that arbitrary Unicode characters will work with all plugins and interfaces. We can therefore make recommendations to users about characters that should be safe to use in identifiers, and we are preparing resources for plugin and interface developers to help them make their software as robust as possible. As developer resources become available, we will announce them in the `Developer Discussion category`_ on the QIIME 2 Forum.

Sample and feature identifiers with problematic characters tend to cause the most issues for our users. Based on our experiences with QIIME 1, QIIME 2, and other bioinformatics and command line tools, we can recommend the following attributes for identifiers:

- Identifiers should be 36 characters long or less.
- Identifiers should contain only ASCII alphanumeric characters (i.e. in the range of ``[a-z]``, ``[A-Z]``, or ``[0-9]``), the period (``.``) character, or the dash (``-``) character.

An important point to remember is that sometimes values in your sample metadata can become identifiers. For example, taxonomy annotations can become feature identifiers following ``qiime taxa collapse``, and sample or feature metadata values can become identifiers after applying ``qiime feature-table group``. If you plan to apply these or similar methods where metadata values can become identifiers, you will be less likely to encounter problems if the values adhere to these identifier recommendations as well.

To help users become aware of these recommendations, the Keemei_ metadata validator will warn users about identifiers that don't meet the above recommendations.

Users may be interested in the cual-id_ software for assistance with creating sample identifiers. The cual-id_ paper also provides some discussion on how to design identifiers.

.. note:: Some bioinformatics tools may have more restrictive requirements on identifiers than the recommendations that are outlined here. For example, Illumina sample sheet identifiers cannot have `.` characters, while we do include those in our set of recommended characters. Similarly, Phylip_ requires that identifiers are a maximum of 10 characters, while we recommend length 36 or less. If you plan to export your data for use with other tools that may have more restrictive requirements on identifiers, we recommend that you adhere to those requirements in your QIIME 2 analyses as well, to simplify subsequent processing steps.

.. note:: The length recommended here (36 characters or less) is designed to be as short as possible while still supporting version 4 UUIDs formatted with dashes.

Metadata Columns
****************

The ID column is the first column in the metadata file, and can optionally be followed by additional columns defining metadata associated with each sample or feature ID. Metadata files are not required to have additional metadata columns, so a file containing only an ID column is a valid QIIME 2 metadata file.

The following rules apply to column names:

- May consist of any Unicode characters.
- Cannot be empty (i.e. column names must consist of at least one character).
- Must be unique (exact string matching is performed to detect duplicates).
- Column names cannot use any of the reserved ID column names described in the section :ref:`identifier-column`.

The following rules apply to column values:

- May consist of any Unicode characters.
- Empty cells represent *missing data*. Other values such as ``NA`` are not interpreted as missing data; only the empty cell is recognized as "missing". Note that cells consisting solely of whitespace characters are also interpreted as *missing data* because leading and trailing whitespace characters are always ignored, effectively making the cell empty.

.. note:: The empty cell simply indicates that data is missing, but doesn't indicate what type of missing data it might be. You can use other values of your choosing to denote different types of missing data (e.g. "not applicable" vs. "not collected"). These custom values won't be interpreted as missing data in QIIME 2, but you can still record and use these "missing" metadata values to perform filtering on your data prior to further analyses (e.g. using ``qiime feature-table filter-samples`` to filter samples based on custom "missing" values).

Column Types
************

QIIME 2 currently supports *categorical* and *numeric* metadata columns. By default, QIIME 2 will attempt to infer the type of each metadata column: if the column consists only of numbers or missing data, the column is inferred to be *numeric*. Otherwise, if the column contains any non-numeric values, the column is inferred to be *categorical*. Missing data (i.e. empty cells) are supported in categorical columns as well as numeric columns.

QIIME 2 supports an **optional** *comment directive* to allow users to explicitly state a column's type, avoiding the column type inference described above. This can be useful if there is a column that appears to be numeric, but should actually be treated as categorical metadata (e.g. a ``Subject`` column where subjects are labeled ``1``, ``2``, ``3``). Explicitly declaring a column's type also makes your metadata file more descriptive because the intended column type is included with the metadata, instead of relying on software to infer the type (which isn't always transparent).

You can use an optional *comment directive* to declare column types in your metadata file. The comment directive must appear **directly** below the header. The row's first cell must be ``#q2:types`` to indicate the row is a *comment directive*. Subsequent cells may contain the values ``categorical`` or ``numeric`` (both case-insensitive). The empty cell is also supported if you do not wish to assign a type to a column (the type will be inferred in that case). Thus, it is easy to include this comment directive without having to declare types for every column in your metadata.

.. tip:: Use ``qiime metadata tabulate`` to see the column types of your QIIME 2 Metadata. This works whether you're using the comment directive, type inference, or a combination of the two approaches.

.. note:: In previous versions of QIIME 2 and QIIME 1, *metadata columns* were often referred to as *metadata categories*. Now that we support metadata column typing, which allows you to say whether a column contains *numeric* or *categorical* data, we would end up using terms like *categorical metadata category* or *numeric metadata category*, which can be confusing. We now avoid using the term *category* unless it is used in the context of *categorical* metadata. We've done our best to update our software and documentation to use the term *metadata column* instead of *metadata category*, but there may still be lingering usage of the previous terms out there.

.. note:: The ``#q2:types`` comment directive is the only supported comment directive; others may be added in the future (e.g. ``#q2:units``). For this reason, rows starting with ``#q2:`` are disallowed, as we reserve that namespace for future comment directives.

Number Formatting
*****************

If a column is to be interpreted as a *numeric* metadata column (either through column type inference or by using the ``#q2:types`` comment directive), numbers in the column must be formatted following these rules:

- Use the decimal number system: ASCII characters ``[0-9]``, ``.`` for an optional decimal point, and ``+`` and ``-`` for positive and negative signs, respectively.

  - Examples: ``123``, ``123.45``, ``0123.40``, ``-0.000123``, ``+1.23``

- Scientific notation may be used with *E-notation*; both ``e`` and ``E`` are supported.

  - Examples: ``1e9``, ``1.23E-4``, ``-1.2e-08``, ``+4.5E+6``

- Only up to 15 digits **total** (including before and after the decimal point) are supported to stay within the 64-bit floating point specification. Numbers exceeding 15 total digits are unsupported and will result in undefined behavior.

- Common representations of *not a number* (e.g. ``NaN``, ``nan``) or infinity (e.g. ``inf``, ``-Infinity``) are **not supported**. Use an empty cell for missing data (e.g. instead of ``NaN``). Infinity is not supported at this time in QIIME 2 metadata files.

Advanced File Format Details
****************************

.. note:: The details in this section generally aren't necessary if you're creating and exporting QIIME 2 metadata files using a spreadsheet program (e.g. Microsoft Excel, Google Sheets). If you're creating TSV files by hand (e.g. in a text editor) or writing your own software to consume or produce QIIME 2 metadata files, the details in this section may be important, so read on!

TSV Dialect and Parser
~~~~~~~~~~~~~~~~~~~~~~

QIIME 2 attempts to interoperate with TSV files exported from Microsoft Excel, as this is the most common TSV "dialect" we have seen in use. The QIIME 2 metadata parser (i.e. reader) uses the `Python csv module`_ ``excel-tab`` dialect for parsing TSV metadata files. This dialect supports wrapping fields in double quote characters (``"``) to allow for tab, newline, and carriage return characters within a field. To include a literal double quote character in a field, the double quote character must be immediately preceded by another double quote character. See the `Python csv module`_ for complete documentation on the ``excel-tab`` dialect.

Encoding and Line Endings
~~~~~~~~~~~~~~~~~~~~~~~~~

Metadata files must be encoded as UTF-8, which is backwards-compatible with ASCII encoding.

Unix line endings (``\n``), Windows/DOS line endings (``\r\n``), and "classic Mac OS" line endings (``\r``) are all supported by the metadata parser for interoperability. When metadata files are written to disk in QIIME 2, the line endings will always be ``\r\n`` (Windows/DOS line endings).

Trailing Empty Cells and Jagged Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The metadata parser ignores any trailing empty cells that occur past the fields declared by the header. This is mainly for interoperability with files exported from some spreadsheet programs. These trailing cells/columns may be jagged (or not); they will be ignored either way when the file is read.

If a row doesn't contain as many fields as declared by the header, empty cells will be padded to match the header length (again, this is mainly for interoperability with exported spreadsheets).

Using Metadata Files
--------------------

To get started with understanding sample metadata files, download an example TSV file:

.. command-block::
   :no-exec:

   mkdir qiime2-metadata-tutorial
   cd qiime2-metadata-tutorial

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/moving-pictures/sample_metadata.tsv
   :saveas: sample-metadata.tsv

Since this is a TSV file, it can be opened and edited in a variety of applications, including text editors, Microsoft Excel, and Google Sheets (e.g. if you plan to validate your metadata with Keemei_).

QIIME 2 also provides a visualizer for viewing metadata in an interactive table:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv \
     --o-visualization tabulated-sample-metadata.qzv

.. question::
   Based on the table in ``tabulated-sample-metadata.qzv``, how many samples are associated with ``subject-1``? How many samples are associated with the ``gut`` body site? Hint: use the search box and/or the column sorting options to assist with this query.

.. _artifacts-as-metadata:

Using QIIME 2 Artifacts as Metadata
-----------------------------------

In addition to TSV metadata files, QIIME 2 also supports viewing some kinds of artifacts as metadata. An example of this is artifacts of type ``SampleData[AlphaDiversity]``.

To get started with understanding artifacts as metadata, first download an example artifact:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/metadata/faith_pd_vector.qza
   :saveas: faith_pd_vector.qza

To view this artifact as metadata, simply pass it in to any method or visualizer that expects to see metadata (e.g. ``metadata tabulate`` or ``emperor plot``):

.. command-block::
   qiime metadata tabulate \
     --m-input-file faith_pd_vector.qza \
     --o-visualization tabulated-faith-pd-metadata.qzv

.. question::
   What is the largest value of Faith's PD? What is the smallest? Hint: use the column sorting functions to assist with this query.

When an artifact is viewed as metadata, the result includes that artifact's provenance in addition to its own.

.. question::
   Try inspecting ``tabulated-faith-pd-metadata.qzv`` at https://view.qiime2.org and locate this artifact in the interactive provenance graph.

Merging metadata
----------------

Since metadata can come from many different sources, QIIME 2 supports metadata merging when running commands. Building upon the examples above, simply passing ``--m-input-file`` multiple times will combine the metadata columns in the specified files:

.. command-block::
   qiime metadata tabulate \
     --m-input-file sample-metadata.tsv \
     --m-input-file faith_pd_vector.qza \
     --o-visualization tabulated-combined-metadata.qzv

The resulting metadata after the merge will contain the intersection of the identifiers across all of the specified files. In other words, the merged metadata will only contain identifiers that are shared across all provided metadata files. This is an *inner join* using database terminology.

.. question::
   Modify the command above to merge the `evenness vector`_ of ``SampleData[AlphaDiversity]`` after the Faith's PD vector. What happens when merging the three artifacts? How many columns are present in the resulting metadata visualization? How many of those columns represent the sample IDs? How many of those columns represent ``SampleData[AlphaDiversity]`` metrics? What happens to the visualization if the order of the metadata files is reversed? Hint, take a closer look at the column ordering.

Metadata merging is supported anywhere that metadata is accepted in QIIME 2. For example, it might be interesting to color an Emperor plot based on the study metadata, or sample alpha diversity. This can be accomplished by providing both the sample metadata file *and* the ``SampleData[AlphaDiversity]`` artifact:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/metadata/unweighted_unifrac_pcoa_results.qza
   :saveas: unweighted_unifrac_pcoa_results.qza

.. command-block::
   qiime emperor plot \
     --i-pcoa unweighted_unifrac_pcoa_results.qza \
     --m-metadata-file sample-metadata.tsv \
     --m-metadata-file faith_pd_vector.qza \
     --o-visualization unweighted-unifrac-emperor-with-alpha.qzv

.. question::
   What body sites are associated with the highest Faith's phylogentic diversity value? Hint: first color by body site, and then color by Faith's PD using a continuous color scheme.


.. _`exploring feature metadata`:

Exploring feature metadata
--------------------------

Metadata in QIIME 2 can be applied to sample or features --- so far we have only dealt with sample metadata. This section will focus on feature metadata, specifically how to view ``FeatureData`` as metadata.

To get started with feature metadata, first download the example files:

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/metadata/rep-seqs.qza
   :saveas: rep-seqs.qza

.. download::
   :url: https://data.qiime2.org/2020.2/tutorials/metadata/taxonomy.qza
   :saveas: taxonomy.qza

We have downloaded a ``FeatureData[Sequence]`` file (``rep-seqs.qza``) and a ``FeatureData[Taxonomy]`` file (``taxonomy.qza``). We can merge (and ``tabulate``) these files to associate the representative sequences with their taxonomic annotations:

.. command-block::
   qiime metadata tabulate \
     --m-input-file rep-seqs.qza \
     --m-input-file taxonomy.qza \
     --o-visualization tabulated-feature-metadata.qzv

The resulting table shows the joined metadata files with a column of the the feature IDs, a column of the representative sequences, a column of the taxonomic assignments, and lastly, a column of the assignment confidence.

.. question::
   Are all artifacts (``.qza`` files) viewable as metadata? Hint: try tabulating a `feature table artifact`_. Are all metadata files stored as ``.qza`` files?

Finally, there are export options available in the visualizations produced from ``metadata tabulate``. Using the results from ``tabulated-feature-metadata.qzv``, export the data as a new TSV. Open that file in a TSV viewer or text editor and note that the contents are the same as the interactive metadata table in the visualization.

.. question::
   Can the exported TSV from the above step be used as metadata? What are some benefits of being able to export metadata (hint: see the discussion above about metadata merging)? What about some potential drawbacks (hint: what happens to data :doc:`provenance <../concepts>` when data is exported from QIIME 2)?

.. _MIMARKS: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3367316/
.. _ENA: https://www.ebi.ac.uk/ena
.. _Qiita: https://qiita.ucsd.edu/
.. _TSV: https://en.wikipedia.org/wiki/Tab-separated_values
.. _`mapping files`: http://qiime.org/documentation/file_formats.html#metadata-mapping-files
.. _Keemei: https://keemei.qiime2.org/
.. _`Developer Discussion category`: https://forum.qiime2.org/c/dev-discussion
.. _`cual-id`: http://msystems.asm.org/content/1/1/e00010-15
.. _`Phylip`: http://evolution.genetics.washington.edu/phylip.html
.. _`Python csv module`: https://docs.python.org/3/library/csv.html
.. _`evenness vector`: https://docs.qiime2.org/2020.2/data/tutorials/moving-pictures/core-metrics-results/evenness_vector.qza
.. _`feature table artifact`: https://docs.qiime2.org/2020.2/data/tutorials/moving-pictures/table.qza
