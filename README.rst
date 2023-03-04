turba
=====
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/turba
    :target: https://pypi.org/project/turba/
    :alt: PyPI
.. image:: https://github.com/jshwi/turba/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/jshwi/turba/actions/workflows/build.yaml
    :alt: Build
.. image:: https://github.com/jshwi/turba/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/turba/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://results.pre-commit.ci/badge/github/jshwi/turba/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/turba/master
   :alt: pre-commit.ci status
.. image:: https://codecov.io/gh/jshwi/turba/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/turba
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/turba/badge/?version=latest
    :target: https://turba.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort
.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: docformatter
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. image:: https://snyk.io/test/github/jshwi/turba/badge.svg
    :target: https://snyk.io/test/github/jshwi/turba/badge.svg
    :alt: Known Vulnerabilities
.. image:: https://snyk.io/advisor/python/turba/badge.svg
    :target: https://snyk.io/advisor/python/turba
    :alt: turba

Turbocharged torrent scraper
----------------------------

Requires `transmission-daemon`

Usage
*****

.. code-block:: console

    usage: turba [-h] URL

    positional arguments:
      URL         url to harvest

    optional arguments:
      -h, --help  show this help message and exit
