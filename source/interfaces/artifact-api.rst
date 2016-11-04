Artifact API
============

.. note:: This guide assumes you have performed the steps in the :doc:`Moving Pictures tutorial <../tutorials/moving-pictures>`. The ``table.qza`` and ``sample-metadata.tsv`` files generated in that tutorial are used here.

The Artifact API is a Python 3 application programmer interface (API) for QIIME 2. The Artifact API supports interactive computing with QIIME 2 using the Python 3 programming language. This API is intended for advanced/technical users. The Artifact API has been optimized for use in the `Jupyter Notebook`_, which is currently our primary target for use of this API. The Artifact API is a part of the QIIME 2 framework; no additional software needs to be installed to use it. This API is automatically generated, and its availability depends on which QIIME 2 plugins are currently installed. To see this in action, begin by uninstalling the ``q2-feature-table`` plugin.

.. command-block::
   :no-exec:

   conda uninstall q2-feature-table

Then, open a Python interpreter such as IPython and enter the following command. You should get an error message telling you that the plugin you're trying to access is not available. Leave the interpreter by typing ``exit``.

.. code-block:: python

   >>> from qiime.plugins import feature_table
   ImportError: cannot import name 'feature_table'
   >>> exit

Next, reinstall the ``q2-feature-table`` and ``q2-diversity`` plugins (``q2-diversity`` was uninstalled automatically when we uninstalled ``q2-feature-table`` above because it depends on ``q2-feature-table``).

.. command-block::
   :no-exec:

   conda install -c qiime2 q2-feature-table q2-diversity

Open your interpreter, and you should now be able to import this plugin:

.. code-block:: python

   >>> from qiime.plugins import feature_table

We'll now explore some of the same methods and visualizers introduced in the :doc:`Moving Pictures tutorial <../tutorials/moving-pictures>`, this time in the Python interpreter instead of the command line interface. First, we'll load a QIIME 2 ``Artifact``, in this case a feature table. We'll then pass that to the ``q2-feature-table`` plugin's ``rarefy`` method, which will return a new Artifact.

.. code-block:: python

   >>> from qiime import Artifact
   >>> unrarefied_table = Artifact.load('table.qza')
   >>> rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100)
   >>> rarefied_table = rarefy_result.rarefied_table

While we recommend working with QIIME 2 ``Artifacts`` directly, it is possible to access the underlying data in one or more compatible *views* (Python objects/data structures or file formats). For example, you may want to access the rarefied feature table that was just created as a ``biom.Table`` object. You can do this as follows:

.. code-block:: python

   >>> import biom
   >>> biom_table = rarefied_table.view(biom.Table)
   >>> print(biom_table.head())
   # Constructed from biom file
   #OTU ID	K3.H	K3.Z	M2.Middle.L	K3.A	K3.R
   New.CleanUp.ReferenceOTU0	2.0	0.0	0.0	0.0	0.0
   New.CleanUp.ReferenceOTU1	0.0	1.0	1.0	0.0	1.0
   New.CleanUp.ReferenceOTU3	0.0	0.0	0.0	0.0	0.0
   New.CleanUp.ReferenceOTU7	0.0	0.0	0.0	0.0	0.0
   New.CleanUp.ReferenceOTU9	0.0	0.0	0.0	0.0	0.0

You can also view the artifact's data as a ``pandas.DataFrame`` object:

.. code-block:: python

   >>> import pandas as pd
   >>> df = rarefied_table.view(pd.DataFrame)
   >>> df.head()
                New.CleanUp.ReferenceOTU0  New.CleanUp.ReferenceOTU1  \
   K3.H                               2.0                        0.0
   K3.Z                               0.0                        1.0
   M2.Middle.L                        0.0                        1.0
   K3.A                               0.0                        0.0
   K3.R                               0.0                        1.0
   ...

A powerful feature of QIIME 2 is that you can export different types of views from QIIME artifacts as illustrated here, then operate on the resulting data types, and import those data back into QIIME. This is useful if there are some operations that are available on the view's data type (e.g., the ``pandas.DataFrame``) that are not available through the QIIME API. An important caveat is that you will lose all artifact provenance in the process, because QIIME can't track what happens to data outside of QIIME. You can import the ``pandas.DataFrame`` back into a new QIIME artifact as follows:

.. code-block:: python

   imported_artifact = Artifact.import_data("FeatureTable[Frequency]", df)

The ``rarefied_table`` artifact can be passed to methods of other QIIME 2 plugins. Here we'll compute the *Observed OTUs* alpha diversity metric using the ``q2-diversity`` plugin. The resulting ``Artifact`` will be of type ``SampleData[AlphaDiversity]``, and we can access a ``pd.Series`` as a view of this ``Artifact``.

.. code-block:: python

   >>> from qiime.plugins import diversity
   >>> alpha_result = diversity.methods.alpha(table=rarefied_table, metric='observed_otus')
   >>> alpha_diversity = alpha_result.alpha_diversity
   >>> alpha_diversity.view(pd.Series)
   K3.H           37
   K3.Z           49
   M2.Middle.L    32
   K3.A           35
   K3.R           48
   K3.V           46
   K3.K           36
   K3.B           48
   ...
   Name: observed_otus, dtype: int64

Finally, we can save our ``Artifacts`` as ``.qza`` files and exit the interpreter as follows:

.. code-block:: python

   >>> rarefied_table.save('rare.qza')
   >>> alpha_diversity.save('oo.qza')
   >>> exit

Another powerful feature of QIIME 2 is that you can combine interfaces. For example, you could develop a Python script that automatically processes files for you to generate results as we just did, and then perform analysis of those files using the :doc:`command line interface <q2cli>` or the :doc:`QIIME 2 Studio <q2studio>`. For instance, you could now continue your analysis and view some results on the command line as follows:

.. command-block::
   :no-exec:

   qiime diversity alpha-group-significance --i-alpha-diversity oo.qza --m-metadata-file sample-metadata.tsv  --o-visualization oo-group-significance

.. _`Jupyter Notebook`: http://jupyter.org/
