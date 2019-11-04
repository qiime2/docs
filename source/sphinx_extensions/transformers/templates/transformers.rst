Transformers
============

{% for transfomer in plugin_manager.transformers %}
- {{ transfomer }}
{% endfor %}

Reverse Transformers
--------------------
{% for reverse_transformer in plugin_manager._reverse_transformers %}
- {{ reverse_transformer }}
{% endfor %}