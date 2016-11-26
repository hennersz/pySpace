from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Satellite Simulator",
    version = "0.0.1",
    author = "Henry Mortimer",
    author_email = "henry@ucl.ac.uk",
    description = ("A simplistic simulation of satellite orbits based on the two body problem"),
    long_description = read("README.md"),
    license = "GNU",
    keywords = "space satellite simulation",
    url = "https://github.com/hennersz/pySpace",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: GNU Licence",
    ],
    include_package_data = True
)

