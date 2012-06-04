# -*- coding: utf-8 -*-
#
# Kate/Pâté plugins to work with code blocks
# Copyright 2010-2012 by Alex Trubov <i.zaufi@gmail.com>
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
