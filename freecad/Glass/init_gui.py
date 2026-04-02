# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

"""Glass module for FreeCAD."""

from PySide import QtCore


p = FreeCAD.ParamGet("User parameter:BaseApp/Glass")


if p.GetBool("Enabled", 1) and QtCore.qVersion() >= "5":
    import GlassGui
