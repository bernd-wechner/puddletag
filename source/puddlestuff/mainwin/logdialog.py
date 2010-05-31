# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from puddlestuff.constants import RIGHTDOCK

class LogDialog(QWidget):
    def __init__(self, parent=None, status=None):
        QWidget.__init__(self, parent)
        self.emits = []
        self.receives = [('logappend', self.appendText)]

        self._text = QTextEdit()

        copy = QPushButton('&Copy')
        clear = QPushButton('&Clear')

        self.connect(copy, SIGNAL('clicked()'), self._copy)
        self.connect(clear, SIGNAL('clicked()'), self._clear)

        vbox = QVBoxLayout()
        vbox.addWidget(self._text)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(copy)
        hbox.addWidget(clear)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def _clear(self):
        self._text.setPlainText('')

    def setText(self, text, html=True):
        if html:
            self._text.setHtml(text)
        else:
            self._text.setPlaintext(text)

    def appendText(self, text):
        self._text.append(text)

    def _copy(self):
        text = self._text.toPlainText()
        QApplication.clipboard().setText(text)

control = ('Logs', LogDialog, RIGHTDOCK, False)

if __name__ == '__main__':
    app = QApplication([])
    win = LogDialog()
    win.show()
    app.exec_()