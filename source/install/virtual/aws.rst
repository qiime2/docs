Installing QIIME 2 using Amazon Web Services
============================================

1. Set up an AWS account at https://aws.amazon.com, and log in.
2. Set your region to "US West (Oregon)".
3. When launching an instance, select "Community AMIs", and search for "QIIME 2 Core" (the AMI ID is `ami-c401aca4`).
4. When prompted to set up a security group, make sure that port 22 is open.
5. When prompted to set up an SSH keypair, choose "Proceed without a keypair".
6. Once the machine has finished booting, you can SSH into it by running ``ssh qiime2@<PUBLIC_AWS_IP_ADDRESS>``, replacing ``<PUBLIC_AWS_IP_ADDRESS>`` with the public IP address for the machine (this will be provided by AWS). When prompted, provide the password ``qiime2``.
