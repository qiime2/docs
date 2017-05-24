Installing QIIME 2 using Amazon Web Services
============================================

1. Determine which AWS AMI to use
---------------------------------

For a full list of QIIME 2 AWS AMIs, please check out the `AWS AMIs`_ link. Once you have determined which image you would like to use, please resume this guide.


2. Set up an AWS account
------------------------

Point your browser to https://aws.amazon.com and log in (you will need to provide a credit card if you haven't already created an account).

3. Choose region
----------------

Set your region to "US West (Oregon)".

4. Launch an instance
---------------------

When launching an instance, select "Community AMIs", and search for the AMI you selected in Step 1 (above).

5. Configure
------------

When prompted to set up a security group, make sure that port 22 is open. Next, when prompted to set up an SSH keypair, choose "Proceed without a keypair".

6. Log in
---------

Once the machine has finished booting, you can SSH into it by running ``ssh qiime2@<PUBLIC_AWS_IP_ADDRESS>``, replacing ``<PUBLIC_AWS_IP_ADDRESS>`` with the public IP address for the machine (this will be provided by AWS). When prompted, provide the password ``qiime2``.

.. _`AWS AMIs`: https://data.qiime2.org/distro/core/aws-amis.txt
