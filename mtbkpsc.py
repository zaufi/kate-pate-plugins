# -*- coding: utf-8 -*-
#
# Kate/Pâté experemental plugin to collect some key-presses stats
# Copyright 2013 by Alex Turbov <i.zaufi@gmail.com>
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

import kate
import kate.ui
import kate.document


class transitions_node:
    def __init__(self):
        self.counter = 0
        self.tree = dict()


class initial_points:
    def __init__(self):
        self.points = dict()                                # Map of chars (transition cause) to transition instance
        self.last = None

    def feed_text(self, doc, cursor, text):
        if self.last is None:
            


class keys_tracker:
    def __init__(self):
        self.tracks = dict()

    def feed_text(self, doc, cursor, text):
        hl_iface = doc.highlightInterface()
        assert(hl_iface is not None)
        mode = hl_iface.highlightingModeAt(cursor)
        if mode not in self.tracks:
            self.tracks[mode] = initial_points()
        self.tracks[mode].feed_text(doc, cursor, text)


_tracker = None

@kate.init
def load():
    global _tracker
    if _tracker is None:
        if 'MTBKPSCTRK' in kate.sessionConfiguration:
            _tracker = kate.sessionConfiguration['MTBKPSCTRK']
        else:
            _tracker = keys_tracker()


@kate.unload
def unload():
    global _tracker
    if _tracker is not None:
        kate.sessionConfiguration['MTBKPSCTRK'] = _tracker


@kate.document.textInserted
def on_text_inserted(doc, rng):
    global _tracker
    kate.kDebug('New text: {}'.format(repr(doc.text(rng))))
    _tracker.feed_text(doc, rng.start(), doc.text(rng))


@kate.document.textRemoved
def on_text_removed(doc, rng, text):
    kate.kDebug('Remove text: {}'.format(repr(text)))


@kate.document.textChanged
def on_text_changed(doc, rng1, text, rng2):
    kate.kDebug('Text changed: rng1={}, rng2={}, text={}'.format(repr(text)))
