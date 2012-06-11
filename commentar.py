# -*- coding: utf-8 -*-
#
# Kate/Pâté plugins to work with C++ comments
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
#   Inline Comment (Alt+D)
#       put a comment (//) after a code line (at position 60)
#       or just move cursor at comment if already present.
#       If there wasn't any comment aside of #else/#endif put
#       corresponding #if condition as default comment
#
#   Move Comment Above (Meta+Left)
#       move on-same-line comment (if presnt) to the line above the current
#
#   Move Comment Inline (Meta+Right)
#       move comment from current line to the line below as
#       on-same-line comment
#
#   Comment Block (Meta+D)
#       wrap selected text (or current line) into a #if0/#endif block
#
#   Toggle Comment Block (Meta+Shift+D)
#       switch current code block to ON(#if1)/OFF(#if0) state.
#       Current means that cursor located inside of it.
#
#   Remove Commented Block (Meta+R)
#       remove #if0 or #if1 and closing #endif around current code block
#       leaving #else part as is
#
#   Transform Doxygen Comments (Meta+X)
#       turn block of '///' doxygen comments into
#       /**
#        *
#        */
#       and vise versa
#
#   Select Current Block (Meta+S)
#       set selection of current (where cursor positioned) #if/#endif block
#

import kate
import kate.gui
import re
from PyKDE4.ktexteditor import KTextEditor


if 'commentar:comment-position' not in kate.configuration:
    kate.configuration['commentar:comment-position'] = int(60)
if 'commentar:comment-threashold' not in kate.configuration:
    kate.configuration['commentar:comment-threashold'] = int(50)

COMMENT_POS = kate.configuration['commentar:comment-position']
COMMENT_THRESHOLD = kate.configuration['commentar:comment-threashold']
BLOCK_ANY_START_SEARCH_RE = re.compile('^\s*#\s*if.*$')
BLOCK_START_SEARCH_RE = re.compile('^\s*#\s*if\s*([01])$')
BLOCK_ELSE_SEARCH_RE = re.compile('^\s*#\s*else.*$')
BLOCK_END_SEARCH_RE = re.compile('^\s*#\s*endif.*$')
BLOCK_ELSE_ENDIF_MATCH_RE = re.compile('^\s*#\s*(endif|else).*$')
BLOCK_START_GET_COND_RE = re.compile('^\s*#\s*(if((n)?def)?)\s+(.*)\s*$')
COMMENT_STRING = {
    'Python' : '# '
  , 'CMake'  : '# '
  , 'Bash'   : '# '
  , 'C++'    : '//'
}


def isApplicableMime():
    return str(kate.activeDocument().mimeType()).find('c++') != -1

def insertTextBlock(document, line, text):
    """Put lines from a list into the current position (line) in a document
    """
    if bool(text):
        for l in text:
            document.insertLine(line, l)
            line += 1

#
# Build a list of tuples (start, end, elseif, is_comment) for all #if/#elseif/#endif blocks
# in a document. If block contains #endif 3rd element will point its line, -1 otherwise.
# For blocks #if1/#if0 4th element is True, otherwise False.
#
def buildIfEndifMap(document):
    # Make list of ranges of #if*/#endif blocks
    openBlockStack = list()
    blockRanges = list()
    for i in range(0, document.lines()):
        currentLine = str(document.line(i))
        # Is #if block start?
        isComment = False
        matchObj = BLOCK_ANY_START_SEARCH_RE.search(currentLine)
        if bool(matchObj):
            matchObj = BLOCK_START_SEARCH_RE.search(currentLine)
            isComment = bool(matchObj)
            openBlockStack.append((True, i, isComment))
            continue
        # Is #else block?
        matchObj = BLOCK_ELSE_SEARCH_RE.search(currentLine)
        if bool(matchObj):
            openBlockStack.append((False, i, False))
            continue
        # Close block?
        matchObj = BLOCK_END_SEARCH_RE.search(currentLine)
        # Match? Is there any open block remain?
        if bool(matchObj) and bool(openBlockStack):
            isStart, blockLine, isComment = openBlockStack.pop()
            if isStart:
                blockRanges.append((blockLine, i, -1, isComment))
            else:
                isStart, start, isComment = openBlockStack.pop()
                blockRanges.append((start, i, blockLine, isComment))

    return blockRanges

def locateBlock(currentLine, blockRanges, ignoreComments = False):
    """Find an index of a current block

        Return index into blockRanges of the block pointer by current cursor position
        or -1 if nothing found.

        TODO Rename to better name?
        TODO Is there any better way to implement a code similar to std::find_if in C++?
    """
    # Locate a block where cursor currently positioned
    idx = -1
    c = 0
    for i in blockRanges:
        if i[0] <= currentLine and currentLine <= i[1] and (ignoreComments or i[3]):
            idx = c
            break
        c += 1
    return idx;

def processLine(line, commentCh):
    result = []
    column = COMMENT_POS
    # Split line before and after a comment
    (before, comment, after) = line.partition(commentCh)
    before_s = before.rstrip()
    # Is there a comment on a line?
    if bool(comment):
        # Is there is any text before inline comment position?
        if bool(before_s):
            # Yes! Is text before not longer than desired comment position
            if len(before_s) < (COMMENT_POS + 1):
                # Yep, just reformat the line...
                result.append(before_s + (' ' * (COMMENT_POS - len(before_s))) + commentCh + after.rstrip())
            else:
                # Move comment to the line above
                column = len(before) - len(before.lstrip())
                result.append(' ' * column + commentCh + after.rstrip())
                result.append(before_s)
        else:
            # No! The line contains only whitespaces...
            # Is comment after or 'close before' to inline comment position?
            if len(before) > COMMENT_THRESHOLD:
                # Align comment to desired position...
                result.append(' ' * COMMENT_POS + commentCh + after.rstrip())
            else:
                # TODO Align comment to closest to div 4 position...
                result.append(line.rstrip())
    else:
        # There is no comments... What about any text?
        if bool(before_s):
            # Is it longer that inline comment position?
            if len(before_s) > (COMMENT_POS):
                column = len(before) - len(before.lstrip())
                result.append(' ' * column + commentCh + ' ')
                result.append(before_s)
            else:
                result.append(before_s + ' ' * (COMMENT_POS - len(before_s)) + commentCh + ' ')
            # Check for preprocessor directives #else/#endif and try to append
            # corresponding #if condition as a comment for current line
            if bool(BLOCK_ELSE_ENDIF_MATCH_RE.search(before_s)):
                document = kate.activeDocument()
                view = kate.activeView()
                # Make list of ranges of #if*/#endif blocks
                blocksList = buildIfEndifMap(document)
                # Locate an index of a block where cursor currently positioned (check commented block too)
                idx = locateBlock(view.cursorPosition().line(), blocksList, True)
                # Get #if condition (if block located)
                if idx != -1:
                    # TODO Need to strip possible comment!
                    matchObj = BLOCK_START_GET_COND_RE.search(document.line(blocksList[idx][0]))
                    if bool(matchObj):
                        result[-1] += matchObj.group(4)
        else:
            # No text! Just add a comment...
            result.append(' ' * COMMENT_POS + commentCh + ' ')
    return (result, column + len(commentCh) + 1)

@kate.action('Inline Comment', shortcut='Alt+D', menu='Edit')
def commentar():
    """Append or align an inlined comment to COMMENT_POS for the current line or the selection.

        Move cursor to the start of a comment, if nothing has changed.
    """
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()
    commentCh = COMMENT_STRING.get(document.highlightingMode(), '#')

    if view.selection():
        selectedText = view.selectionText().split('\n')
        if not bool(selectedText[len(selectedText) - 1]):
            selectedText = selectedText[0:-1]
        insertionText = []
        firstColumn = -1
        for textLine in selectedText:
            (currentLine, column) = processLine(textLine, commentCh)
            if firstColumn == -1:
                firstColumn = column
            insertionText += currentLine

        # Modify current document
        if bool(insertionText):
            document.startEditing()
            document.removeText(view.selectionRange())
            currentPosition = view.cursorPosition()
            insertTextBlock(document, currentPosition.line(), insertionText)
            currentPosition.setColumn(firstColumn)
            view.setCursorPosition(currentPosition)
            view.removeSelection()
            document.endEditing()

    else:
        (text, column) = processLine(document.line(currentPosition.line()), commentCh)

        # Apply result (if smth really has changed)
        originalText = document.line(currentPosition.line())
        if bool(text) and (len(text) != 1 or originalText != text[0]):
            document.startEditing()                         # Start edit transaction:
            document.removeLine(currentPosition.line())     # Remove current line
            # insert resulting text line by line...
            insertTextBlock(document, currentPosition.line(), text)
            document.endEditing()                           # End transaction

        # Move cursor to desired position
        currentPosition.setColumn(column)
        view.setCursorPosition(currentPosition)


