Installing QIIME 2 using Docker
===============================

The following QIIME 2 distributions are available as Docker images:

- ``amplicon``
- ``metagenome``
- ``pathogenome``
- ``tiny``

Please replace <distribution> with your desired distribution in the installation instructions below.

1. Set up Docker
----------------

See https://www.docker.com for details.

2. Download desired QIIME 2 Distribution Image
----------------------------------------------

In a terminal with Docker activated, run:

.. command-block::
   :no-exec:

   docker pull quay.io/qiime2/<distribution>:2025.4

3. Confirm the installation
---------------------------

Run the following to confirm that the image was successfully fetched.

.. command-block::
   :no-exec:

   docker run -t -i -v $(pwd):/data quay.io/qiime2/<distribution>:2025.4 qiime
