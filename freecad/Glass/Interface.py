# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2018 Triplus
# SPDX-FileNotice: Part of the Glass addon.

from FreeCAD import Gui
from PySide6 import QtWidgets , QtCore , QtGui

from .Preferences import getOwnPreferences
from .Setup import runSetup


timer : QtCore.QTimer
dock : QtWidgets.QDockWidget

window = Gui.getMainWindow()
title = QtWidgets.QWidget()

active = False

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


def createActions ():

    action = QtGui.QAction(window)
    
    action.setParent(window)
    action.setText('Glass toggle dock mode')
    action.setObjectName('GlassToggleMode')
    action.setShortcut(QtGui.QKeySequence('Q,1'))
    
    action.triggered.connect(toggleActive)
    
    window.addAction(action)
    

    action = QtGui.QAction(window)
    
    action.setObjectName('GlassToggleVisibility')
    action.setShortcut(QtGui.QKeySequence('Q,2'))
    action.setParent(window)
    action.setText('Glass toggle dock visibility')
    
    action.triggered.connect(setVisibility)
    
    window.addAction(action)


def applyGlass ( 
    widget : QtWidgets.QWidget , 
    active : bool
):

    widget.setAutoFillBackground(active)

    if widget is QtWidgets.QTabWidget :
        
        widget.setDocumentMode(active)
        widget.tabBar().setDrawBase(False)
        
        if active:
            widget.header().hide()
        else:
            widget.header().show()


    if widget is QtWidgets.QMdiSubWindow :
        
        widget.setAttribute(QtCore.Qt.WindowType.WindowTransparentForInput,active)
        widget.setAttribute(QtCore.Qt.WindowType.NoTitleBarBackgroundHint,active)
    

    if widget is QtWidgets.QScrollBar :
        
        if active:
            policy = QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        else:
            policy = QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        
        widget.setHorizontalScrollBarPolicy(policy)
        widget.setVerticalScrollBarPolicy(policy)
    

    if active:
        widget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        widget.setStyleSheet('background:transparent;border:none;color:white;')
    else:
        widget.setWindowFlags(dock.windowFlags() & ~QtCore.Qt.WindowType.FramelessWindowHint)
        widget.setStyleSheet('')
    

def updateWidgets ( active ):

    widgets : list[ QtWidgets.QWidget ] = [ dock ]

    hasMore = True

    while hasMore:
        
        hasMore = False
        
        for widget in widgets:
            
            if not widget.children():
                continue

            for child in widget.children():
                
                if child in widgets:
                    continue

                if issubclass(type(child),QtWidgets.QWidget):
                    widgets.append(child) # type: ignore
                    hasMore = True

    for widget in widgets :
        applyGlass(widget,active)


def toggleActive ():

    global active

    mdi = window.findChild(QtWidgets.QMdiArea)

    active = not active

    if active:

        dock.setParent(mdi)
        dock.setTitleBarWidget(title)
        
        title.hide()

    else:

        dock.setParent(window)
        dock.setTitleBarWidget(None) # type: ignore

        window.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,dock)
        
    dock.show()

    updateWidgets(active)

    onResize()


def setVisibility ():
    dock.toggleViewAction().trigger()


def onResize ():

    mdi = window.findChild(QtWidgets.QMdiArea)

    if not mdi:
        return

    if active:

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
        toggleActive()

    timer.timeout.connect(onResize)
    timer.start(2000)


def init ():

    if preferences.GetBool('FirstRun',1):

        runSetup()
        
        preferences.SetBool('FirstRun',0)

    global timer

    timer = QtCore.QTimer()
    timer.timeout.connect(onStart)
    timer.start(500)
