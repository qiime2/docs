# QIIME 2 documentation source
Source repository for https://docs.qiime2.org.

This repository does not include built docs. **Do not commit built docs to this repository.**

Make source changes in this repository as described in **Contributing to the docs** below and submit these changes as a pull request.

Contributing source changes is a separate step from building and publishing the changes. See **Publishing** below for building and publishing the docs to the live site (typically this will be done by one of the QIIME 2 developers).

## Publishing

Docs are hosted on AWS S3. Perform the following steps to build and publish the docs:

1. Install the AWS CLI. There are [many ways to do this](http://docs.aws.amazon.com/cli/latest/userguide/installing.html). For example, it is pip-installable:

   ```shell
   pip install awscli
   ```

2. [Configure the AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) with the proper login credentials (e.g. access key, secret access key, etc.) to access the ``docs.qiime2.org`` S3 bucket. Access is currently limited to core QIIME 2 developers.

3. Build the docs:

   ```shell
   make html
   ```

4. Upload the built docs to S3, specifying the QIIME 2 version these docs were built for. For example, if the docs were built for the QIIME 2 2.0.6 release, use the bucket prefix (i.e. subdirectory) `2.0.6`. Use ``--delete`` in case the build is replacing a previous versioned build.

   ```shell
   aws s3 sync build/html s3://docs.qiime2.org/<build-version> --acl public-read --delete
   ```

5. **Optional:** If this build should be the default version accessible from https://docs.qiime2.org, modify the HTTP redirect in ``publish-assets/index.html`` to point to this build's version.

   **Note:** The default version should be the latest public release of QIIME 2. Development version builds can be uploaded but should not be redirected to.

   i. Upload the modified ``publish-assets/index.html`` file:

   ```shell
   aws s3 cp publish-assets/index.html s3://docs.qiime2.org/ --acl public-read
   ```

   ii. Commit the modified ``publish-assets/index.html`` file and submit a pull request.

The build should now be available on the live site! :beers:
