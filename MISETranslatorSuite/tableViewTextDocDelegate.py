﻿#!/usr/bin/python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        tableViewTextDocDelegate
#-------------------------------------------------------------------------------
##import sip
##sip.setapi('QString', 2)
from Qt import QtCore, QtGui
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import QStyledItemDelegate
import re
import highlightRulesGlobal


class TextDocDelegate(QStyledItemDelegate):
    font = QtGui.QFont()
    moreFont = QtGui.QFont()


    def __init__(self):
        super(TextDocDelegate, self).__init__()
        self.font = QtGui.QFont()
        self.font.setFamily('Arial')
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)
        self.moreFont = QtGui.QFont()
        self.moreFont.setFamily('Arial')
        self.moreFont.setFixedPitch(True)
        self.moreFont.setPointSize(8)
        self.moreFont.setWeight(QFont.Bold)
        self.installEventFilter(self)

    # override displayText, since otherwise we get duplicates with Paint-ed QTextDocument (which we need for the highlighting)
    def displayText(self, value, locale):
        text = ""
        return text

    def createEditor(self, parent, option, index):
        ## Just creates a plain line edit.
        #editor = QLineEdit(parent)

        ##editor.setAcceptRichText(True)
        ##editor.setReadOnly(False)
        ##editor.setGeometry(option.rect);
        ##sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        ##editor.setSizePolicy(sizePolicy);
        #font = QtGui.QFont()
        #font.setFamily('Arial')
        #font.setFixedPitch(True)
        #font.setPointSize(10)

        editor = QtGui.QTextEdit(parent)
        editor.setFont(self.font)

        self.highlighter = Highlighter(editor.document(), index.column(), index.row())

        return editor

    def paint(self, painter, option, index):
        if option is None or index is None or painter is None:
            return
        else:
            painter.save()
            ##default = QStyledItemDelegate.sizeHint(self, option, index)
            ##print("painter option" , (option.rect.x(),option.rect.y(), default.width(), default.height()))
            ##painter.drawRect(option.rect)
            QStyledItemDelegate.paint(self, painter, option, index)
            text = index.model().data(index, Qt.DisplayRole).toString()
            doc = QTextDocument()
            doc.setPlainText(text)
            doc.adjustSize()
            doc.setDefaultFont(self.font)
            doc.setDocumentMargin(3)

            docTextOption = QTextOption()
            docTextOption.setAlignment(Qt.AlignVCenter)

            doc.setDefaultTextOption(docTextOption)
#            FilterSyntaxHighlighter* highlighter = new FilterSyntaxHighlighter(regExp, doc);
            highlighter = Highlighter(doc, index.column(), index.row())
            highlighter.rehighlight()

            #QAbstractTextDocumentLayout :: PaintContext context;
            context = QtGui.QAbstractTextDocumentLayout.PaintContext();

            doc.setPageSize(QSizeF ( option.rect.size()))
            #painter.setClipRect(option.rect);
            docuRect, hasMore = self.getTextDocumentRect(option, doc)

            painter.setClipRect(docuRect);
            painter.translate( docuRect.x(), docuRect.y() )
            doc.documentLayout().draw(painter,context)
            #origColor= index.model().parent().palette().color(QPalette.Base)
            #if  (index.row() % 2) > 0:
            #    origColor= index.model().parent().palette().color(QPalette.AlternateBase)
            #index.model().item(index.row(),index.column()).setBackground(origColor)
            painter.restore()
            painter.save()
            if hasMore:
                #print("Has More", index.row(), index.column())
                docMoreNote = QTextDocument()
                docMoreNote.setPlainText("...")
                docMoreNote.adjustSize()
                docMoreNote.setDefaultFont(self.moreFont)
                docMoreNote.setDocumentMargin(1)
                docMoreNote.setPageSize(QSizeF ( docMoreNote.size()))
                docuCornerRect, hasMore = self.getCornerTextDocumentRect(option, docMoreNote)
                painter.setClipRect(docuCornerRect);
                painter.translate( docuCornerRect.x(), docuCornerRect.y() )
                docMoreNote.documentLayout().draw(painter,context)

            painter.restore()


    def getCornerTextDocumentRect(self, option, cornerDocu):
        hasMore = False
        docu_point = None
        docu_croppedSize = None
        if cornerDocu.size().toSize().height() <= option.rect.height() and cornerDocu.size().toSize().width() <= option.rect.width():
            docu_point = QPoint (option.rect.x() + option.rect.width() - cornerDocu.size().toSize().width(),
            					 option.rect.y() + (option.rect.height()  - cornerDocu.size().toSize().height()))
            docu_croppedSize= QSize(cornerDocu.size().toSize().width(), cornerDocu.size().toSize().height()  ) #width, height
        elif cornerDocu.size().toSize().height() > option.rect.height() and cornerDocu.size().toSize().width() <= option.rect.width():
            docu_point = QPoint (option.rect.x() + option.rect.width() - cornerDocu.size().toSize().width(), option.rect.y())
            docu_croppedSize = QSize(cornerDocu.size().toSize().width(), option.rect.height() )
            hasMore = True
        elif cornerDocu.size().toSize().height() <= option.rect.height() and cornerDocu.size().toSize().width() > option.rect.width():
            docu_point = QPoint(option.rect.x(),
            					 option.rect.y() + (option.rect.height()  - cornerDocu.size().toSize().height()))
            docu_croppedSize = QSize(option.rect.width(), cornerDocu.size().toSize().height() )
            hasMore = True
        else: #both are larger and need crop
            docu_point = QPoint (option.rect.x(), option.rect.y())
            docu_croppedSize = QSize(option.rect.width(), option.rect.height() )
            hasMore = True
        return QRect(docu_point, docu_croppedSize), hasMore

    def getTextDocumentRect(self, option, textDocu):
        hasMore = False
        docu_point = None
        docu_croppedSize = None
        if textDocu.size().toSize().height() <= option.rect.height() and textDocu.size().toSize().width() <= option.rect.width():
            docu_point = QPoint (option.rect.x(),
            					 option.rect.y() + (option.rect.height()  - textDocu.size().toSize().height()) / 2)
            docu_croppedSize= QSize(textDocu.size().toSize().width(), (option.rect.height()  + textDocu.size().toSize().height()) / 2 ) #width, height
        elif textDocu.size().toSize().height() > option.rect.height() and textDocu.size().toSize().width() <= option.rect.width():
            docu_point = QPoint (option.rect.x(), option.rect.y())
            docu_croppedSize = QSize(textDocu.size().toSize().width(), option.rect.height() )
            hasMore = True
        elif textDocu.size().toSize().height() <= option.rect.height() and textDocu.size().toSize().width() > option.rect.width():
            docu_point = QPoint (option.rect.x(),
            					 option.rect.y() + (option.rect.height()  - textDocu.size().toSize().height()) / 2)
            docu_croppedSize = QSize(option.rect.width(), (option.rect.height()  + textDocu.size().toSize().height()) / 2  )
            hasMore = True
        else: #both are larger and need crop
            docu_point = QPoint (option.rect.x(), option.rect.y())
            docu_croppedSize = QSize(option.rect.width(), option.rect.height() )
            hasMore = True
        return QRect(docu_point, docu_croppedSize), hasMore

        ##print("something")
##
##    def sizeHint(self, option, index):
##        default = QStyledItemDelegate.sizeHint(self, option, index)
##        print("size hint option" , (option.rect.x(),option.rect.y(), default.width(), default.height()))
##        return QSize(default.width(), default.height())

    def setEditorData(self, editor, index):
    # Fetch current data from model.
        value = index.model().data(index, Qt.DisplayRole).toString();
        #print(value)
