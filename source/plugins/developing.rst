Developing a QIIME 2 plugin
===========================

.. note:: This document is a work in progress, and serves as basic instructions for creating a QIIME 2 plugin. You can also find some (very preliminary) developer documentation at `https://dev.qiime2.org <https://dev.qiime2.org/latest/>`__.

Creating a QIIME 2 plugin allows you to provide microbiome analysis functionality to QIIME 2 users. A plugin can be a standalone software project, or you can make a few small additions to your existing software project to make it a QIIME 2 plugin. Creating a single QIIME 2 plugin will make your functionality accessible through any QIIME 2 interface, including the :doc:`QIIME 2 Studio <../interfaces/q2studio>`, :doc:`q2cli <../interfaces/q2cli>`, and the :doc:`Artifact API <../interfaces/artifact-api>`.

Overview
--------

There are several high-level steps to creating a QIIME 2 plugin:

1. A QIIME 2 plugin must define one or more Python 3 functions that will be accessible through QIIME. The plugin must be a Python 3 package that can be installed with ``setuptools``.
2. The plugin must then instantiate a ``qiime2.plugin.Plugin`` object and define some information including the name of the plugin and its URL. In the plugin package's ``setup.py`` file, this instance will be defined as an entry point.
3. The plugin must then register its functions as QIIME 2 ``Actions``, which will be accessible to users through any of the QIIME 2 interfaces.
4. Optionally, the plugin should be distributed through `Anaconda`_, as that will simplify its installation for QIIME 2 users (since that is the supported mechanism for installing QIIME 2).

These steps are covered in detail below.

Writing a simple QIIME 2 plugin should be a straightforward process. For example, the `q2-emperor`_ plugin, which connects `Emperor`_ to QIIME 2, is written in only around 100 lines of code. It is a standalone plugin that defines how and which functionality in Emperor should be accessible through QIIME 2. Plugins will vary in their complexity. For example, a plugin that defines a lot of new functionality would likely be quite a bit bigger. `q2-diversity`_ is a good example of this. Unlike ``q2-emperor``, there is some specific functionality (and associated unit tests) defined in this project, and it depends on several other Python 3 compatible libraries.

Before starting to write a plugin, you should :doc:`install QIIME 2 and some plugins <../install/index>` to familiarize yourself with the system and to provide a means for testing your plugin.

Plugin components
-----------------

The following discussion will refer to the `q2-diversity`_ plugin as an example. This plugin can serve as a reference as you define your own QIIME 2 plugins.

.. note:: **QIIME 2 does not place restrictions on how a plugin package is structured.** The `q2-diversity`_ plugin is however a good representative of the conventions present in many of the initial QIIME 2 plugins. This package structure is simply a recommendation and a starting point for developing your own plugin; feel free to deviate from this structure as necessary or desired.

Define functionality
++++++++++++++++++++

QIIME 2 users will access your functionality as QIIME 2 ``Actions``. These ``Actions`` can be either ``Methods`` or ``Visualizers``. A ``Method`` is an operation that takes some combination of ``Artifacts`` and ``Parameters`` as input, and produces one or more ``Artifacts`` as output. These output ``Artifacts`` could subsequently be used as input to other QIIME 2 ``Methods`` or ``Visualizers``. A ``Visualizer`` is an operation that takes some combination of ``Artifacts`` and ``Parameters`` as input, and produces exactly one ``Visualization`` as output. Output ``Visualizations``, by definition, cannot be used as input to other QIIME 2 ``Methods`` or ``Visualizers``. ``Methods`` therefore can produce intermediate or terminal output in a QIIME analysis, while ``Visualizers`` can only create terminal output.

This section will describe how to define Python 3 functions that can be converted to QIIME 2 ``Methods`` or ``Visualizers``. These functions can be defined anywhere in your project; QIIME doesn't put restrictions on how your plugin package is structured.

Create a function to register as a Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A function that can be registered as a ``Method`` will have a Python 3 API, and the inputs and outputs for that function will be annotated with their data types using `mypy`_ syntax. mypy annotation does not impact functionality (though the syntax is new to Python 3), so these can be added to existing functions in your Python 3 software project. An example is ``q2_diversity.beta_phylogenetic``, which takes a ``biom.Table``, an ``skbio.TreeNode`` and a ``str`` as input, and produces an ``skbio.DistanceMatrix`` as output. The signature for this function is:

