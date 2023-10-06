Installing QIIME 2
==================

QIIME 2 can be installed natively or using a virtual machine. The following
pages describe how to install the available :ref:`distributions`
in either scenario.

.. toctree::
   :maxdepth: 2

   native
   virtual/index

Recommendations
---------------

The :doc:`native conda installation <native>` is generally the recommended
method of installation, but this isn't always available or a straight-forward
option for all cases. In general we recommend the following:

* `macOS`_ users

  - A :doc:`native conda installation <native>` usually works well
  - :doc:`Docker <virtual/docker>` is a good backup option

* `Windows`_ users

  - On newer versions of Windows, performing a :doc:`native conda
    installation <native>` in the `Windows Subsystem for Linux`_ usually
    works well. See :doc:`the WSL guide <virtual/wsl>` for instructions on
    how to set up the Windows Subsystem for Linux.
  - :doc:`Docker <virtual/docker>` is a good backup option

* Linux users

  - A :doc:`native conda installation <native>` usually works well
  - :doc:`Docker <virtual/docker>` is a good backup option

.. _distributions:

QIIME 2 2023.9 distributions
----------------------------

As of 2023.9, QIIME 2 releases now include the following QIIME 2 distributions that are available for install:

- ``Amplicon``
- ``Shotgun``
- ``Tiny``

QIIME 2 2023.9 Amplicon distribution
....................................

The 2023.9 release of the QIIME 2 Amplicon distribution includes the QIIME 2 framework, ``q2cli`` (a QIIME 2 command-line interface) and the following plugins:

- ``q2-alignment``
- ``q2-composition``
- ``q2-cutadapt``
- ``q2-dada2``
- ``q2-deblur``
- ``q2-demux``
- ``q2-diversity``
- ``q2-diversity-lib``
- ``q2-emperor``
- ``q2-feature-classifier``
- ``q2-feature-table``
- ``q2-fragment-insertion``
- ``q2-longitudinal``
- ``q2-metadata``
- ``q2-phylogeny``
- ``q2-quality-control``
- ``q2-quality-filter``
- ``q2-sample-classifier``
- ``q2-taxa``
- ``q2-types``
- ``q2-vsearch``

QIIME 2 2023.9 Shotgun distribution
...................................

The 2023.9 release of the QIIME 2 Shotgun distribution includes the QIIME 2 framework, ``q2cli`` (a QIIME 2 command-line interface) and the following plugins:

- ``q2-assembly``
- ``q2-cutadapt``
- ``q2-demux``
- ``q2-diversity``
- ``q2-diversity-lib``
- ``q2-emperor``
- ``q2-feature-classifier``
- ``q2-feature-table``
- ``q2-metadata``
- ``q2-moshpit``
- ``q2-quality-control``
- ``q2-quality-filter``
- ``q2-sample-classifier``
- ``q2-sapienns``
- ``q2-taxa``
- ``q2-types``
- ``q2-types-genomics``
- ``rescript``

QIIME 2 2023.9 Tiny distribution
................................

The 2023.9 release of the QIIME 2 Tiny distribution includes the QIIME 2 framework and ``q2cli`` (a QIIME 2 command-line interface) and the following plugins:

- ``q2-types``

The QIIME 2 Tiny distribution is a minimal QIIME 2 environment that can be used by developers who are in need of a basic development environment, or community plugin users who do not need the entire Amplicon or Shotgun distributions in their QIIME 2 environment.

.. note:: The QIIME 2 Amplicon, Shotgun and Tiny distributions include plugins and interfaces that are developed, maintained, tested, and distributed by the QIIME 2 development team. The Amplicon distribution is necessary to run the commands in the :doc:`QIIME 2 tutorials <../tutorials/index>`. If there are additional QIIME 2 plugins or interfaces you would like to install, please consult the relevant package(s) documentation.

.. _macOS: https://www.apple.com/macos/
.. _Windows: https://www.microsoft.com/en-us/windows
.. _Windows Subsystem for Linux: https://docs.microsoft.com/en-us/windows/wsl/install-win10
