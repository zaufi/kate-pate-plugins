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

import functools
import kate
from libkatepate import ui
from libkatepate import common

def append_constraint(action, constraint):
    if not hasattr(action, 'constraints'):
        action.constraints = []
    print("*** append_constraint: c=" + repr(constraint))
    action.constraints.append(constraint)


def check_constraints(action):
    ''' Decorator to evaluate constraints assigned to a given action '''
    def checker(*args, **kw):
        document = kate.activeDocument()
        # TODO Why this shit^W`if` doesn't work? WTF?!
        #if not hasattr(action, 'constraints') or reduce(lambda i, j: i(document) and j(document), action.constraints)():
        if hasattr(action, 'constraints'):
            for c in action.constraints:
                if not c(document):
                    return
        return action(*args, **kw)
    return checker


def restrict_doc_type(docType):
    def restrict_doc_type_decorator(action):
        # TODO Investgate required why in opposite params order
        # keyword arguments can't pass through `partial` binder
        # WTF?? WTF!!
        def doc_type_checker(doc_type, document):
            if document.highlightingMode() != doc_type:
                ui.popup(
                    "Alert"
                  , "This action have sense <b>only</b> for " + doc_type + " documents!"
                  , "face-wink"
                  )
                return False
            return True
        binded_predicate = functools.partial(doc_type_checker, docType)
        append_constraint(action, binded_predicate)
        return action
    return restrict_doc_type_decorator


def comment_char_must_be_known(dummy = None):
    def comment_char_known_decorator(action):
        # TODO Same shit here as for restrict_doc_type!
        def comment_char_checker(dummy, document):
            doc_type = document.highlightingMode()
            result = common.isKnownCommentStyle(doc_type)
            if not result:
                ui.popup(
                    "Oops!"
                  , "Don't know how comments look like for " + doc_type + " documents!"
                  , "face-uncertain"
                  )
            return result
        binded_predicate = functools.partial(comment_char_checker, dummy)
        append_constraint(action, binded_predicate)
        return action
    return comment_char_known_decorator
