#!/bin/bash

cd myDocs
sphinx-apidoc -f -o source ../financeMacroFactors
sphinx-build -b html -aE -d doctrees -c source source build/html
cd ..
rm -rf docs
cp -r myDocs/build/html docs
touch docs/.nojekyll
