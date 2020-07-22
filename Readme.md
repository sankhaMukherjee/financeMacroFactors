# financeMacroFactors

One Paragraph of project description goes here

## Prerequisites

You will need to have a valid Python installation on your system. This has been tested with Python 3.6. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development 
and testing purposes. Detailed documentation is present [here](https://sankhamukherjee.github.io/financeMacroFactors/).

### Package Installation

This is the repository is meant to be used for installing the financeMacroFactors package. 
A wheel dstribution of this package is present in the [`dist`](../master/dist) folder and may be 
installed within your virtual enviroonment. Just download this directly into your folder and install 
like any other pip package as:

`pip3 install financeMacroFactors-<version>-py3-none-any.whl`

Git alternatively allows you to install packages directly from Github. Consider doing the following:

`pip3 install git+https://github.com/sankhaMukherjee/financeMacroFactors.git`

This has been built upon a Unix system. If you use this for other systems, you may wish to consider building this library from source.

### Package Building

You may wish to make customize this package for your own use. For that, you need to build the system:

 - Clone this repo to your computer
 - Install a virtual enviromnent, and istall the required packages
 - Buid the system

 A `Makefile` has been provided for aiding with this process. The following commands should allow you do do the following

  - `make grantPermission`: grants execute permission to all shell scripts in the [`bin`](../master/bin) folder
  - `make clean`: clean unwanted and temporary files that are generated
  - `make build`: This will allow you to build Wheel packages for your system

## Contributing

Please make any changes/updates in a new branch, and then send in a pull request. When you incorporate new
changes to the repo, please consider updating the documentation including creating some examples and some
tutorials that will allow users to properly use this repo.

Furthermore, it is very useful to create unit tests for your package. This is going to allow you to generate
high-quality packages that will have lower failure-rates in the real world.

There is a Makefile that will aid you in the process.

  - `make docs`: automatically generate the documentation after making changes to it. 
  - `make tests`: will allow you to run unit tests

Additionally, if `tox` is properly installed on your system, you can use it to test across multiple
Python installed versions just by issuing the `tox` command. 

## Authors

Sankha S. Mukherjee - Initial work (2020)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

 - Hat tip to anyone who's code was used
 - Inspiration
 - etc.
 