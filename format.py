# -*- coding: utf-8 -*-
#
# Kate/Pâté plugins to work with C++ code formatting
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
# Here is a short list of plugins in this file:
#
#
#   Boost-like Format Params (Meta+F)
#       Format function's/template's parameters list (or `for`'s) in a boost-like style
#       I.e. when 2nd and the rest parameters has leading comma/semicolon
#       and closing ')' or '>' on a separate line.
#       THIS IS REALLY BETTER TO HAVE SUCH STYLE WHEN U HAVE A LONG PARAMETERS LIST!
#
#   Unformat Function Params (Meta+Shift+F)
#       merge everything between '(' and ')' into a single line
#
#

import kate

from PyKDE4.ktexteditor import KTextEditor
from libkatepate import ui

def getLeftNeighbour(lineStr, column):
    if column:
        return lineStr[column - 1]
    return None

def getRightNeighbour(lineStr, column):
    if (column + 1) < len(lineStr):
        return lineStr[column + 1]
    return None

def looksLikeTemplateAngelBracket(lineStr, column):
    """ Check if a symbol at given position looks like a template angel bracket
    """
    assert(lineStr[column] in '<>')
    print("?LLTAB: ch='" + lineStr[column] + "'")
    ln = getLeftNeighbour(lineStr, column)
    print("?LLTAB: ln='" + str(ln) + "'")
    rn = getRightNeighbour(lineStr, column)
    print("?LLTAB: rn='" + str(rn) + "'")
    # Detect possible template
    if lineStr[column] == '<':                              # --[current char is '<']-------
        if ln == '<' or rn == '<':                          # "<<" in any place on a line...
            return False                                    # ... can't be a template!
        if ln == ' ' and rn == '=':                         # " <="
            return False                                    # operator<=()
        if lineStr[0:column].strip().startswith('template'):# template declaration at the start of line
            return True                                     # ... possible smth like `template < typename ...'
        if ln == ' ' and rn == ' ':                         # " < "
            return False                                    # operator<()
        return True
    if lineStr[column] == '>':                              # --[current char is '>']-------
        if lineStr.strip().startswith('>'):                 # line starts w/ one or more '>'
            return True                                     # ... can be end of formatted `typedef <...\n> type;' for example
        if ln == ' ' and rn == ' ':                         # " > "
            return False                                    # operator>()
        if ln == ' ' and rn == '=':                         # ">="
            return False                                    # operator>=()
        if ln == '-':
            return False                                    # operator->()
        return True
    pass

