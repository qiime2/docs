Available plugins
=================

QIIME 2 microbiome analysis functionality is made available to users via plugins. The following official plugins are currently included in QIIME 2 train releases:

.. toctree::
   :maxdepth: 3

   {% for name, _ in plugins|dictsort %}
   {{ name }}: {{ _.short_description }} <{{ name }}/index>
   {% endfor %}

