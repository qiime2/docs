{{ plugin.name }}
{{ '=' * plugin.name|length }}

.. raw:: html

   <table class="table plugin-info">
     <tbody>
       <tr>
         <th scope="row">Description</th>
         <td>{{ plugin.description|urlize }}</td>
       </tr>
       <tr>
         <th scope="row">Version</th>
         <td>{{ plugin.version }}</td>
       </tr>
       <tr>
         <th scope="row">Website</th>
         <td>{{ plugin.website|urlize }}</td>
       </tr>
       <tr>
         <th scope="row">Support</th>
         <td>
           {% for line in plugin.user_support_text.splitlines() %}
           {{ line|urlize }}<br/>
           {% endfor %}
         </td>
       </tr>
       <tr>
         <th scope="row">Citation</th>
         <td>
           {% for line in plugin.citation_text.splitlines() %}
           {{ line|urlize }}<br/>
           {% endfor %}
         </td>
       </tr>
     </tbody>
   </table>

Methods
-------

{% if plugin.methods %}
.. toctree::
   :maxdepth: 1

   {% for id, _ in plugin.methods|dictsort %}
   {{ id }}
   {% endfor %}
{% else %}
This plugin does not have any methods.
{% endif %}

Visualizers
-----------

{% if plugin.visualizers %}
.. toctree::
   :maxdepth: 1

   {% for id, _ in plugin.visualizers|dictsort %}
   {{ id }}
   {% endfor %}
{% else %}
This plugin does not have any visualizers.
{% endif %}
