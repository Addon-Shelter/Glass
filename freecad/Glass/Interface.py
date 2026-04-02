# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

from FreeCAD import Gui
from PySide6 import QtWidgets , QtCore , QtGui

from .Preferences import getOwnPreferences
from .Setup import runSetup


timer : QtCore.QTimer
dock : QtWidgets.QDockWidget

mode = 0
title = QtWidgets.QWidget()
window = Gui.getMainWindow()


preferences = getOwnPreferences()

try:

    options = window.dockOptions() \
        | window.DockOption.GroupedDragging

    window.setDockOptions(options)

except AttributeError:
    pass


def findDock ():
    
    widget = window.findChild(QtWidgets.QDockWidget,'Tree view')

    if widget:
        global dock
        dock = widget


def createActions():
    a1 = QtGui.QAction(window)
    a1.setParent(window)
    a1.setText("Glass toggle dock mode")
    a1.setObjectName("GlassToggleMode")
    a1.setShortcut(QtGui.QKeySequence("Q, 1"))
    a1.triggered.connect(updateMode)
    window.addAction(a1)
    a2 = QtGui.QAction(window)
    a2.setParent(window)
    a2.setText("Glass toggle dock visibility")
    a2.setObjectName("GlassToggleVisibility")
    a2.setShortcut(QtGui.QKeySequence("Q, 2"))
    a2.triggered.connect(setVisibility)
    window.addAction(a2)


def applyGlass ( widget , active ):

    try:
        if active:
            widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        else:
            widget.setWindowFlags(dock.windowFlags() & ~QtCore.
                                  Qt.
                                  FramelessWindowHint)
    except:
        pass

    try:
        widget.setAttribute(QtCore.Qt.WA_NoSystemBackground, active)
    except:
        pass

    try:
        widget.setAttribute(QtCore.Qt.WA_TranslucentBackground, active)
    except:
        pass

    try:
        if active:
            widget.setStyleSheet("background:transparent; border:none; color:white;")
        else:
            widget.setStyleSheet("")
    except:
        pass

    try:
        widget.setAutoFillBackground(active)
    except:
        pass

    try:
        if active:
            widget.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
        else:
            widget.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
    except:
        pass

    try:
        if active:
            widget.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
        else:
            widget.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
    except:
        pass

    try:
        widget.setDocumentMode(active)
    except:
        pass

    try:
        widget.tabBar().setDrawBase(False)
    except:
        pass
    
    try:
        if active:
            widget.header().hide()
        else:
            widget.header().show()
    except:
        pass


def widgetList ( active ):

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

    for child in children :
        applyGlass(child,active)


def updateMode ():

    global mode

    mdi = window.findChild(QtWidgets.QMdiArea)

    if mode == 0:

        dock.setParent(mdi)
        dock.setTitleBarWidget(title)
        
        title.hide()
        
        dock.show()
        
        widgetList(True)
        
        mode = 1

    else:
        
        dock.setParent(window)
        dock.setTitleBarWidget(None)

        window.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,dock)
        
        dock.show()

        widgetList(False)
        
        mode = 0

    onResize()


def setVisibility ():
    dock.toggleViewAction().trigger()


def onResize ():

    mdi = window.findChild(QtWidgets.QMdiArea)

    if not mdi:
        return

    if mode == 1:

        bar = mdi.findChild(QtWidgets.QTabBar)

        if bar:

            bar_height = bar.geometry().height()

            geometry = mdi.geometry()

            mdi_width = geometry.height()
            mdi_height = geometry.width()

            width = int( mdi_width / 100 * 20 )
            height = int( mdi_height - bar_height )

            dock.setGeometry(0,0,width,height)

    view = str( Gui.activeView() )

    if view == 'View3DInventor' :
        dock.show()
    else:
        dock.hide()


def onStart ():

    if not window.property('eventLoop'):
        return

    timer.stop()
    timer.timeout.disconnect(onStart)

    findDock()
    createActions()

    if preferences.GetBool('glassAuto',1):
        updateMode()

    timer.timeout.connect(onResize)
    timer.start(2000)


def init ():

    if preferences.GetBool('FirstRun',1):

        runSetup()
        
        preferences.SetBool('FirstRun',0)


    timer = QtCore.QTimer()
    timer.timeout.connect(onStart)
    timer.start(500)
