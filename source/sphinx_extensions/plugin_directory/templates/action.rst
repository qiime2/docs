{{ title }}
{{ '=' * title|length }}

{% if has_citations %}
.. raw:: html

   <table class="table action-info">
     <tbody>
       <tr>
         <th scope="row"><p></p>Citations</th>
         <td>

.. bibliography:: {{ bib_id }}.bib
   :list: bullet
   :all:
   :keyprefix: {{ bib_id }}:
   :labelprefix: {{ bib_id}}:

.. raw:: html

         </td>
       </tr>
     </tbody>
   </table>
{% endif %}

.. raw:: html

   <div class="tabbed">
     <ul class="nav nav-tabs">
       <li class="active"><a data-toggle="tab" href="#cli">Command line interface</a></li>
       <li><a data-toggle="tab" href="#api">Artifact API</a></li>
     </ul>
     <div class="tab-content">
       <div id="cli" class="tab-pane fade in active">
         <h4>Docstring:</h4>
         <pre>{{- cli_help -}}</pre>
       </div>
       <div id="api" class="tab-pane fade">
       <h4>Import:</h4>

.. command-block::
   :no-exec:

   from {{import_path}} import {{action_api_name}}

.. raw:: html

       <h4>Docstring:</h4>
         <pre>
           {{- api_help -}}
         </pre>
       </div>
     </div>
   </div>
