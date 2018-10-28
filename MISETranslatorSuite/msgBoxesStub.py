#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Qt import QtCore, QtGui
from Qt.QtWidgets import QMessageBox
from Qt.QtCore import *
from Qt.QtGui import *
#
# MESSAGEBOX FUNCTIONS
#
def qMsgBoxQuestion(parentWidg, titleMsgBx, messageMsgBx, buttonFlagsMsgBxm = QMessageBox.Yes | QMessageBox.No, defaultBtnMsgBx = QMessageBox.No):
    qmsgParent = None
    if(parentWidg is not None):
        qmsgParent = parentWidg
    reply = defaultBtnMsgBx
    try:
        reply = QMessageBox.question(qmsgParent, titleMsgBx, messageMsgBx, buttonFlagsMsgBxm, defaultBtnMsgBx)
    except:
        parentScreen = QtGui.QApplication.desktop().screen(QtGui.QApplication.desktop().primaryScreen())
        qmsgParent = QtGui.QMainWindow(parentScreen)
        reply = QMessageBox.question(qmsgParent, titleMsgBx, messageMsgBx, buttonFlagsMsgBxm, defaultBtnMsgBx)
    return reply

def qMsgBoxCritical(parentWidg, titleMsgBx, messageMsgBx, buttonFlagsMsgBxm = QMessageBox.Ok | QMessageBox.Default, defaultBtnMsgBx = QMessageBox.NoButton ):
    qmsgParent = None
    if(parentWidg is not None):
        qmsgParent = parentWidg
    reply = defaultBtnMsgBx
    try:
        reply = QMessageBox.critical(qmsgParent, titleMsgBx, messageMsgBx, buttonFlagsMsgBxm, defaultBtnMsgBx)
    except:
        parentScreen = QtGui.QApplication.desktop().screen(QtGui.QApplication.desktop().primaryScreen())
        qmsgParent = QtGui.QMainWindow(parentScreen)
        reply = QMessageBox.critical(qmsgParent, titleMsgBx, messageMsgBx, buttonFlagsMsgBxm, defaultBtnMsgBx)
    return reply


def qMsgBoxInformation(parentWidg, titleMsgBx, messageMsgBx):
    qmsgParent = None
    if(parentWidg is not None):
        qmsgParent = parentWidg
    reply = QMessageBox.Ok
    try:
        reply = QMessageBox.information(qmsgParent, titleMsgBx, messageMsgBx)
    except:
        parentScreen = QtGui.QApplication.desktop().screen(QtGui.QApplication.desktop().primaryScreen())
        qmsgParent = QtGui.QMainWindow(parentScreen)
        reply = QMessageBox.information(qmsgParent, titleMsgBx, messageMsgBx)
    return reply

def qMsgBoxAbout(parentWidg, titleMsgBx, messageMsgBx):
    qmsgParent = None
    if(parentWidg is not None):
        qmsgParent = parentWidg
    reply = QMessageBox.Ok
    try:
        reply = QMessageBox.about(qmsgParent, titleMsgBx, messageMsgBx)
    except:
        parentScreen = QtGui.QApplication.desktop().screen(QtGui.QApplication.desktop().primaryScreen())
        qmsgParent = QtGui.QMainWindow(parentScreen)
        reply = QMessageBox.about(qmsgParent, titleMsgBx, messageMsgBx)
    return reply

def qMsgBoxWarning(parentWidg, titleMsgBx, messageMsgBx):
    qmsgParent = None
    if(parentWidg is not None):
        qmsgParent = parentWidg
    reply = QMessageBox.Ok
    try:
        reply = QMessageBox.warning(qmsgParent, titleMsgBx, messageMsgBx)
    except:
        parentScreen = QtGui.QApplication.desktop().screen(QtGui.QApplication.desktop().primaryScreen())
        qmsgParent = QtGui.QMainWindow(parentScreen)
        reply = QMessageBox.warning(qmsgParent, titleMsgBx, messageMsgBx)
    return reply


def main():
    pass

if __name__ == '__main__':
    main()
