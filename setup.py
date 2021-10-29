#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open('requirements.txt', 'r') as _requirements:
    requires = _requirements.read()

requirements = [r.strip() for r in requires.split('\n') if ((r.strip()[0] != "#"))]

version = "0.1.0"

setup(
    author="Carsten Frommhold",
    author_email="carsten.frommhold@datadrivers.de",
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    description="Match Classifier",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    name="reco-preprocessing",
    package_dir={"": "src"},
    packages=find_packages("src"),
    version=version,
    zip_safe=False
)
