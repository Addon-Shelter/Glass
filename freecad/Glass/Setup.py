# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

from .Preferences import (
    getMainPreferences ,
    getTreePreferences ,
    getViewPreferences
)


def runSetup ():

    tree = getTreePreferences()
    tree.SetBool('Enabled', True)

    main = getMainPreferences()
    main.SetString('StyleSheet','Dark-blue.qss')

    view = getViewPreferences()
    view.SetUnsigned('BackgroundColor2',1852731135)
    view.SetUnsigned('BackgroundColor3',2829625599)
    view.SetUnsigned('BackgroundColor4',1852731135)
