**IMPORTANT:** These instructions no longer work. We are working on fixing them.

*These instructions are intended for QIIME 2 and plugin developers. If you are just using QIIME 2, you probably don't need to, but are welcome to read these notes.*

# Publishing a Plugin on Conda

You'll need to have ``conda-build`` and ``anaconda-client`` installed to perform these steps. Both can be conda-installed. First, log into anaconda with your anaconda username using the following command. You should have access to push to the anaconda account through your account (if you don't, get in touch with the owner of that account).

    anaconda login

Due to the fact that Conda is a binary distribution manager, an ``osx-64`` package will need to be built on OS X, and a ``linux-64`` package will need to be built on 64-bit Linux. These steps will be the same on all platforms, so you should repeat them for every platform you want to release for.

First we need to create the recipe, we can use the `--manual-url` flag to base it on a github release:

    conda skeleton pypi --manual-url <url to github release .zip>

Next you should expect to run `conda build` to see what is not available on conda, those packages you should place `pip install` commands for in `build.sh` file in the generated recipe. For some dependencies you may need to specify multiple channels to get them from for example:

    conda build -c <dependency1> -c <dependency2> <project name> --python 3.5

The order in which the channels are specified are very important, as soon as conda finds the package, it will use that channel, even if the package does not meet the version requirements.

Once the build completes successfully you will have a bdist of a 3.5 package. The absolute path to the packages will be provided as output from the ``conda build`` command.

    anaconda upload -u <your-conda-channel> <package-filepath>

``<package-filepath>`` should be replaced with the path to the package that was was created above.

After uploading, you should create a new environment for the package you uploaded, install the package, and re-run the tests. You can install the package you uploaded as follows:

    conda install -c <your-conda-channel> <your package>

**NOTE: an admin must be the first user to upload to a conda channel, then other users on a release-manager list can upload**
