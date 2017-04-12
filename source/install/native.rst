Natively installing QIIME 2
===========================

This guide describes how to natively install the :ref:`core-distribution`.

.. note:: QIIME 2 does not currently support Windows. We recommend using one of the :doc:`QIIME 2 virtual machines <virtual/index>`.

Install Miniconda
-----------------

`Miniconda`_ provides the ``conda`` environment and package manager, and is the recommended way to install QIIME 2. Follow the instructions for downloading and installing Miniconda. You may choose either Miniconda2 or Miniconda3 (i.e. Miniconda Python 2 or 3). QIIME 2 will work with either version of Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of ``conda``:

.. command-block::
   :no-exec:

   conda update conda

Install QIIME 2 within a ``conda`` environment
----------------------------------------------

Once you have Miniconda installed, create a ``conda`` environment and install the QIIME 2 Core 2017.2 distribution within the environment. We **highly** recommend creating a *new* environment specifically for the QIIME 2 release being installed, as there are many required dependencies that you may not want added to an existing environment. You can choose whatever name you'd like for the environment. In this example, we'll name the environment ``qiime2-2017.2`` to indicate what QIIME 2 release is installed (i.e. ``2017.2``).

The installation process differs slightly across platforms. Please choose the installation instructions that are appropriate for your platform.

macOS/OS X (64-bit)
~~~~~~~~~~~~~~~~~~~

.. command-block::
   :no-exec:

   conda create -n qiime2-2017.2 --file https://data.qiime2.org/distro/core/qiime2-2017.2-conda-osx-64.txt

Linux (64-bit)
~~~~~~~~~~~~~~

.. command-block::
   :no-exec:

   conda create -n qiime2-2017.2 --file https://data.qiime2.org/distro/core/qiime2-2017.2-conda-linux-64.txt

.. tip:: If you receive errors during the installation process, such as ``gfortran`` errors, please ensure you are following the installation instructions that are compatible with your platform.

Activate the ``conda`` environment
----------------------------------

Now that you have a QIIME 2 environment, activate it using the environment's name:

.. command-block::
   :no-exec:

   source activate qiime2-2017.2

To deactivate an environment, run ``source deactivate``.

Test your installation
----------------------

You can test your installation by activating your QIIME 2 environment and running:

.. command-block::
   :no-exec:

   qiime --help

The ``q2-dada2`` plugin, which is part of the QIIME 2 core distribution, relies on the ``dada2`` R package so it is a good idea to test that that was also installed correctly. To test that ``dada2`` installed correctly, run:

.. command-block::
   :no-exec:

   R -e 'library("dada2")'

If no errors are reported when running these commands, the installation was successful!

Next steps
----------

Now that you have the Core distribution installed, check out the :doc:`q2cli docs <../interfaces/q2cli>` to get familiar with the QIIME 2 command-line interface (it is used extensively in the :doc:`tutorials <../tutorials/index>`). After that, try out the :doc:`QIIME 2 tutorials <../tutorials/index>` for examples of using QIIME 2 to analyze microbiome datasets. You might also try installing other QIIME 2 :doc:`interfaces <../interfaces/index>`.

.. _`Miniconda`: https://conda.io/miniconda.html
