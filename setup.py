"""setup.py controls the build, testing, and distribution of the egg"""
import re
import os.path
from setuptools import setup, find_packages

VERSION_REGEX = re.compile(r"""
    ^__version__\s=\s
    ['"](?P<version>.*?)['"]
""", re.MULTILINE | re.VERBOSE)

VERSION_FILE = os.path.join("hcl2", "version.py")


def get_long_description():
    """Reads the long description from the README"""
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as file:
        return file.read()


def get_version():
    """Reads the version from the package"""
    with open(VERSION_FILE, encoding='utf8') as handle:
        lines = handle.read()
        result = VERSION_REGEX.search(lines)
        if result:
            return result.groupdict()["version"]
        raise ValueError("Unable to determine __version__")


def get_requirements():
    """Reads the installation requirements from requirements.txt"""
    with open("requirements.txt", encoding='utf8') as reqfile:
        return [line for line in reqfile.read().split("\n") if not line.startswith(('#', '-'))]


setup(
    name='bc-python-hcl2',
    python_requires='>=3.8',
    version=get_version(),
    description="A parser for HCL2",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Typing :: Typed',
    ],
    keywords='',
    author='bridgecrew',
    author_email='meet@bridgecrew.io',
    url='https://github.com/bridgecrewio/python-hcl2',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    scripts=[
        'bin/hcl2tojson',
    ],
)
