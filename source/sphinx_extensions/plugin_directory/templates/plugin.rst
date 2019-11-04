{{ title }}
{{ '=' * title|length }}

.. raw:: html

   <table class="table plugin-info">
     <tbody>
       <tr>
         <th scope="row">Description</th>
         <td>
           {% for line in plugin.description.splitlines() %}
           {{ line|urlize }}<br/>
           {% endfor %}
         </td>
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
       <tr>
         <th scope="row">q2cli Invocation</th>
         <td>

.. command-block::
   :no-exec:

   qiime {{ title }}

.. raw:: html

         </td>
       </tr>
       <tr>
         <th scope="row">Artifact API Import</th>
         <td>

.. command-block::
   :no-exec:

   from qiime2.plugins import {{ title.replace('-', '_') }}

.. raw:: html

         </td>
       </tr>

{% if plugin.citations %}
.. raw:: html

         </td>
       </tr>
       <tr>
         <th scope="row"><p></p>Citations</th>
         <td>

.. bibliography:: citations.bib
   :list: bullet
   :all:
   :keyprefix: {{ plugin.name }}:
   :labelprefix: {{ plugin.name }}:
{% endif %}

.. raw:: html

         </td>
       </tr>
     </tbody>
   </table>

{% if plugin.pipelines %}
Pipelines
---------

.. toctree::
   :maxdepth: 1

   {% for id, _ in plugin.pipelines|dictsort %}
   {{ id.replace('_', '-') }}
   {% endfor %}
{% endif %}

{% if plugin.methods %}
Methods
-------

.. toctree::
   :maxdepth: 1

   {% for id, _ in plugin.methods|dictsort %}
   {{ id.replace('_', '-') }}
   {% endfor %}
{% endif %}

{% if plugin.visualizers %}
Visualizers
-----------

.. toctree::
   :maxdepth: 1

   {% for id, _ in plugin.visualizers|dictsort %}
   {{ id.replace('_', '-') }}
   {% endfor %}
{% endif %}
