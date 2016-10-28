Installing QIIME 2
==================

.. note:: QIIME 2 does not currently support Windows. It is something we will be working on soon, and in the meantime we recommend using a virtual machine or services such as Amazon Elastic Compute Cloud if a Unix/Mac platform is not available to you.

This document describes how to install the QIIME 2 framework, a command-line interface, and some plugins used in the :doc:`tutorials <tutorials/index>`.

Install Miniconda
-----------------

`Miniconda`_ is the recommended way to install QIIME 2, which provides the ``conda`` environment and package manager. Follow the instructions for downloading and installing Miniconda.

.. tip:: You may choose either Miniconda2 or Miniconda3 (i.e. Miniconda Python 2 or 3) as QIIME 2 will work with either version of Miniconda.

Create a conda environment and install QIIME 2
--------------------------------------------------

Once you have Miniconda installed, create a ``conda`` environment to install QIIME 2 software in. You can use an existing environment if you have one, though we recommend creating an environment specifically for QIIME 2 as there are many required dependencies that you may not want added to an existing environment.

You can choose whatever name you'd like for the environment. In this example, we'll name the environment ``qiime2``. While creating the environment, we will also instruct ``conda`` to install Python 3.5, the QIIME 2 framework, and `q2cli`_ (a command-line interface for QIIME 2).

.. command-block::
   :no-exec:

   conda create -n qiime2 -c qiime2 python=3.5 qiime q2cli

``-n qiime2`` specifies the name of the environment, and ``-c qiime2`` specifies the channel to search for packages.

Now that you have an environment, activate it using the environment's name:

.. command-block::
   :no-exec:

   source activate qiime2

To deactivate an environment, run ``source deactivate``.

Try out the command-line interface
----------------------------------

Installing ``q2cli`` includes a new command, ``qiime``, to execute QIIME analyses from the command line. Run ``qiime`` to see the available commands. You can discover what plugins you currently have installed (there aren't any installed yet), as well as other information about your QIIME deployment, by running ``qiime info``.

.. command-block::

   qiime
   qiime info

.. tip:: Supply ``--help`` to any command to display information about the command, including any subcommands, options, and arguments the command defines.

Enable command-line tab completion
----------------------------------

If you are using Bash as your shell (you probably are), you can enable tab completion, which substantially improves the usability of the QIIME 2 command-line interface (CLI). When tab completion is enabled, pressing the tab key will attempt to complete the command or option you have typed, or provide you with a list of available commands or options based on what you have typed so far. This reduces the amount of typing you have to do and makes commands and options more easily discoverable without passing ``--help`` to every command you're wanting to run.

.. tip:: QIIME 2 CLI tab completion is currently only supported in the Bash shell. To check what shell you have, run ``echo $0``. You should see ``-bash`` in the output.

Run this command to enable tab completion:

.. command-block::

   source tab-qiime

You will need to run this command each time you open a new terminal and activate your QIIME 2 ``conda`` environment.

.. note::

   You can add the ``source tab-qiime`` command to your ``.bashrc``/``.bash_profile`` to avoid running the command each time you open a new terminal and activate your QIIME 2 environment. If you choose to do this, you will need ``q2cli`` available when your terminal opens, as that's when the command will be executed in your ``.bashrc``/``.bash_profile``. Since ``conda`` environments are the recommended way of installing and using QIIME 2, this is typically not the case, unless you have ``q2cli`` installed to your root ``conda`` environment or the relevant environment is activated before ``source tab-qiime`` is executed in the file.

To test that tab completion is working, try typing in the following (partial) command, and without actually running the command, press the tab key. If tab completion is working, the command should auto-complete the ``info`` command.

.. command-block::
   :no-exec:

   qiime i

Install plugins
---------------

Out of the box, installing the QIIME 2 framework and command-line interface does not provide microbiome analysis functionality (plugins provide this). Install the ``q2-types`` and ``q2-feature-table`` plugins:

.. command-block::
   :no-exec:

   conda install matplotlib==1.5.1
   conda install -c qiime2 q2-types q2-feature-table

Now execute the ``qiime info`` command again:

.. command-block::

   qiime info

All installed plugins will be listed here, so you should now see that you have two plugins installed.

If you run ``qiime`` again, you'll see that you have a new command available corresponding to the ``q2-feature-table`` plugin. The ``q2-types`` plugin does not have any actions to perform so it is not listed as a subcommand (``q2-types`` only defines semantic types and data formats used by many of the plugins). To see what actions the ``q2-feature-table`` plugin defines, run:

.. command-block::

   qiime feature-table

You will also see some other information about the plugin here, including its website, how it should be cited, and how users can get technical support with the plugin.

Install the ``q2-diversity`` and ``q2-emperor`` plugins as well:

.. command-block::
   :no-exec:

   conda install -c qiime2 -c conda-forge q2-diversity q2-emperor emperor=1.0.0beta5

You'll now have four plugins installed:

.. command-block::

   qiime info
   qiime diversity
   qiime emperor

To see more information about an action provided by a plugin, pass ``--help`` to the command. For example, running the following command will display information about the phylogenetic beta-diversity support provided by ``q2-diversity``:

.. command-block::

   qiime diversity beta-phylogenetic --help

Let's wrap up by installing several more plugins used in the tutorials.

.. command-block::
   :no-exec:

   conda install -c bioconda -c r bioconductor-dada2 mafft
   conda install -c biocore fasttree
   conda install -c qiime2 q2-demux q2-alignment q2-phylogeny q2-dada2 q2-composition q2-taxa q2-feature-classifier

Now that you have some plugins installed and have explored the command-line interface a bit, you're ready to analyze microbiome data! Check out the :doc:`QIIME 2 tutorials <tutorials/index>` for analyses of tutorial datasets.

Working with other QIIME 2 interfaces
-------------------------------------

So far we have seen how to install QIIME 2 and explore its command-line interface. In the same way that QIIME 2 plugins can be added or removed to change the functionality of QIIME, you can also choose which interfaces to install and use for your analyses. Unlike QIIME 1, the command-line interface is only one possible interface for QIIME 2. You can explore :doc:`QIIME 2 Studio <interfaces/q2studio>`, the first graphical user interface for QIIME 2, and the :doc:`Artifact API <interfaces/artifact-api>`, an *Application Programmer Interface* that is optimized for users working in the `Jupyter Notebook`_.

.. _`q2cli`: https://github.com/qiime2/q2cli

.. _`Miniconda`: http://conda.pydata.org/miniconda.html

.. _`Jupyter Notebook`: http://jupyter.org