.. code-block:: python

   def beta_phylogenetic(table: biom.Table, phylogeny: skbio.TreeNode,
                         metric: str)-> skbio.DistanceMatrix:

As far as QIIME is concerned, it doesn't matter what happens inside this function (as long as it adheres to the contract defined by the signature regarding the input and output types). For example, ``q2_diversity.beta_phylogenetic`` is making some calls to the ``skbio`` and ``biom`` APIs, but it could be doing anything, including making system calls (if your plugin is wrapping a command line application), executing an R library, etc.

Create a function to register as a Visualizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defining a function that can be registered as a ``Visualizer`` is very similar to defining one that can be registered as a ``Method`` with a few additional requirements.

First, the first parameter to this function must be ``output_dir``. This parameter should be annotated with type ``str``.

Next, at least one ``index.*`` file must be written to ``output_dir`` by the function. This index file will provide the starting point for your users to explore the ``Visualization`` object that is generated by the ``Visualizer``. Index files with different extensions can be created by the function (e.g., ``index.html``, ``index.tsv``, ``index.png``), but at least one must be created. You can write whatever files you want to ``output_dir``, including tables, graphics, and textual descriptions of the results, but you should expect that your users will want to find those files through your index file(s). If your function does create many different files, an ``index.html`` containing links to those files is likely to be helpful.

Finally, the function cannot return anything, and its return type should be annotated as ``None``.

``q2_diversity.alpha_group_significance`` is an example of a function that can be registered as a ``Visualizer``. In addition to its ``output_dir``, it takes alpha diversity results in a ``pandas.Series`` and sample metadata in a ``qiime2.Metadata`` object and creates several different files (figures and tables) that are linked and/or presented in an ``index.html`` file. The signature of this function is:

.. code-block:: python

   def alpha_group_significance(output_dir: str, alpha_diversity: pd.Series,
                                metadata: qiime2.Metadata) -> None:

Instantiating a plugin
++++++++++++++++++++++

The next step is to instantiate a QIIME 2 ``Plugin`` object. This might look like the following:

.. code-block:: python

   from qiime2.plugin import Plugin
   import q2_diversity

   plugin = Plugin(
       name='diversity',
       version=q2_diversity.__version__,
       website='https://qiime2.org',
       user_support_text='https://forum.qiime2.org',
       package='q2_diversity'
   )

This will provide QIIME with essential information about your ``Plugin``.

The ``name`` parameter is the name that users will use to access your plugin from within different QIIME 2 interfaces. It should be a "command line friendly" name, so should not contain spaces or punctuation. (Avoiding uppercase characters and using dashes (``-``) instead of underscores (``_``) are preferable in the plugin ``name``, but not required).

``version`` should be the version number of your package (the same that is used in its ``setup.py``).

``website`` should be the page where you'd like end users to refer for more information about your package. Since ``q2-diversity`` doesn't have its own website, we're including the QIIME 2 website here.

``package`` should be the Python package name for your plugin.

While not shown in the previous example, plugin developers can optionally provide the following parameters to ``qiime2.plugin.Plugin``:

* ``citation_text``: free text describing how users should cite the plugin and/or the underlying tools it wraps. If not provided, users are told to cite the ``website``.

* ``user_support_text``: free text describing how users should get help with the plugin (e.g. issue tracker, StackOverflow tag, mailing list, etc.). If not provided, users are referred to the ``website`` for support. ``q2-diversity`` is supported on the QIIME 2 Forum, so we include that URL here. We encourage plugin developers to support their plugins on the QIIME 2 Forum, so you can include that URL as the ``user_support_text`` for your plugin. If you do that, you should get in the habit of monitoring the QIIME 2 Forum for technical support questions.

The ``Plugin`` object can live anywhere in your project, but by convention it will be in a file called ``plugin_setup.py``. For an example, see ``q2_diversity/plugin_setup.py``.

Registering an Action
+++++++++++++++++++++

Once you have functions that you'd like to register as ``Actions`` (i.e., either ``Methods`` or ``Visualizers``), and you've instantiated your ``Plugin`` object, you are ready to register those functions. This will likely be done in the file where the ``Plugin`` object was instantiated, as it will use that instance (which will be referred to as ``plugin`` in the following examples).

Registering a Method
~~~~~~~~~~~~~~~~~~~~

