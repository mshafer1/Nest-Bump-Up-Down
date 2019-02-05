from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='PythonTempSetterShifter',  # Required
    version='0.0.1',  # Required
    description='A basic util for shifting a nest thermostat up or down',  # Optional
    packages=find_packages(),  # Required
    install_requires=['python-nest'],
    )
