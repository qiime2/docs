Installing QIIME 2 using Virtual Machines
=========================================

QIIME 2 "core distribution" builds are available as VirtualBox VMDK Images, Amazon Web Services (AWS) EC2 AMI Images, and Docker Images. These options can get you a working QIIME 2 installation very quickly.

The core distribution builds contain the following plugins:

- ``alignment``
- ``composition``
- ``dada2``
- ``demux``
- ``diversity``
- ``emperor``
- ``feature-classifier``
- ``feature-table``
- ``phylogeny``
- ``taxa``
- ``types``

.. note:: At this stage we're unsure of what types of virtual machine builds we'll continue to release in the future. We expect that for at least the next few QIIME 2 releases we'll provide the three builds included here, but we may ultimately phase out the AWS and VirtualBox builds. This is because our release of these builds restricts users to a specific operating system/cloud platform/etc, so we feel that we may better serve our user community by providing cross-platform builds (e.g., Docker containers) and detailed instructions for how to work with these.

VirtualBox
----------

1. Set up VirtualBox on your computer (see https://VirtualBox.org for details).
2. Download the QIIME 2 Core VirtualBox Image here: https://data.qiime2.org/distro/core/qiime206.zip.
3. Unzip the ``qiime206.zip`` file.
4. Launch VirtualBox, and create a new machine (click "New").
5. A new window will show up. Click "Next".
6. In this screen type *QIIME 2 Core 2.0.6* as the name for the virtual machine then select Linux as the Operating System, and Ubuntu (64 bit) as the version. Click "Next".
7. Select the amount of RAM (memory). You will need at least 2048 MB, but the best option is based on your machine. After selecting the amount of RAM. Click "Next".
8. Select "Use existing hard drive", and click the folder icon next to the selector (it has a green up arrow). In the new window click "Add", and locate the virtual hard drive that was unzipped in step 3. Click "Select" and then click "Next".
9. In the new window, click "Finish".
10. Launch the virtual machine. When prompted, select the user ``qiime2``, and enter the password ``qiime2``.

Amazon Web Services
-------------------

1. Set up an AWS account at https://aws.amazon.com, and log in.
2. Set your region to "US West (Oregon)".
3. When launching an instance, select "Community AMIs", and search for "QIIME 2 Core" (the AMI ID is `ami-c401aca4`).
4. When prompted to set up a security group, make sure that port 22 is open.
5. When prompted to set up an SSH keypair, choose "Proceed without a keypair".
6. Once the machine has finished booting, you can SSH into it by running ``ssh qiime2@<PUBLIC_AWS_IP_ADDRESS>``, replacing ``<PUBLIC_AWS_IP_ADDRESS>`` with the public IP address for the machine (this will be provided by AWS). When prompted, provide the password ``qiime2``.

Docker
------

1. Set up Docker on your computer (see https://docker.com for details).
2. In a terminal with Docker activated, run ``docker pull qiime2/core:latest``.
3. Run ``docker run -t -i -v $(pwd):/data qiime2/core qiime`` to confirm that the image was successfully fetched.
