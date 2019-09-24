# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name              = 'stepwisereg',
    packages          = ['stepwisereg'],
    version           = '0.1.0',
    description       = 'Stepwise Regression in Python',
    long_description  = 'Forward Stepwise Regression in Python like R using AIC',
    author = 'Avinash Barnwal',
    author_email = 'avinashbarnwal123@gmail.com',
    url = 'https://github.com/avinashbarnwal/stepwisereg',
    maintainer='Avinash Barnwal',
    maintainer_email='avinashbarnwal123@gmail.com',
    install_requires=[
    'numpy',
    'pandas',
	'sklearn',
	'patsy',
	'statsmodel',
	'functools',
	're'
    ],
    download_url = 'https://github.com/avinashbarnwal/stepwisereg/tarball/0.1.11',
    keywords = ['stepwise', 'python3', 'sklearn','regression'],
    license='The MIT License (MIT)',
    classifiers = ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
)