First we'll register a ``Method`` by calling ``plugin.methods.register_function`` as follows:

.. code-block:: python

   from q2_types import (FeatureTable, Frequency, Phylogeny,
                         Rooted, DistanceMatrix)
   from qiime2.plugin import Str, Choices, Properties, Metadata

   import q2_diversity
   import q2_diversity._beta as beta

   plugin.methods.register_function(
       function=q2_diversity.beta_phylogenetic,
       inputs={'table': FeatureTable[Frequency],
               'phylogeny': Phylogeny[Rooted]},
       parameters={'metric': Str % Choices(beta.phylogenetic_metrics())},
       outputs=[('distance_matrix', DistanceMatrix % Properties('phylogenetic'))],
       input_descriptions={
           'table': ('The feature table containing the samples over which beta '
                     'diversity should be computed.'),
           'phylogeny': ('Phylogenetic tree containing tip identifiers that '
                         'correspond to the feature identifiers in the table. '
                         'This tree can contain tip ids that are not present in '
                         'the table, but all feature ids in the table must be '
                         'present in this tree.')
       },
       parameter_descriptions={
           'metric': 'The beta diversity metric to be computed.'
       },
       output_descriptions={'distance_matrix': 'The resulting distance matrix.'},
       name='Beta diversity (phylogenetic)',
       description=("Computes a user-specified phylogenetic beta diversity metric"
                    " for all pairs of samples in a feature table.")
   )

The values being provided are:

``function``: The function to be registered as a method.

``inputs``: A dictionary indicating the parameter name and its *semantic type*, for each input ``Artifact``. These semantic types differ from the data types that you provided in your `mypy`_ annotation of the input, as semantic types describe the data, where the data types indicate the structure of the data. The currently available semantic types are :doc:`detailed here <../semantic-types>`, along with a discussion of the motivation for defining semantic types. In the example above we're indicating that the ``table`` parameter must be a ``FeatureTable`` of ``Frequency`` (i.e. counts), and that the ``phylogeny`` parameter must be a ``Phylogeny`` that is ``Rooted``.  Notice that the keys in ``inputs`` map directly to the parameter names in ``q2_diversity.beta_phylogenetic``.

``parameters``: A dictionary indicating the parameter name and its *semantic type*, for each input ``Parameter``. These parameters are primitive values (i.e., non-``Artifacts``). In the example above, we're indicating that the ``metric`` should be a string from a specific set (in this case, the set of known phylogenetic beta diversity metrics).

``outputs``: A list of tuples indicating each output name and its semantic type.

``input_descriptions``: A dictionary containing input artifact names and their corresponding descriptions. This information is used by interfaces to instruct users how to use each specific input artifact.

``parameter_descriptions``: A dictionary containing parameter names and their corresponding descriptions. This information is used by interfaces to instruct users how to use each specific input parameter. You should not include any default parameter values in these descriptions, as these will generally be added automatically by an interface.

``output_descriptions``: A dictionary containing output artifact names and their corresponding descriptions. This information is used by interfaces to inform users what each specific output artifact will be.

``name``: A human-readable name for the ``Method``. This may be presented to users in interfaces.

``description``: A human-readable description of the ``Method``. This may be presented to users in interfaces.

Registering a Visualizer
~~~~~~~~~~~~~~~~~~~~~~~~

Registering ``Visualizers`` is the same as registering ``Methods``, with two exceptions.

First, you call ``plugin.visualizers.register_function`` to register a ``Visualizer``.

Next, you do not provide ``outputs`` or ``output_descriptions`` when making this call, as ``Visualizers``, by definition, only return a single visualization. Since the visualization output path is a required parameter, you do not include this in an ``outputs`` list (it would be the same for every ``Visualizer`` that was ever registered, so it is added automatically).

Registering ``q2_diversity.alpha_group_significance`` as a ``Visualizer`` looks like the following:

.. code-block:: python

   plugin.visualizers.register_function(
       function=q2_diversity.alpha_group_significance,
       inputs={'alpha_diversity': SampleData[AlphaDiversity]},
       parameters={'metadata': Metadata},
       input_descriptions={
           'alpha_diversity': 'Vector of alpha diversity values by sample.'
       },
       parameter_descriptions={
           'metadata': 'The sample metadata.'
       },
       name='Alpha diversity comparisons',
       description=("Visually and statistically compare groups of alpha diversity"
                    " values.")
   )

