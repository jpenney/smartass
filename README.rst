========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/smartass/badge/?style=flat
    :target: https://smartass.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/jpenney/smartass.svg?branch=main
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/jpenney/smartass

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jpenney/smartass?branch=main&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jpenney/smartass

.. |requires| image:: https://requires.io/github/jpenney/smartass/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/jpenney/smartass/requirements/?branch=main

.. |codecov| image:: https://codecov.io/gh/jpenney/smartass/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/jpenney/smartass

.. |version| image:: https://img.shields.io/pypi/v/smartass.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/smartass

.. |wheel| image:: https://img.shields.io/pypi/wheel/smartass.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/smartass

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/smartass.svg
    :alt: Supported versions
    :target: https://pypi.org/project/smartass

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/smartass.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/smartass

.. |commits-since| image:: https://img.shields.io/github/commits-since/jpenney/smartass/v0.8.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jpenney/smartass/compare/v0.1.0...main



.. end-badges

Apply smart punctuation to subtitles.

* Free software: BSD 3-Clause License

Installation
============

You can install the in-development version with:

.. code-block:: console

    $ pip install -e git://github.com/jpenney/smartass.git#egg=smartass


Documentation
=============

    https://smartass.readthedocs.io/

Command Line Usage
==================

Smarten punctuation:

.. code-block:: console

    $ smartass --skip-actor sign subs1.ass

Unsmarted punctuation:

.. code-block:: console

    $ dumbass subs2.ass

See usage:

.. code-block:: console

    $ smartass --help
    Usage: smartass [OPTIONS] FILE

      Smarten punctionation on ass subtitle files.

    Options:
      --log-level [debug|info|warning|error|critical]
                                      log level displayed  [default: info]
      --no-backup / --backup          enable/disable creation of backup files
                                      [default: True]

      --process-comments / --no-process-comments
                                      enable/disable processing of comment events
                                      [default: False]

      --skip-name ACTOR_NAME          lines by this actor (case insensitive) will
                                      be skipped. May be passed multiple times.

      --version                       Show the version and exit.
      --help                          Show this message and exit.

Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
