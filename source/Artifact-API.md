# Artifact API

**This guide assumes you have performed the steps in the [Moving Pictures tutorial](../tutorials/moving-pictures). The `table.qza` and `sample-metadata.tsv` files generated in that tutorial are used here.**

The Artifact API is an application programmer interface for QIIME 2. This is useful for interactive use of QIIME 2, including in Jupyter Notebooks which is currently our primary target for use of this interface. The Artifact API is a part of the QIIME 2 framework, so does not need to be installed separately. This API is automatically generated, depending on which plugins are currently installed. To see this in action, begin by uninstalling the ``q2-feature-table`` plugin.

```bash
conda uninstall q2-feature-table
```

Then, open a Python interpreter such as IPython and enter the following command. You should get an error telling you that the plugin you're trying to access is not available. Leave the interpreter by typing ``exit``.

```python
>>> from qiime.plugins import feature_table
ImportError: cannot import name 'feature_table'
>>> exit
```

Then, reinstall the ``q2-feature-table`` and ``q2-diversity`` plugins (`q2-diversity` was uninstalled automatically when we uninstalled `q2-feature-table` above because it depends on `q2-feature-table`).

```bash
conda install -c qiime2 q2-feature-table q2-diversity
```

Open your interpreter, and you should now be able to import this plugin:

```python
>>> from qiime.plugins import feature_table
```

We'll now explore some of the same methods and visualizers, but this time in the interpreter. First, we'll load a QIIME 2 ``Artifact``, in this case a feature table. We'll then pass that to the ``q2-feature-table`` plugin's ``rarefy`` method, which will return a new Artifact.

```python
>>> from qiime import Artifact
>>> rarefy_result = feature_table.methods.rarefy(table=Artifact.load('table.qza'), sampling_depth=100)
```

While we recommend working with QIIME 2 ``Artifacts`` directly, it is possible to access the underlying data in one or more compatible *views* (or Python objects/data structures). For example, you may want to access the rarefied feature table that was just created as a ``biom.Table`` object. You can do this as follows:

```python
>>> import biom
>>> biom_table = rarefy_result.rarefied_table.view(biom.Table)
>>> print(biom_table.head())
# Constructed from biom file
#OTU ID	K3.H	K3.Z	M2.Middle.L	K3.A	K3.R
New.CleanUp.ReferenceOTU0	2.0	0.0	0.0	0.0	0.0
New.CleanUp.ReferenceOTU1	0.0	1.0	1.0	0.0	1.0
New.CleanUp.ReferenceOTU3	0.0	0.0	0.0	0.0	0.0
New.CleanUp.ReferenceOTU7	0.0	0.0	0.0	0.0	0.0
New.CleanUp.ReferenceOTU9	0.0	0.0	0.0	0.0	0.0
```

You can also view the artifact's data as a `pandas.DataFrame` object:

```python
>>> import pandas as pd
>>> df = rarefy_result.rarefied_table.view(pd.DataFrame)
>>> df.head()
             New.CleanUp.ReferenceOTU0  New.CleanUp.ReferenceOTU1  \
K3.H                               2.0                        0.0
K3.Z                               0.0                        1.0
M2.Middle.L                        0.0                        1.0
K3.A                               0.0                        0.0
K3.R                               0.0                        1.0
...
```

A powerful feature of QIIME 2 is that you can export different types of views from QIIME artifacts as illustrated here, then operate on the resulting data types, and import those data back into QIIME. This is useful if there are some operations that are available on the view's data type (e.g., the `pandas.DataFrame`) that are not available through the QIIME API. (An important caveat is that you will lose all artifact provenance in the process, because QIIME can't track what happens to data outside of QIIME. ) You can import the `pandas.DataFrame` back into a new QIIME artifact as follows:

```python
imported_artifact = Artifact.import_data("FeatureTable[Frequency]", df)
```

The ``rarefied_table`` artifact can be passed to methods of other QIIME 2 plugins. Here we'll compute the *Observed OTUs* alpha diversity metric using the ``q2-diversity`` plugin. The resulting ``Artifact`` will be of type ``SampleData[AlphaDiversity]``, and we can access a ``pd.Series`` as a view of this ``Artifact``.

```python
>>> from qiime.plugins import diversity
>>> alpha_result = diversity.methods.alpha(table=rarefy_result.rarefied_table, metric='observed_otus')
>>> alpha_result.alpha_diversity.view(pd.Series)
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
```

Finally, we can save our ``Artifacts`` and exit the interpreter as follows:

```python
>>> rarefy_result.rarefied_table.save('rare.qza')
>>> alpha_result.alpha_diversity.save('oo.qza')
>>> exit
```

Another powerful feature of QIIME 2 is that you can combine interfaces. For example, you could develop a Python script that automatically processes files for you to generate results as we just did, and then perform analysis of those files using the command line interface or [QIIME 2 Studio](QIIME-2-Studio.html). For example, you could now continue your analysis and view some results on the command line as follows:

```bash
qiime diversity alpha-group-significance --i-alpha-diversity oo.qza --m-metadata-file sample-metadata.tsv  --o-visualization oo-group-significance
```
