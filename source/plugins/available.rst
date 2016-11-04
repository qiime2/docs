Available plugins
=================

QIIME's microbiome analysis functionality is defined and made available to users via QIIME 2 plugins. As we progress through our alpha release phase we plan to develop a mechanism for allowing users to discover what plugins are available. Our initial draft of this is the `QIIME 2 Plugins spreadsheet`_.

The ``Status`` categories used in this spreadsheet are:

* ``Released`` : The plugin is currently installable with ``conda install -c qiime2 <plugin-name>``.
* ``Pre-release development`` : The plugin is currently under active development. See the *Estimated release date* for when this plugin is expected to be moved to ``Release`` status.
* ``Planning`` : The plugin is in the planning stage. Development has not officially started, but it is expected to start soon. Someone has already committed to working on this plugin. There may be ``Unmet dependencies`` that are blocking its transition to ``Pre-release development``.
* ``Needs developer`` : The plugin is in the early planning phase. It represents functionality that is needed or wanted, but no one has yet committed to working on this plugin. There may be ``Unmet dependencies`` that are blocking its transition to ``Planning`` or ``Pre-release development``.

If you'd like to develop a QIIME 2 plugin, :doc:`get in touch <../community>` to request edit access to the spreadsheet. If you're looking for documentation on how to develop a plugin, see :doc:`this guide <developing>`.

.. _QIIME 2 Plugins spreadsheet: https://docs.google.com/spreadsheets/d/1KdgbooDDuh_aE-aCGlVLNgMCli513wU9E5_PgpL6tbY/pubhtml?gid=0&single=true
