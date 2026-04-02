# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

from FreeCAD import ParamGet


Root = 'User parameter:BaseApp/Preferences'


def getOwnPreferences ():
    return ParamGet(f'{ Root }/Glass')

def getTreePreferences ():
    return ParamGet(f'{ Root }/DockWindows/TreeView')

def getMainPreferences ():
    return ParamGet(f'{ Root }/DockWindows/MainWindow')

def getViewPreferences ():
    return ParamGet(f'{ Root }/DockWindows/View')

