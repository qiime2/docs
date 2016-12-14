{{ title }}
{{ '=' * title|length }}

{{ action.description }}

.. raw:: html

   <table class="table action-signature">
     {% for group, specs in (('Inputs', input_specs),
                             ('Parameters', parameter_specs),
                             ('Outputs', output_specs)) %}
     <thead>
       <tr>
         <th colspan="3">{{ group }}</th>
       </tr>
       {% if specs %}
       <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Default</th>
       </tr>
       {% else %}
       <tr>
         <th colspan="3" class="text-muted">N/A</th>
       </tr>
       {% endif %}
     </thead>
     <tbody>
       {% for spec in specs %}
       <tr>
         {% for content in spec %}
         <td>
           <code class="docutils literal">
             <span class="pre">{{ content }}</span>
           </code>
         </td>
         {% endfor %}
       </tr>
       {% endfor %}
     </tbody>
     {% endfor %}
   </table>
