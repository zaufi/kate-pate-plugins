# -*- coding: utf-8 -*-

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