@kate.action('Move Comment Above', shortcut='Meta+Left')
def moveAbove():
    """Move inlined comment before the current line at same align
    """
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    if not view.selection():
        insertionText = list()
        line = document.line(currentPosition.line())
        # Split a line before and after a comment
        (before, comment, after) = str(line).partition('//')

        before_ls = before.lstrip()
        column = len(before) - len(before_ls)
        doxCommentOffset = 0
        # Is there is a comment in a line?
        if bool(comment):
            # Yeah! It is... Now what about any text??
            if bool(before.strip()):
                if after[0:2] == '/<':
                    after = '/' + after[2:]
                    doxCommentOffset = 1
                insertionText.append(' ' * column + comment + after)
            else:
                # There is comment alone... Just leave it...
                return
        else:
            # Oops! There is no inline comment... Ok just add new one above.
            insertionText.append(' ' * column + '// ')

        column += 3 + doxCommentOffset
        insertionText.append(before.rstrip());

        # Update the document
        if bool(insertionText):
            document.startEditing()                         # Start edit transaction:
            document.removeLine(currentPosition.line())     # Remove current line

            # insert resulting text line by line...
            insertTextBlock(document, currentPosition.line(), insertionText)

            # Move cursor to desired position
            currentPosition.setColumn(column)
            view.setCursorPosition(currentPosition)
            document.endEditing()                           # End transaction


#
# Move comment above the current line as inline comment or
# if current line contains just comment try to make it inline
# (if line below still has no one)
#
@kate.action('Move Comment Inline', shortcut='Meta+Right')
def moveInline():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    if not view.selection():
        insertionText = list()
        currentLine = document.line(currentPosition.line())
        auxLine2Remove = 0
        # Split a line before and after a comment
        (before, comment, after) = str(currentLine).partition('//')

        # Is there is some text on a line?
        if bool(before.strip()):
            return                                          # Aha... move cursor co comment u stupid bastard!
        else:
            # No! What about comment?
            if bool(comment):
                # Aha... the comment is here. Ok. Lets get a line below the current...
                lineBelow = document.line(currentPosition.line() + 1)
                (b_before, b_comment, b_after) = str(lineBelow).partition('//')
                auxLine2Remove = 1
                # Check for text and comment in it...
                if bool(b_before.strip()):
                    # Text present... Comment?
                    if bool(b_comment):
                        # Comment too... just leave it...
                        return
                    else:
                        # Just text.... no comment. Ok lets work!
                        # (if there is some space remains for inline comment)
                        b_before_s = b_before.rstrip()
                        if len(b_before_s) > COMMENT_POS:
                            # Oops! No space remains! Get outa here
                            return
                        else:
                            doxCommentOffset = 0
                            if after[0:2] == '/ ':
                                after = '/< ' + after[2:]
                                doxCommentOffset = 2
                            insertionText.append(b_before_s + ' ' * (COMMENT_POS - len(b_before_s)) + '//' + after.rstrip())
                            column = COMMENT_POS + 3 + doxCommentOffset
                else:
                    # No text on the line below! Dunno what damn user wants...
                    return
            else:
                # Nothing! Just blank line... Dunno what to do...
                return
            pass

        # Update the document
        if bool(insertionText):
            document.startEditing()                         # Start edit transaction:
            if auxLine2Remove != 0:
                document.removeLine(currentPosition.line() + auxLine2Remove)
            document.removeLine(currentPosition.line())     # Remove current line

            # insert resulting text line by line...
            insertTextBlock(document, currentPosition.line(), insertionText)

            # Move cursor to desired position
            currentPosition.setColumn(column)
            view.setCursorPosition(currentPosition)
            document.endEditing()                           # End transaction


