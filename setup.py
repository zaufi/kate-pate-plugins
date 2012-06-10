# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Alex Turbov <i.zaufi@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name = 'kate-pate-plugins'
  , version = '0.5'
  , description = 'Kate+Pâté plugins (mostly for C++)'
  , author = 'Alex Turbov'
  , author_email = 'i.zaufi@gmail.com'
  , url = 'https://github.com/zaufi/kate-pate-plugins/'
  , license = 'GPL-3'
  , keywords = ['kate', 'pate']
  , packages = ['libkatepate']
  , py_modules = ['format', 'commentar', 'block']
  , data_files = ['README.md', 'CHANGES.md']
  , requires = ['kate']
  , classifiers = [
        "Development Status :: 4 - Beta"
      , "Environment :: Plugins"
      , "Intended Audience :: Developers"
      , "Natural Language :: English"
      , "Programming Language :: Python :: 2.7"
      , "Topic :: Software Development"
    ]
  )
