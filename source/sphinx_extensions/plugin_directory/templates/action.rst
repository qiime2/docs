{{ title }}
{{ '=' * title|length }}

.. raw:: html

   <div class="tabbed">
      <ul class="nav nav-tabs">
         <li class="active"><a data-toggle="tab" href="#cli">Command line interface</a></li>
         <li><a data-toggle="tab" href="#api">Artifact API</a></li>
      </ul>
      <div class="tab-content">
         <div id="cli" class="tab-pane fade in active">
            <pre>
{{ cli_help }}   </pre>
         </div>
         <div id="api" class="tab-pane fade">
            <pre>
{{ api_help }}   </pre>
         </div>
      </div>
   </div>
