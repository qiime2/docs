Types List
==========

{% for type in type_list %}
- {{ type }}
{% endfor %}

Formats List
============

All Formats
-----------
{% for format in format_list %}
- {{ format }}
{% endfor %}

Importable Formats
------------------
{% for imp in importable_formats %}
- {{ imp }}
{% endfor %}

Exportable Formats
------------------
{% for exp in exportable_formats %}
- {{ exp }}
{% endfor %}

Transformers
============

Transformers
------------
{% for from, to in transformers_list %}
- {{ from }} -> {{ to }}
{% endfor %}

Reverse Transformers
--------------------
{% for from, to in reverse_transformers_list %}
- {{ from }} -> {{ to }}
{% endfor %}
