#!/bin/bash

find . -name __pycache__ | xargs rm -rf
rm -rf build
rm -rf src/financeMacroFactors.egg-info
rm -rf .pytest_cache