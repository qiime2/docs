Upgrading QIIME 2
=================

Existing :ref:`QIIME 2 Core distribution <core-distribution>` installations can be either upgraded (i.e. installing a newer release of QIIME 2) or updated (i.e. patch updates within a given release of QIIME 2). Please see the section below that most closely matches your existing QIIME 2 installation.

.. _upgrading:

Upgrading to QIIME 2 Core 2017.6
--------------------------------

Native Installation
    Please see the :doc:`native install doc <install/native>` for instructions on how to create a new QIIME 2 Core 2017.6 ``conda`` environment.

VirtualBox
    Please see the :doc:`VirtualBox install doc <install/virtual/virtualbox>` for instructions on how to download and set up a new QIIME 2 Core 2017.6 VirtualBox virtual machine.

Docker
    Please see the :doc:`Docker install doc <install/virtual/docker>` for instructions on how to download and set up a new QIIME 2 Core 2017.6 Docker container.

Amazon AWS
    Please see the :doc:`Amazon AWS install doc <install/virtual/aws>` for instructions on how to set up a new QIIME 2 Core 2017.6 AWS instance.

.. _updating:

Updating QIIME 2 Core 2017.6
----------------------------

macOS/OS X (Native Installation)
    In a terminal run the following commands:

    .. command-block::
       :no-exec:

       conda update conda
       # If you named your conda environment something else when you initially installed QIIME 2, use that name here.
       source activate qiime2-2017.6
       conda install --file https://data.qiime2.org/distro/core/qiime2-2017.6-conda-osx-64.txt

Linux (Native Installation)
    In a terminal run the following commands:

    .. command-block::
       :no-exec:

       conda update conda
       # If you named your conda environment something else when you initially installed QIIME 2, use that name here.
       source activate qiime2-2017.6
       conda install --file https://data.qiime2.org/distro/core/qiime2-2017.6-conda-linux-64.txt

VirtualBox
    In a terminal on the virtual machine, run the following command:

    .. command-block::
       :no-exec:

       sudo env "PATH=$PATH" conda update conda
       sudo env "PATH=$PATH" conda install --file https://data.qiime2.org/distro/core/qiime2-2017.6-conda-linux-64.txt

Docker
    In a terminal run the following command:

    .. command-block::
       :no-exec:

       docker pull qiime2/core:2017.6

Amazon AWS
    In a shell on the remote AWS machine, run the following command:

    .. command-block::
       :no-exec:

       sudo env "PATH=$PATH" conda update conda
       sudo env "PATH=$PATH" conda install --file https://data.qiime2.org/distro/core/qiime2-2017.6-conda-linux-64.txt
