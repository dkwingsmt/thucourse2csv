#!/usr/bin/python2
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import sys

sys.argv = (sys.argv[0], 'py2exe')
setup(console=["tkgui.py"])