#
# TODO Probably decorators may help to simplify this code ???
#
def getRangeTopology(breakChars):
    """Get range opened w/ `openCh' and closed w/ `closeCh'

        @return tuple w/ current range, list of nested ranges
                and list of positions of break characters

        @note Assume cursor positioned whithin that range already.
    """
    document = kate.activeDocument()
    view = kate.activeView()
    pos = view.cursorPosition()

    stack = list()
    nestedRanges = list()
    breakPositions = list()
    firstIteration = True
    found = False
    # Iterate from the current line towards a document start
    for cl in range(pos.line(), -1, -1):
        lineStr = str(document.line(cl))
        if not firstIteration:                              # skip first iteration
            pos.setColumn(len(lineStr))                     # set current column to the end of current line
        else:
            firstIteration = False                          # do nothing on first iteration
        # Iterate from the current column to a line start
        for cc in range(pos.column() - 1, -1, -1):
            #print("c: current position" + str(cl) + "," + str(cc) + ",ch='" + lineStr[cc] + "'")
            # Check open/close brackets
            if lineStr[cc] == ')':                          # found closing char: append its position to the stack
                stack.append((cl, cc, False))
                print("o( Add position: " + str(stack[-1]))
                continue
            if lineStr[cc] == '(':                          # found open char...
                if len(stack):                              # if stack isn't empty (i.e. there are some closing chars met)
                    print("o( Pop position: " + str(stack[-1]))
                    nrl, nrc, isT = stack.pop()             # remove last position from the stack
                    if not isT:
                        nestedRanges.append(                # and append a nested range
                            KTextEditor.Range(cl, cc, nrl, nrc)
                          )
                    else:
                        raise LookupError(
                            "Misbalanced brackets: '(' @" + str(cl + 1) + ',' + str(cc + 1) +
                            " and '>' @ " + str(nrl + 1) + ',' + str(nrc + 1)
                          )
                else:                                       # otherwise,
                    openPos = (cl, cc + 1, False)           # remember range start (exclude an open char)
                    print("o( Found position: " + str(openPos))
                    found = True
                    break
                continue
            # Check for template angel brackets
            if lineStr[cc] == '>':
                if looksLikeTemplateAngelBracket(lineStr, cc):
                    stack.append((cl, cc, True))
                    print("o< Add position: " + str(stack[-1]))
                else:
                    print("o< Doesn't looks like template: " + str(cl) + "," + str(cc))
                continue
            if lineStr[cc] == '<':
                if not looksLikeTemplateAngelBracket(lineStr, cc):
                    print("o< Doesn't looks like template: " + str(cl) + "," + str(cc + 1))
                elif len(stack):                            # if stack isn't empty (i.e. there are some closing chars met)
                    print("o< Pop position: " + str(stack[-1]))
                    nrl, nrc, isT = stack.pop()             # remove last position from the stack
                    if isT:
                        nestedRanges.append(                # and append a nested range
                            KTextEditor.Range(cl, cc, nrl, nrc)
                        )
                    else:
                        raise LookupError(
                            "Misbalanced brackets: '<' @" + str(cl + 1) + ',' + str(cc + 1) +
                            " and ')' @ " + str(nrl + 1) + ',' + str(nrc + 1)
                          )
                        raise LookupError("Misbalanced brackets")
                else:
                    openPos = (cl, cc + 1, True)            # remember range start (exclude an open char)
                    print("o< Found position: " + str(openPos))
                    found = True
                    break
                continue
            if lineStr[cc] in breakChars and len(stack) == 0:
                breakPositions.append(KTextEditor.Cursor(cl, cc))
        # Did we found smth on the current line?
        if found:
            break                                           # Yep! Break the outer loop

    if not found:
        return (KTextEditor.Range(), list(), list())        # Return empty ranges if nothing found

    assert(len(stack) == 0)                                 # stack expected to be empty!

    breakPositions.reverse()                                # reverse breakers list required cuz we found 'em in a reverse order :)

    # Iterate from the current position towards the end of a document
    pos = view.cursorPosition()                             # get current cursor position again
    firstIteration = True
    found = False
    for cl in range(pos.line(), document.lines()):
        lineStr = str(document.line(cl))
        if not firstIteration:                              # skip first iteration
            pos.setColumn(0)                                # set current column to the start of current line
        else:
            firstIteration = False                          # do nothing on first iteration
        for cc in range(pos.column(), len(lineStr)):
            #print("c: current position" + str(cl) + "," + str(cc) + ",ch='" + lineStr[cc] + "'")
            # Check open/close brackets
            if lineStr[cc] == '(':
                stack.append((cl, cc, False))
                print("c) Add position: " + str(stack[-1]))
                continue
            if lineStr[cc] == ')':
                if len(stack):
                    print("c) Pop position: " + str(stack[-1]))
                    nrl, nrc, isT = stack.pop()             # remove a last position from the stack
                    if not isT:
                        nestedRanges.append(                # and append a nested range
                            KTextEditor.Range(nrl, nrc, cl, cc)
                        )
                    else:
                        raise LookupError(
                            "Misbalanced brackets: '<' @" + str(nrl + 1) + ',' + str(nrc + 1) +
                            " and ')' @ " + str(cl + 1) + ',' + str(cc + 1)
                          )
                else:
                    closePos = (cl, cc, False)              # remember the range end
                    print("c) Found position: " + str(closePos))
                    found = True
                    break
                continue
            # Check for template angel brackets
            if lineStr[cc] == '<':
                if looksLikeTemplateAngelBracket(lineStr, cc):
                    stack.append((cl, cc, True))
                    print("c> Add position: " + str(stack[-1]))
                else:
                    print("c> Doesn't looks like template: " + str(cl) + "," + str(cc))
                continue
            if lineStr[cc] == '>':
                if not looksLikeTemplateAngelBracket(lineStr, cc):
                    print("c> Doesn't looks like template: " + str(cl) + "," + str(cc))
                elif len(stack):                            # if stack isn't empty (i.e. there are some closing chars met)
                    print("c> Pop position: " + str(stack[-1]))
                    nrl, nrc, isT = stack.pop()             # remove last position from the stack
                    if isT:
                        nestedRanges.append(                # and append a nested range
                            KTextEditor.Range(cl, cc, nrl, nrc)
                        )
                    else:
                        raise LookupError(
                            "Misbalanced brackets: '(' @" + str(nrl + 1) + ',' + str(nrc + 1) +
                            " and '>' @ " + str(cl + 1) + ',' + str(cc + 1)
                          )
                else:
                    closePos = (cl, cc, True)               # remember the range end
                    print("c> Found position: " + str(closePos))
                    found = True
                    break
                continue
            if lineStr[cc] in breakChars and len(stack) == 0:
                breakPositions.append(KTextEditor.Cursor(cl, cc))
        # Did we found smth on the current line?
        if found:
            break                                           # Yep! Break the outer loop

    if not found:
        return (KTextEditor.Range(), list(), list())        # Return empty ranges if nothing found

    assert(len(stack) == 0)                                 # stack expected to be empty!

    if openPos[2] != closePos[2]:
        raise LookupError(
            "Misbalanced brackets: at " + str(openPos[0] + 1) + ',' + str(openPos[1] + 1) +
            " and " + str(closePos[0] + 1) + ',' + str(closePos[1] + 1)
          )

    return (KTextEditor.Range(openPos[0], openPos[1], closePos[0], closePos[1]), nestedRanges, breakPositions)


