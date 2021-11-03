import setuptools

from persisty.__version__ import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lambsync',
    version=__version__,
    author="Tim O'Farrell",
    author_email='tofarr@gmail.com',
    description='A better persistence layer for python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/tofarr/lambsync",
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=['typing-inspect>=0.7.1', 'marshy>=1.1.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