##        valueDato = index.model().data(index, Qt.EditRole).toPyObject();
##        print(valueDato)
        ## Set line edit text to current data.
        #editor.setText(value)
        ## Deselect text. (lineEdit)
        #editor.deselect();
        ## Move the cursor to the beginning. (lineEdit)
        #editor.setCursorPosition(0);
        editor.setPlainText(value)

    def setModelData(self, editor, model, index):
    # Set the model data with the text in line edit.
        #model.setData(index, QVariant(editor.text()), Qt.EditRole); # ;lineEdit
        if index.column() > 0:   # first column won't be edited!
            model.setData(index, QVariant(editor.toPlainText()), Qt.EditRole); # ;lineEdit


    def updateEditorGeometry(self, editor, option, index):
        #print((option.rect.x(),option.rect.y(),editor.sizeHint().width(),editor.sizeHint().height()))
        editor.setGeometry(option.rect)
        return

    def eventFilter(self, editor, event):
        if event.type() == QEvent.KeyPress:
            #print("key: ", event.key(), " mod: ", event.modifiers(), " keyEnter: ", Qt.Key_Enter)
            #print(Qt.Key_Enter == event.key() , (event.modifiers() & QtCore.Qt.ShiftModifier == QtCore.Qt.ShiftModifier), ((event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter) ))
            #keyEvent = (QKeyEvent)(event);
            if (event.modifiers() & QtCore.Qt.ShiftModifier == QtCore.Qt.ShiftModifier) and \
                            (event.modifiers() & QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier) and \
                             ((event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter) ):
                self.emit(SIGNAL("commitData(QWidget *)"), editor)
                self.emit(SIGNAL("closeEditor(QWidget *, QAbstractItemDelegate::EndEditHint)"), editor, QStyledItemDelegate.NoHint)
                self.emit(SIGNAL("customMoveEditCursor(int)"), 0) # we use this, instead of the core signal (closeEditor with EditPreviousItem  hint) because that one also moved the focus to another column.
                return True # handled
            elif (event.modifiers() & QtCore.Qt.ShiftModifier == QtCore.Qt.ShiftModifier) and ((event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter) ):
                self.emit(SIGNAL("commitData(QWidget *)"), editor)
                self.emit(SIGNAL("closeEditor(QWidget *, QAbstractItemDelegate::EndEditHint)"), editor, QStyledItemDelegate.NoHint)
                self.emit(SIGNAL("customMoveEditCursor(int)"), 1) # we use this, instead of the core signal (closeEditor with EditNextItem hint) because that one also moved the focus to another column.
                return True # handled
        return QStyledItemDelegate.eventFilter(self, editor, event)

    def muteCloseEditorSignal(self, editor, qEditHint):
        if qEditHint == QStyledItemDelegate.EditPreviousItem or qEditHint == QStyledItemDelegate.EditNextItem:
            print("akakaka")
            return

class HighlightingRule:
    pass

class Highlighter(QtGui.QSyntaxHighlighter):

    parentColNumber = -1
    def __init__(self, parent=None, pParntColNum=-1, pParntRowNum=-1):
        super(Highlighter, self).__init__(parent)
        highlightRulesGlobal.addHighlighterWatcher(self)
        self.parentColNumber = pParntColNum
        self.parentRowNumber = pParntRowNum
        #self.multiLineCommentFormat = QtGui.QTextCharFormat()
        #self.multiLineCommentFormat.setForeground(QtCore.Qt.red)
        #self.commentStartExpression = QtCore.QRegExp("/\\*")
        #self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        #print("checking hight")
        #for pattern, format, forColumnNum, forRowNum in highlightRulesGlobal.getAllHighlightRules():
        for (compliledREpattern, format, forColumnNum, forRowNum) in highlightRulesGlobal.getAllHighlightRules():
            if((self.parentColNumber == forColumnNum or forColumnNum==-1 ) and (self.parentRowNumber == forRowNum or forRowNum==-1)):
                resIter = compliledREpattern.finditer(text)
                for elem in resIter:
                    groupIndex = 1
                    if len(elem.groups()) > 0:
                        for groupIt in elem.groups():
                            if (groupIt is not None):
                                if (elem.start(groupIndex) != -1 and elem.end(groupIndex) != -1 and elem.start(groupIndex) != elem.end(groupIndex)):
                                    index = elem.start(groupIndex)
                                    length = elem.end(groupIndex) - index
                                    #matchedString = elem.string[elem.start(groupIndex):elem.end(groupIndex)]
                                    self.setFormat(index, length, format)
                            groupIndex += 1
                    elif (elem.start(0) != -1 and elem.end(0) != -1 and elem.start(0) != elem.end(0)):
                            index = elem.start(0)
                            length = elem.end(0) - index
                            #matchedString = elem.string[elem.start(0):elem.end(0)]
                            self.setFormat(index, length, format)

##                expression = QtCore.QRegExp(pattern)
##                index = expression.indexIn(text)
##                while index >= 0:
##                    length = expression.matchedLength()
##                    self.setFormat(index, length, format)
##                    index = expression.indexIn(text, index + length)


##        self.setCurrentBlockState(0)
##
##        startIndex = 0
##        if self.previousBlockState() != 1:
##            startIndex = self.commentStartExpression.indexIn(text)
##
##        while startIndex >= 0:
##            endIndex = self.commentEndExpression.indexIn(text, startIndex)
##
##            if endIndex == -1:
##                self.setCurrentBlockState(1)
##                commentLength = len(text) - startIndex
##            else:
##                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()
##
##            self.setFormat(startIndex, commentLength,
##                    self.multiLineCommentFormat)
##            startIndex = self.commentStartExpression.indexIn(text,
##                    startIndex + commentLength);

def main():
    pass

if __name__ == '__main__':
    main()
