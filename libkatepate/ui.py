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

''' Reusable code for Kate/Pâté plugins: UI elements '''

import kate

from PyKDE4.kdeui import KPassivePopup, KIcon

from PyQt4 import QtCore
from PyQt4.QtCore import QSize


def popup(caption, text, iconName = None, iconSize = 16):
    ''' Show passive popup using native KDE API
    '''
    parentWidget = kate.mainWindow()
    if iconName:
        icon = KIcon ("dialog-cancel").pixmap(QSize(iconSize, iconSize))
        KPassivePopup.message(caption, text, icon, parentWidget)
    else:
        KPassivePopup.message(caption, text, parentWidget)
