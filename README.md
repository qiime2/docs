# QIIME 2 documentation source
Source repository for https://docs.qiime2.org.

This repository does not include built docs. **Do not commit built docs to this repository.**

Make source changes in this repository as described in **Contributing to the docs** below and submit these changes as a pull request.

Contributing source changes is a separate step from building and publishing the changes. See **Publishing** below for building and publishing the docs to the live site (typically this will be done by one of the QIIME 2 developers).

## Contributing to the docs

1. Install the QIIME 2 framework. Typically you'll want the latest development version (i.e. master branch). You can find the [latest builds for your operating system here](https://github.com/qiime2/environment-files/tree/master/latest/staging). Make sure you get the raw link for your OS (e.g. `linux-64` or `osx-64`), download that file and then you can use `conda env create -n qiime2-docs --file path-to-yml` to install.

2. Install the dependencies necessary to build the docs, you need to run this command within the `qiime2-docs` folder:

   ```shell
   pip install -r requirements.txt
   ```

3. Make your changes to the source RST.

   When writing shell commands in the docs, use the custom ``.. command-block::`` directive. This directive formats the commands with shell syntax highlighting and will execute each command, reporting any errors (similar to doctests). You'll need the latest development versions (i.e. master branches) of the QIIME 2 packages required by the commands in the docs.

   If you're writing shell commands that shouldn't be automatically executed (e.g. ``conda`` install commands, ``cd`` commands, etc.), use the ``:no-exec:`` option with the ``command-block`` directive. Check out the existing docs for examples.

4. Run ``make preview`` to build the docs without running any of the ``command-block`` commands. Use this to quickly build the docs while developing them (e.g. to check correct rendering of RST).

5. Run ``make linkcheck`` to make sure all URLs can be reached.

6. When you're done with your changes, run ``make html`` to build the docs and run all ``command-block`` commands. This can take awhile to complete (currently 20-30 minutes). If you didn't make changes to any ``command-block`` commands, or add any new ones, you can skip this step.

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
