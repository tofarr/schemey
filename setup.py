import setuptools

from schemey.__version__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schemey",
    version="5.0.0",
    author="Tim O'Farrell",
    author_email="tofarr@gmail.com",
    description="Convention over configuration Object Schemas for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tofarr/schemey",
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    install_requires=["marshy~=2.4", "jsonschema~=4.8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
