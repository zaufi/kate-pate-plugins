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

''' Reusable code for Kate/Pâté plugins: general purpose shared code '''

import kate

_COMMENT_STRINGS_MAP = {
    'Python' : '# '
  , 'Perl'   : '# '
  , 'CMake'  : '# '
  , 'Bash'   : '# '
  , 'C++'    : '//'
}


def isKnownCommentStyle(docType):
    ''' Check if we know how to comment a line in a given document type '''
    return docType in _COMMENT_STRINGS_MAP

def getCommentStyleForDoc(document):
    ''' Get single line comment string for a document '''
    assert(document.highlightingMode() in _COMMENT_STRINGS_MAP)
    return _COMMENT_STRINGS_MAP[document.highlightingMode()]
