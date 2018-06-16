from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

# workaround from https://github.com/pypa/setuptools/issues/308 to avoid "normalizing" version "2018.01.09" to "2018.1.9":
import pkg_resources
pkg_resources.extern.packaging.version.Version = pkg_resources.SetuptoolsLegacyVersion

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name="mediathekview_change_downloads_to_http",
    version="2018.06.16.1",
    description="Modify pending MediathekView download URLs from https to http",
    author="Karl Voit",
    author_email="tools@Karl-Voit.at",
    url="https://github.com/novoid/mediathekview_change_downloads_to_http",
    download_url="https://github.com/novoid/mediathekview_change_downloads_to_http/zipball/master",
    keywords=["ORF", "downloads", "workaround", "MediathekView"],
    install_requires=['shutil'],
    packages=find_packages(), # Required
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        ],
    entry_points={  # Optional
        'console_scripts': [
            'mediathekview_change_downloads_to_http=mediathekview_change_downloads_to_http:main',
        ],
    },
#    long_description=long_description, # Optional
    long_description="""\
Usage:
    mediathekview_change_downloads_to_http.py

    This little Python script tries to locate the MediathekView XML
    file containing pending downloads, change their protocol from
    https to http and re-writes the XML file accordingly.

    Read
    https://github.com/novoid/mediathekview_change_downloads_to_http
    for further information.

:copyright: (c) by Karl Voit
:license: GPL v3 or any later version
:URL: https://github.com/novoid/mediathekview_change_downloads_to_http
:bugreports: via github or <tools@Karl-Voit.at>

Options:
  -h, --help     show this help message and exit
  -d, --dryrun   enable dryrun mode: just simulate what would happen, do not
                 modify files
  -v, --verbose  enable verbose mode
  -q, --quiet    enable quiet mode
  --version      display version and exit
"""
)
