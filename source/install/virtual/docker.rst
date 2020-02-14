Installing QIIME 2 using Docker
===============================

1. Set up Docker
----------------

See https://www.docker.com for details.

2. Download QIIME 2 Image
-------------------------

In a terminal with Docker activated, run:

.. command-block::
   :no-exec:

   docker pull qiime2/core:2020.2

3. Confirm the installation
---------------------------

Run the following to confirm that the image was successfully fetched.

.. command-block::
   :no-exec:

   docker run -t -i -v $(pwd):/data qiime2/core:2020.2 qiime
