"""
Lotus Stat
=====================

This package covers python routines, objects and structures to analyse Lotus output files.

=====================
C.Losada de la Lastra
"""

from .__version__ import version
from .plots import *

def hello():
    # test function to confirm import has succeded
    print('hello from Lotus Stat version {0}'.format(version))