def boostFormatText(textRange, indent, breakPositions):
    document = kate.activeDocument()
    originalText = document.text(textRange)
    print("Original text:\n'" + originalText + "'")

    # Slice text whithin a given range into pieces to be realigned
    ranges = list()
    prevPos = textRange.start()
    breakCh = None
    indentStr = ' ' * (indent + 2);
    breakPositions.append(textRange.end())
    for b in breakPositions:
        print("* prev pos: " + str(prevPos.line()) + ", " + str(prevPos.column()))
        print("* current pos: " + str(b.line()) + ", " + str(b.column()))
        chunk = (document.text(KTextEditor.Range(prevPos, b))).strip()
        print("* current chunk:\n'" + chunk + "'")
        t = ('\n    ').join(chunk.splitlines())
        print("* current line:\n'" + t + "'")
        if breakCh:
            outText += indentStr + breakCh + ' ' + t + '\n'
        else:
            outText = '\n' + indentStr + '  ' + t + '\n'

        breakCh = document.character(b)
        prevPos = KTextEditor.Cursor(b.line(), b.column() + 1)

    outText += indentStr

    print("Out text:\n'" + outText + "'")
    if outText != originalText:
        document.startEditing()
        document.replaceText(textRange, outText)
        document.endEditing()

@kate.action('Boost-like Format Params', shortcut='Meta+F')
def boostFormat():
    document = kate.activeDocument()
    view = kate.activeView()

    try:
        r, nestedRanges, breakPositions = getRangeTopology(',')
    except LookupError as error:
        ui.popup("Failed to parse C++ expression", str(error), "face-sad")
        return

    if r.isEmpty():                                         # Is range empty?
        ui.popup(
            "Failed to parse C++ expression"
          , "Didn't found anything to format. Sorry..."
          , "face-sad"
          )
        return                                              # Nothing interesting wasn't found...

    # Rescan the range w/ ';' as breaker added if current range is a `for` statement
    if document.line(r.start().line())[0:r.start().column() - 1].rstrip().endswith('for'):
        try:
            r, nestedRanges, breakPositions = getRangeTopology(',;')
        except LookupError as error:
            ui.popup("Failed to parse C++ expression", str(error), "face-sad")
            return

    # Going to format a text whithin a selected range
    lineStr = document.line(r.start().line())
    lineStrStripped = lineStr.lstrip()
    indent = len(lineStr) - len(lineStrStripped)
    if lineStrStripped.startswith(', '):
        indent += 2
    text = boostFormatText(r, indent, breakPositions)


def boostUnformatText(textRange, breakPositions):
    document = kate.activeDocument()
    originalText = document.text(textRange)
    #print("Original text:\n'" + originalText + "'")

    # Join text within a selected range
    prevPos = textRange.start()
    outText = ''.join([line.strip() for line in originalText.splitlines()])

    #print("Out text:\n'" + outText + "'")
    if outText != originalText:
        document.startEditing()
        document.replaceText(textRange, outText)
        document.endEditing()


@kate.action('Unformat Function Params', shortcut='Meta+Shift+F')
def boostFormat():
    document = kate.activeDocument()
    view = kate.activeView()

    try:
        r, nestedRanges, breakPositions = getRangeTopology(',')
    except LookupError as error:
        ui.popup("Failed to parse C++ expression", str(error), "face-sad")
        return

    if r.isEmpty():                                         # Is range empty?
        ui.popup(
            "Failed to parse C++ expression"
          , "Didn't found anything to format. Sorry"
          , "face-sad"
          )
        return                                              # Nothing interesting wasn't found...

    # Rescan the range w/ ';' as breaker added if current range is a `for` statement
    if document.line(r.start().line())[0:r.start().column() - 1].rstrip().endswith('for'):
        try:
            r, nestedRanges, breakPositions = getRangeTopology(',;')
        except LookupError as error:
            ui.popup("Failed to parse C++ expression", str(error), "face-sad")
            return

    # Going to unformat a text whithin a selected range
    text = boostUnformatText(r, breakPositions)
