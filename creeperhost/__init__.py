"""
Creeperhost.py - An asynchronous wrapper for the CreeperHost API written in Python
"""


__name__ = "creeperhost"
__author__ = "CheesyGamer77"
__version__ = "0.0.1a"


import logging
from collections import namedtuple
from .client import Client


VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel')
version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha')

logging.getLogger(__name__).addHandler(logging.NullHandler())
