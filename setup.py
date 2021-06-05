#from distutils.core import setup
from setuptools import setup

setup(
    name='FileSer',
    version='1.0',
    description="Convert data to json/pickle/toml/yaml formats",
    author="YULIYA2001",
    url='https://github.com/YULIYA2001',
    packages=["lib/parsers", "lib/serializer", "lib/convertor"],
    install_requires=["pytomlpp", "pyyaml"],
    #test_suite='unittests',
    scripts=["start.py"]
)
