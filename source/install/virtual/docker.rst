Installing QIIME 2 using Docker
===============================

1. Set up Docker on your computer (see https://docker.com for details).
2. In a terminal with Docker activated, run ``docker pull qiime2/core:latest``.
3. Run ``docker run -t -i -v $(pwd):/data qiime2/core qiime`` to confirm that the image was successfully fetched.
