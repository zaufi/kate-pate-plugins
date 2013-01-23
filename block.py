# -*- coding: utf-8 -*-
#
# Kate/Pâté plugins to work with code blocks
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
#
# Here is a short list of plugins in this file:
#
#   Insert Char From Line Above (Meta+E)
#       add the same char to the current cursor position as in the line above
#
#   Insert Char From Line Below (Meta+W)
#       add the same char to the current cursor position as in the line below
#
#   Kill Text After Cursor (Meta+K)
#       remove text from cursor position to the end of the current line
#
#   Kill Text Before Cursor (Meta+U)
#       remove text from cursor position to the start of the current line
#       but keep leading spaces (to avoid breaking indentation)
#
#   Wrap into Braces (Ctrl+'(')
#       wrap current word (identifier) or selection into pair of '(' and ')' characters
#
#   Wrap into Brackets (Ctrl+{')
#       wrap current word (identifier) or selection into pair of '[' and ']' characters
#
#   Wrap into Curve Brackets (Meta+{')
#       wrap current word (identifier) or selection into pair of '{' and '}' characters
#
#   Wrap into Angle Brackets (Ctrl+<')
#       wrap current word (identifier) or selection into pair of '<' and '>' characters
#
#   Wrap into Quotes (Ctrl+')
#       wrap current word (identifier) or selection into pair of '"' characters
#

import kate
import kate.gui

from PyKDE4.ktexteditor import KTextEditor

from libkatepate import ui, common

@kate.action('Insert Char From Line Above', shortcut='Meta+E')
def insertCharFromLineAbove():
    '''add the same char to the current cursor position as in the line above'''
    doc = kate.activeDocument()
    view = kate.activeView()
    pos = view.cursorPosition()

    if pos.line() == 0:
        return

    lineAbove = doc.line(pos.line() - 1)
    char = lineAbove[pos.column():pos.column() + 1]
    if not bool(char):
        return

    doc.startEditing()
    doc.insertText(pos, char)
    doc.endEditing()


@kate.action('Insert Char From Line Below', shortcut='Meta+W')
def insertCharFromLineBelow():
    '''add the same char to the current cursor position as in the line below'''
    doc = kate.activeDocument()
    view = kate.activeView()
    pos = view.cursorPosition()

    if pos.line() == 0:
        return

    lineBelow = doc.line(pos.line() + 1)
    char = lineBelow[pos.column():pos.column() + 1]
    if not bool(char):
        return

    doc.startEditing()
    doc.insertText(pos, char)
    doc.endEditing()


@kate.action('Kill Text After Cursor', shortcut='Meta+K')
def killRestOfLine():
    '''remove text from cursor position to the end of the current line'''
    doc = kate.activeDocument()
    view = kate.activeView()
    pos = view.cursorPosition()

    endPosition = KTextEditor.Cursor(pos.line(), doc.lineLength(pos.line()))
    killRange = KTextEditor.Range(pos, endPosition)

    doc.startEditing()
    doc.removeText(killRange)
    doc.endEditing()


@kate.action('Kill Text Before Cursor', shortcut='Meta+U')
def killLeadOfLine():
    ''' Remove text from a start of a line to the current crsor position

        NOTE This function suppose spaces as indentation character!
        TODO Get indent character from config
    '''
    doc = kate.activeDocument()
    view = kate.activeView()
    pos = view.cursorPosition()

    indent = common.getCurrentLineIndentation(view)
    startPosition = KTextEditor.Cursor(pos.line(), 0)
    killRange = KTextEditor.Range(startPosition, pos)

    doc.startEditing()
    doc.removeText(killRange)
    doc.insertText(startPosition, ' ' * indent)
    doc.endEditing()


def _wrapRange(rangeToWrap, openCh, closeCh, doc = None):
    if not doc:
        doc = kate.activeDocument()

    doc.startEditing()                                      # Start atomic UnDo operation
    doc.replaceText(rangeToWrap, openCh + doc.text(rangeToWrap) + closeCh)
    doc.endEditing()                                        # Done editing


def _wrapBlockWithChar(openCh, closeCh, indentMultiline = True):
    '''Wrap next word or selection (if any) into given open and close chars

       If current selection is multiline, add one indentation level and put
       open/close chars on separate lines
    '''
    doc = kate.activeDocument()
    view = kate.activeView()
    pos = view.cursorPosition()

    # Try to extend selection to be started from 0 columns at both ends
    common.extendSelectionToWholeLine(view)

    selectedRange = view.selectionRange()
    if selectedRange.isEmpty():
        # No text selected. Ok, lets wrap a word where cursor positioned
        wordRange = common.getBoundTextRangeSL(
            common.CXX_IDENTIFIER_BOUNDARIES
          , common.CXX_IDENTIFIER_BOUNDARIES
          , pos
          , doc
          )
        _wrapRange(wordRange, openCh, closeCh, doc)
    else:
        if selectedRange.start().line() == selectedRange.end().line() or indentMultiline == False:
            # single line selection (or no special indentation required)
            _wrapRange(selectedRange, openCh, closeCh, doc)

            # extend current selection
            selectedRange.end().setColumn(selectedRange.end().column() + len(openCh) + len(closeCh))
            view.setSelection(selectedRange)
        else:
            # multiline selection
            # 0) extend selection to capture whole lines
            gap = ' ' * common.getLineIndentation(selectedRange.start().line(), doc)
            text = gap + openCh + '\n' \
              + '\n'.join([' ' * 4 + line for line in doc.text(selectedRange).split('\n')[:-1]]) \
              + '\n' + gap + closeCh + '\n'
            doc.startEditing()
            doc.replaceText(selectedRange, text)
            doc.endEditing()

            # extend current selection
            selectedRange.end().setColumn(selectedRange.end().column() + len(openCh) + len(closeCh))
            r = KTextEditor.Range(selectedRange.start().line(), 0, selectedRange.end().line() + 2, 0)
            view.setSelection(r)


@kate.action('Wrap into Braces', shortcut='Ctrl+(')
def wrapBlockWithBraces():
    '''wrap current word (identifier) or selection into pair of '(' and ')' characters'''
    _wrapBlockWithChar('(', ')')

@kate.action('Wrap into Brackets', shortcut='Ctrl+{')
def wrapBlockWithBraces():
    '''wrap current word (identifier) or selection into pair of '[' and ']' characters'''
    _wrapBlockWithChar('[', ']')

@kate.action('Wrap into Curve Brackets', shortcut='Meta+{')
def wrapBlockWithBraces():
    '''wrap current word (identifier) or selection into pair of '{' and '}' characters'''
    _wrapBlockWithChar('{', '}')

@kate.action('Wrap into Angle Brackets', shortcut='Ctrl+<')
def wrapBlockWithBraces():
    '''wrap current word (identifier) or selection into pair of '<' and '>' characters'''
    _wrapBlockWithChar('<', '>')

@kate.action('Wrap into Quotes', shortcut='Ctrl+\'')
def wrapBlockWithBraces():
    '''wrap current word (identifier) or selection into pair of '"' characters'''
    _wrapBlockWithChar('"', '"', False)
