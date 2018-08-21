Artifact API
============

.. note:: This guide assumes you have performed the steps in the :doc:`Moving Pictures tutorial <../tutorials/moving-pictures>`. The ``table.qza`` and ``sample-metadata.tsv`` files generated in that tutorial are used here.

The Artifact API is a Python 3 application programmer interface (API) for QIIME 2. The Artifact API supports interactive computing with QIIME 2 using the Python 3 programming language. This API is intended for advanced/technical users. The API is automatically generated, and its availability depends on which QIIME 2 plugins are currently installed. It has been optimized for use in the `Jupyter Notebook`_, which is currently our primary target for use of this API. The Artifact API is a part of the QIIME 2 framework; no additional software needs to be installed to use it.

We'll now explore some of the same methods and visualizers introduced in the :doc:`Moving Pictures tutorial <../tutorials/moving-pictures>`, this time in the Python interpreter instead of the command line interface. First, we'll load a QIIME 2 ``Artifact``, in this case a feature table. We'll then pass that to the ``q2-feature-table`` plugin's ``rarefy`` method, which will return a new Artifact.

.. code-block:: python

   >>> from qiime2.plugins import feature_table
   >>> from qiime2 import Artifact
   >>> unrarefied_table = Artifact.load('table.qza')
   >>> rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100)
   >>> rarefied_table = rarefy_result.rarefied_table

While we recommend working with QIIME 2 ``Artifacts`` directly, it is possible to access the underlying data in one or more compatible *views* (Python objects/data structures or file formats). For example, you may want to access the rarefied feature table that was just created as a ``biom.Table`` object. You can do this as follows:

.. code-block:: python

   >>> import biom
   >>> biom_table = rarefied_table.view(biom.Table)
   >>> print(biom_table.head())
   # Constructed from biom file
   #OTU ID	L1S105	L1S140	L1S208	L1S257	L1S281
   b32621bcd86cb99e846d8f6fee7c9ab8	25.0	31.0	27.0	29.0	23.0
   99647b51f775c8ddde8ed36a7d60dbcd	0.0	0.0	0.0	0.0	0.0
   d599ebe277afb0dfd4ad3c2176afc50e	0.0	0.0	0.0	0.0	0.0
   51121722488d0c3da1388d1b117cd239	0.0	0.0	0.0	0.0	0.0
   1016319c25196d73bdb3096d86a9df2f	11.0	17.0	12.0	4.0	2.0

You can also view the artifact's data as a ``pandas.DataFrame`` object:

.. code-block:: python

   >>> import pandas as pd
   >>> df = rarefied_table.view(pd.DataFrame)
   >>> df.head()
           b32621bcd86cb99e846d8f6fee7c9ab8  99647b51f775c8ddde8ed36a7d60dbcd  \
   L1S105                              25.0                               0.0
   L1S140                              31.0                               0.0
   L1S208                              27.0                               0.0
   L1S257                              29.0                               0.0
   L1S281                              23.0                               0.0
   ...

A powerful feature of QIIME 2 is that you can export different types of views from QIIME artifacts as illustrated here, then operate on the resulting data types, and import those data back into QIIME. This is useful if there are some operations that are available on the view's data type (e.g., the ``pandas.DataFrame``) that are not available through the QIIME API. An important caveat is that you will lose all artifact provenance in the process, because QIIME can't track what happens to data outside of QIIME. You can import the ``pandas.DataFrame`` back into a new QIIME artifact as follows:

.. code-block:: python

   imported_artifact = Artifact.import_data("FeatureTable[Frequency]", df)

The ``rarefied_table`` artifact can be passed to methods of other QIIME 2 plugins. Here we'll compute the *Observed OTUs* alpha diversity metric using the ``q2-diversity`` plugin. The resulting ``Artifact`` will be of type ``SampleData[AlphaDiversity]``, and we can access a ``pd.Series`` as a view of this ``Artifact``.

.. code-block:: python

   >>> from qiime2.plugins import diversity
   >>> alpha_result = diversity.methods.alpha(table=rarefied_table, metric='observed_otus')
   >>> alpha_diversity = alpha_result.alpha_diversity
   >>> alpha_diversity.view(pd.Series)
   L1S105    24
   L1S140    19
   L1S208    25
   L1S257    30
   L1S281    29
   L1S57     23
   L1S76     20
   L1S8      17
   ...
   Name: observed_otus, dtype: int64

Finally, we can save our ``Artifacts`` as ``.qza`` files and exit the interpreter as follows:

.. code-block:: python

   >>> rarefied_table.save('rare.qza')
   'rare.qza'
   >>> alpha_diversity.save('oo.qza')
   'oo.qza'
   >>> exit

Another powerful feature of QIIME 2 is that you can combine interfaces. For example, you could develop a Python script that automatically processes files for you to generate results as we just did, and then perform analysis of those files using the :doc:`command line interface <q2cli>` or the :doc:`QIIME 2 Studio <q2studio>`. For instance, you could now continue your analysis and view some results on the command line as follows:

.. command-block::
   :no-exec:

   qiime diversity alpha-group-significance --i-alpha-diversity oo.qza --m-metadata-file sample-metadata.tsv  --o-visualization oo-group-significance.qzv

The above command as an API call is:

.. code-block:: python

   >>> from qiime2 import Metadata
   >>> metadata = Metadata.load('sample-metadata.tsv')
   >>> group_significance = diversity.actions.alpha_group_significance(alpha_diversity=alpha_diversity, metadata=metadata)

.. _`Jupyter Notebook`: http://jupyter.org/
