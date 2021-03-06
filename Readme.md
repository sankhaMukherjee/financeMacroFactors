# financeMacroFactors

This library generates provides a set of convenience functions that will allow one to
generate macro economic factors and company financials within a single library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development 
and testing purposes. Detailed documentation is present [here](https://sankhamukherjee.github.io/financeMacroFactors/).

### Package Installation

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
 