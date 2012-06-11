# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 by Alex Trubov <i.zaufi@gmail.com>
#
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
#

''' Reusable code for Kate/Pâté plugins: C++ document types related common code '''

import kate
from libkatepate import ui


def cpp_only(action):
    ''' Decorator to enable @kate.action only for C++ documents
    '''
    def checker(**params):
        document = kate.activeDocument()
        if document.highlightingMode() == 'C++':
            return action(**params)
        else:
            ui.popup("Alert", "This action have sense <b>only</b> for C++ documents!")
    return checker
