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

Install dada2
-------------

If you plan to use the ``q2-dada2`` plugin that's included in the Core distribution, you will need to install the `latest version of dada2 through Bioconductor <https://www.bioconductor.org/packages/release/bioc/html/dada2.html>`_. Installing dada2 through Bioconductor is necessary because the latest version of dada2 is not available through ``conda`` at the time of this writing. There is work being done to make the latest version of dada2 available through ``conda``. When the ``conda`` package is available, these installation steps will no longer be necessary.

.. command-block::
   :no-exec:

   CDPATH= R -e 'source("https://bioconductor.org/biocLite.R"); biocLite("dada2")'

.. tip::

   If installing dada2 via Bioconductor fails, try the following suggestions:

   * Per the `Bioconductor installation instructions <https://www.bioconductor.org/install/>`_, try using ``http://`` instead of ``https://`` in the Bioconductor URL that is sourced above.

   * If you are using a Mac (i.e. macOS or OS X), install the Xcode Command Line Tools by running:

     .. command-block::
        :no-exec:

        xcode-select --install

     See this `Apple technical note <https://developer.apple.com/library/content/technotes/tn2339/_index.html>`_ for more details and alternate ways of obtaining the Xcode Command Line Tools.

   * To test that dada2 installed correctly, run:

     .. command-block::

        R -e 'library("dada2")'

     If no errors are reported, the installation was successful!

Next steps
----------

Now that you have the Core distribution installed, check out the :doc:`q2cli docs <../interfaces/q2cli>` to get familiar with the QIIME 2 command-line interface (it is used extensively in the :doc:`tutorials <../tutorials/index>`). After that, try out the :doc:`QIIME 2 tutorials <../tutorials/index>` for examples of using QIIME 2 to analyze microbiome datasets. You might also try installing other QIIME 2 :doc:`interfaces <../interfaces/index>`.

.. _`Miniconda`: http://conda.pydata.org/miniconda.html
