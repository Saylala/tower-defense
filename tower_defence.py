import graphics
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtGui.QPixmap('field/cursor.png'), 0, 0))
    window = graphics.MainWindow(app.desktop().screenGeometry())
    window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    window.show()
    sys.exit(app.exec_())
