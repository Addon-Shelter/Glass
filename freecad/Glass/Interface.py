# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

from FreeCAD import Gui
from PySide6 import QtWidgets , QtCore , QtGui

from .Preferences import getOwnPreferences
from .Setup import runSetup


timer : QtCore.QTimer
mode = 0
wid = QtWidgets.QWidget()
window = Gui.getMainWindow()


preferences = getOwnPreferences()

try:
    window.setDockOptions(window.dockOptions() | window.GroupedDragging)
except AttributeError:
    pass


def findDock():
    global dock
    dock = window.findChild(QtWidgets.QDockWidget, "Tree view")


def createActions():
    a1 = QtGui.QAction(window)
    a1.setParent(window)
    a1.setText("Glass toggle dock mode")
    a1.setObjectName("GlassToggleMode")
    a1.setShortcut(QtGui.QKeySequence("Q, 1"))
    a1.triggered.connect(setMode)
    window.addAction(a1)
    a2 = QtGui.QAction(window)
    a2.setParent(window)
    a2.setText("Glass toggle dock visibility")
    a2.setObjectName("GlassToggleVisibility")
    a2.setShortcut(QtGui.QKeySequence("Q, 2"))
    a2.triggered.connect(setVisibility)
    window.addAction(a2)


def applyGlass(boolean, widget):
    try:
        if boolean:
            widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        else:
            widget.setWindowFlags(dock.windowFlags() & ~QtCore.
                                  Qt.
                                  FramelessWindowHint)
    except:
        pass
    try:
        widget.setAttribute(QtCore.Qt.WA_NoSystemBackground, boolean)
    except:
        pass
    try:
        widget.setAttribute(QtCore.Qt.WA_TranslucentBackground, boolean)
    except:
        pass
    try:
        if boolean:
            widget.setStyleSheet("background:transparent; border:none; color:white;")
        else:
            widget.setStyleSheet("")
    except:
        pass
    try:
        widget.setAutoFillBackground(boolean)
    except:
        pass
    try:
        if boolean:
            widget.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
        else:
            widget.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
    except:
        pass
    try:
        if boolean:
            widget.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
        else:
            widget.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
    except:
        pass
    try:
        widget.setDocumentMode(boolean)
    except:
        pass
    try:
        widget.tabBar().setDrawBase(False)
    except:
        pass
    try:
        if boolean:
            widget.header().hide()
        else:
            widget.header().show()
    except:
        pass


def widgetList(boolean):
    children = []
    children.append(dock)

    child = True
    while child:
        child = False
        for i in children:
            if i.children():
                for c in i.children():
                    if c not in children:
                        children.append(c)
                        child = True

    for child in children:
        applyGlass(boolean, child)


def setMode():
    global mode
    mdi = window.findChild(QtGui.QMdiArea)

    if mode == 0:
        dock.setParent(mdi)
        dock.setTitleBarWidget(wid)
        wid.hide()
        dock.show()
        widgetList(True)
        mode = 1
    else:
        dock.setParent(window)
        dock.setTitleBarWidget(None)
        window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        dock.show()
        widgetList(False)
        mode = 0

    onResize()


def setVisibility():
    dock.toggleViewAction().trigger()


def onResize():
    mdi = window.findChild(QtWidgets.QMdiArea)

    if not mdi:
        return

    if mode == 1:
        x = 0
        y = 0
        w = mdi.geometry().width() / 100 * 20
        h = (mdi.geometry().height() -
             mdi.findChild(QtGui.QTabBar).geometry().height())
        dock.setGeometry(x, y, w, h)

    if str(Gui.activeView()) == "View3DInventor":
        dock.show()
    else:
        dock.hide()


def onStart():
    if window.property("eventLoop"):
        timer.stop()
        timer.timeout.disconnect(onStart)
        findDock()
        createActions()
        if preferences.GetBool("glassAuto", 1):
            setMode() # activate Glass mode
        timer.timeout.connect(onResize)
        timer.start(2000)

def init ():

    if preferences.GetBool("FirstRun", 1):
        runSetup()
        preferences.SetBool("FirstRun", 0)


    timer = QtCore.QTimer()
    timer.timeout.connect(onStart)
    timer.start(500)
