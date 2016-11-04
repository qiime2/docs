Developing a QIIME 2 plugin
===========================

.. note:: This document is a work in progress, and serves as basic instructions for creating a QIIME 2 plugin.

Creating a QIIME 2 plugin allows you to provide microbiome analysis functionality to QIIME 2 users. A plugin can be a standalone software project, or you can make a few small additions to your existing software project to make it a QIIME 2 plugin. Creating a single QIIME 2 plugin will make your functionality accessible through any QIIME 2 interface, including the :doc:`QIIME 2 Studio <../interfaces/q2studio>`, :doc:`q2cli <../interfaces/q2cli>`, and the :doc:`Artifact API <../interfaces/artifact-api>`.

Overview
--------

There are several high-level steps to creating a QIIME 2 plugin:

1. A QIIME 2 plugin must define one or more Python 3 functions that will be accessible through QIIME. The plugin must be a Python 3 package that can be installed with ``setuptools``.
2. The plugin must then instantiate a ``qiime.plugin.Plugin`` object and define some information including the name of the plugin and its URL. In the plugin package's ``setup.py`` file, this instance will be defined as an entry point.
3. The plugin must then register its functions as QIIME 2 ``Actions``, which will be accessible to users through any of the QIIME 2 interfaces.
4. Optionally, the plugin should be distributed through `Anaconda`_, as that will simplify its installation for QIIME 2 users (since that is the supported mechanism for installing QIIME 2).

These steps are covered in detail below.

Writing a simple QIIME 2 plugin should be a straightforward process. For example, the `q2-emperor`_ plugin, which connects `Emperor`_ to QIIME 2, is written in only around 100 lines of code. It is a standalone plugin that defines how and which functionality in Emperor should be accessible through QIIME 2. Plugins will vary in their complexity. For example, a plugin that defines a lot of new functionality would likely be quite a bit bigger. `q2-diversity`_ is a good example of this. Unlike ``q2-emperor``, there is some specific functionality (and associated unit tests) defined in this project, and it depends on several other Python 3 compatible libraries.

Before starting to write a plugin, you should :doc:`install QIIME 2 and some plugins <../install>` to familiarize yourself with the system and to provide a means for testing your plugin.

Initializing a plugin package
-----------------------------

