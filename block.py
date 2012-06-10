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

import kate
import kate.gui

@kate.action('Insert Char From Line Above', shortcut='Meta+E')
def insertCharFromLineAbove():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    if currentPosition.line() == 0:
        return

    lineAbove = document.line(currentPosition.line() - 1)
    char = lineAbove[currentPosition.column():currentPosition.column() + 1]
    if not bool(char):
        return

    document.startEditing()
    document.insertText(currentPosition, char)
    document.endEditing()


@kate.action('Insert Char From Line Below', shortcut='Meta+W')
def insertCharFromLineBelow():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    if currentPosition.line() == 0:
        return

    lineBelow = document.line(currentPosition.line() + 1)
    char = lineBelow[currentPosition.column():currentPosition.column() + 1]
    if not bool(char):
        return

    document.startEditing()
    document.insertText(currentPosition, char)
    document.endEditing()


@kate.action('Kill Text After Cursor', shortcut='Meta+K')
def killRestOfLine():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    originalLine = document.line(currentPosition.line())
    line = originalLine[0:currentPosition.column()]

    if line != originalLine:
        document.startEditing()
        document.removeLine(currentPosition.line())
        document.insertLine(currentPosition.line(), line)
        document.endEditing()


@kate.action('Kill Text Before Cursor', shortcut='Meta+U')
def killRestOfLine():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    originalLine = document.line(currentPosition.line())
    line = originalLine
    spaceCount = len(line) - len(line.lstrip())
    line = ' ' * spaceCount + line[currentPosition.column():]

    if line != originalLine:
        document.startEditing()
        document.removeLine(currentPosition.line())
        document.insertLine(currentPosition.line(), line)
        currentPosition.setColumn(spaceCount)
        view.setCursorPosition(currentPosition)
        document.endEditing()
