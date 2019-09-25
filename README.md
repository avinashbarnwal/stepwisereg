# Stepwise-Regression


[![PyPI version](https://badge.fury.io/py/stepwisereg.svg)](https://badge.fury.io/py/stepwisereg)

Stepwise Regression in Python.

# Table of Contents

* About OR-Tools
Codemap
Installation
Experimental Build with CMake
Quick Start
Documentation
Contributing
License
Currently Statmodels package in python doesn't have stepwise regression, so i thought why not we create it. I have implemented using AIC and BIC and it has been motivated from http://trevor-smith.github.io/stepwise-post/.

Idea is to build like R-Stepwise having null and full models formula.

I have also added complete example in code.py using test_data.csv . Here dependent variable is "OS_MONTHS" and we can change it based on dataset.
