Installing QIIME 2 using WSL
---------------------------------

This tutorial demonstrates how to set up QIIME 2 on the Windows Subsystem for Linux.

Please see the `official windows tutorial <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__ to install WSL2. Then install an appropriate linux distribution e.g. the latest stable version of Ubuntu. Once installation is complete run ``sudo apt-get update`` and ``sudo apt-get upgrade`` to ensure everything is up to date.

Then install miniconda (or alternatively you could install Anaconda) using the following commands:

.. command-block::
    :no-exec:
    
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    #once installation has completed
    conda init 

Restart the terminal to have changes take effect. Packages for your project can now be installed in environments, keeping them separate from any other projects you may have, and ensuring that different dependencies do not clash. You can now proceed to :doc:`native conda installation <native>` for instructions on how to install Qiime 2. 

**References**

1. https://docs.microsoft.com/en-us/windows/wsl/install-win10

2. https://wiki.ubuntu.com/WSL