For convenience, tools are provided to help developers initialize a QIIME 2 plugin package. An initialized plugin includes examples of functionality that can be executed out of the box (no changes to the plugin's code are required!). Once you are familiar with the example functionality provided in the plugin, you can update relevant sections of the plugin to support your own functionality. There are comments in the generated plugin code indicating relevant sections to remove or update, and this document describes each plugin component in detail below.

.. note:: QIIME 2 does not place restrictions on how a plugin package is structured. The plugin initializer tool uses the package structure and conventions present in other QIIME 2 plugins. This package structure is simply a recommendation and a starting point for developing your own plugin; feel free to modify the initialized plugin as necessary or desired.

The easiest way to initialize a plugin package is via :doc:`q2cli's <../interfaces/q2cli>` ``qiime dev plugin-init`` command. For example, to initialize a plugin package directory in your current working directory:

.. command-block::
   :no-exec:

   qiime dev plugin-init

Use the ``--output-dir`` option to create a plugin directory in a location other than the current working directory.

After running the above command, you will be prompted to enter several pieces of information about your plugin, including the plugin name, description, author details, etc. **Defaults are provided as examples only**; you must provide the relevant information about your plugin. The prompts only gather basic information about your plugin so a functioning package can be initialized. There are other pieces of the plugin that can be manually configured (detailed below).

Assuming all default values were used in response to the above command's prompts, you should see that a ``q2-my-plugin`` directory was created in your current working directory. This directory contains the initialized plugin package based on the information you provided.

The plugin includes some example functionality that you can try out (for example, using ``q2cli``). If you intend to use the plugin's example functionality, install `q2-dummy-types`_, which provides the semantic types used by the plugin:

.. command-block::
   :no-exec:

   conda install -c qiime2 q2-dummy-types

Next, navigate to the plugin directory that was created and install the plugin in development mode:

.. command-block::
   :no-exec:

   cd q2-my-plugin
   pip install -e .

To see that the plugin is discoverable by QIIME, run:

.. command-block::
   :no-exec:

   qiime

You should see ``my-plugin`` listed as one of the available commands. To see the available plugin commands:

.. command-block::
   :no-exec:

   qiime my-plugin --help

Once you are done exploring the plugin's example functionality, update it with your own. The relevant sections of the code that need to change are commented.

The following sections describe various plugin components, configuration, and how to define your own functionality. As you read through the following sections, it may be useful to refer back to the example functionality defined in the plugin to see how it is implemented.

.. note:: The initialized plugin also includes some basic continuous integration configuration for `Travis-CI`_, including ``flake8`` linting/style-checking and a ``nose`` command for running unit tests (you'll need to enable Travis-CI on your repository for your tests to be run). There aren't any unit tests included in the initialized plugin; plugin developers are encouraged to add unit tests for their plugin's functionality. The initialized plugin's code is flake8-compliant.

Plugin components
-----------------

The following discussion will refer to the `q2-diversity`_ plugin as an example. This plugin will serve as a reference as you define your own QIIME 2 plugins, in addition to the initialized plugin you created above.

Define functionality
++++++++++++++++++++

QIIME 2 users will access your functionality as QIIME 2 ``Actions``. These ``Actions`` can be either ``Methods`` and/or ``Visualizers``. A ``Method`` is an operation that takes some combination of ``Artifacts`` and ``Parameters`` as input, and produces one or more ``Artifacts`` as output. These output ``Artifacts`` could subsequently be used as input to other QIIME 2 ``Methods`` or ``Visualizers``. A ``Visualizer`` is an operation that takes some combination of ``Artifacts`` and ``Parameters`` as input, and produces exactly one ``Visualization`` as output. Output ``Visualizations``, by definition, cannot be used as input to other QIIME 2 ``Methods`` or ``Visualizers``. ``Methods`` therefore can produce intermediate or terminal output in a QIIME analysis, while ``Visualizers`` can only create terminal output.

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

``q2_diversity.alpha_group_significance`` is an example of a function that can be registered as a ``Visualizer``. In addition to its ``output_dir``, it takes alpha diversity results in a ``pandas.Series`` and sample metadata in a ``qiime.Metadata`` object and creates several different files (figures and tables) that are linked and/or presented in an ``index.html`` file. The signature of this function is:

.. code-block:: python

   def alpha_group_significance(output_dir: str, alpha_diversity: pd.Series,
                                metadata: qiime.Metadata) -> None:

Instantiating a plugin
++++++++++++++++++++++

The next step is to instantiate a QIIME 2 ``Plugin`` object. This might look like the following:

.. code-block:: python

   from qiime.plugin import Plugin
   import q2_diversity

   plugin = Plugin(
       name='diversity',
       version=q2_diversity.__version__,
       website='https://github.com/qiime2/q2-diversity',
       package='q2_diversity'
   )

This will provide QIIME with essential information about your ``Plugin``.

The ``name`` parameter is the name that users will use to access your plugin from within different QIIME 2 interfaces. It should be a "command line friendly" name, so should not contain spaces or punctuation. (Avoiding uppercase characters and using dashes (``-``) instead of underscores (``_``) are preferable in the plugin ``name``, but not required).

``version`` should be the version number of your package (the same that is used in its ``setup.py``).

``website`` should be the page where you'd like end users to refer for more information about your package.

``package`` should be the Python package name for your plugin.

While not shown in the previous example, plugin developers can optionally provide the following parameters to ``qiime.plugin.Plugin``:

* ``citation_text``: free text describing how users should cite the plugin and/or the underlying tools it wraps. If not provided, users are told to cite the ``website``.

* ``user_support_text``: free text describing how users should get help with the plugin (e.g. issue tracker, StackOverflow tag, mailing list, etc.). If not provided, users are referred to the ``website`` for support.

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
   from qiime.plugin import Str, Choices, Properties, Metadata

   import q2_diversity
   import q2_diversity._beta as beta

   plugin.methods.register_function(
       function=q2_diversity.beta_phylogenetic,
       inputs={'table': FeatureTable[Frequency],
               'phylogeny': Phylogeny[Rooted]},
       parameters={'metric': Str % Choices(beta.phylogenetic_metrics())},
       outputs=[('distance_matrix', DistanceMatrix % Properties('phylogenetic'))],
       name='Beta diversity (phylogenetic)',
       description=("Computes a user-specified phylogenetic beta diversity metric"
                    " for all pairs of samples in a feature table.")
   )

The values being provided are:

``function``: The function to be registered as a method.

``inputs``: A dictionary indicating the parameter name and its *semantic type*, for each input ``Artifact``. These semantic types differ from the data types that you provided in your `mypy`_ annotation of the input, as semantic types describe the data, where the data types indicate the structure of the data. The currently available semantic types are :doc:`detailed here <../semantic-types>`, along with a discussion of the motivation for defining semantic types. In the example above we're indicating that the ``table`` parameter must be a ``FeatureTable`` of ``Frequency`` (i.e. counts), and that the ``phylogeny`` parameter must be a ``Phylogeny`` that is ``Rooted``.  Notice that the keys in ``inputs`` map directly to the parameter names in ``q2_diversity.beta_phylogenetic``.

``parameters``: A dictionary indicating the parameter name and its *semantic type*, for each input ``Parameter``. These parameters are primitive values (i.e., non-``Artifacts``). In the example above, we're indicating that the ``metric`` should be a string from a specific set (in this case, the set of known phylogenetic beta diversity metrics).

``outputs``: A list of tuples indicating each output name and its semantic type.

``name``: A human-readable name for the ``Method``. This may be presented to users in interfaces.

``description``: A human-readable description of the ``Method``. This may be presented to users in interfaces.

Registering a Visualizer
~~~~~~~~~~~~~~~~~~~~~~~~

Registering ``Visualizers`` is the same as registering ``Methods``, with two exceptions.

First, you call ``plugin.visualizers.register_function`` to register a ``Visualizer``.

Next, you do not provide ``outputs`` when making this call, as ``Visualizers``, by definition, do not return anything (they only write to ``output_dir``). Since ``output_dir`` is a required parameter, you do not include this in the ``parameters`` list (it would be the same for every ``Visualizer`` that was ever registered, so it is added automatically).

Registering ``q2_diversity.alpha_group_significance`` as a ``Visualizer`` looks like the following:

.. code-block:: python

   plugin.visualizers.register_function(
       function=q2_diversity.alpha_group_significance,
       inputs={'alpha_diversity': SampleData[AlphaDiversity]},
       parameters={'metadata': Metadata},
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
           'qiime.plugins': ['q2-diversity=q2_diversity.plugin_setup:plugin']
       }
   )

The relevant key in the ``entry_points`` dictionary will be ``'qiime.plugins'``, and the value will be a single element list containing a string formatted as ``<distribution-name>=<import-path>:<instance-name>``. ``<distribution-name>`` is the name of the Python package distribution (matching the value passed for ``name`` in this call to ``setup``); ``<import-path>`` is the import path for the ``Plugin`` instance you created above; and ``<instance-name>`` is the name for the ``Plugin`` instance you created above.

Advanced plugin development
---------------------------

Defining semantic types, data layouts, and view readers/writers
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This section is currently stubbed and will be completed during the alpha release phase. For examples of plugins that define semantic types, data layouts, and view readers/writers, see `q2-dummy-types`_ and `q2-types`_. ``q2-dummy-types`` provides simple examples with heavily-commented code, and ``q2-types`` provides more complex types for bioinformatics/microbiome analyses.

Example plugins
---------------

* `q2-emperor`_: This is a simple plugin that is defined as a stand-alone package. It provides QIIME 2 access to functionality defined in `Emperor`_.

* `q2-diversity`_: This is a more complex plugin, where the plugin is defined in the same package as the functionality that it's providing access to.

* `q2-dummy-types`_: This is a simple plugin defining dummy QIIME 2 types to serve as examples for plugin developers creating their own semantic types.

* `q2-types`_: This is a more complex plugin defining real-world QIIME 2 types for bioinformatics/microbiome analyses.

.. _`Anaconda`: https://anaconda.org/

.. _`q2-emperor`: https://github.com/qiime2/q2-emperor

.. _`Emperor`: https://github.com/biocore/emperor

.. _`q2-diversity`: https://github.com/qiime2/q2-diversity

.. _`q2-dummy-types`: https://github.com/qiime2/q2-dummy-types

.. _`Travis-CI`: https://travis-ci.org/

.. _`mypy`: http://mypy-lang.org/

.. _`q2-types`: https://github.com/qiime2/q2-types
