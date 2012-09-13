#!/usr/bin/python2
# -*- coding: utf-8 -*-

#    © Copyright 2012 MOU Tong (DKWings).
#
#    This file is part of thucourse2csv.
#
#    Thucourse2csv is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Thucourse2csv is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with thucourse2csv.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
import py2exe
import sys

sys.argv = (sys.argv[0], 'py2exe')
setup(console=["tkgui.py"])
