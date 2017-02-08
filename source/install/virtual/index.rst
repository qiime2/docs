Installing QIIME 2 using Virtual Machines
=========================================

*QIIME 2 Core distribution* builds are available as VirtualBox VMDK Images, Amazon Web Services (AWS) EC2 AMI Images, and Docker Images. See :ref:`core-distribution` for more details about the Core distribution.

.. toctree::
   :maxdepth: 1

   virtualbox
   aws
   docker

.. note:: At this stage we're unsure of what types of virtual machine builds we'll continue to release in the future. We expect that for the first half of 2017 we'll provide the three builds included here, but we may ultimately phase out the AWS and VirtualBox builds. This is because our release of these builds restricts users to a specific operating system/cloud platform/etc, so we feel that we may better serve our user community by providing cross-platform builds (e.g., Docker containers) and detailed instructions for how to work with these.
