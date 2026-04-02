# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

from .Preferences import getOwnPreferences
from .Interface import init


preferences = getOwnPreferences()

if preferences.GetBool('Enabled',1):
    init()
