Glossary
========

This document is currently a work-in-progress QIIME 2 terminology glossary.

.. glossary::

   Action
      A general term for a *method* or *visualizer*.

   Artifact
      Data that can be used as input to a QIIME *method* or *visualizer*, or that can be generated as output from a QIIME *method*. Artifacts typically have the file extension ``.qza``.

   Method
      An *action* that takes some combination of *artifacts* and *parameters* as input, and produces one or more *artifacts* as output. These output *artifacts* could subsequently be used as input to other QIIME 2 *methods* or *visualizers*. *Methods* can produce intermediate or terminal outputs in a QIIME analysis.

   Parameter
      A primitive (i.e., non-*artifact*) input to an *action*. For example, strings, integers, and booleans are primitives. Primitives are never output from an *action*.

   Pipeline
         A combination of *actions*. This is not yet implemented.

   Plugin
      A plugin provides microbiome (i.e. domain-specific) analysis functionality that is accessible to users through a variety of interfaces built around the QIIME 2 framework. Plugins can be developed and distributed by anyone. In more technical terms, a plugin is a Python 3 package that instantiates a ``qiime2.plugin.Plugin`` object, and registers *actions*, *data formats*, and/or *semantic types* that become discoverable in the QIIME 2 framework.

   Result
      A general term for an *artifact* or *visualization*. A *result* is produced by a *method*, *visualizer*, or *pipeline*.

   Visualization
         Data that can be generated as output from a QIIME *visualizer*. Visualizations typically have the file extension ``.qzv``.

   Visualizer
      An *action* that takes some combination of *artifacts* and *parameters* as input, and produces exactly one *visualization* as output. Output *visualizations*, by definition, cannot be used as input to other QIIME 2 *methods* or *visualizers*. *Visualizers* can only produce terminal output in a QIIME analysis.
