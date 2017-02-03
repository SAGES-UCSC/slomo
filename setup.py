from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "_version.py"), encoding="utf-8") as f:
    # sets version
    exec(f.readline())

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="dynamo",
      version=version,
      long_description=long_description,
      description="Dynamical modeling of elliptical galaxies",
      url="https://github.com/adwasser/dynamo",
      author="AsherWasserman",
      author_email="adwasser@ucsc.edu",
      license="MIT",
      packages=["dynamo"],
      install_requires=["numpy", "scipy", "astropy", "emcee", "PyYAML"],
      scripts=["bin/dynamo"])
      

      
