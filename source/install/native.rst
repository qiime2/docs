Natively installing QIIME 2
===========================

This guide describes how to natively install the :ref:`core-distribution`.

Miniconda
---------

Installing Miniconda
....................

`Miniconda`_ provides the ``conda`` environment and package manager, and is
the recommended way to install QIIME 2. Follow the `Miniconda instructions`_
for downloading and installing Miniconda. You may choose either Miniconda2 or
Miniconda3 (i.e. Miniconda Python 2 or 3). QIIME 2 will work with either
version of Miniconda. It is important to follow all of the directions
provided in the `Miniconda instructions`_, particularly ensuring that you run
``conda init`` at the end of the installation process, to ensure that your
Miniconda installation is fully installed and available for the following
commands.

Updating Miniconda
..................

After installing Miniconda and opening a new terminal, make sure you're
running the latest version of ``conda``:

.. command-block::
   :no-exec:

   conda update conda

Installing ``wget``
...................

.. command-block::
   :no-exec:

   conda install wget

Install QIIME 2 within a ``conda`` environment
----------------------------------------------

Once you have Miniconda installed, create a ``conda`` environment and install
the QIIME 2 Core 2023.9 distribution within the environment. We **highly**
recommend creating a *new* environment specifically for the QIIME 2 release
being installed, as there are many required dependencies that you may not
want added to an existing environment. You can choose whatever name you'd
like for the environment. In this example, we'll name the environment
``qiime2-2023.9`` to indicate what QIIME 2 release is installed (i.e.
``2023.9``).


.. raw:: html

   <div class="tabbed">
      <ul class="nav nav-tabs">
         <li class="active"><a data-toggle="tab" href="#instructions">Instructions</a></li>
         <li><a data-toggle="tab" href="#macOS-intel">macOS (Intel) and OS X</a></li>
         <li><a data-toggle="tab" href="#macOS-apple-silicon">macOS (Apple Silicon)</a></li>
         <li><a data-toggle="tab" href="#linux">Linux</a></li>
         <li><a data-toggle="tab" href="#wsl">Windows (via WSL)</a></li>
      </ul>
      <div class="tab-content">
         <div id="instructions" class="tab-pane fade in active">
            <p class="alert alert-warning" style="margin-bottom: 10px;">
              From the above tabs, please choose the installation instructions that are appropriate for your platform.
            </p>
         </div>
         <div id="macOS-intel" class="tab-pane fade">
            <pre>wget https://data.qiime2.org/distro/core/qiime2-2023.9-py38-osx-conda.yml
   conda env create -n qiime2-2023.9 --file qiime2-2023.9-py38-osx-conda.yml</pre>
   <span>OPTIONAL CLEANUP</span>
   <pre>rm qiime2-2023.9-py38-osx-conda.yml</pre>
         </div>
         <div id="macOS-apple-silicon" class="tab-pane fade">
            <p>These instructions are for users with <a href="https://support.apple.com/en-us/HT211814">Apple Silicon</a> chips (M1, M2, etc), and configures the installation of QIIME 2 in <a href="https://developer.apple.com/documentation/apple-silicon/about-the-rosetta-translation-environment">Rosetta 2 emulation mode</a>.</p>
            <pre>wget https://data.qiime2.org/distro/core/qiime2-2023.9-py38-osx-conda.yml
   CONDA_SUBDIR=osx-64 conda env create -n qiime2-2023.9 --file qiime2-2023.9-py38-osx-conda.yml
   conda activate qiime2-2023.9
   conda config --env --set subdir osx-64</pre>
   <span>OPTIONAL CLEANUP</span>
   <pre>rm qiime2-2023.9-py38-osx-conda.yml</pre>
         </div>
         <div id="linux" class="tab-pane fade">
            <pre>wget https://data.qiime2.org/distro/core/qiime2-2023.9-py38-linux-conda.yml
   conda env create -n qiime2-2023.9 --file qiime2-2023.9-py38-linux-conda.yml</pre>
   <span>OPTIONAL CLEANUP</span>
   <pre>rm qiime2-2023.9-py38-linux-conda.yml</pre>
         </div>
         <div id="wsl" class="tab-pane fade">
            <p>These instructions are identical to the Linux instructions and are intended for users of the <a href="https://learn.microsoft.com/en-us/windows/wsl/about">Windows Subsystem for Linux</a>.</p>
            <pre>wget https://data.qiime2.org/distro/core/qiime2-2023.9-py38-linux-conda.yml
   conda env create -n qiime2-2023.9 --file qiime2-2023.9-py38-linux-conda.yml</pre>
   <span>OPTIONAL CLEANUP</span>
   <pre>rm qiime2-2023.9-py38-linux-conda.yml</pre>
         </div>
      </div>
   </div>


Activate the ``conda`` environment
----------------------------------

Now that you have a QIIME 2 environment, activate it using the environment's name:

.. command-block::
   :no-exec:

   conda activate qiime2-2023.9

To deactivate an environment, run ``conda deactivate``.

Test your installation
----------------------

You can test your installation by activating your QIIME 2 environment and running:

.. command-block::
   :no-exec:

   qiime --help

If no errors are reported when running this command, the installation was successful!

Next steps
----------

Now that you have the Core distribution installed, check out the :doc:`q2cli
docs <../interfaces/q2cli>` to get familiar with the QIIME 2 command-line
interface (it is used extensively in the :doc:`tutorials
<../tutorials/index>`). After that, try out the :doc:`QIIME 2 tutorials
<../tutorials/index>` for examples of using QIIME 2 to analyze microbiome
datasets. You might also try installing other QIIME 2 :doc:`interfaces
<../interfaces/index>`.

How do I update to the newest version of QIIME 2?
-------------------------------------------------

In order to to update/upgrade to the newest release, you simply install the
newest version in a new conda environment by following the instructions
above. Then you will have two conda environments, one with the older version
of QIIME 2 and one with the newer version.

(Re-)Activating QIIME 2
-----------------------

If at any point during the analysis the QIIME 2 conda environment is closed
or deactivated, QIIME 2 2023.9 can be activated (or reactivated) by running
the following command:

.. command-block::
   :no-exec:

   conda activate qiime2-2023.9

To determine the currently active conda environment, run the following
command and look for the line that starts with "active environment":

.. command-block::
   :no-exec:

   conda info

.. _`Miniconda`: https://docs.conda.io/en/latest/miniconda.html
.. _`Miniconda instructions`: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
