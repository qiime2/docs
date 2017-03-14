Available plugins
=================

QIIME 2 microbiome analysis functionality is made available to users via plugins. The following official plugins are currently included in QIIME 2 train releases:

.. toctree::
   :maxdepth: 3

   {% for name, plugin in plugins|dictsort %}
   {% if plugin.short_description %}
   {{ name }}: {{ plugin.short_description }} <{{ name }}/index>
   {% else %}
   {{ name }}/index
   {% endif %}
   {% endfor %}

