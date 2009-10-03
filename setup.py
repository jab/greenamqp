#!/usr/bin/env python
"""
Python Distutils setup for for amqp.  Build and install with

    python setup.py install

2009-10-01 Luke Tucker <ltucker@openplans.org>
2007-11-10 Barry Pederson <bp@barryp.org>

"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name = "greenamqp",
      description = "AMQP Client Library -- for eventlet",
      version = "0.6.1",
      license = "LGPL",
      author = "Luke Tucker",
      author_email = "ltucker@openplans.org",
      url = "http://github.com/ltucker/greenamqp",
      install_requires=['eventlet'],
      packages = ['greenamqp', 'greenamqp.client_0_8']
     )
