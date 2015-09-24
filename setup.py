#!/usr/bin/env python
# ----------------------------------------------------------------------- #
# Gregor von Laszewski, Indiana UNiversity, SDSC TBD
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may #
# not use this file except in compliance with the License. You may obtain #
# a copy of the License at                                                #
#                                                                         #
# http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                         #
# Unless required by applicable law or agreed to in writing, software     #
# distributed under the License is distributed on an "AS IS" BASIS,       #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.#
# See the License for the specific language governing permissions and     #
# limitations under the License.                                          #
# ------------------------------------------------------------------------#
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
from cloudmesh_base.util import path_expand
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import auto_create_version
from cloudmesh_base.setup import parse_requirements, os_execute, get_version_from_git

version = get_version_from_git()

banner("nucleus cli {:}".format(version))

requirements = parse_requirements('requirements.txt')

auto_create_version("nucleus_cli", version, filename="version.py")
        
class UploadToPypi(install):
    """Upload the package to pypi. -- only for Maintainers."""

    description = __doc__

    def run(self):
        auto_create_version("cloudmesh_client", version, filename="version.py")
        os.system("make clean")
        commands = """
            python setup.py install
            python setup.py bdist_wheel            
            python setup.py sdist --format=bztar,zip upload
            """
        os_execute(commands)    

class InstallBase(install):
    """Install the cloudmesh_client package."""

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
        import cloudmesh_client
        banner("Install Cloudmesh_client {:}".format(version))
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
            'vcluster = nucleus_cli.cli:main',
        ],
    },
    cmdclass={
        'install': InstallBase,
        'pypi': UploadToPypi,
    },
    dependency_links =
        ['git+https://github.com/cloudmesh/base.git']
)

