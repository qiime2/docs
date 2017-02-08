QIIME 2 command-line interface (q2cli)
======================================

.. note:: This guide assumes you have installed the QIIME 2 Core distribution using one of the procedures in the :doc:`install documents <../install/index>`.

This guide provides an introduction to ``q2cli``, a QIIME 2 command-line interface included in the QIIME 2 Core distribution. The :doc:`tutorials <../tutorials/index>` use ``q2cli`` extensively, so it is recommended to review this document first before beginning the tutorials. This document is a work-in-progress and will be expanded in the future.

Basic usage
-----------

``q2cli`` includes a ``qiime`` command that is used to execute QIIME analyses from the command line. Run ``qiime`` to see a list of available subcommands:

.. command-block::

   qiime

There will be several subcommands listed, including plugin commands (e.g. ``feature-table``, ``diversity``) and built-in commands (e.g. ``info``, ``tools``).

You can discover what plugins you currently have installed, as well as other information about your QIIME deployment, by running ``qiime info``:

.. command-block::

   qiime info

Supply ``--help`` to any command to display information about the command, including any subcommands, options, and arguments the command defines. For example, to learn more about the ``feature-table`` plugin command, run:

.. command-block::

  qiime feature-table --help

This will list the actions (subcommands) made available by the ``feature-table`` plugin, as well as information about the plugin itself (e.g. citation, website, user support).

Try learning about other commands using ``--help``. For example, what actions are available in the built-in ``tools`` command?

Enable command-line tab completion
----------------------------------

If you are using Bash or Zsh as your shell, you can enable tab completion, which substantially improves the usability of the QIIME 2 command-line interface (CLI). When tab completion is enabled, pressing the tab key will attempt to complete the command or option you have typed, or provide you with a list of available commands or options based on what you have typed so far. This reduces the amount of typing you have to do and makes commands and options more easily discoverable without passing ``--help`` to every command you're wanting to run.

.. tip:: QIIME 2 CLI tab completion is currently only supported in the Bash and Zsh shells. To check what shell you have, run ``echo $0``. You should see ``-bash`` or ``-zsh`` in the output.

Please choose the instructions appropriate for your shell to enable tab completion.

Bash
~~~~

Run this command to enable tab completion:

.. command-block::
   :no-exec:

   source tab-qiime

You will need to run this command each time you open a new terminal and activate your QIIME 2 ``conda`` environment unless it is added to your ``.bashrc``/``.bash_profile``.

Zsh
~~~

Run this command to enable tab completion:

.. command-block::
   :no-exec:

   autoload bashcompinit && bashcompinit && source tab-qiime

You will need to run this command each time you open a new terminal and activate your QIIME 2 ``conda`` environment unless it is added to your ``.zshrc``.

Verify tab completion
~~~~~~~~~~~~~~~~~~~~~

To test that tab completion is working, try typing in the following partial command, and without actually running the command, press the tab key (you may need to press it a couple of times). If tab completion is working, the command should auto-complete to ``qiime info``.

.. command-block::
   :no-exec:

   qiime i