Defining your plugin object as an entry point
+++++++++++++++++++++++++++++++++++++++++++++

Finally, you need to tell QIIME where to find your instantiated ``Plugin`` object. This is done by defining it as an ``entry_point`` in your project's ``setup.py`` file. In ``q2-diversity``, this is done as follows:

.. code-block:: python

   setup(
       ...
       entry_points={
           'qiime2.plugins': ['q2-diversity=q2_diversity.plugin_setup:plugin']
       }
   )

The relevant key in the ``entry_points`` dictionary will be ``'qiime2.plugins'``, and the value will be a single element list containing a string formatted as ``<distribution-name>=<import-path>:<instance-name>``. ``<distribution-name>`` is the name of the Python package distribution (matching the value passed for ``name`` in this call to ``setup``); ``<import-path>`` is the import path for the ``Plugin`` instance you created above; and ``<instance-name>`` is the name for the ``Plugin`` instance you created above.

Testing your plugin with q2cli during development
-------------------------------------------------

If you are testing your plugin with ``q2cli`` (i.e. the ``qiime`` command) while you are developing it, you'll need to run ``qiime dev refresh-cache`` to see the latest changes to your plugin reflected in the command line interface (CLI). You'll need to run this command anytime you modify your plugin's interface (e.g. add/rename/remove a command or its inputs/parameters/outputs, and edit any of the plugin/action/input/parameter/output descriptions).

Another option is to set the environment variable ``Q2CLIDEV=1`` so that the cache is refreshed every time a command is run. This will slow down the CLI while developing because refreshing the cache is slow. However, the CLI is much faster when a user installs release versions of QIIME 2 and plugins, so this slowdown should only be apparent when *developing* a plugin.

This manual refreshing of the ``q2cli`` cache is necessary because it can't detect when changes are made to a plugin's code while under development (the plugin's version remains the same across code edits). This manual refreshing of the cache should only be necessary while developing a plugin; when users install QIIME 2 and your released plugin (i.e. no longer in development), the cache will automatically be updated when necessary.

Plugin testing
--------------

Many of the QIIME 2 plugins, including `q2-emperor`_ and `q2-diversity`_, have continuous integration (CI) configuration for `Travis-CI`_ in their software repositories. This allows for automated testing any time a change to the plugin code is committed on GitHub if Travis-CI is enabled on the plugin's software repository. Plugin CI testing generally includes ``flake8`` linting/style-checking and a ``nose`` or ``py.test`` command for running unit tests.

Plugin developers are encouraged to add unit tests for their plugin's functionality, and to perform style checking with ``flake8``. Unit tests are an important part of determining if your software is working as expected, which will give you and your users confidence in the plugin. Adhering to a style convention, and checking that style with a tool like ``flake8``, is very helpful for others who want to understand your code, including users who want an in depth understanding of the functionality and potential open source software contributors.

`Wilson et al. (2014)`_ present a good discussion of software testing and related topics that is very helpful for scientists who are beginning to develop and distribute software.

Advanced plugin development
---------------------------

Defining semantic types, data layouts, and view readers/writers
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This section is currently incomplete. In the meantime, if you have questions about these advanced plugin development topics, feel free to get in touch with us on the `forum`_. For an example of a plugin that define semantic types, data layouts, and view readers/writers, see `q2-types`_.

Example plugins
---------------

* `q2-emperor`_: This is a simple plugin that is defined as a stand-alone package. It provides QIIME 2 access to functionality defined in `Emperor`_.

* `q2-diversity`_: This is a more complex plugin, where the plugin is defined in the same package as the functionality that it's providing access to.

* `q2-types`_: This is a more complex plugin defining real-world QIIME 2 types for bioinformatics/microbiome analyses.

.. _`Anaconda`: https://anaconda.org/

.. _`q2-emperor`: https://github.com/qiime2/q2-emperor

.. _`Emperor`: https://github.com/biocore/emperor

.. _`q2-diversity`: https://github.com/qiime2/q2-diversity

.. _`Travis-CI`: https://travis-ci.org/

.. _`mypy`: http://mypy-lang.org/

.. _`q2-types`: https://github.com/qiime2/q2-types

.. _`forum`: https://forum.qiime2.org

.. _`Wilson et al. (2014)`: http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745