@kate.action('Comment Block w/ `#if0`', shortcut='Meta+D', menu='Edit')
def commentBlock():
    view = kate.activeView()

    start = -1
    end = -1
    if view.selection():
        sr = view.selectionRange()
        start = sr.start().line()
        end = sr.end().line() + 1
    else:
        start = view.cursorPosition().line()
        end = start + 2

    # Do it!
    document = kate.activeDocument()
    if start != -1 and end != -1:
        document.startEditing()                             # Start edit transaction
        document.insertLine(start, "#if 0")
        document.insertLine(end, "#endif")
        view.removeSelection()
        document.endEditing()                               # End transaction


@kate.action('Toggle `#if0/#if1` Block', shortcut='Meta+Shift+D', menu='Edit')
def toggleBlock():
    document = kate.activeDocument()
    view = kate.activeView()

    # Make list of ranges of #if*/#endif blocks
    blocksList = buildIfEndifMap(document)

    # Locate a block where cursor currently positioned
    idx = locateBlock(view.cursorPosition().line(), blocksList, False)

    if idx != -1:
        # Get current value
        v = BLOCK_START_SEARCH_RE.search(str(document.line(blocksList[idx][0]))).group(1)
        # Toggle it!
        if v in ('0', 'false'):
            newValue = '1'
        elif v in ('1', 'true'):
            newValue = '0'
        else:
            return

        # Replace string
        document.startEditing()                                 # Start edit transaction
        document.removeLine(blocksList[idx][0])
        # TODO Do not lose formatting!
        document.insertLine(blocksList[idx][0], "#if " + newValue)
        document.endEditing()                                   # End transaction


@kate.action('Remove `#if 0` Block', shortcut='Meta+R', menu='Edit')
def removeBlock():
    document = kate.activeDocument()
    view = kate.activeView()

    # Make list of ranges of #if*/#endif blocks
    blocksList = buildIfEndifMap(document)

    # Locate a block where cursor currently positioned
    idx = locateBlock(view.cursorPosition().line(), blocksList, False)

    if idx != -1:
        # Get current value
        v = BLOCK_START_SEARCH_RE.search(str(document.line(blocksList[idx][0]))).group(1)
        # Do nothing if it's not a #if0/#if1
        if v not in ('0', 'false', '1', 'true'):
            return

        document.startEditing()                             # Start edit transaction
        # What to remove?
        if v in ('0', 'false'):                             # Remove `then` part
            if blocksList[idx][2] != -1:                    # Is there `#else` part?
                # Yeah! Remove `#endif` line and then from `#if` to `#else` (including)
                document.removeLine(blocksList[idx][1])
                r = KTextEditor.Range(blocksList[idx][0], 0, blocksList[idx][2] + 1, 0)
            else:
                # No! So just remove whole block
                r = KTextEditor.Range(blocksList[idx][0], 0, blocksList[idx][1] + 1, 0)
            print r
            document.removeText(r)
        else:
            if blocksList[idx][2] != -1:                    # Is there `#else` part?
                # Yeah! Remove from `#else` to `#endif` block and then `#if` line
                r = KTextEditor.Range(blocksList[idx][2], 0, blocksList[idx][1] + 1, 0)
                document.removeText(r)
                document.removeLine(blocksList[idx][0])
            else:
                # No! Ok just remove `#endif` line and then `#if`
                document.removeLine(blocksList[idx][1])
                document.removeLine(blocksList[idx][0])
        document.endEditing()                                   # End transaction


@kate.action('Select Current Block', shortcut='Meta+S', menu='Edit')
def selectBlock():
    document = kate.activeDocument()
    view = kate.activeView()

    # Make list of ranges of #if*/#endif blocks
    blocksList = buildIfEndifMap(document)

    # Locate a block where cursor currently positioned
    idx = locateBlock(view.cursorPosition().line(), blocksList)

    if idx != -1:
        r = KTextEditor.Range(blocksList[idx][0], 0, blocksList[idx][1] + 1, 0)
        view.setSelection(r)


