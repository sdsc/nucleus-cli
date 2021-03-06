from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install
import os
import shutil
import sys
import platform

try:
    import cloudmesh_base
    print ("Using cloudmesh_base version:", cloudmesh_base.__version__)
except:
    # os.system("pip install cloudmesh_base")
    os.system("pip install git+https://github.com/cloudmesh/base.git")

from cloudmesh_base.util import banner
from cloudmesh_base.setup import os_execute, get_version_from_git
from nucleus_cli import __version__
version = get_version_from_git()

banner("nucleus cli {:}".format(__version__))

requirements = [
    "cloudmesh_base",
    "cloudmesh_cmd3light",
    "docopt",]

class UploadToPypi(install):
    """Upload the package to pypi. -- only for Maintainers."""

    description = __doc__

    def run(self):
        os.system("make clean")
        commands = """
            python setup.py install
            python setup.py bdist_wheel            
            python setup.py sdist --format=bztar,zip upload
            """
        os_execute(commands)    

class InstallBase(install):
    """Install the nucleus_cli package."""

    description = __doc__

    def run(self):
        banner("Install readline")
        commands = None
        this_platform = platform.system().lower()
        if  this_platform in ['darwin']:
            commands = """
                easy_install readline
                """
        elif this_platform in ['windows']:
            commands = """
                pip install pyreadline
                """
        if commands:
            os_execute(commands)
        import nucleus_cli
        banner("Install nucleus_cli {:}".format(version))
        install.run(self)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    version=version,
    name="nucleus_cli",
    description="nucleaus_cli - Creating virtual clusters",
    long_description=read('README.rst'),
    license="Apache License, Version 2.0",
    author="Gregor von Laszewski",
    author_email="laszewski@gmail.com",
    url="https://github.com/sdsc/nucleus-roll.git",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console"
    ],
    keywords="comet virtual cluster",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'comet = nucleus_cli.cm:main',
        ],
    },
    cmdclass={
        'install': InstallBase,
        'pypi': UploadToPypi,
    },
    dependency_links = []
)

