import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import graphics

if __name__ == '__main__':
    APP = QtWidgets.QApplication(sys.argv)

    QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtGui.QPixmap('field/cursor.png'), 0, 0))

    WINDOW = graphics.MainWindow(APP.desktop().screenGeometry())
    WINDOW.setWindowFlags(
        QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    WINDOW.show()

    sys.exit(APP.exec_())