def detectSimpleComment(start, step):
    document = kate.activeDocument()

    while (start > 0 and start < document.lines()):
        line = str(document.line(start)).lstrip()
        if line.startswith('///') or line.startswith('//!'):
            start += step
            continue
        break
    return start - step                                     # One step back!


def turnToBlockComment():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    if view.selection():
        sr = view.selectionRange()
        start = sr.start().line()
        end = sr.end().line()
    else:
        start = detectSimpleComment(currentPosition.line(), -1)
        end = detectSimpleComment(currentPosition.line(), 1) + 1

    # Replace comments
    insertionText = list()
    align = None
    for i in range(start, end):
        line = str(document.line(i))
        sline = line.lstrip()
        if align == None:
            align = ' ' * (len(line) - len(sline))
        insertionText.append(align + sline.replace('///', ' *', 1).replace('//!', ' *', 1))

    originRange = KTextEditor.Range(start, 0, end, 0)
    currentPosition.setPosition(start + 1, len(align) + 3)

    # Update the document
    if bool(insertionText):
        document.startEditing()                             # Start edit transaction:
        document.removeText(originRange)                    # Remove current line

        # insert resulting text line by line...
        insertTextBlock(document, start, [align + '/**'] + insertionText + [align + ' */'])

        # Move cursor to desired position
        view.setCursorPosition(currentPosition)
        document.endEditing()                               # End transaction


def detectBlockComment(start, step, terminate):
    document = kate.activeDocument()

    while (start > 0 and start < document.lines()):
        line = str(document.line(start)).lstrip()
        if line.startswith(terminate):
            break
        if line.startswith('*'):
            start += step
            continue
        break
    return start


def turnFromBlockComment():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    if view.selection():
        sr = view.selectionRange()
        start = sr.start().line()
        end = sr.end().line()
    else:
        start = detectBlockComment(currentPosition.line(), -1, '/*')
        end = detectBlockComment(currentPosition.line(), 1, '*/') + 1

    # Replace comments
    insertionText = list()
    align = None
    for i in range(start, end):
        line = str(document.line(i))
        sline = line.lstrip()
        if align == None:
            align = ' ' * (len(line) - len(sline))
        if sline.startswith('/**') or sline.startswith('*/'):
            continue
        if sline.startswith('*'):
            insertionText.append(align + sline.replace('*', '///', 1))

    originRange = KTextEditor.Range(start, 0, end, 0)
    currentPosition.setPosition(start, len(align) + 3)

    # Update the document
    if bool(insertionText):
        document.startEditing()                             # Start edit transaction:
        document.removeText(originRange)                    # Remove current line

        # insert resulting text line by line...
        insertTextBlock(document, start, insertionText)

        # Move cursor to desired position
        view.setCursorPosition(currentPosition)
        document.endEditing()                               # End transaction


@kate.action('Transform Doxygen Comments', shortcut='Meta+X', menu='Edit')
def toggleDoxyComment():
    document = kate.activeDocument()
    view = kate.activeView()
    currentPosition = view.cursorPosition()

    # Determine type of current comment
    line = str(document.line(currentPosition.line())).strip()
    if line.startswith('///'):
        turnToBlockComment()
    elif line.startswith('*') or line.startswith('/*') or line.startswith('*/'):
        turnFromBlockComment()
    else:
        return

#@kate.viewChanged
#def vc1():
    #kate.gui.popup("On view changed: " + kate.activeDocument().mimeType(), 10)

#@kate.viewCreated
#def vc2():
    #kate.gui.popup("On view created: " + kate.activeDocument().mimeType(), 10)

#@kate.init
#def vc3():
    #kate.gui.popup("On init: " + kate.activeDocument().mimeType(), 10)

#@kate.unload
#def vc4():
    #kate.gui.popup("On unload: " + kate.activeDocument().mimeType(), 10)
