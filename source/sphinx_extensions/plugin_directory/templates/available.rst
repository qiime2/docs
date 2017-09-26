Available plugins
=================

QIIME 2 microbiome analysis functionality is made available to users via plugins. The following official plugins are currently included in QIIME 2 train releases:

.. toctree::
   :maxdepth: 3

   {% for name, plugin in plugins|dictsort %}
   {% set cli_name = name.replace('_', '-') %}
   {% if plugin.short_description %}
   {{ cli_name }}: {{ plugin.short_description }} <{{ cli_name }}/index>
   {% else %}
   {{ cli_name }}/index
   {% endif %}
   {% endfor %}
