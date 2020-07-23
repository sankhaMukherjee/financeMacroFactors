Installing
==========

TLDR
-----

```bash
python3 -m venv env
source env/bin/activate
pip3 install git+https://github.com/sankhaMukherjee/financeMacroFactors.git
```

Detailed Installation
---------------------

This is the repository is meant to be used for installing the financeMacroFactors package. 
A wheel dstribution of this package is present in the `dist` folder and may be 
installed within your virtual enviroonment. 

`pip3 install financeMacroFactors-<version>-py3-none-any.whl`

Note that the `dist` folder is not included within this repo because the package might 
become excessively large. You will need do clone the repository and build the package yourself
on your system.

Alternatively, since git allows you to install packages directly from Github. Consider 
doing the following within your virtual environment:

`pip3 install git+https://github.com/sankhaMukherjee/financeMacroFactors.git`

Building from source
--------------------

You may wish to make customize this package for your own use. For that, you need to build the system:

 - Clone this repo to your computer
 - Install a virtual enviromnent, and istall the required packages
 - Buid the system

 A `Makefile` has been provided for aiding with this process. The following commands should allow you do do the following

  - `make grantPermission`: grants execute permission to all shell scripts in the [`bin`](../master/bin) folder
  - `make clean`: clean unwanted and temporary files that are generated
  - `make build`: This will allow you to build Wheel packages for your system
