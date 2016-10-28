QIIME 2 overview
================

QIIME 2 is a complete redesign and rewrite of the `QIIME 1`_ microbiome analysis pipeline. QIIME 2 will address many of the limitations of QIIME 1, while retaining the features that makes QIIME 1 a powerful and widely-used analysis pipeline. See the :doc:`key concepts <concepts>` page for details on how QIIME 2 addresses many of the limitations of QIIME 1.

QIIME 2 is ready for experimental use while in its alpha release stage. **It currently supports an initial end-to-end microbiome analysis pipeline.** Because our microbiome analysis functionality is currently very new, QIIME 2 is not yet recommended as a replacement for QIIME 1, but we are very interested in having users test QIIME 2 and give us feedback. Until the QIIME 2 microbiome analysis functionality has expanded, we recommend that you continue to use `QIIME 1`_ and `Qiita`_ for your microbiome analyses, as these will provide you with complete analysis solutions supporting high-performance computing environments.

New functionality will regularly become available through QIIME 2 plugins. You can view a list of plugins, including those that are currently available, in development, or being planned, on the QIIME 2 :doc:`plugins <plugins>` page.

To see where we're headed with QIIME 2, take a look at Greg Caporaso's `American Gut blog post`_ (15 April 2016) and `SciPy 2016 presentation`_ (15 July 2016).

Getting started
---------------

QIIME 2 introduces several new concepts that are not present in QIIME 1, and these concepts are important to understand as they are central to how you will interact with QIIME 2 to perform microbiome analyses. It is **highly recommended** to start with the :doc:`key concepts <concepts>` documentation before moving on to installing and using QIIME 2.

To begin using QIIME 2, start with the :doc:`installation guide <install>`, which will show you how to install the QIIME 2 framework, a command-line interface, and some plugins used in the :doc:`tutorials <tutorials/index>`.

Staying updated
---------------

For updates on QIIME 2, follow `@qiime2`_ on Twitter.

Requesting features, reporting bugs, providing feedback
-------------------------------------------------------

If there is specific functionality you'd like to see in QIIME 2, you notice a bug, or want to leave feedback, please post to the QIIME 2 `issue tracker`_. We appreciate all feedback as we strive to make QIIME 2 a useful and accessible tool for microbiome analyses.

Extending QIIME 2 through plugins and interfaces
------------------------------------------------

A key design goal of QIIME 2 is to enable third-party developers to create plugins and interfaces for QIIME 2 in order to extend its functionality available to users.

Plugins provide a way for microbiome bioinformatics developers to make their tools accessible to end users in their QIIME deployment. A plugin enables access to its functionality through any of QIIME's :doc:`interfaces <interfaces/index>`. If you're interested in developing a QIIME 2 plugin, you should begin with :doc:`Creating a QIIME 2 plugin <Creating-a-QIIME-2-plugin>`. You should also refer to the QIIME 2 :doc:`plugins <plugins>` page to see what plugins already exist or are being developed.

QIIME 2 provides a software development kit (SDK) accessible from the ``qiime.sdk`` package. The SDK provides a way for software engineers to build custom interfaces around QIIME, which can include embedding QIIME as a component in other systems (e.g., cloud-based bioinformatics platforms). We have not yet developed our SDK/interface developer documentation, but two examples of QIIME 2 interfaces are currently available: `q2cli`_ and `QIIME 2 Studio`_. We will have detailed SDK/interface developer documentation available soon.

**While QIIME 2 is in its alpha release stage, backward incompatible interface changes that impact plugins and interfaces can and will occur.** We will make every effort to minimize these, and we will make every effort to let developers know through the ``#developers`` Slack channel and help developers update their plugins to match the latest API. We will have a better way of notifying developers of these changes in the future. See below for details on joining the QIIME 2 Slack team.

.. _slack-team:

Slack team
----------

**The QIIME 2 developers use Slack for instant message discussion of development topics.** If you're working on plugin or interface development and need help, you should join our `Slack team`_ and then get in touch on the ``#developers`` channel at https://qiime2.slack.com. This will be more reliable than emailing one of the developers directly.

.. _`QIIME 1`: http://qiime.org

.. _`Qiita`: https://qiita.ucsd.edu/

.. _`American Gut blog post`: http://americangut.org/qiime-2-will-revolutionize-microbiome-bioinformatics/

.. _`SciPy 2016 presentation`: https://www.youtube.com/watch?v=tLtGg21Yu9Q

.. _`@qiime2`: https://twitter.com/qiime2

.. _`issue tracker`: https://github.com/qiime2/qiime2/issues

.. _`q2cli`: https://github.com/qiime2/q2cli

.. _`QIIME 2 Studio`: https://github.com/qiime2/q2studio

.. _`Slack team`: http://qiime2-slackin.qiime.org
